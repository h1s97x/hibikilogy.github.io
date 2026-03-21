#!/usr/bin/env python3
"""
Migrate images from main repository to blog-images repository.
Detects new/modified images and copies them to the blog-images repo.
"""

import os
import shutil
import subprocess
from pathlib import Path

def get_changed_files():
    """Get list of changed files in the current commit."""
    try:
        # For push events
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1..HEAD'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip().split('\n')
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
            return result.stdout.strip().split('\n')
    except:
        pass
    
    return []

def migrate_images():
    """Migrate new/modified images to blog-images repository."""
    images_dir = Path('images')
    blog_images_path = Path('blog-images')
    
    if not images_dir.exists():
        print("No images directory found")
        return False
    
    changed_files = get_changed_files()
    print(f"Changed files: {changed_files}")
    
    images_migrated = False
    
    # Get all image files
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}
    
    for image_file in images_dir.rglob('*'):
        if image_file.is_file() and image_file.suffix.lower() in image_extensions:
            # Check if this image was changed
            relative_path = image_file.relative_to('.')
            
            if str(relative_path) in changed_files or not (blog_images_path / image_file.relative_to(images_dir)).exists():
                # Copy to blog-images repo
                dest_path = blog_images_path / image_file.relative_to(images_dir)
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                print(f"Migrating: {relative_path} -> {dest_path}")
                shutil.copy2(image_file, dest_path)
                images_migrated = True
    
    # Set output for GitHub Actions
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"images_migrated={'true' if images_migrated else 'false'}\n")
    
    return images_migrated

if __name__ == '__main__':
    migrate_images()
