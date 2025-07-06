#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys

def testar_login():
    print("🔑 Testando login no sistema...")
    
    # URL do sistema
    base_url = "http://localhost:5000"
    
    # Dados de login
    dados_login = {
        'cpf': '39445247809',  # CPF sem máscara
        'senha': 'admin'
    }
    
    try:
        # Criar sessão
        session = requests.Session()
        
        # Primeiro, fazer GET na página de login para obter o cookie de sessão
        print("📡 Fazendo GET na página de login...")
        response_get = session.get(f"{base_url}/login")
        
        if response_get.status_code == 200:
            print("✅ Página de login carregada com sucesso")
        else:
            print(f"❌ Erro ao carregar página de login: {response_get.status_code}")
            return
        
        # Fazer POST com os dados de login
        print("🔐 Tentando fazer login...")
        response_post = session.post(f"{base_url}/login", data=dados_login, allow_redirects=False)
        
        print(f"📊 Status da resposta: {response_post.status_code}")
        
        if response_post.status_code == 302:  # Redirecionamento = login bem-sucedido
            location = response_post.headers.get('Location', '')
            print(f"✅ LOGIN BEM-SUCEDIDO! Redirecionando para: {location}")
            
            # Tentar acessar a página principal
            print("🏠 Testando acesso à página principal...")
            response_index = session.get(f"{base_url}/")
            
            if response_index.status_code == 200:
                print("✅ Acesso à página principal bem-sucedido!")
                print("🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
            else:
                print(f"❌ Erro ao acessar página principal: {response_index.status_code}")
        
        elif response_post.status_code == 200:
            # Se retornou 200, provavelmente houve erro de login
            if "incorretos" in response_post.text.lower() or "inválido" in response_post.text.lower():
                print("❌ LOGIN FALHOU - CPF ou senha incorretos")
            else:
                print("❌ LOGIN FALHOU - Erro desconhecido")
                print("📄 Conteúdo da resposta:", response_post.text[:500])
        
        else:
            print(f"❌ Erro inesperado: {response_post.status_code}")
            print(f"📄 Conteúdo da resposta: {response_post.text[:500]}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao servidor. Verifique se está rodando em localhost:5000")
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")

if __name__ == "__main__":
    testar_login()
