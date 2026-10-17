@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "terminal\Registro_De_Habitos.py"
) else (
  python "terminal\Registro_De_Habitos.py"
)
if errorlevel 1 (
  echo.
  echo No se pudo iniciar. Verifica que Python 3 este instalado.
  pause
)
