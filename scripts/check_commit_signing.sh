#!/bin/sh

# Check if commits are configured to be signed
SIGNING_ENABLED=$(git config --bool commit.gpgsign)

if [ "$SIGNING_ENABLED" != "true" ]; then
    echo "Warning: Commit signing is not enabled! Use 'git config --global commit.gpgsign true' to enable."
    exit 1  # Remove 'exit 1' if you don't want to block commits
fi

exit 0