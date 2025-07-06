#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido da configuração de rede
"""

import socket
import sys


def teste_rede():
    """Testa a configuração de rede"""
    try:
        print("🌐 TESTE DE CONFIGURAÇÃO DE REDE")
        print("=" * 50)

        # Teste de socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        print(f"✅ Hostname: {hostname}")
        print(f"✅ IP Local: {local_ip}")

        # Teste de porta
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()

        if result == 0:
            print("⚠️  Porta 5000 já está em uso")
        else:
            print("✅ Porta 5000 disponível")

        print("\n📍 URLs de acesso:")
        print(f"   🏠 Local: http://127.0.0.1:5000")
        print(f"   🌐 Rede:  http://{local_ip}:5000")

        print("\n✅ Configuração de rede OK!")
        return True

    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False


if __name__ == "__main__":
    teste_rede()
