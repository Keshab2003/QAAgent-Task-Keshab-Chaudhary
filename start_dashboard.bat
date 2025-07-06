@echo off
echo Starting Test Automation Dashboard...
echo.
echo Installing required packages...
pip install streamlit plotly pandas

echo.
echo Starting dashboard...
echo The dashboard will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run dashboard.py

pause 