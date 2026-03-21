#!/usr/bin/env python3
"""
Replace local image links with jsDelivr CDN URLs in markdown files.
Converts relative paths and github.io URLs to jsDelivr CDN format.
"""

import os
import re
import subprocess
from pathlib import Path

def get_changed_markdown_files():
    """Get list of changed markdown files."""
    try:
        # For push events
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1..HEAD'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout:
            files = result.stdout.strip().split('\n')
            return [f for f in files if f.endswith('.md') or f.endswith('.markdown')]
    except:
        pass
    
    try:
        # For PR events
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'origin/main...HEAD'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout:
            files = result.stdout.strip().split('\n')
            return [f for f in files if f.endswith('.md') or f.endswith('.markdown')]
    except:
        pass
    
    return []

def replace_image_links():
    """Replace image links in markdown files with jsDelivr CDN URLs."""
    repo_owner = os.environ.get('REPO_OWNER', 'hibikilogy')
    repo_name = 'blog-images'
    cdn_base = f'https://cdn.jsdelivr.net/gh/{repo_owner}/{repo_name}@main'
    
    posts_dir = Path('_posts')
    if not posts_dir.exists():
        print("No _posts directory found")
        return False
    
    links_replaced = False
    
    # Patterns to match different image link formats
    patterns = [
        # Markdown image syntax with relative paths
        (r'!\[([^\]]*)\]\(\.?/?images/([^)]+)\)', 
         lambda m: f'![{m.group(1)}]({cdn_base}/images/{m.group(2)})'),
        
        # Markdown image syntax with github.io URLs
        (r'!\[([^\]]*)\]\(https://hibikilogy\.github\.io/images/([^)]+)\)',
         lambda m: f'![{m.group(1)}]({cdn_base}/images/{m.group(2)})'),
        
        # HTML img tags with relative paths
        (r'<img\s+([^>]*?)src=["\']\.?/?images/([^"\']+)["\']',
         lambda m: f'<img {m.group(1)}src="{cdn_base}/images/{m.group(2)}"'),
        
        # HTML img tags with github.io URLs
        (r'<img\s+([^>]*?)src=["\']https://hibikilogy\.github\.io/images/([^"\']+)["\']',
         lambda m: f'<img {m.group(1)}src="{cdn_base}/images/{m.group(2)}"'),
    ]
    
    for md_file in posts_dir.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all replacement patterns
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            
            # If content changed, write it back
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Updated image links in: {md_file}")
                links_replaced = True
        
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    # Set output for GitHub Actions
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"links_replaced={'true' if links_replaced else 'false'}\n")
    
    return links_replaced

if __name__ == '__main__':
    replace_image_links()
