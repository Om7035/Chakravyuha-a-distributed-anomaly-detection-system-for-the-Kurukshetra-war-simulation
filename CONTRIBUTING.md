# Contributing to Chakravyuha

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/chakravyuha.git
   cd chakravyuha
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Test your changes**:
   ```bash
   python simulation/war_generator_standalone.py
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** with a clear description

## Code Style

- **Python**: Follow PEP 8
- **Naming**: Use descriptive names for variables and functions
- **Comments**: Add comments for complex logic
- **Type hints**: Use type hints where possible

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Include a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed

## Areas for Contribution

### Easy Wins
- [ ] Add unit tests
- [ ] Improve documentation
- [ ] Add error handling
- [ ] Performance optimizations

### Medium Difficulty
- [ ] Add Grafana dashboard
- [ ] Implement data drift monitoring
- [ ] Add CI/CD pipeline
- [ ] Create Docker Compose alternative

### Advanced
- [ ] Deploy to AWS EKS
- [ ] Implement model retraining pipeline
- [ ] Add A/B testing framework
- [ ] Integrate Prometheus metrics

## Reporting Issues

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

## Questions?

Feel free to open an issue or discussion for questions!

---

**Thank you for contributing! 🙏**
