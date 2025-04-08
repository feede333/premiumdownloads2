@echo off
echo Sincronizando con GitHub...

git add .
git commit -m "Actualización de programas y contenido"
git push origin main

echo Sincronización completada!
pause