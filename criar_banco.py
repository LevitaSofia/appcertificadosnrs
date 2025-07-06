#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from werkzeug.security import generate_password_hash
import os

# Caminho para o banco de dados
db_path = r'g:\Meu Drive\000 ALTA TELAS\ALGORITOS AQUI NESTA PASTAS\certificados-nr\instance\certificados.db'

def criar_tabelas_e_admin():
    print("🔧 Criando banco de dados e tabelas...")
    
    # Garante que o diretório instance existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Conecta ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cria tabela funcionarios (compatível com SQLAlchemy)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
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
    
    # Cria tabela treinamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treinamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id INTEGER NOT NULL,
            modulo TEXT NOT NULL,
            data_conclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            validade TIMESTAMP,
            certificado_gerado BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios (id)
        )
    ''')
    
    print("✅ Tabelas criadas com sucesso!")
    
    # Verifica se o admin já existe
    cpf_admin = '39445247809'
    cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", (cpf_admin,))
    admin = cursor.fetchone()
    
    if not admin:
        print("🔐 Criando usuário administrador...")
        
        # Cria o admin
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
    else:
        print("✅ Admin já existe!")
    
    # Lista todos os funcionários
    print("\n📋 Lista de funcionários:")
    cursor.execute("SELECT id, nome, cpf FROM funcionarios")
    funcionarios = cursor.fetchall()
    
    if funcionarios:
        for func in funcionarios:
            print(f"   ID: {func[0]}, Nome: {func[1]}, CPF: {func[2]}")
    else:
        print("   Nenhum funcionário encontrado.")
    
    conn.close()
    print("\n🎉 Processo concluído!")

if __name__ == "__main__":
    criar_tabelas_e_admin()
