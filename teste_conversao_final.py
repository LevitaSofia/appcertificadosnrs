"""
Script para testar a conversão PowerPoint para PDF
"""
import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import converter_pptx_para_pdf

def testar_conversao():
    print("=== TESTE DE CONVERSÃO POWERPOINT PARA PDF ===")
    
    # Verificar se existe algum modelo PowerPoint
    modelos_dir = "modelos_nr"
    if not os.path.exists(modelos_dir):
        print(f"❌ Diretório {modelos_dir} não encontrado!")
        return False
    
    # Listar arquivos .pptx
    arquivos_pptx = [f for f in os.listdir(modelos_dir) if f.endswith('.pptx')]
    if not arquivos_pptx:
        print("❌ Nenhum arquivo .pptx encontrado!")
        return False
    
    # Usar o primeiro arquivo encontrado
    arquivo_teste = os.path.join(modelos_dir, arquivos_pptx[0])
    print(f"📄 Arquivo de teste: {arquivo_teste}")
    
    # Arquivo de saída
    arquivo_pdf = "teste_conversao.pdf"
    
    # Testar conversão
    print("🔄 Iniciando conversão...")
    resultado = converter_pptx_para_pdf(arquivo_teste, arquivo_pdf)
    
    if resultado and os.path.exists(arquivo_pdf):
        # Verificar tamanho do arquivo
        tamanho = os.path.getsize(arquivo_pdf)
        print(f"✅ CONVERSÃO BEM-SUCEDIDA!")
        print(f"📊 Tamanho do PDF: {tamanho:,} bytes")
        
        if tamanho > 100000:  # Maior que 100KB indica boa qualidade
            print("🎯 QUALIDADE ALTA (arquivo grande = alta resolução)")
        else:
            print("⚠️ Qualidade pode estar baixa (arquivo pequeno)")
            
        return True
    else:
        print("❌ FALHA NA CONVERSÃO!")
        return False

if __name__ == "__main__":
    testar_conversao()
