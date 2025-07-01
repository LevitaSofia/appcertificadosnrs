#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para iniciar o Sistema de Treinamentos NR em rede
Permite acesso de múltiplos dispositivos na mesma rede local
"""

import os
import sys
import socket
import subprocess
import platform

def obter_ip_local():
    """Obtém o IP local da máquina"""
    try:
        # Conecta a um servidor remoto para descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        # Fallback para hostname
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

def verificar_firewall():
    """Verifica e fornece instruções sobre firewall"""
    sistema = platform.system()
    
    print("🔥 CONFIGURAÇÃO DO FIREWALL:")
    print("-" * 50)
    
    if sistema == "Windows":
        print("📋 Para Windows:")
        print("   1. Abra o 'Windows Defender Firewall'")
        print("   2. Clique em 'Permitir um aplicativo através do firewall'")
        print("   3. Adicione Python.exe à lista de exceções")
        print("   4. Ou execute como administrador:")
        print("      netsh advfirewall firewall add rule name='Python Flask' dir=in action=allow protocol=TCP localport=5000")
    elif sistema == "Linux":
        print("📋 Para Linux (Ubuntu/Debian):")
        print("   sudo ufw allow 5000")
        print("   sudo ufw reload")
    elif sistema == "Darwin":  # macOS
        print("📋 Para macOS:")
        print("   O macOS geralmente permite por padrão")
        print("   Se houver problemas, verifique 'Preferências do Sistema > Segurança'")
    
    print("-" * 50)

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'werkzeug',
        'python-pptx',
        'pandas',
        'openpyxl'
    ]
    
    print("📦 Verificando dependências...")
    faltando = []
    
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltando.append(dep)
    
    if faltando:
        print("❌ Dependências faltando:")
        for dep in faltando:
            print(f"   - {dep}")
        print("\n💡 Execute: pip install", " ".join(faltando))
        return False
    else:
        print("✅ Todas as dependências estão instaladas!")
        return True

def main():
    """Função principal"""
    print("🌐 SISTEMA DE TREINAMENTOS NR - CONFIGURAÇÃO DE REDE")
    print("=" * 70)
    
    # Verificar dependências
    if not verificar_dependencias():
        input("\n⏸️  Pressione Enter para sair...")
        return
    
    # Obter IP local
    ip_local = obter_ip_local()
    
    print(f"\n📍 INFORMAÇÕES DE REDE:")
    print(f"   🏠 IP Local: {ip_local}")
    print(f"   🌐 URL de Acesso: http://{ip_local}:5000")
    print(f"   📱 Acesso Local: http://127.0.0.1:5000")
    
    # Instruções de firewall
    print("\n")
    verificar_firewall()
    
    print("\n🚀 INSTRUÇÕES DE USO:")
    print("-" * 50)
    print("1. Certifique-se que todos os dispositivos estão na mesma rede WiFi")
    print("2. Configure o firewall conforme instruções acima")
    print("3. Em outros dispositivos, abra o navegador e acesse:")
    print(f"   http://{ip_local}:5000")
    print("4. Use as credenciais de login do sistema")
    print("-" * 50)
    
    print("\n📋 RECURSOS DISPONÍVEIS:")
    print("   📊 Dashboard de funcionários")
    print("   🎓 Sistema de treinamentos")
    print("   📜 Geração de certificados")
    print("   👥 Gerenciamento de usuários")
    print("   📱 Interface responsiva (mobile-friendly)")
    
    print("\n" + "=" * 70)
    resposta = input("🤔 Deseja iniciar o servidor agora? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\n🚀 Iniciando servidor...")
        try:
            # Executa o app principal
            subprocess.run([sys.executable, 'app.py'], cwd=os.path.dirname(os.path.abspath(__file__)))
        except KeyboardInterrupt:
            print("\n\n🛑 Servidor interrompido pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro ao iniciar servidor: {e}")
    else:
        print("\n👋 Até logo! Execute novamente quando quiser iniciar o servidor.")
    
    input("\n⏸️  Pressione Enter para sair...")

if __name__ == "__main__":
    main()
