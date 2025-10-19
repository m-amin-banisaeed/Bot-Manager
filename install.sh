#!/bin/bash

# چک کردن سیستم‌عامل
OS=$(uname -s)

# تابع برای نصب پایتون در لینوکس
install_python_linux() {
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip
    else
        echo "پشتیبانی‌نشده: لطفاً پایتون رو دستی نصب کنید از python.org"
        exit 1
    fi
}

# تابع برای نصب پایتون در مک
install_python_mac() {
    if ! command -v brew &> /dev/null; then
        echo "Homebrew نصب نیست. نصب می‌کنم..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install python
}

# چک کردن پایتون
if ! command -v python3 &> /dev/null; then
    echo "پایتون نصب نیست. شروع به نصب..."
    if [ "$OS" = "Linux" ]; then
        install_python_linux
    elif [ "$OS" = "Darwin" ]; then
        install_python_mac
    else
        echo "سیستم‌عامل ناشناخته. لطفاً پایتون رو دستی نصب کنید."
        exit 1
    fi
else
    echo "پایتون قبلاً نصب شده."
fi

# نصب پیش‌نیازها
echo "نصب پیش‌نیازها..."
python3 -m pip install --upgrade pip
python3 -m pip install python-telegram-bot

echo "سیستم آماده شد! حالا می‌تونی کد ربات رو اجرا کنی با: python3 main.py"
