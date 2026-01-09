# SAGE Intent Recognition

**Independent package for intent recognition and classification in conversational AI systems**

[![PyPI version](https://badge.fury.io/py/isage-intent.svg)](https://badge.fury.io/py/isage-intent)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

`sage-intent` provides flexible intent recognition capabilities for conversational AI:

- **Keyword-Based Recognition**: Fast, rule-based intent matching
- **LLM-Based Recognition**: Semantic intent understanding with LLMs
- **Hybrid Classification**: Combine multiple recognizers
- **Extensible Architecture**: Easy to add custom recognizers

## 📦 Installation

```bash
# Basic installation (keyword-based only)
pip install isage-intent

# With LLM support
pip install isage-intent[llm]

# Development installation
pip install isage-intent[dev]
```

## 🚀 Quick Start

### Keyword-Based Recognition

```python
from sage_intent import KeywordIntentRecognizer, IntentCatalog

# Create intent catalog
catalog = IntentCatalog()
catalog.add_intent(
    name="search",
    keywords=["find", "search", "look for", "query"],
    description="Search for information"
)
catalog.add_intent(
    name="greeting",
    keywords=["hello", "hi", "hey"],
    description="Greet the user"
)

# Create recognizer
recognizer = KeywordIntentRecognizer(catalog)

# Recognize intent
intent = recognizer.recognize("Can you help me search for papers?")
print(intent.name)  # "search"
print(intent.confidence)  # 0.85
```

### LLM-Based Recognition

```python
from sage_intent import LLMIntentRecognizer, IntentCatalog

# Create catalog with descriptions
catalog = IntentCatalog()
catalog.add_intent(
    name="data_analysis",
    description="Analyze data, generate visualizations, compute statistics"
)
catalog.add_intent(
    name="code_generation",
    description="Write code, create functions, implement algorithms"
)

# Create LLM recognizer
recognizer = LLMIntentRecognizer(
    catalog=catalog,
    llm_client=your_llm_client
)

# Recognize with semantic understanding
intent = recognizer.recognize(
    "I need a function to calculate the mean and standard deviation"
)
print(intent.name)  # "code_generation"
```

### Hybrid Classifier

```python
from sage_intent import IntentClassifier, KeywordIntentRecognizer, LLMIntentRecognizer

# Create classifier with multiple recognizers
classifier = IntentClassifier(
    recognizers=[
        KeywordIntentRecognizer(catalog),
        LLMIntentRecognizer(catalog, llm_client)
    ],
    strategy="vote"  # or "confidence", "cascade"
)

# Classify with combined approach
intent = classifier.classify("Find research papers about transformers")
```

## 📚 Key Components

### 1. **Intent Catalog** (`catalog.py`)

Manages intent definitions:
- Intent registration with keywords and descriptions
- Hierarchical intent organization
- Intent metadata and examples

### 2. **Keyword Recognizer** (`keyword_recognizer.py`)

Fast rule-based matching:
- Multiple keyword patterns per intent
- Fuzzy matching support
- Priority-based disambiguation

### 3. **LLM Recognizer** (`llm_recognizer.py`)

Semantic understanding with LLMs:
- Zero-shot intent classification
- Few-shot with examples
- Confidence scoring

### 4. **Classifier** (`classifier.py`)

Combines multiple recognizers:
- Voting strategies
- Confidence-based selection
- Cascade fallback

### 5. **Factory** (`factory.py`)

Easy recognizer creation:
- Pre-configured recognizers
- Custom recognizer registration
- Dynamic loading

## 🔧 Architecture

```
sage_intent/
├── base.py                  # Base classes and protocols
├── types.py                 # Common types
├── catalog.py               # Intent catalog management
├── keyword_recognizer.py    # Keyword-based recognition
├── llm_recognizer.py        # LLM-based recognition
├── classifier.py            # Multi-recognizer classification
├── factory.py               # Recognizer factory
└── __init__.py             # Public API exports
```

## 🎓 Use Cases

1. **Chatbots**: Route user queries to appropriate handlers
2. **Voice Assistants**: Understand user commands
3. **Customer Support**: Classify support tickets
4. **Search Systems**: Detect search intent for better results
5. **Agent Systems**: Determine agent actions based on user intent

## 🔗 Integration with SAGE

This package is part of the SAGE ecosystem but can be used independently:

```python
# Standalone usage
from sage_intent import KeywordIntentRecognizer, IntentCatalog

# With SAGE agentic (optional)
from sage_agentic import Agent
from sage_intent import IntentClassifier

agent = Agent()
classifier = IntentClassifier(catalog)

def process_query(query):
    intent = classifier.classify(query)
    return agent.execute(intent)
```

## 📖 Documentation

- **Repository**: https://github.com/intellistream/sage-intent
- **SAGE Documentation**: https://intellistream.github.io/SAGE-Pub/
- **Issues**: https://github.com/intellistream/sage-intent/issues

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Originally part of the [SAGE](https://github.com/intellistream/SAGE) framework, now maintained as an independent package for broader community use.

## 📧 Contact

- **Team**: IntelliStream Team
- **Email**: shuhao_zhang@hust.edu.cn
- **GitHub**: https://github.com/intellistream
