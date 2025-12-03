# RotoClear Camera Server Documentation

[![Deploy Docs](https://github.com/JayeshKakkad-Rotoclear/Rotoclear-C-Pro-Docs/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/JayeshKakkad-Rotoclear/Rotoclear-C-Pro-Docs/actions/workflows/deploy-docs.yml)

Comprehensive documentation for the RotoClear Camera Server - an industrial camera server for real-time streaming and control.

## View Documentation

The live documentation is available at: **https://jayeshkakkad-rotoclear.github.io/Rotoclear-C-Pro-Docs/**

## Quick Start

This documentation is built using a custom static site generator that converts Markdown files to HTML with navigation and styling.

### Local Development

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the documentation:**
   ```bash
   python build.py
   ```

3. **Serve locally (using Python):**
   ```bash
   cd site
   python -m http.server 8000
   ```

4. **Open your browser to:** `http://localhost:8000`

### Building Documentation

To build the documentation:

```bash
python build.py
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

The build process:
1. Converts all Markdown files to HTML
2. Applies custom styling and navigation
3. Deploys to GitHub Pages

## Contributing

To contribute to the documentation:

1. Edit Markdown files in the `docs/` directory
2. Test locally with `python build.py && cd site && python -m http.server 8000`
3. Commit and push to the repository
4. GitHub Actions will automatically build and deploy your changes

## Tech Stack

- **Python & Markdown** - Content format
- **Custom Build Script** - Static site generation
- **HTML/CSS/JavaScript** - Front-end
- **GitHub Pages** - Hosting
- **GitHub Actions** - CI/CD automation
