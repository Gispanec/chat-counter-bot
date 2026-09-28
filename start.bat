@echo off
cd /d "%~dp0"
echo Enter the new token from BotFather when prompted.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$secureToken = Read-Host 'BotFather token' -AsSecureString; $env:BOT_TOKEN = [System.Net.NetworkCredential]::new('', $secureToken).Password; Remove-Variable secureToken; py bot.py"
if errorlevel 1 (
    echo.
    echo Bot stopped or could not start. Check the message above.
    pause
)
