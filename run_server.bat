@echo off
call .venv\Scripts\activate.bat
uvicorn api.main:app --reload 