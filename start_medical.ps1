# 启动 medical 独立服务（Django，端口 8010）
# 用法：在 PowerShell 中执行 .\start_medical.ps1
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "未找到 .venv，请先执行：python -m venv --system-site-packages .venv" -ForegroundColor Yellow
    exit 1
}
& ".\.venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8010 --noreload
