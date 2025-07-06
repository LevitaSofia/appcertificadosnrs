#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para encontrar e corrigir erro medicoes_old em qualquer sistema
"""

import sqlite3
import os
import glob

def buscar_bancos_com_medicoes():
    print("🔍 Buscando bancos de dados com tabela 'medicoes'...")
    
    # Buscar todos os arquivos .db no computador (caminhos comuns)
    caminhos_busca = [
        "C:/Users/*/Documents/**/*.db",
        "C:/projetos/**/*.db", 
        "G:/Meu Drive/**/*.db",
        "D:/**/*.db",
        "./**/*.db"
    ]
    
    bancos_encontrados = []
    
    for padrao in caminhos_busca:
        try:
            arquivos = glob.glob(padrao, recursive=True)
            for arquivo in arquivos:
                if os.path.exists(arquivo):
                    bancos_encontrados.append(arquivo)
        except:
            continue
    
    # Remover duplicatas
    bancos_encontrados = list(set(bancos_encontrados))
    
    print(f"📂 Encontrados {len(bancos_encontrados)} bancos de dados")
    
    for banco in bancos_encontrados:
        try:
            conn = sqlite3.connect(banco)
            cursor = conn.cursor()
            
            # Verificar se tem tabela medicoes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medicoes'")
            if cursor.fetchone():
                print(f"\n✅ BANCO COM MEDIÇÕES ENCONTRADO: {banco}")
                
                # Verificar se precisa da tabela medicoes_old
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medicoes_old'")
                tem_old = cursor.fetchone()
                
                if not tem_old:
                    print("⚠️ Tabela medicoes_old não existe. Criando...")
                    
                    # Criar medicoes_old igual à medicoes
                    cursor.execute("CREATE TABLE medicoes_old AS SELECT * FROM medicoes WHERE 1=0")
                    conn.commit()
                    print("✅ Tabela medicoes_old criada!")
                else:
                    print("✅ Tabela medicoes_old já existe")
                
                # Mostrar tabelas do banco
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tabelas = [t[0] for t in cursor.fetchall()]
                print(f"📋 Tabelas: {', '.join(tabelas)}")
            
            conn.close()
            
        except Exception as e:
            # Ignorar bancos que não conseguimos abrir
            continue

def corrigir_erro_especifico():
    """Correção específica para o erro que você está vendo"""
    print("\n🔧 CORREÇÃO ESPECÍFICA PARA O ERRO...")
    
    # Se você souber o caminho exato do banco, coloque aqui
    banco_obras = input("Digite o caminho completo do banco de dados do sistema de obras (ou Enter para buscar): ").strip()
    
    if not banco_obras:
        print("Buscando automaticamente...")
        buscar_bancos_com_medicoes()
        return
    
    if not os.path.exists(banco_obras):
        print(f"❌ Arquivo não encontrado: {banco_obras}")
        return
    
    try:
        conn = sqlite3.connect(banco_obras)
        cursor = conn.cursor()
        
        # Verificar estrutura atual
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [t[0] for t in cursor.fetchall()]
        print(f"📋 Tabelas existentes: {', '.join(tabelas)}")
        
        if 'medicoes' in tabelas:
            if 'medicoes_old' not in tabelas:
                print("⚠️ Criando tabela medicoes_old...")
                
                # Obter estrutura da tabela medicoes
                cursor.execute("PRAGMA table_info(medicoes)")
                info = cursor.fetchall()
                
                # Criar SQL para medicoes_old
                colunas = []
                for col in info:
                    nome, tipo, not_null, default, pk = col[1], col[2], col[3], col[4], col[5]
                    col_def = f"{nome} {tipo}"
                    if not_null:
                        col_def += " NOT NULL"
                    if default:
                        col_def += f" DEFAULT {default}"
                    if pk:
                        col_def += " PRIMARY KEY"
                    colunas.append(col_def)
                
                create_sql = f"CREATE TABLE medicoes_old ({', '.join(colunas)})"
                cursor.execute(create_sql)
                conn.commit()
                print("✅ Tabela medicoes_old criada!")
            else:
                print("✅ Tabela medicoes_old já existe")
        else:
            print("❌ Tabela medicoes não encontrada neste banco")
        
        conn.close()
        print("✅ Correção concluída!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    print("🏗️ CORRETOR DE ERRO MEDICOES_OLD")
    print("="*50)
    
    opcao = input("Escolha uma opção:\n1 - Buscar automaticamente\n2 - Informar caminho do banco\nOpção: ").strip()
    
    if opcao == "2":
        corrigir_erro_especifico()
    else:
        buscar_bancos_com_medicoes()
