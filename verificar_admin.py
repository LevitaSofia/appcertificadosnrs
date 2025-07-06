#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Caminho para o banco de dados
db_path = r'g:\Meu Drive\000 ALTA TELAS\ALGORITOS AQUI NESTA PASTAS\certificados-nr\instance\certificados.db'

def verificar_e_criar_admin():
    # Verifica se o banco existe
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return
    
    print(f"✅ Banco de dados encontrado: {db_path}")
    
    # Conecta ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verifica se a tabela funcionarios existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='funcionarios'")
    if not cursor.fetchone():
        print("❌ Tabela 'funcionarios' não encontrada!")
        conn.close()
        return
    
    print("✅ Tabela 'funcionarios' encontrada")
    
    # Verifica se o admin existe
    cpf_admin = '39445247809'
    cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", (cpf_admin,))
    admin = cursor.fetchone()
    
    if admin:
        print(f"✅ Admin já existe no banco:")
        print(f"   CPF: {admin[2]}")  # Assumindo que CPF é a 3ª coluna
        print(f"   Nome: {admin[1]}")  # Assumindo que nome é a 2ª coluna
        print(f"   Senha hash: {admin[3][:20]}...")  # Primeiros 20 chars do hash
        
        # Testa se a senha está correta
        if check_password_hash(admin[3], 'admin'):
            print("✅ Senha 'admin' está correta!")
        else:
            print("❌ Senha 'admin' não confere! Atualizando...")
            nova_senha_hash = generate_password_hash('admin')
            cursor.execute("UPDATE funcionarios SET senha = ? WHERE cpf = ?", (nova_senha_hash, cpf_admin))
            conn.commit()
            print("✅ Senha atualizada!")
    else:
        print("❌ Admin não encontrado. Criando...")
        
        # Cria o admin
        nome_admin = 'Administrador'
        senha_hash = generate_password_hash('admin')
        
        cursor.execute("""
            INSERT INTO funcionarios (nome, cpf, senha) 
            VALUES (?, ?, ?)
        """, (nome_admin, cpf_admin, senha_hash))
        
        conn.commit()
        print("✅ Admin criado com sucesso!")
        print(f"   CPF: {cpf_admin}")
        print(f"   Nome: {nome_admin}")
        print("   Senha: admin")
    
    # Lista todos os funcionários para debug
    print("\n📋 Lista de todos os funcionários:")
    cursor.execute("SELECT id, nome, cpf FROM funcionarios")
    funcionarios = cursor.fetchall()
    
    for func in funcionarios:
        print(f"   ID: {func[0]}, Nome: {func[1]}, CPF: {func[2]}")
    
    conn.close()

if __name__ == "__main__":
    verificar_e_criar_admin()
