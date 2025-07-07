@echo off
echo ========================================
echo    Sistema de Despesas - Build Script
echo ========================================
echo.

echo [1/3] Instalando dependencias...
pip install -r build_requirements.txt

echo.
echo [2/3] Criando executavel unico...
copy /Y build.spec.template build.spec
pyinstaller build.spec --clean --distpath dist

echo.
echo [3/3] Limpando arquivos temporarios...
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