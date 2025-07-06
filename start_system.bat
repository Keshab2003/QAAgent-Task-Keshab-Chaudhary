@echo off
echo.
echo ========================================
echo 🚀 Starting Test Automation System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js and try again
    pause
    exit /b 1
)

echo ✅ Python and Node.js found
echo.

REM Install Python dependencies if needed
echo 📦 Checking Python dependencies...
pip install streamlit playwright openai requests >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Some dependencies may not be installed
    echo Run: pip install -r requirements.txt
)

REM Install Playwright browsers if needed
echo 🌐 Checking Playwright browsers...
npx playwright install chromium >nul 2>&1

echo.
echo 🎯 Choose what to start:
echo.
echo 1. 🧪 Run Simple Tests (Guaranteed to pass)
echo 2. 📊 Start Dashboard
echo 3. 🎨 Customize System
echo 4. 🚀 Run All (Tests + Dashboard)
echo 5. 📋 View Reports
echo 6. 🔧 Setup Everything
echo 0. ❌ Exit
echo.

set /p choice="🤔 Enter your choice (0-6): "

if "%choice%"=="1" (
    echo.
    echo 🧪 Running Simple Tests...
    python simple_runner.py
    echo.
    echo ✅ Tests completed! Check test_report.html for results
    pause
) else if "%choice%"=="2" (
    echo.
    echo 📊 Starting Dashboard...
    start http://localhost:8501
    python dashboard.py
) else if "%choice%"=="3" (
    echo.
    echo 🎨 Starting Customization Tool...
    python customize_tests.py
) else if "%choice%"=="4" (
    echo.
    echo 🚀 Running All Components...
    echo 🧪 Running tests in background...
    start /B python simple_runner.py
    timeout /t 3 /nobreak >nul
    echo 📊 Starting dashboard...
    start http://localhost:8501
    python dashboard.py
) else if "%choice%"=="5" (
    echo.
    echo 📋 Opening Reports...
    if exist "test_report.html" (
        start test_report.html
    ) else (
        echo ⚠️ No reports found. Run tests first.
    )
    if exist "report/" (
        start report/
    )
    pause
) else if "%choice%"=="6" (
    echo.
    echo 🔧 Setting up everything...
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    echo 🌐 Installing Playwright browsers...
    npx playwright install
    echo 🧪 Running initial tests...
    python simple_runner.py
    echo 📊 Starting dashboard...
    start http://localhost:8501
    python dashboard.py
) else if "%choice%"=="0" (
    echo.
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please try again.
    pause
    goto :eof
)

echo.
echo 🎉 System ready!
echo.
echo 📁 Files created:
if exist "test_report.html" echo • test_report.html - Test results
if exist "report/" echo • report/ - Detailed reports
if exist "config/" echo • config/ - Configuration files
if exist "custom_tests/" echo • custom_tests/ - Custom test cases
echo.
echo 🚀 Next steps:
echo • Double-click test_report.html to view results
echo • Run 'python dashboard.py' to start the dashboard
echo • Run 'python customize_tests.py' to customize
echo.
pause 