# Contributing

Thank you for your interest in contributing to Geni client! This guide will help you set up your development environment
and ensure code quality.

## Setting Up Your Development Environment

### 1. Clone the Repository

```sh
# Replace <your-username> with your GitHub username
 git clone https://github.com/bryndin/geni.git
 cd geni
```

### 2. Create and Activate a Virtual Environment

```sh
# Create a virtual environment
python3 -m venv my_env

# Activate the virtual environment
# On macOS/Linux
source my_env/bin/activate

# On Windows
my_env\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running Tests

Ensure your changes do not break existing functionality by running tests with `pytest`:

```sh
pytest --cov=geni tests
```

This will also report the test coverage. We try to keep it at 100%.

## Linting and Type Checking

Before submitting changes, make sure your code follows best practices:

```sh
# Run Ruff for linting
ruff check ./geni/ ./tests

# Run MyPy for static type checking
mypy ./geni/ ./tests/
```

## Code Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Use [Ruff](https://beta.ruff.rs/docs/) for linting.
- Write type hints and check them with MyPy.
- Ensure tests pass before submitting a PR.
- Keep test coverage at 100%.

Thank you for contributing! 🚀
