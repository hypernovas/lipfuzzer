# Setup Multiple GitHub Accounts on One Laptop

## The Problem
Your SSH key is already used by `yangyongzhang` account. GitHub doesn't allow the same SSH key on multiple accounts. You need separate keys.

## Solution: Multiple SSH Keys + SSH Config

### Step 1: Generate New SSH Key for Hypernovas

Run these commands in your terminal:

```bash
# Generate a new SSH key specifically for hypernovas account
ssh-keygen -t ed25519 -C "hypernovas@github.com" -f ~/.ssh/id_ed25519_hypernovas

# When prompted:
# - Enter passphrase (optional, can leave empty for convenience)
# - Confirm passphrase

# Verify the keys were created
ls -lh ~/.ssh/id_ed25519*
```

You should now see:
- `id_ed25519` (your current yangyongzhang key)
- `id_ed25519_hypernovas` (new key for hypernovas)

### Step 2: Add New Key to SSH Agent

```bash
# Start ssh-agent if not running
eval "$(ssh-agent -s)"

# Add the new hypernovas key
ssh-add ~/.ssh/id_ed25519_hypernovas

# Add your existing yangyongzhang key too
ssh-add ~/.ssh/id_ed25519

# Verify both keys are loaded
ssh-add -l
```

### Step 3: Create/Update SSH Config

Create or edit `~/.ssh/config`:

```bash
# Open in your favorite editor
nano ~/.ssh/config
# or
vim ~/.ssh/config
# or
code ~/.ssh/config
```

Add this configuration:

```
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
```

Save and close the file.

### Step 4: Add New SSH Key to Hypernovas GitHub Account

```bash
# Display the NEW hypernovas public key
cat ~/.ssh/id_ed25519_hypernovas.pub
```

**Copy the output**, then:

1. Login to GitHub as **hypernovas**
2. Go to: https://github.com/settings/keys
3. Click "New SSH key"
4. Title: `MacBook Air - Hypernovas`
5. Paste the key from above
6. Click "Add SSH key"

### Step 5: Update Git Remote for Hypernovas Repos

For the lipfuzzer project, update the remote URL to use the custom host:

```bash
cd /Users/yangyong/projects/lipfuzzer

# Update remote to use github-hypernovas host
git remote set-url origin git@github-hypernovas:hypernovas/lipfuzzer.git

# Verify the change
git remote -v
```

### Step 6: Test Both Connections

```bash
# Test yangyongzhang account (default)
ssh -T git@github.com

# Test hypernovas account (custom host)
ssh -T git@github-hypernovas
```

Both should say: "Hi [username]! You've successfully authenticated..."

### Step 7: Push Your Changes

```bash
cd /Users/yangyong/projects/lipfuzzer

# Now push will use the hypernovas SSH key automatically
git push origin master
```

## How It Works

The SSH config maps different "hosts" to different SSH keys:

- `git@github.com` → uses `id_ed25519` (yangyongzhang)
- `git@github-hypernovas` → uses `id_ed25519_hypernovas` (hypernovas)

When you use `github-hypernovas` in your remote URL, SSH automatically uses the hypernovas key!

## Quick Reference

### For Hypernovas Repos
```bash
# Clone
git clone git@github-hypernovas:hypernovas/repo-name.git

# Set remote
git remote set-url origin git@github-hypernovas:hypernovas/repo-name.git
```

### For Yangyongzhang Repos
```bash
# Clone (use regular github.com)
git clone git@github.com:yangyongzhang/repo-name.git

# Set remote
git remote set-url origin git@github.com:yangyongzhang/repo-name.git
```

## Troubleshooting

### "Permission denied"
- Check SSH config syntax: `cat ~/.ssh/config`
- Verify keys are loaded: `ssh-add -l`
- Test connection: `ssh -T git@github-hypernovas`

### "Key already in use"
- Make sure you're adding the NEW key (id_ed25519_hypernovas.pub)
- Not the old key (id_ed25519.pub)

### Wrong account being used
- Check your remote URL: `git remote -v`
- Should be: `git@github-hypernovas:hypernovas/...`
- NOT: `git@github.com:hypernovas/...`

## Alternative: HTTPS Authentication

If SSH is too complex, use HTTPS with Personal Access Tokens:

```bash
# Change to HTTPS
git remote set-url origin https://github.com/hypernovas/lipfuzzer.git

# When pushing, GitHub will prompt for:
# - Username: hypernovas
# - Password: [Personal Access Token from https://github.com/settings/tokens]

git push origin master
```

---

**Current Status:**
- ✅ Existing key: `yangyongzhang` account
- 🔄 Need to create: new key for `hypernovas` account
- 📝 Next: Follow steps above to set up multiple keys
