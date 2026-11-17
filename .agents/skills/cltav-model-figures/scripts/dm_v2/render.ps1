param([string[]]$Keys = @())
$ErrorActionPreference = "Continue"
$py = "C:/Users/Chi Zhang/.codex/worktrees/cltav-finite-loop-runtime/protocol-confirmance-verification/.venv/Scripts/python.exe"
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
Set-Location $PSScriptRoot
$lines = & $py build_all.py @Keys
New-Item -ItemType Directory -Force preview | Out-Null
foreach ($l in $lines) {
    $name, $w, $h = $l -split " "
    $svg = (Resolve-Path "$name.svg").Path -replace '\\', '/'
    Get-ChildItem preview -Filter "$name*.png" | Remove-Item
    $png = Join-Path $PSScriptRoot "preview\$name-$((Get-Date).ToString('HHmmss')).png"
    & $chrome --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1.5 --screenshot="$png" --window-size="$([int]$w),$([int]$h)" "file:///$svg" 2>$null | Out-Null
    Write-Output $png
}
