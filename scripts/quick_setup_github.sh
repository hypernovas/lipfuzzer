#!/bin/bash
# Quick setup script for multiple GitHub accounts

echo "================================================"
echo "GitHub Multiple Account Setup for LipFuzzer"
echo "================================================"
echo ""
echo "This will set up SSH keys for both accounts:"
echo "  - yangyongzhang (current)"
echo "  - hypernovas (needs setup)"
echo ""

# Step 1: Generate new key for hypernovas
echo "Step 1: Generating new SSH key for hypernovas..."
if [ ! -f ~/.ssh/id_ed25519_hypernovas ]; then
    ssh-keygen -t ed25519 -C "hypernovas@github.com" -f ~/.ssh/id_ed25519_hypernovas -N ""
    echo "✅ New key created: ~/.ssh/id_ed25519_hypernovas"
else
    echo "⚠️  Key already exists: ~/.ssh/id_ed25519_hypernovas"
fi

# Step 2: Add keys to ssh-agent
echo ""
echo "Step 2: Adding keys to SSH agent..."
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519 2>/dev/null && echo "✅ Added yangyongzhang key"
ssh-add ~/.ssh/id_ed25519_hypernovas 2>/dev/null && echo "✅ Added hypernovas key"

# Step 3: Create SSH config
echo ""
echo "Step 3: Creating SSH config..."

if [ ! -f ~/.ssh/config ]; then
    cat > ~/.ssh/config << 'EOF'
# GitHub account: yangyongzhang (default)
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

# GitHub account: hypernovas
Host github-hypernovas
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_hypernovas
    IdentitiesOnly yes
EOF
    echo "✅ Created ~/.ssh/config"
else
    echo "⚠️  SSH config already exists. Please add this manually:"
    echo ""
    cat << 'EOF'
# GitHub account: hypernovas
Host github-hypernovas
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_hypernovas
    IdentitiesOnly yes
EOF
fi

# Step 4: Display the new public key
echo ""
echo "Step 4: Your NEW hypernovas SSH public key:"
echo "================================================"
cat ~/.ssh/id_ed25519_hypernovas.pub
echo "================================================"
echo ""
echo "📋 COPY THE KEY ABOVE and add it to GitHub:"
echo "   1. Login as hypernovas"
echo "   2. Go to: https://github.com/settings/keys"
echo "   3. Click 'New SSH key'"
echo "   4. Title: 'MacBook Air - Hypernovas'"
echo "   5. Paste the key above"
echo "   6. Click 'Add SSH key'"
echo ""

# Step 5: Update git remote
echo "Step 5: Updating git remote for lipfuzzer..."
cd /Users/yangyong/projects/lipfuzzer
git remote set-url origin git@github-hypernovas:hypernovas/lipfuzzer.git
echo "✅ Remote updated to use github-hypernovas"
echo ""
git remote -v

echo ""
echo "================================================"
echo "Setup Complete! 🎉"
echo "================================================"
echo ""
echo "⏭️  NEXT STEPS:"
echo "   1. Add the SSH key to your hypernovas GitHub account"
echo "   2. Test connection: ssh -T git@github-hypernovas"
echo "   3. Push your changes: git push origin master"
echo ""
echo "For detailed instructions, see:"
echo "   SETUP_MULTIPLE_GITHUB_ACCOUNTS.md"
echo ""
