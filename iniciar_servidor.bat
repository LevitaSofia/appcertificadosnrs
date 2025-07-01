@echo off
chcp 65001 > nul
title Sistema de Treinamentos NR - Servidor de Rede

echo.
echo ═════════════════════════════════════════════════════════════════
echo                 🌐 SISTEMA DE TREINAMENTOS NR                    
echo                      Configuração de Rede                       
echo ═════════════════════════════════════════════════════════════════
echo.

echo 📋 Verificando Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! 
    echo 💡 Instale o Python em: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
echo.

echo 📦 Instalando/Verificando dependências...
pip install -q flask flask-sqlalchemy flask-login python-pptx pandas openpyxl werkzeug

echo.
echo 🚀 Iniciando servidor de rede...
echo.
echo ⚠️  IMPORTANTE:
echo    - Certifique-se que o firewall permite conexões na porta 5000
echo    - Todos os dispositivos devem estar na mesma rede WiFi
echo.

python iniciar_rede.py

echo.
echo 📱 Para parar o servidor, pressione Ctrl+C na janela do Python
echo.
pause
