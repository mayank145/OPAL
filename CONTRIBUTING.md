# Contributing to FATS System

Thank you for your interest in contributing to the Fault Tracking System!

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. **Set up development environment**
   - Follow the setup instructions in `README.md`
   - Create `.env` files from `.env.production.example`
   - Install all dependencies

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- **Python**: Follow PEP 8 style guide
- **JavaScript**: Follow ESLint rules
- **Comments**: Add comments for complex logic
- **Logging**: Use proper logging (not print statements)

### Commit Messages

Use clear, descriptive commit messages:
```
feat: Add image zoom functionality
fix: Resolve timeout error in FATS list
docs: Update deployment guide
refactor: Improve error handling
```

### Testing

- Test your changes locally before committing
- Ensure no console errors
- Test both backend and frontend functionality

## Pull Request Process

1. **Update your branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git merge main
   ```

2. **Push your changes**
   ```bash
   git push origin your-feature-branch
   ```

3. **Create Pull Request**
   - Use the PR template
   - Describe your changes clearly
   - Link any related issues

4. **Code Review**
   - Address review comments
   - Update PR as needed

## Important Reminders

- ⚠️ **Never commit** `.env` files
- ⚠️ **Never commit** sensitive data
- ⚠️ **Never commit** `node_modules/` or `venv/`
- ✅ **Always** test your changes
- ✅ **Always** update documentation if needed

## Questions?

If you have questions, please:
- Check the documentation files
- Review existing code
- Ask team members

Thank you for contributing!
