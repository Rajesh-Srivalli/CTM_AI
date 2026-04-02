# Project Structure Guide

This document explains the project structure and conventions.

## Directory Layout

- **src/** - Contains all source code
  - Application modules go here
  - Should be installable as a package

- **tests/** - Contains all test code
  - Unit tests, integration tests
  - Mirrors the structure of src/

- **docs/** - Documentation
  - Project documentation, guides, API docs

## Development Workflow

1. Create a virtual environment
2. Install the project in development mode: `pip install -e .`
3. Make your changes
4. Run tests: `pytest tests/`
5. Commit and push

## Code Standards

- Use meaningful variable and function names
- Write docstrings for modules, classes, and functions
- Keep functions small and focused
- Write tests for new functionality
