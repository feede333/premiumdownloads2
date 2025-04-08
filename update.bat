@echo off
echo Actualizando repositorio...
git add .
git commit -m "Update: %date% %time%"
git push origin main
echo.
echo Cambios subidos a GitHub exitosamente!
echo Presiona cualquier tecla para cerrar...
pause > nul