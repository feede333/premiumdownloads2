REM filepath: c:\Users\Federico\Downloads\downloads site\premiumdownloads2\update.bat
@echo off
echo Verificando rutas y archivos...

cd ..
echo Working directory: %CD%

echo.
echo Verificando estructura...
python tools/verify_setup.py

echo.
echo Actualizando repositorio...
git add frontend/public/data/programs.json
git add frontend/public/images/*
git add .

echo.
echo Estado del repositorio:
git status

echo.
echo Confirmando cambios...
git commit -m "Update: Nuevos programas agregados %date% %time%"

echo.
echo Subiendo a GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo Cambios subidos exitosamente!
    echo Por favor espera unos minutos para que GitHub Pages se actualice.
    timeout /t 5 >nul
) else (
    echo.
    echo Hubo un error al subir los cambios.
    echo Revisa la consola para más detalles.
    pause
)