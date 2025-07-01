#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cadastrar funcionários em lote no sistema de certificados NR
"""

from app import app, db, Funcionario
import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def converter_data(data_str):
    """Converte data do formato DD/MM/AAAA para objeto date"""
    try:
        return datetime.strptime(data_str, '%d/%m/%Y').date()
    except:
        return None


def limpar_cpf(cpf):
    """Remove formatação do CPF mantendo apenas números"""
    return ''.join(filter(str.isdigit, cpf))


def cadastrar_funcionarios():
    """Cadastra todos os funcionários no banco de dados"""

    funcionarios_dados = [
        {
            'nome': 'ANDRE ROBERTO DOS SANTOS',
            'cpf': '313.673.508-08',
            'data_nascimento': '12/01/1980',
            'telefone': '11 94870-7283',
            'email': 'andrealtatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'BRUNO PINHEIRO DE LIMA',
            'cpf': '401.201.328-93',
            'data_nascimento': '27/04/1990',
            'telefone': '11 95273-9404',
            'email': 'brunoaltatelas@gmail.com',
            'senha': 'Alta972600#'
        },
        {
            'nome': 'CAIO VINICIUS PAES DO NASCIMENTO',
            'cpf': '414.038.588-02',
            'data_nascimento': '30/05/1991',
            'telefone': '11 95487-5236',
            'email': '',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'CARLOS ALBERTO DOS SANTOS',
            'cpf': '288.915.798-90',
            'data_nascimento': '21/11/1978',
            'telefone': '16 98865-1612',
            'email': 'carlosaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'CLEUTON CLEBER VIEIRA ROMANO',
            'cpf': '270.176.758-00',
            'data_nascimento': '05/12/1979',
            'telefone': '19 990058626',
            'email': 'cleutonaltatelas@gmail.com',
            'senha': 'Alta972600#'
        },
        {
            'nome': 'DIOGO PEREIRA CARDOSO',
            'cpf': '058.224.705-56',
            'data_nascimento': '30/12/1991',
            'telefone': '16 98103-7258',
            'email': 'diogoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'EDERSON GONÇALVES VIEIRA DA SILVA',
            'cpf': '495.685.328-97',
            'data_nascimento': '10/09/1999',
            'telefone': '16 99430-4340',
            'email': 'edersongonsalvesaltatelas@gmail.com',
            'senha': 'Alta972600'
        },
        {
            'nome': 'ERDESSON QUIRINO DE LIMA',
            'cpf': '385.283.058-30',
            'data_nascimento': '17/10/1988',
            'telefone': '16 98192-4980',
            'email': 'erdersonaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'EVERTON SAMPAIO MELO DA COSTA',
            'cpf': '258.334.658-00',
            'data_nascimento': '14/01/1976',
            'telefone': '11 96917-5480',
            'email': 'evertonaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'FELIPE ARAUJO DOS SANTOS',
            'cpf': '101.876.985-46',
            'data_nascimento': '13/03/2003',
            'telefone': '16 99292-3212',
            'email': 'felipealtatelas@gmail.com',
            'senha': 'Alta972600'
        },
        {
            'nome': 'FERNANDO SILVA DE SOUZA',
            'cpf': '005.378.972-59',
            'data_nascimento': '25/01/1989',
            'telefone': '16 99278-2701',
            'email': 'fernandoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'FILIPE DELFINO',
            'cpf': '350.969 688-39',
            'data_nascimento': '07/05/1987',
            'telefone': '16 99261-7738',
            'email': 'filipedelfinoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'GABRIEL JACKSON PEIXOTO RIBEIRO',
            'cpf': '438.515.568-28',
            'data_nascimento': '08/07/1996',
            'telefone': '16 99361-7195',
            'email': 'gabrielaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'GUSTAVO ADOLFO CASTANEDA CARDENAS',
            'cpf': '023.066.106-81',
            'data_nascimento': '23/12/1986',
            'telefone': '11 96293-9343',
            'email': 'gustavoaltatelas@gmail.com',
            'senha': 'Alta972600@'
        },
        {
            'nome': 'JARDIEL NUNES DA SILVA',
            'cpf': '070.368.533-36',
            'data_nascimento': '13/09/2000',
            'telefone': '16 98191-9551',
            'email': 'jardielaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'JUNIEL DE SOUSA',
            'cpf': '011.619.363-86',
            'data_nascimento': '07/09/1984',
            'telefone': '16 99204-7416',
            'email': 'junielaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'KAIQUE DE OLIVEIRA SANTOS',
            'cpf': '435.731.658-85',
            'data_nascimento': '02/12/1997',
            'telefone': '16 99447-8913',
            'email': 'kaiquealtatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'LEANDRO RODRIGUES DE SOUZA',
            'cpf': '414.455.308-64',
            'data_nascimento': '26/07/1987',
            'telefone': '16 99396-5158',
            'email': 'leandroaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'LEONARDO DOUGLAS DE OLIVEIRA CORREA',
            'cpf': '525.803.638-31',
            'data_nascimento': '05/03/2003',
            'telefone': '11 93397-5926',
            'email': 'leonardoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'LUCAS EDUARDO RIBEIRO FRANÇA E SILVA',
            'cpf': '468.944.148-07',
            'data_nascimento': '27/10/2006',
            'telefone': '16 98836-9753',
            'email': 'lucasaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'LUCIANO DE JESUS',
            'cpf': '264.298.638-16',
            'data_nascimento': '06/11/1975',
            'telefone': '16 99754-1563',
            'email': 'lucianoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'LUIS HENRIQUE ROCETTI DA SILVA',
            'cpf': '412.241.338-97',
            'data_nascimento': '08/03/1992',
            'telefone': '16 99649-4762',
            'email': 'luisaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'MAICON DOUGLAS DOS SANTOS INFORZATO',
            'cpf': '463.539.228-76',
            'data_nascimento': '01/05/1993',
            'telefone': '16 98152-5822',
            'email': 'maiconaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'MATHEUS SOUSA COSTA',
            'cpf': '538.169.808-99',
            'data_nascimento': '01/12/2001',
            'telefone': '16 99111-6444',
            'email': 'matheusaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'MOEMIA COSTA DE OLIVEIRA',
            'cpf': '362.026.838-05',
            'data_nascimento': '05/02/1987',
            'telefone': '11 96150-8453',
            'email': 'moemia.costa@altatelas.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'PABLO HENRIQUE RIBEIRO FRIZI',
            'cpf': '584.518.788-57',
            'data_nascimento': '22/12/2007',
            'telefone': '16 99449-1102',
            'email': 'pabloaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'PAULO FERREIRA CARDOSO',
            'cpf': '427.979.418-96',
            'data_nascimento': '27/10/1997',
            'telefone': '16 99715-6763',
            'email': 'pauloaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'RAFAEL DE SOUZA COSTA',
            'cpf': '106.957.083-41',
            'data_nascimento': '09/05/2005',
            'telefone': '89 9421-1070',
            'email': 'rafaelaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'RODRIGO APARECIDO COELHO PAULISTA',
            'cpf': '218.937.248-83',
            'data_nascimento': '02/12/1982',
            'telefone': '16 99627-3207',
            'email': 'rodrigoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'RONALDO HENRIQUE DO CARMO',
            'cpf': '342.202.368-21',
            'data_nascimento': '14/09/1986',
            'telefone': '16 98846-2058',
            'email': 'ronaldoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'VICTOR HUGO VIANA GARCEZ',
            'cpf': '384.657.848-76',
            'data_nascimento': '15/09/2000',
            'telefone': '16 99307-5592',
            'email': 'victorhugoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'VITOR BRENO DE SOUZA ARAUJO',
            'cpf': '485.789.938-88',
            'data_nascimento': '15/09/2001',
            'telefone': '16 98187-3464',
            'email': 'vitorbrenoaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'WAGNER ZAMBONI',
            'cpf': '286246658-17',
            'data_nascimento': '17/08/1980',
            'telefone': '16 99722-6712',
            'email': 'wagneraltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'WENDEL HENRIQUE ANTONIO DA SILVA',
            'cpf': '504.069.548-95',
            'data_nascimento': '09/12/1998',
            'telefone': '16 99166-2527',
            'email': 'wendelaltatelas@gmail.com',
            'senha': 'Alta972600$'
        },
        {
            'nome': 'WILLIAM RODRIGUES DA SILVA',
            'cpf': '524.429.368-01',
            'data_nascimento': '16/03/2001',
            'telefone': '16 99650-8192',
            'email': 'williamaltatelas@gmail.com',
            'senha': 'Alta972600$'
        }
    ]

    with app.app_context():
        cadastrados = 0
        atualizados = 0
        erros = 0

        for dados in funcionarios_dados:
            try:
                cpf_limpo = limpar_cpf(dados['cpf'])

                # Verificar se funcionário já existe
                funcionario_existente = Funcionario.query.filter_by(
                    cpf=cpf_limpo).first()

                if funcionario_existente:
                    # Atualizar funcionário existente
                    funcionario_existente.nome = dados['nome']
                    funcionario_existente.data_nascimento = converter_data(
                        dados['data_nascimento'])
                    funcionario_existente.telefone = dados['telefone']
                    funcionario_existente.email = dados['email']
                    funcionario_existente.set_password(dados['senha'])

                    print(
                        f"✅ ATUALIZADO: {dados['nome']} - CPF: {dados['cpf']}")
                    atualizados += 1
                else:
                    # Criar novo funcionário
                    funcionario = Funcionario(
                        nome=dados['nome'],
                        cpf=cpf_limpo,
                        data_nascimento=converter_data(
                            dados['data_nascimento']),
                        telefone=dados['telefone'],
                        email=dados['email'],
                        funcao='Funcionário',
                        ativo=True,
                        admin=False,
                        primeiro_login=True
                    )
                    funcionario.set_password(dados['senha'])

                    db.session.add(funcionario)
                    print(
                        f"✅ CADASTRADO: {dados['nome']} - CPF: {dados['cpf']}")
                    cadastrados += 1

            except Exception as e:
                print(f"❌ ERRO ao processar {dados['nome']}: {str(e)}")
                erros += 1
                continue

        try:
            db.session.commit()
            print(f"\n🎯 RESUMO DO PROCESSAMENTO:")
            print(f"   📝 Funcionários cadastrados: {cadastrados}")
            print(f"   🔄 Funcionários atualizados: {atualizados}")
            print(f"   ❌ Erros encontrados: {erros}")
            print(f"   📊 Total processado: {cadastrados + atualizados}")
            print(f"\n✅ Dados salvos no banco de dados com sucesso!")

        except Exception as e:
            db.session.rollback()
            print(f"❌ ERRO ao salvar no banco de dados: {str(e)}")


if __name__ == '__main__':
    print("🚀 Iniciando cadastro em lote de funcionários...")
    print("=" * 60)
    cadastrar_funcionarios()
    print("=" * 60)
    print("🏁 Processamento concluído!")
