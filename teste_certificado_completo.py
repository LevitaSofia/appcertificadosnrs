"""
Teste completo de geração de certificado
"""
import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Funcionario, ModeloNR, gerar_certificado

def testar_certificado():
    print("=== TESTE DE GERAÇÃO DE CERTIFICADO ===")
    
    with app.app_context():
        # Verificar se existe funcionário de teste
        funcionario = Funcionario.query.first()
        if not funcionario:
            print("❌ Nenhum funcionário encontrado no banco de dados!")
            return False
            
        print(f"👤 Funcionário: {funcionario.nome}")
        
        # Verificar se existe modelo NR06
        modelo = ModeloNR.query.filter_by(tipo_nr='NR06').first()
        if not modelo:
            print("❌ Modelo NR06 não encontrado!")
            return False
            
        print(f"📋 Modelo: {modelo.tipo_nr}")
        
        # Gerar certificado
        print("🔄 Gerando certificado...")
        resultado, mensagem = gerar_certificado(
            funcionario=funcionario,
            tipo_nr='NR06',
            tipo_treinamento='Inicial_Admissional',
            data_emissao=datetime.now()
        )
        
        if resultado:
            print("✅ CERTIFICADO GERADO COM SUCESSO!")
            print(f"📁 Mensagem: {mensagem}")
            
            # Verificar se o arquivo foi criado
            if os.path.exists(mensagem):
                tamanho = os.path.getsize(mensagem)
                print(f"📊 Tamanho do certificado: {tamanho:,} bytes")
                if tamanho > 100000:
                    print("🎯 QUALIDADE ALTA - Certificado com boa resolução")
                else:
                    print("⚠️ Possível problema de qualidade")
            return True
        else:
            print(f"❌ ERRO: {mensagem}")
            return False

if __name__ == "__main__":
    testar_certificado()
