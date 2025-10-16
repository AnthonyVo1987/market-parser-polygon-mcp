#!/bin/bash
# Fix Docker permissions by adding user to docker group

echo "🔧 Fixing Docker permissions..."
echo ""

# Add user to docker group
sudo usermod -aG docker $USER

echo "✅ User '$USER' added to docker group"
echo ""
echo "⚠️  IMPORTANT: You need to log out and log back in for changes to take effect"
echo ""
echo "Options:"
echo "  1. Log out and log back in (recommended)"
echo "  2. Run: newgrp docker (temporary for this session)"
echo "  3. Use sudo with docker commands (scripts now support this)"
echo ""
echo "After logging back in, verify with: groups | grep docker"
