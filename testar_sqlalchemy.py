#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

# Adiciona o diretório do projeto ao path
sys.path.append(r'g:\Meu Drive\000 ALTA TELAS\ALGORITOS AQUI NESTA PASTAS\certificados-nr')

from app import app, db, Funcionario
from werkzeug.security import check_password_hash

def testar_busca_usuario():
    """Testa se conseguimos encontrar o usuário através do SQLAlchemy"""
    
    with app.app_context():
        print("🔍 Testando busca de usuário no banco via SQLAlchemy...")
        
        # Dados de teste
        cpf_raw = '394.452.478-09'
        cpf_limpo = re.sub(r'[^0-9]', '', cpf_raw)
        senha = 'admin'
        
        print(f"CPF raw: '{cpf_raw}'")
        print(f"CPF limpo: '{cpf_limpo}'")
        
        # Busca todos os funcionários
        todos_funcionarios = Funcionario.query.all()
        print(f"\n📋 Total de funcionários no banco: {len(todos_funcionarios)}")
        
        for func in todos_funcionarios:
            print(f"   ID: {func.id}, Nome: {func.nome}, CPF: '{func.cpf}', Admin: {func.admin}")
            print(f"   Senha hash: {func.senha_hash[:30]}..." if func.senha_hash else "   Sem senha hash")
        
        # Busca o funcionário específico
        funcionario = Funcionario.query.filter_by(cpf=cpf_limpo).first()
        
        if funcionario:
            print(f"\n✅ Funcionário encontrado!")
            print(f"   Nome: {funcionario.nome}")
            print(f"   CPF: {funcionario.cpf}")
            print(f"   Admin: {funcionario.admin}")
            print(f"   Ativo: {funcionario.ativo}")
            print(f"   Tem senha: {bool(funcionario.senha_hash)}")
            
            if funcionario.senha_hash:
                senha_correta = funcionario.check_password(senha)
                print(f"   Senha '{senha}' está correta: {senha_correta}")
                
                # Teste direto do hash
                hash_ok = check_password_hash(funcionario.senha_hash, senha)
                print(f"   Teste direto do hash: {hash_ok}")
            else:
                print("   ❌ Funcionário não tem senha definida!")
        else:
            print(f"\n❌ Funcionário com CPF '{cpf_limpo}' não encontrado!")
        
        # Teste alternativo: buscar por CPF com máscara
        funcionario_alt = Funcionario.query.filter_by(cpf=cpf_raw).first()
        if funcionario_alt:
            print(f"\n🔍 Encontrado com CPF com máscara: {funcionario_alt.nome}")
        else:
            print(f"\n🔍 Não encontrado com CPF com máscara")

if __name__ == "__main__":
    testar_busca_usuario()
