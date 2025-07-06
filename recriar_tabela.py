#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from werkzeug.security import generate_password_hash
import os

# Caminho para o banco de dados
db_path = r'g:\Meu Drive\000 ALTA TELAS\ALGORITOS AQUI NESTA PASTAS\certificados-nr\instance\certificados.db'

def recriar_tabela_funcionarios():
    print("🔧 Recriando tabela funcionarios com estrutura correta...")
    
    # Conecta ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Remove a tabela existente se houver
    cursor.execute('DROP TABLE IF EXISTS funcionarios')
    
    # Cria tabela funcionarios (compatível com SQLAlchemy)
    cursor.execute('''
        CREATE TABLE funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            cpf VARCHAR(14) NOT NULL UNIQUE,
            rg VARCHAR(20),
            funcao VARCHAR(100) DEFAULT 'Não informado',
            data_admissao DATE,
            data_nascimento DATE,
            telefone VARCHAR(20),
            email VARCHAR(100),
            senha_hash VARCHAR(200),
            foto VARCHAR(200),
            ativo BOOLEAN DEFAULT 1 NOT NULL,
            admin BOOLEAN DEFAULT 0 NOT NULL,
            primeiro_login BOOLEAN DEFAULT 1 NOT NULL,
            data_ultimo_login DATETIME
        )
    ''')
    
    print("✅ Tabela funcionarios recriada!")
    
    # Cria o admin
    cpf_admin = '39445247809'
    nome_admin = 'Administrador'
    senha_hash = generate_password_hash('admin')
    
    cursor.execute("""
        INSERT INTO funcionarios (nome, cpf, senha_hash, admin, ativo) 
        VALUES (?, ?, ?, ?, ?)
    """, (nome_admin, cpf_admin, senha_hash, True, True))
    
    conn.commit()
    print("✅ Admin criado com sucesso!")
    print(f"   CPF: {cpf_admin}")
    print(f"   Nome: {nome_admin}")
    print("   Senha: admin")
    
    # Verifica se foi criado
    cursor.execute("SELECT id, nome, cpf, admin FROM funcionarios WHERE cpf = ?", (cpf_admin,))
    admin = cursor.fetchone()
    
    if admin:
        print(f"✅ Verificação: Admin criado com ID {admin[0]}, Admin: {bool(admin[3])}")
    else:
        print("❌ Erro: Admin não foi criado!")
    
    conn.close()
    print("\n🎉 Processo concluído!")

if __name__ == "__main__":
    recriar_tabela_funcionarios()
