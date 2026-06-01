# Contributing to HelpDesk Lite

Thank you for your interest in contributing to HelpDesk Lite! We welcome contributions from the community.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/helpdesk_lite.git
   cd helpdesk_lite
   ```

3. **Create a virtual environment**:
   ```powershell
   cd helpdesk
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development

- Run the development server: `python server/main.py`
- Run smoke tests: `python smoke_test.py`
- Keep code clean and well-documented
- Follow PEP 8 style guidelines

## Before Submitting a Pull Request

1. **Test your changes**:
   - Run the application locally
   - Run smoke tests: `python smoke_test.py`
   - Test with different browsers if you modified templates/CSS

2. **Update documentation**:
   - Update README.md if you add new features
   - Add comments to complex code sections

3. **Commit messages**:
   - Use clear, descriptive commit messages
   - Start with a capital letter
   - Use present tense: "Add feature" not "Added feature"

## Pull Request Process

1. Update the README.md with details of changes (if applicable)
2. Ensure all tests pass
3. Create a pull request with a clear description
4. Link any related issues

## Reporting Bugs

- Use GitHub Issues to report bugs
- Include:
  - Clear description of the bug
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Screenshots if applicable
  - Your environment (OS, Python version, etc.)

## Suggesting Enhancements

- Use GitHub Issues for feature requests
- Describe the use case
- Explain why this feature would be useful

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and reasonably sized

## Questions?

Feel free to open an issue or contact the maintainers!
