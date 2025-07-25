import os
import markdown
from pathlib import Path
import re

def convert_markdown_to_html():
    """Convert all markdown files to HTML and create an index page"""
    
    # Get all markdown files from the archive directory
    archive_dir = Path('archive')
    if not archive_dir.exists():
        print("Archive directory not found.")
        return
    
    md_files = sorted([f.name for f in archive_dir.glob('*.md')])
    
    if not md_files:
        print("No markdown files found in the archive directory.")
        return
    
    # Create output directory if it doesn't exist
    output_dir = Path('html_output')
    output_dir.mkdir(exist_ok=True)
    
    # Initialize markdown converter
    md = markdown.Markdown(extensions=['extra', 'codehilite'])
    
    html_files = []
    
    # Convert each markdown file to HTML
    for md_file in md_files:
        print(f"Converting {md_file}...")
        
        # Read markdown content from archive directory
        md_path = archive_dir / md_file
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
        except UnicodeDecodeError:
            # Try with latin-1 encoding for files with special characters
            with open(md_path, 'r', encoding='latin-1') as f:
                md_content = f.read()
        
        # Convert to HTML
        html_content = md.convert(md_content)
        
        # Create full HTML document
        html_filename = md_file.replace('.md', '.html')
        title = md_file.replace('.md', '').replace('_', ' ')  # Keep hyphens for dates
        
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
    <link rel="preload" href="style.css" as="style">
</head>
<body>
    <nav class="nav">
        <a href="index.html" class="back-link">← Back to Index</a>
    </nav>
    <main class="content">
        <h1 class="page-title">{title}</h1>
        {html_content}
    </main>
</body>
</html>"""
        
        # Write HTML file
        html_path = output_dir / html_filename
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        html_files.append((html_filename, title))
        
        # Reset markdown converter for next file
        md.reset()
    
    # Create CSS file
    create_css_file(output_dir)
    
    # Create index page
    create_index_page(html_files, output_dir)
    
    print(f"\nConversion complete! Generated {len(html_files)} HTML files.")
    print(f"Output directory: {output_dir}")
    print("Open html_output/index.html to view the index page.")

def create_css_file(output_dir):
    """Create a minimalistic CSS file for styling"""
    
    css_content = """/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #fff;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

/* Navigation */
.nav {
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 1px solid #e5e5e5;
}

.back-link {
    color: #666;
    text-decoration: none;
    font-size: 14px;
    transition: color 0.2s ease;
}

.back-link:hover {
    color: #333;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    margin: 1.5em 0 0.5em 0;
    font-weight: 600;
    line-height: 1.3;
}

.page-title {
    font-size: 2em;
    margin: 0 0 1em 0;
    color: #222;
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 0.5em;
}

p {
    margin: 0 0 1em 0;
}

/* Links */
a {
    color: #0066cc;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Code */
code {
    background: #f5f5f5;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
    font-size: 0.9em;
}

pre {
    background: #f8f8f8;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 1em 0;
    border: 1px solid #e5e5e5;
}

pre code {
    background: none;
    padding: 0;
}

/* Blockquotes */
blockquote {
    border-left: 3px solid #ddd;
    padding-left: 20px;
    margin: 1em 0;
    color: #666;
    font-style: italic;
}

/* Lists */
ul, ol {
    margin: 0 0 1em 0;
    padding-left: 2em;
}

li {
    margin: 0.25em 0;
}

/* Index Page Styles */
.index-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px 0;
}

.index-title {
    font-size: 1.8em;
    margin-bottom: 0.5em;
    color: #222;
    font-weight: 600;
}

.index-subtitle {
    color: #666;
    margin-bottom: 2em;
    font-size: 1em;
}

.file-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.file-item {
    border-bottom: 1px solid #f0f0f0;
}

.file-item:last-child {
    border-bottom: none;
}

.file-link {
    display: block;
    padding: 12px 0;
    color: #333;
    text-decoration: none;
    font-size: 0.95em;
    transition: color 0.2s ease;
}

.file-link:hover {
    color: #0066cc;
    text-decoration: none;
}

/* Responsive */
@media (max-width: 600px) {
    body {
        padding: 15px;
    }
    
    .index-container {
        padding: 15px 0;
    }
    
    .index-title {
        font-size: 1.5em;
    }
}

/* Performance optimizations */
.content {
    contain: layout style paint;
}
"""
    
    css_path = output_dir / 'style.css'
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)

def create_index_page(html_files, output_dir):
    """Create an index page with links to all HTML files"""
    
    index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>John Carmack's Plan Archive</title>
    <link rel="stylesheet" href="style.css">
    <link rel="preload" href="style.css" as="style">
</head>
<body>
    <div class="index-container">
        <h1 class="index-title">John Carmack's Plan Archive</h1>
        <p class="index-subtitle">A collection of John Carmack's development logs and insights</p>
        
        <ul class="file-list">"""
    
    # Add links to each HTML file in a simple list format
    for html_file, title in html_files:
        index_content += f"""
            <li class="file-item">
                <a href="{html_file}" class="file-link">{title}</a>
            </li>"""
    
    index_content += f"""
        </ul>
    </div>
    
    <script>
        // Preload first few pages for snappy navigation
        const links = document.querySelectorAll('.file-link');
        links.forEach((link, index) => {{
            if (index < 5) {{
                const preloadLink = document.createElement('link');
                preloadLink.rel = 'prefetch';
                preloadLink.href = link.href;
                document.head.appendChild(preloadLink);
            }}
        }});
    </script>
</body>
</html>"""
    
    # Write index file
    index_path = output_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

if __name__ == "__main__":
    # Install required package if not available
    try:
        import markdown
    except ImportError:
        print("Installing required package: markdown")
        os.system("pip install markdown")
        import markdown
    
    convert_markdown_to_html()