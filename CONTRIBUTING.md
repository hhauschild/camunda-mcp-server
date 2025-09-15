# Contributing to Camunda MCP Server

Thank you for your interest in contributing to the Camunda MCP Server! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- Clear and descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (OS, Python version, Camunda version)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please:

- Check existing issues first
- Provide a clear description of the feature
- Explain the use case and benefits
- Consider backward compatibility

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/camunda-mcp-server.git
   cd camunda-mcp-server
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your test Camunda server details
   ```

4. **Run tests**
   ```bash
   pytest
   ```

### Development Guidelines

#### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Run `black` for code formatting: `black src/ tests/`
- Run `mypy` for type checking: `mypy src/`

#### Testing

- Write tests for new features and bug fixes
- Maintain test coverage above 80%
- Use descriptive test names that explain what is being tested
- Test both success and error cases

#### Documentation

- Update README.md for new features
- Add docstrings to all functions and classes
- Update relevant documentation in `docs/`
- Include usage examples for new MCP tools

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code with tests
   - Update documentation
   - Follow code style guidelines

3. **Test your changes**
   ```bash
   # Run tests
   pytest -v
   
   # Check code style
   black --check src/ tests/
   mypy src/
   
   # Test MCP server startup
   python -m src.server --help
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new MCP tool for process definitions"
   ```

5. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Guidelines

Follow conventional commit format:

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `test:` adding or updating tests
- `refactor:` code refactoring
- `style:` formatting changes
- `chore:` maintenance tasks

Examples:
- `feat: add support for OAuth authentication`
- `fix: handle connection timeout errors gracefully`
- `docs: update Docker deployment guide`

### Adding New MCP Tools

When adding new MCP tools:

1. **Add the tool function** in `src/server.py`:
   ```python
   @mcp.tool()
   def your_new_tool(param: str) -> str:
       """
       Description of what the tool does.
       
       Args:
           param: Description of parameter
           
       Returns:
           Description of return value
       """
       # Implementation
   ```

2. **Add Camunda client method** in `src/camunda/client.py` if needed

3. **Write tests** in `tests/test_mcp_tools.py`

4. **Update documentation** in `examples/usage_examples.md`

### Adding New Camunda API Endpoints

1. **Add client method** in `src/camunda/client.py`
2. **Add data models** in `src/camunda/models.py` if needed
3. **Write comprehensive tests** in `tests/test_camunda_client.py`
4. **Update API documentation**

### Docker Development

For Docker-related contributions:

1. **Test locally**
   ```bash
   docker build -t camunda-mcp-server .
   docker-compose up -d
   ```

2. **Verify health checks work**
   ```bash
   docker-compose ps
   docker-compose logs camunda-mcp-server
   ```

3. **Test with different Python versions** if changing dependencies

### Documentation

- Keep README.md up to date
- Update relevant files in `docs/`
- Include examples for new features
- Verify all links work

### Release Process

Maintainers handle releases, but contributors should:

- Update version numbers in `pyproject.toml`
- Update CHANGELOG.md with new features/fixes
- Ensure all tests pass
- Update documentation

## Getting Help

- Check existing [documentation](docs/)
- Look through [existing issues](../../issues)
- Ask questions in new issues with the "question" label

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to make Camunda MCP Server better!