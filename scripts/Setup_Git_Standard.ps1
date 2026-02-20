# Setup_Git_Standard.ps1
# This script sets up a Global Gitignore and applies a standard .gitignore to all Anti-Gravity projects.

$GitignoreContent = @"
# Anti-Gravity Standard Ignore
.antigravity/
.gemini/
.agent/
.opencode/

# Development
node_modules/
dist/
build/
.env
.env.*
!.env.example

# Logs and Debug
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS and Cleanup
.DS_Store
Thumbs.db
PATH_BACKUP_*.txt
Cleanup_Python.ps1
Link_Global_Skills.ps1
Link_Global_Skills.ps1
"@

# 1. Set up Global Gitignore (For all future projects)
Write-Host "--- Step 1: Setting up Global Gitignore ---" -ForegroundColor Cyan
$GlobalPath = "$env:USERPROFILE\.gitignore_global"
$GitignoreContent | Out-File -FilePath $GlobalPath -Encoding utf8
git config --global core.excludesfile $GlobalPath
Write-Host "Global Gitignore set at: $GlobalPath" -ForegroundColor Green

# 2. Update Local Gitignores (For existing projects)
Write-Host "`n--- Step 2: Updating Local Gitignores ---" -ForegroundColor Cyan
$Roots = @(
    "E:\2026\AntiGravity",
    "E:\2026\AntiGravity\Website"
)

foreach ($Root in $Roots) {
    if (-not (Test-Path $Root)) { continue }
    $Projects = Get-ChildItem -Path $Root -Directory
    
    foreach ($Project in $Projects) {
        if ($Project.Name -eq "Docs" -or $Project.Name -eq "Skills") { continue }
        
        $TargetPath = Join-Path $Project.FullName ".gitignore"
        Write-Host "Updating: $($Project.Name)..." -NoNewline
        
        if (Test-Path $TargetPath) {
            # Append if not already containing standard markers
            $Existing = Get-Content $TargetPath
            if ($Existing -match "Anti-Gravity Standard Ignore") {
                Write-Host " (Already standardized)" -ForegroundColor Gray
            }
            else {
                "`n" + $GitignoreContent | Out-File -FilePath $TargetPath -Append -Encoding utf8
                Write-Host " (Standard rules added)" -ForegroundColor Green
            }
        }
        else {
            $GitignoreContent | Out-File -FilePath $TargetPath -Encoding utf8
            Write-Host " (CREATED)" -ForegroundColor Green
        }
    }
}

Write-Host "`nAll projects standardized. Future projects will automatically follow these rules via the Global Gitignore." -ForegroundColor Cyan
