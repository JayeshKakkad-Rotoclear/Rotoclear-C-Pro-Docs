#!/usr/bin/env python3
"""
Build script to convert markdown documentation to static HTML site
"""
import os
import re
import json
from pathlib import Path
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

# Navigation structure based on mkdocs.yml
NAV_STRUCTURE = [
    {"title": "Home", "path": "index.md"},
    {"title": "Getting Started", "path": "getting-started.md"},
    {
        "title": "Architecture",
        "children": [
            {"title": "Overview", "path": "architecture/overview.md"},
            {"title": "State Management", "path": "architecture/state-management.md"},
            {"title": "Camera Pipeline", "path": "architecture/camera-pipeline.md"},
            {"title": "Metadata & SQLite", "path": "architecture/metadata-sqlite.md"},
            {
                "title": "Decisions",
                "children": [
                    {"title": "ADR-0001 Nim Language", "path": "architecture/decisions/ADR-0001-nim-language.md"},
                    {"title": "ADR-0002 Corun Framework", "path": "architecture/decisions/ADR-0002-corun-framework.md"},
                    {"title": "ADR-0003 Observable State", "path": "architecture/decisions/ADR-0003-observable-state.md"},
                ]
            }
        ]
    },
    {
        "title": "API Reference",
        "children": [
            {"title": "Overview", "path": "api/README.md"},
            {"title": "WebSocket API", "path": "api/websocket-api.md"},
            {"title": "HTTP API", "path": "api/http-api.md"},
            {"title": "RTSP Streaming", "path": "api/rtsp-streaming.md"},
            {
                "title": "Examples",
                "children": [
                    {"title": "Python Client", "path": "api/examples/python-client.md"},
                    {"title": "JavaScript Client", "path": "api/examples/javascript-client.md"},
                    {"title": "C# Client", "path": "api/examples/csharp-client.md"},
                ]
            }
        ]
    },
    {
        "title": "Configuration",
        "children": [
            {"title": "Environments", "path": "configuration/environments.md"},
            {"title": "Factory Config", "path": "configuration/factory-config.md"},
            {"title": "License Config", "path": "configuration/license-config.md"},
            {"title": "Deployment Variants", "path": "configuration/deployment-variants.md"},
            {"title": "Camera System", "path": "configuration/camera-system.md"},
            {"title": "Network", "path": "configuration/network.md"},
            {"title": "Storage & Backup", "path": "configuration/storage-backup.md"},
            {"title": "Authentication", "path": "configuration/authentication.md"},
        ]
    },
    {
        "title": "Camera System",
        "children": [
            {"title": "Hardware Interface", "path": "camera/hardware-interface.md"},
            {"title": "Streaming", "path": "camera/streaming.md"},
            {"title": "Recording", "path": "camera/recording.md"},
            {"title": "Image Processing", "path": "camera/image-processing.md"},
        ]
    },
    {
        "title": "Operations",
        "children": [
            {"title": "Build and Deploy", "path": "operations/build-and-deploy.md"},
            {"title": "Build & Deploy (Alt)", "path": "operations/build-deploy.md"},
            {"title": "Monitoring", "path": "operations/monitoring.md"},
            {"title": "Performance", "path": "operations/performance.md"},
            {"title": "Troubleshooting", "path": "operations/troubleshooting.md"},
        ]
    },
    {
        "title": "Security",
        "children": [
            {"title": "Authentication", "path": "security/authentication.md"},
            {"title": "Permissions", "path": "security/permissions.md"},
            {"title": "SSL Certificates", "path": "security/ssl-certificates.md"},
        ]
    },
    {
        "title": "Testing",
        "children": [
            {"title": "Strategy", "path": "testing/testing-strategy.md"},
            {"title": "Strategies", "path": "testing/strategies.md"},
            {"title": "Test Cases", "path": "testing/test-cases.md"},
            {"title": "Validation", "path": "testing/validation.md"},
        ]
    },
    {
        "title": "Integration",
        "children": [
            {"title": "ONVIF Protocol", "path": "integration/onvif-protocol.md"},
            {"title": "Third Party", "path": "integration/third-party.md"},
        ]
    },
    {
        "title": "Reference",
        "children": [
            {"title": "Glossary", "path": "reference/glossary.md"},
            {"title": "Requirements", "path": "reference/requirements.md"},
            {"title": "State Observables", "path": "reference/state-observables.md"},
        ]
    },
    {
        "title": "Releases",
        "children": [
            {"title": "Changelog", "path": "releases/CHANGELOG.md"},
        ]
    },
    {"title": "Glossary", "path": "glossary.md"},
]


