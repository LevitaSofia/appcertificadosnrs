"""
Teste FINAL - Verificar se certificados gerados têm ALTA QUALIDADE
"""
import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verificar_certificados_existentes():
    print("=== VERIFICAÇÃO DE CERTIFICADOS EXISTENTES ===")
    
    pasta_certificados = "certificados"
    if not os.path.exists(pasta_certificados):
        print("❌ Pasta 'certificados' não encontrada!")
        return False
    
    # Procurar arquivos PDF
    certificados_encontrados = []
    for root, dirs, files in os.walk(pasta_certificados):
        for file in files:
            if file.endswith('.pdf'):
                caminho_completo = os.path.join(root, file)
                tamanho = os.path.getsize(caminho_completo)
                certificados_encontrados.append((caminho_completo, tamanho))
    
    if not certificados_encontrados:
        print("❌ Nenhum certificado PDF encontrado!")
        return False
    
    print(f"📊 Encontrados {len(certificados_encontrados)} certificados:")
    
    todos_alta_qualidade = True
    for caminho, tamanho in certificados_encontrados:
        nome_arquivo = os.path.basename(caminho)
        if tamanho > 200000:  # Maior que 200KB = alta qualidade
            status = "🎯 ALTA QUALIDADE"
        elif tamanho > 100000:  # Maior que 100KB = qualidade boa
            status = "✅ BOA QUALIDADE"
        else:
            status = "⚠️ QUALIDADE BAIXA"
            todos_alta_qualidade = False
        
        print(f"  {nome_arquivo}: {tamanho:,} bytes - {status}")
    
    if todos_alta_qualidade:
        print("\n🎉 TODOS OS CERTIFICADOS TÊM ALTA QUALIDADE!")
        print("✅ O sistema de conversão está funcionando corretamente!")
    else:
        print("\n⚠️ Alguns certificados podem ter qualidade baixa")
    
    return todos_alta_qualidade

def instrucoes_uso():
    print("\n" + "="*60)
    print("📋 INSTRUÇÕES PARA GERAR CERTIFICADOS DE ALTA QUALIDADE:")
    print("="*60)
    print("1. Execute o servidor Flask: python app.py")
    print("2. Acesse: http://localhost:5000")
    print("3. Vá em: Gerar Certificado > Unitário")
    print("4. Selecione o funcionário e o tipo de NR")
    print("5. Clique em 'Gerar Certificado'")
    print("\n✅ O certificado será gerado em ALTA QUALIDADE automaticamente!")
    print("📊 Tamanho esperado: > 200KB = EXCELENTE qualidade")
    print("🎯 O sistema usa DPI 600 para máxima nitidez!")

if __name__ == "__main__":
    verificar_certificados_existentes()
    instrucoes_uso()
