@echo off
chcp 65001 >nul
cls
echo.
echo Analisando seus projetos...
echo.

set PYTHON=C:\Users\newda\AppData\Local\Programs\Python\Python313\python.exe
set GITHUB_TOKEN=SEU_TOKEN_AQUI

"%PYTHON%" main.py --agent projects

echo.
echo Pronto! Verifique os arquivos:
echo - PORTFOLIO.md
echo - PROJECTS_HEALTH.md
echo.
pause
