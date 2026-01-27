@echo off
REM Script de automação para atualizar Dashboard de Retorno
REM Executa o script Python de atualização

cd /d "%~dp0"
echo ====================================
echo  Atualizando Dashboard de Retorno
echo ====================================
echo.

python atualizar_dashboard.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo  Atualização concluída com sucesso!
    echo ====================================
) else (
    echo.
    echo ====================================
    echo  ERRO na atualização!
    echo ====================================
)

REM Descomente a linha abaixo se quiser ver o resultado ao executar manualmente
REM pause
