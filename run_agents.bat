@echo off
chcp 65001 >nul
cls
echo ===============================================================
echo.
echo        Sistema de Agentes - Kristian Alexandre
echo.
echo ===============================================================
echo.

set PYTHON=C:\Users\newda\AppData\Local\Programs\Python\Python313\python.exe
set GITHUB_TOKEN=SEU_TOKEN_AQUI

if not exist "%PYTHON%" (
    echo ERRO: Python nao encontrado em: %PYTHON%
    echo.
    pause
    exit /b 1
)

"%PYTHON%" main.py --interactive

pause
