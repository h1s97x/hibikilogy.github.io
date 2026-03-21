#!/bin/bash
# Setup script for image migration automation
# This script helps initialize the image migration workflow

set -e

echo "🚀 Setting up Image Migration Automation"
echo "========================================"
echo ""

# Check if blog-images repository exists
REPO_OWNER=${1:-hibikilogy}
IMAGES_REPO="blog-images"

echo "📋 Checking prerequisites..."
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 is installed"

# Check if required Python packages are available
echo ""
echo "📦 Checking Python dependencies..."

python3 -c "import PIL" 2>/dev/null && echo "✅ Pillow is installed" || echo "⚠️  Pillow not installed (optional)"
python3 -c "import yaml" 2>/dev/null && echo "✅ PyYAML is installed" || echo "⚠️  PyYAML not installed (optional)"

echo ""
echo "📝 Configuration Instructions:"
echo "========================================"
echo ""
echo "1. Create a new public repository named 'blog-images' on GitHub"
echo "   - Go to https://github.com/new"
echo "   - Repository name: blog-images"
echo "   - Make it Public"
echo "   - Click 'Create repository'"
echo ""
echo "2. The GitHub Actions workflow is already configured in:"
echo "   - .github/workflows/image-migration.yml"
echo ""
echo "3. The workflow will automatically:"
echo "   - Detect new/modified images in the 'images/' directory"
echo "   - Migrate them to the blog-images repository"
echo "   - Replace image links in markdown files with CDN URLs"
echo ""
echo "4. No additional configuration needed! Just push your changes."
echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 For more information, see: .github/IMAGE_MIGRATION.md"
