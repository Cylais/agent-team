# PowerShell script to automatically add, commit, and push changes to GitHub
# Usage: Right-click and "Run with PowerShell" or execute in a PowerShell terminal

# Change directory to the script location
Set-Location -Path $PSScriptRoot

# Stage all changes
git add .

# Create a commit message with timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMsg = "Automated commit: $timestamp"

# Commit (ignore error if nothing to commit)
git commit -m "$commitMsg" 2>$null

# Push to GitHub
git push
