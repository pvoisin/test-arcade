# Contributing to test-arcade

Thank you for your interest in contributing to this project!

## Git Configuration

### Personal .gitignore Files

This project's `.gitignore` file only includes patterns directly related to the Python project itself (bytecode, distribution files, virtual environments, etc.).

**Personal preferences should be configured in your global Git ignore file**, such as:
- OS-specific files (`.DS_Store`, `Thumbs.db`, etc.)
- Editor/IDE files (`.vscode/`, `.idea/`, `*.swp`, etc.)
- Personal tooling artifacts

To configure your global gitignore:

```bash
git config --global core.excludesfile ~/.gitignore_global
```

Then add your personal patterns to `~/.gitignore_global`.

This keeps the project's `.gitignore` focused on project-specific artifacts while allowing each contributor to customize their own environment without affecting others.

## Code Style

Please ensure your code follows Python best practices and is well-documented.

## Testing

Run tests before submitting changes to ensure everything works correctly:

```bash
python3 -m pytest
```
