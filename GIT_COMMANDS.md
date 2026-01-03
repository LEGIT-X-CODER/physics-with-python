# Git Commands for Pushing to GitHub

Follow these commands in order to push your project to GitHub:

## Step 1: Initialize Git (if not already done)
```bash
git init
```

## Step 2: Add All Files
```bash
# Add all files (not just README.md)
git add .
```

## Step 3: Commit
```bash
git commit -m "Initial commit: Physics simulations with Python"
```

## Step 4: Set Branch to Main
```bash
git branch -M main
```

## Step 5: Add Remote Repository
```bash
git remote add origin https://github.com/LEGIT-X-CODER/physics-with-python.git
```

## Step 6: Push to GitHub
```bash
git push -u origin main
```

## Complete Command Sequence (Copy-Paste Ready)

```bash
git init
git add .
git commit -m "Initial commit: Physics simulations with Python"
git branch -M main
git remote add origin https://github.com/LEGIT-X-CODER/physics-with-python.git
git push -u origin main
```

## Important Notes

1. **Don't use `echo` command** - It will mess up your README.md
2. **Use `git add .`** - This adds ALL files, not just README.md
3. **Make sure you're in the project directory** before running commands
4. **If repository already exists on GitHub**, you might need to pull first:
   ```bash
   git pull origin main --allow-unrelated-histories
   ```

## If You Get Authentication Error

If GitHub asks for authentication:
1. Use Personal Access Token (not password)
2. Or use GitHub CLI: `gh auth login`

## If You Get "Repository Already Exists" Error

If the remote already exists:
```bash
# Remove old remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/LEGIT-X-CODER/physics-with-python.git

# Push
git push -u origin main
```

