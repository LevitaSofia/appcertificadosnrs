#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from werkzeug.security import generate_password_hash
import os

# Caminho para o banco de dados
db_path = r'g:\Meu Drive\000 ALTA TELAS\ALGORITOS AQUI NESTA PASTAS\certificados-nr\instance\certificados.db'

def adicionar_senha_funcionario():
    print("🔧 Adicionando senha para funcionário existente...")
    
    # Conecta ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lista todos os funcionários primeiro
    print("\n📋 Funcionários no banco:")
    cursor.execute("SELECT id, nome, cpf, senha_hash FROM funcionarios")
    funcionarios = cursor.fetchall()
    
    for func in funcionarios:
        print(f"   ID: {func[0]}, Nome: {func[1]}, CPF: {func[2]}, Tem senha: {bool(func[3])}")
    
    # Verifica se existe funcionário com CPF 394.452.478-09 (com máscara)
    cpf_com_mascara = '394.452.478-09'
    cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", (cpf_com_mascara,))
    funcionario_com_mascara = cursor.fetchone()
    
    if funcionario_com_mascara:
        print(f"\n✅ Encontrado funcionário com CPF mascarado: {funcionario_com_mascara[1]}")
        
        # Remove a máscara do CPF
        cpf_limpo = '39445247809'
        senha_hash = generate_password_hash('admin')
        
        # Atualiza o funcionário: remove máscara do CPF e adiciona senha
        cursor.execute("""
            UPDATE funcionarios 
            SET cpf = ?, senha_hash = ?, admin = 1, ativo = 1
            WHERE cpf = ?
        """, (cpf_limpo, senha_hash, cpf_com_mascara))
        
        conn.commit()
        print(f"✅ Funcionário atualizado:")
        print(f"   CPF atualizado: {cpf_com_mascara} → {cpf_limpo}")
        print(f"   Senha definida: admin")
        print(f"   Admin: Sim")
        print(f"   Ativo: Sim")
        
    else:
        print(f"\n❌ Nenhum funcionário encontrado com CPF {cpf_com_mascara}")
        
        # Verifica se existe com CPF limpo
        cpf_limpo = '39445247809'
        cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", (cpf_limpo,))
        funcionario_limpo = cursor.fetchone()
        
        if funcionario_limpo:
            print(f"✅ Encontrado funcionário com CPF limpo: {funcionario_limpo[1]}")
            senha_hash = generate_password_hash('admin')
            
            cursor.execute("""
                UPDATE funcionarios 
                SET senha_hash = ?, admin = 1, ativo = 1
                WHERE cpf = ?
            """, (senha_hash, cpf_limpo))
            
            conn.commit()
            print(f"✅ Senha adicionada para funcionário existente")
            print(f"   Senha: admin")
            print(f"   Admin: Sim")
            
        else:
            print(f"❌ Nenhum funcionário encontrado com CPF {cpf_limpo}")
            print("🔧 Criando novo funcionário...")
            
            # Cria novo funcionário
            nome_admin = 'Administrador'
            senha_hash = generate_password_hash('admin')
            
            cursor.execute("""
                INSERT INTO funcionarios (nome, cpf, senha_hash, admin, ativo) 
                VALUES (?, ?, ?, ?, ?)
            """, (nome_admin, cpf_limpo, senha_hash, True, True))
            
            conn.commit()
            print(f"✅ Novo funcionário criado:")
            print(f"   Nome: {nome_admin}")
            print(f"   CPF: {cpf_limpo}")
            print(f"   Senha: admin")
    
    # Verifica o resultado final
    print("\n📋 Funcionários após atualização:")
    cursor.execute("SELECT id, nome, cpf, senha_hash, admin FROM funcionarios")
    funcionarios = cursor.fetchall()
    
    for func in funcionarios:
        print(f"   ID: {func[0]}, Nome: {func[1]}, CPF: {func[2]}, Tem senha: {bool(func[3])}, Admin: {bool(func[4])}")
    
    conn.close()
    print("\n🎉 Processo concluído!")
    print(f"\n🔑 DADOS PARA LOGIN:")
    print(f"   CPF: 39445247809 (sem máscara)")
    print(f"   Senha: admin")

if __name__ == "__main__":
    adicionar_senha_funcionario()
