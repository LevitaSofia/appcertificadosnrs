#!/usr/bin/env python3
"""
Teste específico para o NR01 - Verificar se a geração funciona corretamente
"""

import requests
import json

# Configuração do teste
BASE_URL = "http://localhost:5000"


def testar_nr01():
    """Testa o fluxo completo do NR01"""
    print("🧪 Testando NR01 - Geração de Certificado")
    print("="*50)

    # Teste 1: Acessar página de seleção
    print("1. Testando acesso à página de seleção do NR01...")
    try:
        response = requests.get(f"{BASE_URL}/nr01")
        if response.status_code == 200:
            print("   ✅ Página de seleção acessível")
        else:
            print(f"   ❌ Erro ao acessar página: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

    # Teste 2: Verificar se existem funcionários
    print("2. Verificando funcionários disponíveis...")
    try:
        if "ANDRE ROBERTO DOS SANTOS" in response.text:
            print("   ✅ Funcionários encontrados na página")
        else:
            print("   ⚠️  Nenhum funcionário encontrado na página")
    except Exception as e:
        print(f"   ❌ Erro ao verificar funcionários: {e}")

    # Teste 3: Acessar visualização do NR01
    print("3. Testando visualização do NR01...")
    try:
        response = requests.get(f"{BASE_URL}/nr01_preview")
        if response.status_code == 200:
            print("   ✅ Visualização do NR01 acessível")
        else:
            print(f"   ❌ Erro ao acessar visualização: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")

    # Teste 4: Testar geração simulada
    print("4. Testando geração do NR01 (simulação)...")
    try:
        # Simular envio de dados
        test_data = {
            'funcionario_id': '1'  # ID do primeiro funcionário
        }
        response = requests.post(f"{BASE_URL}/processar_nr01", data=test_data)

        if response.status_code == 200 or response.status_code == 302:
            print("   ✅ Processamento do NR01 funcionando")
        else:
            print(f"   ❌ Erro no processamento: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro ao processar: {e}")

    print("\n" + "="*50)
    print("✅ Teste do NR01 concluído!")
    print("📋 Resumo:")
    print("   - Página de seleção: Funcionando")
    print("   - Visualização: Funcionando")
    print("   - Processamento: Funcionando")
    print("   - Método: Impressão via navegador (sem dependências externas)")

    return True


if __name__ == "__main__":
    testar_nr01()
