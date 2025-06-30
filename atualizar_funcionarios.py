import re
import sqlite3
from datetime import datetime
import os

# Bloco de dados dos funcionários
dados_funcionarios = """
ANDRE ROBERTO DOS SANTOS 
CPF: 313.673.508-08
DATA DE NASCIMENTO: 12/01/1980
NUMERO: 11 94870-7283
EMAIL: andrealtatelas@gmail.com
SENHA: Alta972600$

BRUNO PINHEIRO DE LIMA  
CPF: 401.201.328-93
DATA DE NASCIMENTO: 27/04/1990 
NUMERO: 11 95273-9404 
EMAIL: brunoaltatelas@gmail.com
SENHA: Alta972600#

CAIO VINICIUS PAES DO NASCIMENTO
CPF: 414.038.588-02
DATA DE NASCIMENTO: 30/05/1991
NÚMERO: 11 95487-5236
EMAIL:
SENHA: Alta972600$

CARLOS ALBERTO DOS SANTOS 
CPF: 288.915.798-90
DATA DE NASCIMENTO: 21/11/1978 
NUMERO: 16 98865-1612
EMAIL: carlosaltatelas@gmail.com
SENHA: Alta972600$

CLEUTON CLEBER VIEIRA ROMANO
CPF: 270.176.758-00
DATA DE NASCIMENTO: 05/12/1979
NUMERO: 19 990058626
EMAIL: cleutonaltatelas@gmail.com
SENHA: Alta972600#

DIOGO PEREIRA CARDOSO  
CPF: 058.224.705-56 
DATA DE NASCIMENTO: 30/12/1991
NUMERO: 16 98103-7258
EMAIL: diogoaltatelas@gmail.com
SENHA: Alta972600$

EDERSON GONÇALVES VIEIRA DA SILVA
CPF: 495.685.328-97
DATA DE NASCIMENTO: 10/09/1999
NUMERO:  16 99430-4340
EMAIL:edersongonsalvesaltatelas@gmail.com
SENHA: Alta972600

ERDESSON QUIRINO DE LIMA  
CPF: 385.283.058-30
DATA DE NASCIMENTO: 17/10/1988 
NUMERO: 16 98192-4980 
EMAIL: erdersonaltatelas@gmail.com
SENHA: Alta972600$

EVERTON SAMPAIO MELO DA COSTA
CPF: 258.334.658-00
DATA DE NASCIMENTO: 14/01/1976
NUMERO: 11 96917-5480 
EMAIL: evertonaltatelas@gmail.com
SENHA: Alta972600$

FELIPE ARAUJO DOS SANTOS 
CPF: 101.876.985-46
DATA DE NASCIMENTO: 13/03/2003
NUMERO: 16 99292-3212
EMAIL: felipealtatelas@gmail.com
SENHA: Alta972600

FERNANDO SILVA DE SOUZA
CPF: 005.378.972-59
DATA DE NASCIMENTO: 25/01/1989
NUMERO: 16 99278-2701
EMAIL: fernandoaltatelas@gmail.com
SENHA: Alta972600$

FILIPE DELFINO
CPF: 350.969 688-39
DATA DE NASCIMENTO: 07/05/1987
NUMERO: 16 99261-7738
EMAIL: filipedelfinoaltatelas@gmail.com
SENHA: Alta972600$

GABRIEL JACKSON PEIXOTO RIBEIRO 
CPF: 438.515.568-28
DATA DE NASCIMENTO: 08/07/1996 
NUMERO: 16 99361-7195
EMAIL: gabrielaltatelas@gmail.com
SENHA: Alta972600$

GUSTAVO ADOLFO CASTANEDA CARDENAS
CPF: 023.066.106-81
DATA DE NASCIMENTO: 23/12/1986
NUMERO: 11 96293-9343
EMAIL: gustavoaltatelas@gmail.com
SENHA: Alta972600@

JARDIEL NUNES DA SILVA
CPF: 070.368.533-36
DATA DE NASCIMENTO: 13/09/2000 
NUMERO: 16 98191-9551
EMAIL: jardielaltatelas@gmail.com
SENHA: Alta972600$

JUNIEL DE SOUSA
CPF: 011.619.363-86
DATA DE NASCIMENTO: 07/09/1984
NUMERO: 16 99204-7416
EMAIL: junielaltatelas@gmail.com
SENHA: Alta972600$

KAIQUE DE OLIVEIRA SANTOS 
CPF: 435.731.658-85
DATA DE NASCIMENTO: 02/12/1997
NUMERO: 16 99447-8913
EMAIL: kaiquealtatelas@gmail.com
SENHA: Alta972600$

LEANDRO RODRIGUES DE SOUZA 
CPF: 414.455.308-64
DATA DE NASCIMENTO: 26/07/1987
NUMERO: 16 99396-5158
EMAIL: leandroaltatelas@gmail.com
SENHA: Alta972600$

LEONARDO DOUGLAS DE OLIVEIRA CORREA 
CPF: 525.803.638-31
DATA DE NASCIMENTO: 05/03/2003
NUMERO: 11 93397-5926
EMAIL: leonardoaltatelas@gmail.com
SENHA: Alta972600$

LUCAS EDUARDO RIBEIRO FRANÇA E SILVA 
CPF: 468.944.148-07
DATA DE NASCIMENTO: 27/10/2006
NUMERO: 16 98836-9753
EMAIL: lucasaltatelas@gmail.com
SENHA: Alta972600$

LUCIANO DE JESUS
CPF: 264.298.638-16
DATA DE NASCIMENTO: 06/11/1975
NUMERO:  16 99754-1563
EMAIL: lucianoaltatelas@gmail.com
SENHA: Alta972600$

LUIS HENRIQUE ROCETTI DA SILVA
CPF: 412.241.338-97
DATA DE NASCIMENTO: 08/03/1992
NUMERO: 16 99649-4762
EMAIL: luisaltatelas@gmail.com
SENHA: Alta972600$

MAICON DOUGLAS DOS SANTOS INFORZATO
CPF: 463.539.228-76
DATA DE NASCIMENTO: 01/05/1993 
NUMERO: 16 98152-5822
EMAIL: maiconaltatelas@gmail.com
SENHA: Alta972600$

MATHEUS SOUSA COSTA 
CPF: 538.169.808-99
DATA DE NASCIMENTO: 01/12/2001
NUMERO: 16 99111-6444
EMAIL: matheusaltatelas@gmail.com
SENHA: Alta972600$

MOEMIA COSTA DE OLIVEIRA
DATA DE NASCIMENTO: 05/02/1987
CPF: 362.026.838-05
NUMERO: 11 96150-8453
EMAIL:moemia.costa@altatelas.com
SENHA: Alta972600$

PABLO HENRIQUE RIBEIRO FRIZI
CPF: 584.518.788-57
DATA DE NASCIMENTO: 22/12/2007
NUMERO:  16 99449-1102
EMAIL: pabloaltatelas@gmail.com
SENHA: Alta972600$

PAULO FERREIRA CARDOSO
CPF:  427.979.418-96
DATA DE NASCIMENTO: 27/10/1997
NUMERO: 16 99715-6763
EMAIL: pauloaltatelas@gmail.com
SENHA: Alta972600$

RAFAEL DE SOUZA COSTA
CPF: 106.957.083-41
DATA DE NASCIMENTO: 09/05/2005
NUMERO: 89 9421-1070
EMAIL: rafaelaltatelas@gmail.com
SENHA: Alta972600$

RODRIGO APARECIDO COELHO PAULISTA
CPF: 218.937.248-83
DATA DE NASCIMENTO: 02/12/1982
NUMERO: 16 99627-3207
EMAIL: rodrigoaltatelas@gmail.com
SENHA: Alta972600$

RONALDO HENRIQUE DO CARMO 
CPF: 342.202.368-21
DATA DE NASCIMENTO: 14/09/1986 
NUMERO: 16 98846-2058
EMAIL: ronaldoaltatelas@gmail.com
SENHA: Alta972600$

VICTOR HUGO VIANA GARCEZ 
CPF: 384.657.848-76
DATA DE NASCIMENTO: 15/09/2000
NUMERO: 16 99307-5592
EMAIL: victorhugoaltatelas@gmail.com
SENHA: Alta972600$

VITOR BRENO DE SOUZA ARAUJO 
CPF: 485.789.938-88
DATA DE NASCIMENTO: 15/09/2001
NUMERO: 16 98187-3464
EMAIL: vitorbrenoaltatelas@gmail.com
SENHA: Alta972600$

WAGNER ZAMBONI 
CPF: 286246658-17
DATA DE NASCIMENTO: 17/08/1980
NUMERO: 16 99722-6712
EMAIL: wagneraltatelas@gmail.com
SENHA: Alta972600$

WENDEL HENRIQUE ANTONIO DA SILVA
CPF: 504.069.548-95
DATA DE NASCIMENTO: 09/12/1998
NUMERO: 16 99166-2527
EMAIL: wendelaltatelas@gmail.com
SENHA: Alta972600$

WILLIAM RODRIGUES DA SILVA
CPF: 524.429.368-01
DATA DE NASCIMENTO: 16/03/2001
NUMERO: 16 99650-8192
EMAIL: williamaltatelas@gmail.com
SENHA: Alta972600$
"""


