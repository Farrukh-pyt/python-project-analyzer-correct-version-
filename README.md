# Python Project Analyzer

## About

Python Project Analyzer is a command-line tool that analyzes Python projects without executing their code.

The program scans a Python project and provides useful information about its source code.

## Features

- Count Python files
- Count total lines
- Count non-empty code lines
- Count functions
- Count classes
- Detect imported modules
- Find TODO markers
- Detect syntax errors
- Display statistics for each Python file
- Export the analysis report to JSON

## How It Works

The project uses Python's built-in `ast` module to analyze Python source code.

The program does not execute the analyzed project.

Instead, it reads the source files and builds an Abstract Syntax Tree (AST).

This allows the analyzer to identify:

- functions
- classes
- imports
- syntax errors

## Technologies

- Python
- Abstract Syntax Tree 
- Object-Oriented Programming
- File Handling
- JSON
- Unit Testing

## Requirements

Python 3.9 or newer.

No external libraries are required.

## Installation

Clone the repository:
## Author 
Farrukh

```bash
git clone https://github.com/Farrukh-pyt/python-project-analyzer.git
