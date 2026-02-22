param(
  [string]$VaultPath = "..\..\..\AI_Employee_Vault",
  [string]$DropPath = "$env:USERPROFILE\Downloads\Drop"
)

if (-not (Test-Path $DropPath)) {
  New-Item -ItemType Directory -Path $DropPath | Out-Null
}

python "$PSScriptRoot\watcher.py" --vault $VaultPath --drop $DropPath
