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

# Desktop notification (BurntToast preferred, fallback to msgbox)
function Show-Notification {
    param(
        [string]$Title = "GitHub Sync",
        [string]$Message = "Sync complete."
    )
    try {
        Import-Module BurntToast -ErrorAction Stop
        New-BurntToastNotification -Text $Title, $Message
    } catch {
        # Fallback: Windows Forms message box
        Add-Type -AssemblyName PresentationFramework
        [System.Windows.MessageBox]::Show($Message, $Title)
    }
}

Show-Notification -Title "GitHub Sync" -Message "Automated commit and push completed at $timestamp."
