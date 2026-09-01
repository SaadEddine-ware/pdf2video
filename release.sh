#!/usr/bin/env bash
# Usage: ./release.sh [patch|minor|major]
#   patch: 1.0.0 -> 1.0.1 (bug fixes)
#   minor: 1.0.0 -> 1.1.0 (new features)
#   major: 1.0.0 -> 2.0.0 (breaking changes)
set -e

BUMP=${1:-patch}
CURRENT=$(python3 -c "import re; print(re.search(r'version = \"(.+?)\"', open('pyproject.toml').read()).group(1))")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case $BUMP in
    major) MAJOR=$((MAJOR+1)); MINOR=0; PATCH=0 ;;
    minor) MINOR=$((MINOR+1)); PATCH=0 ;;
    patch) PATCH=$((PATCH+1)) ;;
    *) echo "Usage: ./release.sh [patch|minor|major]"; exit 1 ;;
esac

NEW="$MAJOR.$MINOR.$PATCH"
echo "Releasing $CURRENT -> $NEW"

# Update version
sed -i "s/version = \".*\"/version = \"$NEW\"/" pyproject.toml
sed -i "s/__version__ = \".*\"/__version__ = \"$NEW\"/" pdf2video/__init__.py

# Build and upload
python3 -m build
twine upload dist/* -u __token -p "${PYPI_TOKEN}"
rm -rf dist/ build/ *.egg-info/

echo "Done! pip install --upgrade pdf2video==$NEW"
