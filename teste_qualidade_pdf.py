#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste específico de qualidade de conversão
Testa se o texto fica nítido no PDF gerado
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_qualidade_pdf():
    """Testa a qualidade da conversão com as melhorias"""
    
    print("🔍 TESTE DE QUALIDADE DE CONVERSÃO - ALTA RESOLUÇÃO")
    print("=" * 60)
    
    # Importar função melhorada
    from app import converter_pptx_para_pdf
    
    # Definir arquivos de teste
    pasta_teste = "teste_qualidade"
    os.makedirs(pasta_teste, exist_ok=True)
    
    modelo_pptx = "modelos_nr/NR06_modelo.pptx"
    teste_pptx = os.path.join(pasta_teste, "nr06_alta_qualidade.pptx")
    teste_pdf = os.path.join(pasta_teste, "nr06_alta_qualidade.pdf")
    
    if not os.path.exists(modelo_pptx):
        print("❌ Modelo NR06 não encontrado!")
        return False
    
    # Copiar modelo para teste
    import shutil
    shutil.copy2(modelo_pptx, teste_pptx)
    print(f"✅ Modelo copiado para: {teste_pptx}")
    
    # Remover PDF anterior se existir
    if os.path.exists(teste_pdf):
        os.remove(teste_pdf)
        print("🗑️ PDF anterior removido")
    
    print("\n🔄 Iniciando conversão com alta qualidade...")
    print("   Configurações aplicadas:")
    print("   • DPI: 300 (máxima resolução)")
    print("   • Qualidade JPEG: Alta")
    print("   • Preservação de fontes: Ativada")
    print("   • Compressão reduzida: Ativada")
    
    # Testar conversão
    sucesso = converter_pptx_para_pdf(teste_pptx, teste_pdf)
    
    if sucesso and os.path.exists(teste_pdf):
        tamanho_pdf = os.path.getsize(teste_pdf)
        tamanho_pptx = os.path.getsize(teste_pptx)
        
        print(f"\n✅ CONVERSÃO REALIZADA COM SUCESSO!")
        print(f"📊 Estatísticas:")
        print(f"   • PowerPoint: {tamanho_pptx:,} bytes")
        print(f"   • PDF gerado: {tamanho_pdf:,} bytes")
        print(f"   • Ratio: {tamanho_pdf/tamanho_pptx:.2f}x")
        
        # Verificar qualidade baseada no tamanho
        if tamanho_pdf > 200000:  # Mais de 200KB indica boa qualidade
            print("✅ Qualidade: ALTA (arquivo grande = alta resolução)")
        elif tamanho_pdf > 100000:  # Entre 100KB e 200KB
            print("⚠️ Qualidade: MÉDIA")
        else:
            print("❌ Qualidade: BAIXA (arquivo muito pequeno)")
        
        print(f"\n📁 Arquivos gerados:")
        print(f"   • {teste_pptx}")
        print(f"   • {teste_pdf}")
        
        print(f"\n💡 Para verificar a qualidade:")
        print(f"   1. Abra o arquivo: {teste_pdf}")
        print(f"   2. Verifique se o texto está nítido")
        print(f"   3. Amplie para 200% e veja se as letras ficam claras")
        
        return True
        
    else:
        print("❌ Falha na conversão!")
        return False

if __name__ == "__main__":
    testar_qualidade_pdf()
