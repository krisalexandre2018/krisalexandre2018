@echo off
chcp 65001 >nul
cls
echo.
echo ===============================================================
echo   Executando TODOS os agentes...
echo ===============================================================
echo.

set PYTHON=C:\Users\newda\AppData\Local\Programs\Python\Python313\python.exe
set GITHUB_TOKEN=SEU_TOKEN_AQUI

"%PYTHON%" main.py --agent all

echo.
echo ===============================================================
echo   Todos os agentes executados!
echo ===============================================================
echo.
echo Arquivos gerados:
echo - README.md (atualizado)
echo - PORTFOLIO.md
echo - PROJECTS_HEALTH.md
echo - ENGAGEMENT_REPORT.md
echo - WEEKLY_SUMMARY.md
echo - INSIGHTS_DASHBOARD.md
echo.
pause
