#!/usr/bin/env bash
# quickstart.sh — sage-libs-intent dev environment setup
#
# Usage:
#   ./quickstart.sh               # dev mode (default): hooks + .[dev]  (includes [full])
#   ./quickstart.sh --full        # optional backends only: .[full]
#   ./quickstart.sh --standard    # core deps only: no extras
#   ./quickstart.sh --yes         # non-interactive (assume yes)
#   ./quickstart.sh --doctor      # diagnose environment issues
#
# Install matrix:
#   (default / --dev)  pip install -e .[dev]   ← includes [full] via self-ref
#   --full             pip install -e .[full]
#   --standard         pip install -e .
#
# Rules:
#   - NEVER creates a new venv. Must be called in an existing non-venv environment.
#   - Installs hooks via direct copy from hooks/.

set -e

# ─── Colors ─────────────────────────────────────────────────────────────────
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# ─── Arguments ────────────────────────────────────────────────────────────────
EXTRAS="[dev]"   # default — dev includes [full] via pyproject self-reference
DOCTOR=false
YES=false
for arg in "$@"; do
    case "$arg" in
        --doctor)   DOCTOR=true ;;
        --standard) EXTRAS="" ;;
        --full)     EXTRAS="[full]" ;;
        --dev)      EXTRAS="[dev]" ;;
        --yes|-y)   YES=true ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${BLUE}  sage-libs-intent — Quick Start${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ─── Doctor ────────────────────────────────────────────────────────────────────
if [ "$DOCTOR" = true ]; then
    echo -e "${BOLD}${BLUE}Environment Diagnosis${NC}"
    echo ""
    echo -e "${YELLOW}Python:${NC} $(python3 --version 2>/dev/null || echo 'NOT FOUND')"
    echo -e "${YELLOW}Conda env:${NC} ${CONDA_DEFAULT_ENV:-none}"
    echo -e "${YELLOW}Venv:${NC} ${VIRTUAL_ENV:-none}"
    echo -e "${YELLOW}ruff:${NC} $(ruff --version 2>/dev/null || echo 'NOT FOUND')"
    echo -e "${YELLOW}pytest:${NC} $(pytest --version 2>/dev/null || echo 'NOT FOUND')"
    echo ""
    echo -e "${YELLOW}Git hooks installed:${NC}"
    for h in pre-commit pre-push post-commit; do
        if [ -f "$PROJECT_ROOT/.git/hooks/$h" ]; then
            echo -e "  ${GREEN}✓ $h${NC}"
        else
            echo -e "  ${RED}✗ $h${NC}"
        fi
    done
    exit 0
fi

# ─── Step 0: Require an active non-venv environment ────────────────────────────
if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${RED}  ❌ Detected Python venv: $VIRTUAL_ENV${NC}"
    echo -e "${YELLOW}  → This repository forbids venv/.venv usage.${NC}"
    echo -e "${YELLOW}  → Please deactivate the venv and use Conda or a system Python.${NC}"
    exit 1
fi

# ─── Step 1/3: Python version check ──────────────────────────────────────────────
echo -e "${YELLOW}${BOLD}Step 1/3: Checking Python environment${NC}"
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "unknown")
echo -e "  Python version: ${CYAN}${PYTHON_VERSION}${NC}"
if python3 -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)" 2>/dev/null; then
    echo -e "  ${GREEN}✓ Python ≥ 3.10${NC}"
else
    echo -e "  ${RED}✗ Python 3.10+ required (found ${PYTHON_VERSION})${NC}"
    exit 1
fi
echo ""

# ─── Step 2/3: Install Git Hooks ─────────────────────────────────────────────────
echo -e "${YELLOW}${BOLD}Step 2/3: Installing Git hooks${NC}"
if [ -d "$PROJECT_ROOT/hooks" ]; then
    installed=0
    for hook_src in "$PROJECT_ROOT/hooks"/*; do
        hook_name=$(basename "$hook_src")
        hook_dst="$PROJECT_ROOT/.git/hooks/$hook_name"
        cp "$hook_src" "$hook_dst"
        chmod +x "$hook_dst"
        echo -e "  ${GREEN}✓ $hook_name${NC}"
        installed=$((installed + 1))
    done
    echo -e "${GREEN}✓ $installed hook(s) installed${NC}"
else
    echo -e "${YELLOW}⚠  hooks/ directory not found — skipping${NC}"
fi
echo ""

# ─── Step 3/3: Install package ────────────────────────────────────────────────────
echo -e "${YELLOW}${BOLD}Step 3/3: Installing package (editable)${NC}"
if [ -n "$EXTRAS" ]; then
    echo -e "  ${CYAN}pip install -e .$EXTRAS${NC}"
    pip install -e ".$EXTRAS"
else
    echo -e "  ${CYAN}pip install -e .${NC}  (standard — no extras)"
    pip install -e .
fi
echo -e "${GREEN}✓ Package installed in editable mode${EXTRAS:+ with extras: $EXTRAS}${NC}"
echo ""

echo -e "${GREEN}${BOLD}✓ Setup complete!${NC}"
echo ""
echo -e "${BLUE}${BOLD}Next steps:${NC}"
echo -e "  ${CYAN}pytest tests/${NC}                    — run tests"
echo -e "  ${CYAN}ruff check src/${NC}                  — lint"
echo -e "  ${CYAN}./quickstart.sh --full${NC}           — reinstall with optional backends"
echo -e "  ${CYAN}./quickstart.sh --standard${NC}       — install core deps only (no extras)"
echo -e "  ${CYAN}./quickstart.sh --doctor${NC}         — diagnose environment"
echo ""