def generate_nav_html(nav_items, current_path="", depth=0, base_path=""):
    """Generate HTML navigation from navigation structure"""
    html = []
    for item in nav_items:
        if "children" in item:
            # Folder with children
            html.append(f'<li class="nav-folder depth-{depth}">')
            html.append(f'<span class="folder-title">{item["title"]}</span>')
            html.append('<ul class="nav-submenu">')
            html.append(generate_nav_html(item["children"], current_path, depth + 1, base_path))
            html.append('</ul>')
            html.append('</li>')
        else:
            # Single page
            path = item.get("path", "")
            html_path = path.replace(".md", ".html")
            is_active = (html_path == current_path)
            active_class = " active" if is_active else ""
            html.append(f'<li class="nav-item depth-{depth}{active_class}">')
            html.append(f'<a href="{base_path}{html_path}">{item["title"]}</a>')
            html.append('</li>')
    return "\n".join(html)


def get_html_template():
    """Return the HTML template"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} - C Pro Camera Server Documentation</title>
    <link rel="stylesheet" href="{{BASE_PATH}}assets/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1><a href="{{BASE_PATH}}index.html">C Pro Docs</a></h1>
                <p>Camera Server Documentation</p>
            </div>
            <nav class="sidebar-nav">
                <ul class="nav-menu">
                    {{NAVIGATION}}
                </ul>
            </nav>
        </aside>
        
        <main class="content">
            <div class="content-wrapper">
                {{CONTENT}}
            </div>
            <footer class="content-footer">
                <p>Copyright © 2025 Rotoclear</p>
            </footer>
        </main>
        
        <button class="mobile-menu-toggle" id="menuToggle" aria-label="Toggle menu">☰</button>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>
        // Initialize Mermaid
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            fontFamily: 'Inter, sans-serif'
        });
        
        // Syntax highlighting
        hljs.highlightAll();
        
        // Mobile menu toggle
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.querySelector('.sidebar');
        
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768 && 
                !sidebar.contains(e.target) && 
                !menuToggle.contains(e.target) &&
                sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
            }
        });
        
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
</body>
</html>"""


def convert_md_to_html(md_content):
    """Convert markdown to HTML with extensions and handle Mermaid diagrams"""
    # First, convert Mermaid code blocks to proper div format
    # Pattern to match ```mermaid ... ```
    import re
    
    def replace_mermaid(match):
        mermaid_code = match.group(1).strip()
        return f'<div class="mermaid">\n{mermaid_code}\n</div>'
    
    # Replace mermaid code blocks
    md_content = re.sub(r'```mermaid\s*\n(.*?)\n```', replace_mermaid, md_content, flags=re.DOTALL)
    
    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'fenced_code',
        'tables',
        'toc',
        'nl2br',
        'sane_lists',
    ])
    return md.convert(md_content)


def build_site():
    """Build the static site"""
    docs_dir = Path("docs")
    output_dir = Path("site")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    (output_dir / "assets").mkdir(exist_ok=True)
    
    # Create .nojekyll file to prevent GitHub Pages from ignoring files starting with underscore
    (output_dir / ".nojekyll").touch()
    
    # Copy assets
    assets_src = docs_dir / "assets"
    assets_dst = output_dir / "assets"
    if assets_src.exists():
        import shutil
        shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)
    
    # Get template
    template = get_html_template()
    
    # Process all markdown files
    processed_files = []
    
    def process_nav_item(item, parent_path=""):
        if "children" in item:
            for child in item["children"]:
                process_nav_item(child, parent_path)
        else:
            if "path" in item:
                md_path = docs_dir / item["path"]
                if md_path.exists():
                    html_path = item["path"].replace(".md", ".html")
                    process_file(md_path, html_path, item["title"])
                    processed_files.append(item["path"])
    
    def process_file(md_path, html_path, title):
        """Process a single markdown file"""
        print(f"Processing: {md_path} -> {html_path}")
        
        # Calculate relative path depth for base_path
        depth = html_path.count('/')
        base_path = '../' * depth if depth > 0 else './'
        
        # Read markdown
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = convert_md_to_html(md_content)
        
        # Generate navigation
        nav_html = generate_nav_html(NAV_STRUCTURE, html_path, base_path=base_path)
        
        # Fill template
        page_html = template.replace("{{TITLE}}", title)
        page_html = page_html.replace("{{BASE_PATH}}", base_path)
        page_html = page_html.replace("{{NAVIGATION}}", nav_html)
        page_html = page_html.replace("{{CONTENT}}", html_content)
        
        # Write HTML file
        output_path = output_dir / html_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
    
    # Process all files in navigation
    for item in NAV_STRUCTURE:
        process_nav_item(item)
    
    print(f"\nBuild complete! Processed {len(processed_files)} files.")
    print(f"Output directory: {output_dir.absolute()}")


if __name__ == "__main__":
    build_site()
