# چک کردن پایتون
$pythonInstalled = Test-Path (Get-Command python -ErrorAction SilentlyContinue).Source

if (-not $pythonInstalled) {
    Write-Host "پایتون نصب نیست. دانلود و نصب اتوماتیک..."
    # دانلود installer پایتون (نسخه 3.12)
    $url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest -Uri $url -OutFile $installerPath

    # نصب silent (بدون رابط کاربری)
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    # پاک کردن installer
    Remove-Item $installerPath
} else {
    Write-Host "پایتون قبلاً نصب شده."
}

# نصب پیش‌نیازها
Write-Host "نصب پیش‌نیازها..."
python -m pip install --upgrade pip
python -m pip install python-telegram-bot

Write-Host "سیستم آماده شد! حالا می‌تونی کد ربات رو اجرا کنی با: python main.py"
