@echo off
echo ========================================
echo    Sistema de Despesas - Build Script
echo ========================================
echo.

echo [1/4] Instalando dependencias...
pip install -r build_requirements.txt

echo.
echo [2/4] Criando executavel...
copy /Y build.spec.template build.spec
pyinstaller build.spec --clean --distpath dist

echo.
echo [3/4] Copiando arquivos do frontend...
python copy_client_files.py

echo.
echo [4/4] Limpando arquivos temporarios...
rmdir /s /q build
del *.spec

echo.
echo ========================================
echo    Build concluido com sucesso!
echo ========================================
echo.
echo O executavel foi criado em: dist\SistemaDespesas.exe
echo.
echo Para usar:
echo 1. Vá para a pasta "dist"
echo 2. Execute "SistemaDespesas.exe"
echo 3. O navegador abrirá automaticamente
echo.
pause 