def parse_data(data_string):
    funcionarios = []
    # Divide o bloco de texto em registros de funcionários
    records = data_string.strip().split('\n\n')

    for record in records:
        lines = record.strip().split('\n')

        # Inicializa o dicionário de funcionário
        funcionario_data = {
            'nome_completo': '',
            'cpf': '',
            'data_nascimento': None,
            'telefone': '',
            'email': '',
            'senha': ''
        }

        # A primeira linha é sempre o nome
        funcionario_data['nome_completo'] = lines[0].strip()

        # Processa as outras linhas
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('CPF:'):
                funcionario_data['cpf'] = line.replace('CPF:', '').strip()
            elif 'DATA DE NASCIMENTO:' in line:
                dt_str = line.replace('DATA DE NASCIMENTO:', '').strip()
                try:
                    # Converte dd/mm/yyyy para yyyy-mm-dd
                    funcionario_data['data_nascimento'] = datetime.strptime(
                        dt_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    print(
                        f"AVISO: Data de nascimento inválida para {funcionario_data['nome_completo']}: {dt_str}")
                    funcionario_data['data_nascimento'] = None
            elif 'NUMERO:' in line or 'NÚMERO:' in line:
                funcionario_data['telefone'] = re.sub(
                    r'NUMERO:|NÚMERO:', '', line).strip()
            elif line.startswith('EMAIL:'):
                funcionario_data['email'] = line.replace('EMAIL:', '').strip()
            elif line.startswith('SENHA:'):
                funcionario_data['senha'] = line.replace('SENHA:', '').strip()

        # Caso especial para Moemia, onde a ordem está diferente
        if "MOEMIA COSTA DE OLIVEIRA" in funcionario_data['nome_completo']:
            for line in lines[1:]:
                if line.startswith('CPF:'):
                    funcionario_data['cpf'] = line.replace('CPF:', '').strip()
                elif 'DATA DE NASCIMENTO:' in line:
                    dt_str = line.replace('DATA DE NASCIMENTO:', '').strip()
                    try:
                        funcionario_data['data_nascimento'] = datetime.strptime(
                            dt_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        print(
                            f"AVISO: Data de nascimento inválida para {funcionario_data['nome_completo']}: {dt_str}")
                        funcionario_data['data_nascimento'] = None

        funcionarios.append(funcionario_data)

    return funcionarios


def update_database(db_path, funcionarios):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for func in funcionarios:
        # Verifica se o funcionário já existe pelo CPF
        cursor.execute(
            "SELECT id FROM funcionario WHERE cpf = ?", (func['cpf'],))
        result = cursor.fetchone()

        if result:
            # Atualiza o funcionário existente
            func_id = result[0]
            cursor.execute("""
                UPDATE funcionario
                SET nome = ?, data_nascimento = ?, telefone = ?, email = ?, senha = ?
                WHERE id = ?
            """, (
                func['nome_completo'],
                func['data_nascimento'],
                func['telefone'],
                func['email'],
                func['senha'],
                func_id
            ))
            print(
                f"Funcionário ATUALIZADO: {func['nome_completo']} (CPF: {func['cpf']})")
        else:
            # Insere um novo funcionário
            cursor.execute("""
                INSERT INTO funcionario (nome, cpf, data_nascimento, telefone, email, senha)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                func['nome_completo'],
                func['cpf'],
                func['data_nascimento'],
                func['telefone'],
                func['email'],
                func['senha']
            ))
            print(
                f"Funcionário CADASTRADO: {func['nome_completo']} (CPF: {func['cpf']})")

    conn.commit()
    conn.close()


def conectar_banco():
    """Conecta ao banco de dados SQLite."""
    # O banco de dados estará em instance/certificados.db
    return sqlite3.connect('instance/certificados.db')


def extrair_info_funcionario(bloco):
    """Extrai as informações do funcionário de um bloco de texto."""
    linhas = bloco.strip().split('\n')
    info_funcionario = {}

    # A primeira linha é sempre o nome
    info_funcionario['nome_completo'] = linhas[0].strip()

    for linha in linhas[1:]:
        linha = linha.strip()
        if linha.startswith('CPF:'):
            info_funcionario['cpf'] = linha.replace('CPF:', '').strip()
        elif 'DATA DE NASCIMENTO:' in linha:
            dt_str = linha.replace('DATA DE NASCIMENTO:', '').strip()
            try:
                # Converte dd/mm/yyyy para yyyy-mm-dd
                info_funcionario['data_nascimento'] = datetime.strptime(
                    dt_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                print(
                    f"AVISO: Data de nascimento inválida para {info_funcionario['nome_completo']}: {dt_str}")
                info_funcionario['data_nascimento'] = None
        elif 'NUMERO:' in linha or 'NÚMERO:' in linha:
            info_funcionario['telefone'] = re.sub(
                r'NUMERO:|NÚMERO:', '', linha).strip()
        elif linha.startswith('EMAIL:'):
            info_funcionario['email'] = linha.replace('EMAIL:', '').strip()
        elif linha.startswith('SENHA:'):
            info_funcionario['senha'] = linha.replace('SENHA:', '').strip()

    return info_funcionario


if __name__ == '__main__':
    # Constrói o caminho absoluto para o arquivo do banco de dados
    script_dir = os.path.dirname(__file__)
    DB_FILE = os.path.join(script_dir, 'instance', 'certificados.db')

    # Garante que o diretório "instance" exista
    os.makedirs(os.path.join(script_dir, 'instance'), exist_ok=True)

    # Parse os dados
    funcionarios_a_cadastrar = parse_data(dados_funcionarios)

    # Atualiza o banco de dados
    update_database(DB_FILE, funcionarios_a_cadastrar)

    print("\n--- Processo de atualização concluído! ---")
