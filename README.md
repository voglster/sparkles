# Sparkles ✨

Just utilities made by Jim Vogel - commonly used Python functions to avoid rewriting.

## Installation

```bash
pip install sparkles
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest -v

# Run linter
uv run ruff check sparkles/

# Format code
uv run ruff format sparkles/
```

## CI/CD Setup

### Setting up PyPI Publishing

1. **Create a PyPI API token:**
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token (scope: entire account or project-specific)
   - Copy the token (starts with `pypi-`)

2. **Add token to GitHub Secrets:**
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token
   - Click "Add secret"

### How to Release a New Version

1. **Bump the version** (creates commit and tag):
   - Go to GitHub → Actions → "Bump Version" workflow
   - Click "Run workflow"
   - Select bump type: `patch` (0.1.26 → 0.1.27), `minor` (0.1.26 → 0.2.0), or `major` (0.1.26 → 1.0.0)
   - Click "Run workflow"

2. **Automatic publishing:**
   - The bump workflow will create a GitHub release
   - The release will trigger the publish workflow
   - Package will be automatically built and published to PyPI

That's it! No manual builds or uploads needed.

## Features

- Date/time utilities with timezone support
- Data parsing and transformation helpers
- Google Sheets integration
- MongoDB tools
- Slack notification helpers
- General Python utility functions

## License

MIT
