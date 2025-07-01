import pandas as pd
import re
from datetime import datetime
from app import app, db, Funcionario


def limpar_cpf(cpf):
    """Remove caracteres especiais do CPF"""
    if pd.isna(cpf):
        return None
    return re.sub(r'[^0-9]', '', str(cpf))


def converter_data(data_str):
    """Converte string de data para objeto date"""
    if pd.isna(data_str):
        return None

    # Tenta diferentes formatos de data
    formatos = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']

    for formato in formatos:
        try:
            return datetime.strptime(str(data_str), formato).date()
        except ValueError:
            continue
    return None


def atualizar_funcionarios_excel():
    """Atualiza funcionários do banco usando arquivo Excel"""

    try:
        # Lê o arquivo Excel
        df = pd.read_excel('csv alt atelas.xlsx')

        print(f"Arquivo Excel carregado com {len(df)} registros")
        print("Colunas encontradas:", list(df.columns))

        with app.app_context():
            funcionarios_atualizados = 0
            funcionarios_novos = 0

            for index, row in df.iterrows():
                try:
                    # Extrai dados usando os nomes das colunas
                    nome = str(row['Nome Completo']).strip() if not pd.isna(
                        row['Nome Completo']) else None
                    cpf = limpar_cpf(row['CPF']) if not pd.isna(
                        row['CPF']) else None
                    data_nasc = converter_data(row['Data de Nascimento']) if not pd.isna(
                        row['Data de Nascimento']) else None
                    telefone = str(row['Número']).strip(
                    ) if not pd.isna(row['Número']) else None
                    email = str(row['Email']).strip() if not pd.isna(
                        row['Email']) else ""
                    senha = str(row['Senha']).strip() if not pd.isna(
                        row['Senha']) else None
                    cargo = str(row['Cargo']).strip() if not pd.isna(
                        row['Cargo']) else 'Funcionário'

                    if not nome or not cpf:
                        print(
                            f"Linha {index + 1}: Nome ou CPF faltando - pulando")
                        continue

                    # Verifica se funcionário já existe
                    funcionario = Funcionario.query.filter_by(cpf=cpf).first()

                    if funcionario:
                        # Atualiza funcionário existente
                        funcionario.nome = nome
                        funcionario.data_nascimento = data_nasc
                        funcionario.telefone = telefone
                        funcionario.email = email if email else ""
                        funcionario.funcao = cargo

                        # Atualiza senha se fornecida
                        if senha:
                            funcionario.set_password(senha)

                        funcionarios_atualizados += 1
                        print(f"✓ Atualizado: {nome} - {cargo}")
                    else:
                        # Cria novo funcionário
                        funcionario = Funcionario(
                            nome=nome,
                            cpf=cpf,
                            data_nascimento=data_nasc,
                            telefone=telefone,
                            email=email if email else "",
                            funcao=cargo
                        )

                        # Define senha - usa a fornecida ou primeiros 6 dígitos do CPF
                        if senha:
                            funcionario.set_password(senha)
                        else:
                            funcionario.set_password(cpf[:6])

                        db.session.add(funcionario)
                        funcionarios_novos += 1
                        print(f"✓ Novo: {nome} - {cargo}")

                except Exception as e:
                    print(f"Erro na linha {index + 1}: {e}")
                    continue

            # Salva as alterações
            db.session.commit()

            print(f"\n✅ Processamento concluído!")
            print(f"📊 Funcionários atualizados: {funcionarios_atualizados}")
            print(f"📊 Funcionários novos: {funcionarios_novos}")
            print(f"📊 Total no banco: {Funcionario.query.count()}")

    except Exception as e:
        print(f"❌ Erro ao processar arquivo Excel: {e}")


if __name__ == "__main__":
    atualizar_funcionarios_excel()
