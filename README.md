# RotoClear Camera Server Documentation

[![Deploy Docs](https://github.com/JayeshKakkad-Rotoclear/Rotoclear-C-Pro-Docs/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/JayeshKakkad-Rotoclear/Rotoclear-C-Pro-Docs/actions/workflows/deploy-docs.yml)

Comprehensive documentation for the RotoClear Camera Server - an industrial camera server for real-time streaming and control.

## View Documentation

The live documentation is available at: **https://jayeshkakkad-rotoclear.github.io/Rotoclear-C-Pro-Docs/**

## Quick Start

This documentation is built using [MkDocs](https://www.mkdocs.org/) with the [Material theme](https://squidfunk.github.io/mkdocs-material/).

### Local Development

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Serve documentation locally:**
   ```bash
   mkdocs serve
   ```

3. **Open your browser to:** `http://127.0.0.1:8000`

### Building Documentation

To build the documentation locally:

```bash
mkdocs build
```

The generated site will be in the `site/` directory.

## Documentation Structure

```
docs/
├── index.md                    # Home page
├── getting-started.md          # Getting started guide
├── architecture/               # System architecture
├── api/                        # API reference
├── configuration/              # Configuration guides
├── camera/                     # Camera system docs
├── operations/                 # Operations & deployment
├── security/                   # Security documentation
├── testing/                    # Testing guides
└── reference/                  # Technical reference
```

## Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` or `master` branch using GitHub Actions.

## Contributing

To contribute to the documentation:

1. Make your changes in the `docs/` directory
2. Test locally with `mkdocs serve`
3. Commit and push to the repository
4. GitHub Actions will automatically deploy your changes

## License

Copyright © 2025 Rotoclear

## Tech Stack

- **MkDocs** - Static site generator
- **Material for MkDocs** - Theme
- **GitHub Pages** - Hosting
- **GitHub Actions** - CI/CD automation
