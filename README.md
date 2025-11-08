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

### Setting up PyPI Publishing (One-time setup)

1. **Create a PyPI API token:**
   - Go to https://pypi.org/manage/account/token/
   - Create a new project-scoped token for "sparkles"
   - Copy the token (starts with `pypi-`)

2. **Add token to GitHub Secrets:**
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token
   - Click "Add secret"

### How to Release a New Version (Git-Ops Style)

Just push a tag with the bump type you want:

```bash
# For a patch release (0.2.0 → 0.2.1)
git tag release-patch
git push origin release-patch

# For a minor release (0.2.0 → 0.3.0)
git tag release-minor
git push origin release-minor

# For a major release (0.2.0 → 1.0.0)
git tag release-major
git push origin release-major
```

**What happens automatically:**
1. GitHub Actions detects the `release-*` tag
2. Bumps the version in code and commits it
3. Creates a proper version tag (e.g., `v0.2.1`)
4. Builds the package
5. Creates a GitHub Release with release notes
6. Publishes to PyPI

That's it! No manual builds, version edits, or uploads needed.

## Features

- Date/time utilities with timezone support
- Data parsing and transformation helpers
- Google Sheets integration
- MongoDB tools
- Slack notification helpers
- General Python utility functions

## License

MIT
