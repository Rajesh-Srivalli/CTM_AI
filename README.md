# Python Project

A simple Python project with a standard project structure.

## Project Structure

```
project/
├── src/                 # Source code
│   ├── __init__.py
│   └── main.py
├── tests/              # Test files
│   ├── __init__.py
│   └── test_main.py
├── docs/               # Documentation
├── requirements.txt    # Dependencies
├── setup.py            # Project configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

Run the application:
```bash
python -m src.main
```

Or directly:
```bash
python src/main.py
```

## Testing

Run tests:
```bash
python tests/test_main.py
```

Or with pytest (if installed):
```bash
pytest tests/
```

## Development

Install in development mode:
```bash
pip install -e .
```