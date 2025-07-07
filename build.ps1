Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Sistema de Despesas - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Instalando dependencias..." -ForegroundColor Yellow
pip install -r build_requirements.txt

Write-Host ""
Write-Host "[2/3] Criando executavel unico..." -ForegroundColor Yellow
Copy-Item -Path build.spec.template -Destination build.spec -Force
pyinstaller build.spec --clean --distpath dist

Write-Host ""
Write-Host "[3/3] Limpando arquivos temporarios..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "*.spec") {
    Remove-Item "*.spec"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Build concluido com sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "O executavel foi criado em: dist\SistemaDespesas.exe" -ForegroundColor White
Write-Host ""
Write-Host "Para usar:" -ForegroundColor White
Write-Host "1. Vá para a pasta 'dist'" -ForegroundColor White
Write-Host "2. Execute 'SistemaDespesas.exe'" -ForegroundColor White
Write-Host "3. O navegador abrirá automaticamente" -ForegroundColor White
Write-Host ""
Read-Host "Pressione Enter para continuar" 