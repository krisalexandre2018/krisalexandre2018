@echo off
chcp 65001 >nul
cls
echo.
echo Atualizando perfil do GitHub...
echo.

set PYTHON=C:\Users\newda\AppData\Local\Programs\Python\Python313\python.exe
set GITHUB_TOKEN=SEU_TOKEN_AQUI

"%PYTHON%" main.py --agent profile

echo.
echo Pronto! Verifique o arquivo README.md
echo.
pause
