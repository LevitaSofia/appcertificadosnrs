#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das correções para geração de certificados
"""

import re
import os

def teste_limpeza_nomes():
    """Testa a limpeza de nomes de arquivo"""
    print("🧪 TESTE DE LIMPEZA DE NOMES DE ARQUIVO")
    print("=" * 50)
    
    # Casos de teste
    casos_teste = [
        "Inicial/Admissional",
        "Atualização",
        "Reciclagem",
        "Complementar",
        "Teste/Com\\Barras:Especiais*",
        "Nome Com Acentos ção"
    ]
    
    for caso in casos_teste:
        # Aplicar limpeza como no código
        limpo = re.sub(r'[<>:"/\\|?*]', '_', caso)
        print(f"Original: '{caso}' -> Limpo: '{limpo}'")
    
    print("\n✅ Teste de limpeza concluído!")

def teste_mapeamento():
    """Testa o mapeamento de tipos de treinamento"""
    print("\n🔄 TESTE DE MAPEAMENTO DE TIPOS")
    print("=" * 50)
    
    tipos_treinamento_display = {
        'Inicial_Admissional': 'Treinamento Inicial/Admissional',
        'Reciclagem': 'Reciclagem',
        'Atualizacao': 'Atualização',
        'Complementar': 'Complementar'
    }
    
    # Testar cada tipo
    for codigo, descricao in tipos_treinamento_display.items():
        print(f"Código: '{codigo}' -> Exibição: '{descricao}'")
    
    print("\n✅ Teste de mapeamento concluído!")

def teste_path():
    """Testa a criação de caminhos de arquivo"""
    print("\n📁 TESTE DE CAMINHOS DE ARQUIVO")
    print("=" * 50)
    
    nome_funcionario = "ALARICO FIRMINO NETO"
    data_arquivo = "2025-07-03"
    tipo_nr = "NR06"
    tipo_treinamento = "Inicial_Admissional"
    
    # Limpar nome do funcionário
    nome_funcionario_limpo = re.sub(r'[<>:"/\\|?*]', '_', nome_funcionario)
    
    # Limpar tipo de treinamento
    tipo_treinamento_limpo = re.sub(r'[<>:"/\\|?*]', '_', tipo_treinamento)
    
    # Construir nome do arquivo
    nome_arquivo_base = f"{nome_funcionario_limpo}_{data_arquivo}_{tipo_nr}_{tipo_treinamento_limpo}"
    
    # Caminhos
    pasta_funcionario = os.path.join('certificados', nome_funcionario_limpo)
    caminho_pptx = os.path.join(pasta_funcionario, f"{nome_arquivo_base}.pptx")
    caminho_pdf = os.path.join(pasta_funcionario, f"{nome_arquivo_base}.pdf")
    
    print(f"Nome funcionário limpo: {nome_funcionario_limpo}")
    print(f"Tipo treinamento limpo: {tipo_treinamento_limpo}")
    print(f"Nome do arquivo base: {nome_arquivo_base}")
    print(f"Pasta funcionário: {pasta_funcionario}")
    print(f"Caminho PPTX: {caminho_pptx}")
    print(f"Caminho PDF: {caminho_pdf}")
    
    print("\n✅ Teste de caminhos concluído!")

if __name__ == "__main__":
    teste_limpeza_nomes()
    teste_mapeamento()
    teste_path()
    print("\n🎉 TODOS OS TESTES CONCLUÍDOS!")
    print("✅ As correções devem resolver o problema dos caracteres especiais.")
