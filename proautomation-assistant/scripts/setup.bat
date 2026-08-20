@echo off
REM Setup para Windows (PowerShell/CMD)
cd /d %~dp0\..
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts\download_models.py --skip-gguf
python ingest.py
echo.
echo Listo. Ejecuta: .venv\Scripts\activate ^&^& streamlit run app.py
pause
