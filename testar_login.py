#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

def testar_login():
    """Testa o login no sistema"""
    base_url = 'http://127.0.0.1:5000'
    
    # Dados de login
    cpf = '394.452.478-09'  # Com máscara
    senha = 'admin'
    
    print(f"🔐 Testando login com CPF: {cpf} e senha: {senha}")
    
    # Criar sessão para manter cookies
    session = requests.Session()
    
    # Primeiro, acessar a página de login para obter o formulário
    try:
        login_page = session.get(f'{base_url}/login')
        if login_page.status_code != 200:
            print(f"❌ Erro ao acessar página de login: {login_page.status_code}")
            return
        
        print("✅ Página de login acessada com sucesso")
        
        # Tentar fazer login
        login_data = {
            'cpf': cpf,
            'senha': senha
        }
        
        response = session.post(f'{base_url}/login', data=login_data, allow_redirects=False)
        
        print(f"📤 Resposta do login: Status {response.status_code}")
        
        if response.status_code == 302:  # Redirecionamento
            location = response.headers.get('Location', '')
            print(f"🔄 Redirecionamento para: {location}")
            
            if 'login' in location:
                print("❌ Login falhou - redirecionado de volta para login")
            else:
                print("✅ Login bem-sucedido - redirecionado para página principal")
                
                # Tentar acessar página protegida
                protected_page = session.get(f'{base_url}/')
                if protected_page.status_code == 200:
                    print("✅ Acesso à página principal confirmado")
                else:
                    print(f"❌ Erro ao acessar página principal: {protected_page.status_code}")
        else:
            print("❌ Login falhou - nenhum redirecionamento")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor Flask")
        print("   Verifique se o servidor está rodando em http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    testar_login()
