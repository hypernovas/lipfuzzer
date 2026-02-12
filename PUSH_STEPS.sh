#!/bin/bash
# Helper script to push to hypernovas/lipfuzzer

echo "================================================"
echo "LipFuzzer - Push to hypernovas/lipfuzzer"
echo "================================================"

# Check current remote
echo -e "\n1. Current remote configuration:"
git remote -v

# Check authentication
echo -e "\n2. Testing GitHub SSH authentication:"
ssh -T git@github.com 2>&1 | grep -i "successfully authenticated"

# Show what will be pushed
echo -e "\n3. Commits to push:"
git log origin/master..master --oneline 2>/dev/null || git log --oneline -1

# Ask for confirmation
echo -e "\n4. Ready to push?"
echo "   Repository: hypernovas/lipfuzzer"
echo "   Branch: master"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo -e "\n5. Pushing to GitHub..."
    git push origin master
    
    if [ $? -eq 0 ]; then
        echo -e "\n✅ SUCCESS! Your changes are now on GitHub"
        echo "   View at: https://github.com/hypernovas/lipfuzzer"
    else
        echo -e "\n❌ PUSH FAILED"
        echo ""
        echo "Common issues:"
        echo "  1. SSH key not added to hypernovas account"
        echo "     → Add key at: https://github.com/settings/keys"
        echo ""
        echo "  2. No write permission to hypernovas/lipfuzzer"
        echo "     → Verify you own the hypernovas account"
        echo ""
        echo "  3. Branch protection rules"
        echo "     → Check repo settings"
    fi
else
    echo -e "\n❌ Push cancelled"
fi
