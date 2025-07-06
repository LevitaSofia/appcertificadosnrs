#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para corrigir erro de tabela medicoes_old não encontrada
Este script irá:
1. Conectar ao banco de dados
2. Criar a tabela medicoes_old se não existir
3. Ou remover referências à tabela se não for necessária
"""

import sqlite3
import os

def corrigir_erro_medicoes():
    print("🔧 Corrigindo erro da tabela medicoes_old...")
    
    # Buscar arquivos de banco de dados
    caminhos_possiveis = [
        "database.db",
        "app.db", 
        "main.db",
        "obras.db",
        "medicoes.db",
        "instance/database.db",
        "instance/app.db"
    ]
    
    banco_encontrado = None
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            banco_encontrado = caminho
            print(f"✅ Banco encontrado: {caminho}")
            break
    
    if not banco_encontrado:
        print("❌ Nenhum banco de dados encontrado. Procurando em subdiretórios...")
        # Buscar recursivamente
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".db"):
                    caminho_completo = os.path.join(root, file)
                    print(f"📁 Banco encontrado: {caminho_completo}")
                    banco_encontrado = caminho_completo
                    break
            if banco_encontrado:
                break
    
    if not banco_encontrado:
        print("❌ Nenhum banco de dados encontrado!")
        return
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(banco_encontrado)
        cursor = conn.cursor()
        
        # Verificar se a tabela medicoes existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medicoes'")
        if cursor.fetchone():
            print("✅ Tabela 'medicoes' encontrada")
            
            # Verificar se medicoes_old existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medicoes_old'")
            if not cursor.fetchone():
                print("⚠️ Tabela 'medicoes_old' não existe. Criando...")
                
                # Obter estrutura da tabela medicoes
                cursor.execute("PRAGMA table_info(medicoes)")
                colunas = cursor.fetchall()
                
                if colunas:
                    # Criar medicoes_old com a mesma estrutura
                    colunas_sql = []
                    for coluna in colunas:
                        nome = coluna[1]
                        tipo = coluna[2]
                        not_null = "NOT NULL" if coluna[3] else ""
                        default = f"DEFAULT {coluna[4]}" if coluna[4] else ""
                        pk = "PRIMARY KEY" if coluna[5] else ""
                        
                        coluna_sql = f"{nome} {tipo} {not_null} {default} {pk}".strip()
                        colunas_sql.append(coluna_sql)
                    
                    create_sql = f"CREATE TABLE medicoes_old ({', '.join(colunas_sql)})"
                    cursor.execute(create_sql)
                    conn.commit()
                    print("✅ Tabela 'medicoes_old' criada com sucesso!")
                else:
                    print("❌ Não foi possível obter estrutura da tabela medicoes")
            else:
                print("✅ Tabela 'medicoes_old' já existe")
        else:
            print("❌ Tabela 'medicoes' não encontrada")
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        print(f"\n📋 Tabelas no banco:")
        for tabela in tabelas:
            print(f"   - {tabela[0]}")
        
        conn.close()
        print("\n✅ Processo concluído!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    corrigir_erro_medicoes()
