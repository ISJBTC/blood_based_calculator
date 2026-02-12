@echo off
REM Run the Blood-Based Cancer Mathematical Model Calculator

REM Change to the directory of this script
cd /d "%~dp0"

REM Launch the Streamlit app
streamlit run app.py

@echo off
cd /d  %~dp0
python -m streamlit run app.py
