# PytestMate

[![PyPI version](https://img.shields.io/pypi/v/pytestmate.svg)](https://pypi.org/project/pytestmate/)
[![License](https://img.shields.io/github/license/MrMoneyInTheBank/pytestmate.svg)](https://github.com/MrMoneyInTheBank/pytestmate/blob/main/LICENSE)
[![Tests](https://github.com/MrMoneyInTheBank/pytestmate/actions/workflows/ci.yaml/badge.svg)](https://github.com/MrMoneyInTheBank/pytestmate/actions/workflows/ci.yaml)

A command-line tool for managing Python test infrastructure. PytestMate helps you set up, maintain, and run tests for your Python projects with minimal effort.

## Features

- **Automatic Test Structure Creation**: Generate test directories and test files that mirror your project structure
- **Git Integration**: Use Git to track and manage Python files in your project
- **Project Validation**: Ensure you're working within a valid Python project
- **Coming Soon**:
  - Test file updates
  - Test execution
  - Test coverage reporting
  - Additional test file generation

## Installation

```bash
pip install pytestmate
```

## Usage

### Initialize Test Structure

```bash
# Basic usage
ptm init

# Use Git for file discovery
ptm init --git
```

This command:
1. Verifies that you're in a Python project
2. Identifies Python source files
3. Creates a test directory structure
4. Generates test file placeholders

### Other Commands (Coming Soon)

```bash
# Update existing test files
ptm update

# Run tests with pytest
ptm test

# Generate test coverage reports
ptm report

# Generate additional test files
ptm generate
```

## Requirements

- Python 3.7+
- Click
- Git (optional, for Git integration)

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/pytestmate.git
cd pytestmate

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Click](https://click.palletsprojects.com/) for the CLI framework
- [pytest](https://docs.pytest.org/) for the testing framework
