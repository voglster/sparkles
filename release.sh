#!/usr/bin/env bash
set -e

BUMP_TYPE="${1:-patch}"

if [[ "$BUMP_TYPE" != "patch" && "$BUMP_TYPE" != "minor" && "$BUMP_TYPE" != "major" ]]; then
    echo "Usage: ./release.sh [patch|minor|major] (default: patch)"
    exit 1
fi

echo "Triggering $BUMP_TYPE release..."
git tag "release-$BUMP_TYPE"
git push origin "release-$BUMP_TYPE"
echo "Done! Release workflow started."
