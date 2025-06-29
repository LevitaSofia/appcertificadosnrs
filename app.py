from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import shutil
from pptx import Presentation
import re
from werkzeug.utils import secure_filename
import sqlite3
import comtypes.client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/imagens'

db = SQLAlchemy(app)

# Modelos do Banco de Dados


class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    rg = db.Column(db.String(20), nullable=True)
    funcao = db.Column(db.String(100), nullable=True, default='Não informado')
    data_admissao = db.Column(db.Date, nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    senha = db.Column(db.String(100), nullable=True)
    foto = db.Column(db.String(200))

    certificados = db.relationship(
        'CertificadoGerado', backref='funcionario', lazy=True)


class CertificadoGerado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey(
        'funcionario.id'), nullable=False)
    tipo_nr = db.Column(db.String(10), nullable=False)
    tipo_treinamento = db.Column(db.String(50), nullable=False)
    data_emissao = db.Column(db.Date, nullable=False)
    caminho_arquivo = db.Column(db.String(300), nullable=False)


class ModeloNR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_nr = db.Column(db.String(10), unique=True, nullable=False)
    caminho_modelo_pptx = db.Column(db.String(300), nullable=False)
    descricao = db.Column(db.String(200))

# Função para validar CPF


def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    def calcular_digito(cpf, peso):
        soma = sum(int(digito) * peso for digito,
                   peso in zip(cpf, range(peso, 1, -1)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    primeiro_digito = calcular_digito(cpf, 10)
    segundo_digito = calcular_digito(cpf, 11)

    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"

# Função para gerar certificado em PDF


# Função para converter PowerPoint para PDF
def converter_pptx_para_pdf(caminho_pptx, caminho_pdf):
    try:
        print(f"Tentando converter: {caminho_pptx} -> {caminho_pdf}")

        # Método 1: Tentar usar COM (PowerPoint)
        try:
            import comtypes.client

            # Criar aplicação PowerPoint
            powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
            powerpoint.Visible = False  # Executar em background

            # Abrir apresentação
            presentation = powerpoint.Presentations.Open(
                os.path.abspath(caminho_pptx))

            # Salvar como PDF
            presentation.SaveAs(os.path.abspath(
                caminho_pdf), 32)  # 32 = ppSaveAsPDF

            # Fechar apresentação e PowerPoint
            presentation.Close()
            powerpoint.Quit()

            print("Conversão COM bem-sucedida!")
            return True

        except Exception as com_error:
            print(f"Erro COM: {str(com_error)}")

            # Método 2: Tentar usar win32com como alternativa
            try:
                import win32com.client

                powerpoint = win32com.client.Dispatch("PowerPoint.Application")
                powerpoint.Visible = 0  # Não mostrar PowerPoint

                presentation = powerpoint.Presentations.Open(
                    os.path.abspath(caminho_pptx))
                presentation.SaveAs(os.path.abspath(caminho_pdf), 32)
                presentation.Close()
                powerpoint.Quit()

                print("Conversão win32com bem-sucedida!")
                return True

            except Exception as win32_error:
                print(f"Erro win32com: {str(win32_error)}")

                # Método 3: Usar subprocess como último recurso
                try:
                    import subprocess

                    # Comando PowerShell para converter
                    powershell_cmd = f'''
                    $powerpoint = New-Object -ComObject PowerPoint.Application
                    $powerpoint.Visible = $false
                    $presentation = $powerpoint.Presentations.Open("{os.path.abspath(caminho_pptx)}")
                    $presentation.SaveAs("{os.path.abspath(caminho_pdf)}", 32)
                    $presentation.Close()
                    $powerpoint.Quit()
                    '''

                    result = subprocess.run(
                        ["powershell", "-Command", powershell_cmd],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                    if result.returncode == 0:
                        print("Conversão PowerShell bem-sucedida!")
                        return True
                    else:
                        print(f"Erro PowerShell: {result.stderr}")

                except Exception as ps_error:
                    print(f"Erro PowerShell: {str(ps_error)}")

        return False

    except Exception as e:
        print(f"Erro geral na conversão: {str(e)}")
        return False

# Função para gerar certificado usando PowerPoint como base


def gerar_certificado(funcionario, tipo_nr, tipo_treinamento, data_emissao):
    try:
        # Buscar modelo
        modelo = ModeloNR.query.filter_by(tipo_nr=tipo_nr).first()
        if not modelo:
            return False, "Modelo não encontrado para este tipo de NR"

        # Verificar se arquivo modelo existe
        if not os.path.exists(modelo.caminho_modelo_pptx):
            return False, f"Arquivo do modelo não encontrado: {modelo.caminho_modelo_pptx}"

        # Carregar apresentação
        prs = Presentation(modelo.caminho_modelo_pptx)

        # Criar pasta do funcionário se não existir
        nome_funcionario_limpo = re.sub(r'[<>:"/\\|?*]', '_', funcionario.nome)
        pasta_funcionario = os.path.join(
            'certificados', nome_funcionario_limpo)
        os.makedirs(pasta_funcionario, exist_ok=True)

        # Preparar substituições
        data_formatada = data_emissao.strftime('%d/%m/%Y')
        data_admissao_formatada = funcionario.data_admissao.strftime(
            '%d/%m/%Y') if funcionario.data_admissao else 'Não informado'

        substituicoes = {
            '{{NOME}}': funcionario.nome,
            '{{CPF}}': funcionario.cpf,
            '{{RG}}': funcionario.rg if funcionario.rg else 'Não informado',
            '{{CARGO}}': funcionario.funcao if funcionario.funcao else 'Não informado',
            '{{FUNCAO}}': funcionario.funcao if funcionario.funcao else 'Não informado',
            '{{TIPO_TREINAMENTO}}': tipo_treinamento,
            '{{DATA}}': data_formatada,
            '{{DATA_EMISSAO}}': data_formatada,
            '{{DATA_ADMISSAO}}': data_admissao_formatada,
            '{{NR}}': tipo_nr,
            '{{TIPO_NR}}': tipo_nr,
            '{{DESCRICAO_NR}}': modelo.descricao
        }

        # Substituir texto nos slides
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    for find_text, replace_text in substituicoes.items():
                        if find_text in shape.text:
                            shape.text = shape.text.replace(
                                find_text, replace_text)

                # Verificar text_frame
                if hasattr(shape, "text_frame"):
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            for find_text, replace_text in substituicoes.items():
                                if find_text in run.text:
                                    run.text = run.text.replace(
                                        find_text, replace_text)

        # Salvar PowerPoint temporário
        data_formatada_arquivo = data_emissao.strftime('%Y-%m-%d')
        nome_arquivo_base = f"{nome_funcionario_limpo}_{data_formatada_arquivo}_{tipo_nr}_{tipo_treinamento}"
        caminho_pptx_temp = os.path.join(
            pasta_funcionario, f"{nome_arquivo_base}.pptx")
        caminho_pdf_final = os.path.join(
            pasta_funcionario, f"{nome_arquivo_base}.pdf")

        # Salvar PowerPoint preenchido
        print(f"Salvando PowerPoint em: {caminho_pptx_temp}")
        prs.save(caminho_pptx_temp)

        # Converter para PDF
        print("Iniciando conversão para PDF...")
        if converter_pptx_para_pdf(caminho_pptx_temp, caminho_pdf_final):
            print("✅ Conversão para PDF bem-sucedida!")
            # Remover arquivo PowerPoint temporário
            try:
                os.remove(caminho_pptx_temp)
                print("Arquivo PowerPoint temporário removido")
            except:
                print("Não foi possível remover o arquivo PowerPoint temporário")
                pass  # Se não conseguir remover, não é crítico

            caminho_final = caminho_pdf_final
            tipo_arquivo = "PDF"
        else:
            print("⚠️ Não foi possível converter para PDF, mantendo arquivo PowerPoint")
            caminho_final = caminho_pptx_temp
            tipo_arquivo = "PowerPoint"

        # Registrar no banco
        certificado = CertificadoGerado(
            funcionario_id=funcionario.id,
            tipo_nr=tipo_nr,
            tipo_treinamento=tipo_treinamento,
            data_emissao=data_emissao,
            caminho_arquivo=caminho_final
        )
        db.session.add(certificado)
        db.session.commit()

        print(f"✅ Certificado gerado com sucesso em: {caminho_final}")
        return True, caminho_final

    except Exception as e:
        print(f"❌ Erro ao gerar certificado: {str(e)}")
        return False, f"Erro ao gerar certificado: {str(e)}"

# Rotas


@app.route('/')
def index():
    funcionarios = Funcionario.query.all()
    modelos = ModeloNR.query.all()
    return render_template('index.html', funcionarios=funcionarios, modelos=modelos)


@app.route('/funcionarios')
def funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('funcionarios.html', funcionarios=funcionarios)


@app.route('/cadastrar_funcionario', methods=['GET', 'POST'])
def cadastrar_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        rg = request.form.get('rg', '')
        funcao = request.form.get('funcao', 'Não informado')
        data_admissao_str = request.form.get('data_admissao')
        data_nascimento_str = request.form.get('data_nascimento')
        telefone = request.form.get('telefone', '')
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')

        # Converter datas
        data_admissao = None
        if data_admissao_str:
            data_admissao = datetime.strptime(
                data_admissao_str, '%Y-%m-%d').date()

        data_nascimento = None
        if data_nascimento_str:
            data_nascimento = datetime.strptime(
                data_nascimento_str, '%Y-%m-%d').date()

        # Validar CPF
        if not validar_cpf(cpf):
            flash('CPF inválido!', 'error')
            return render_template('cadastrar_funcionario.html')

        # Verificar se CPF já existe
        if Funcionario.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado!', 'error')
            return render_template('cadastrar_funcionario.html')

        # Salvar funcionário
        funcionario = Funcionario(
            nome=nome,
            cpf=cpf,
            rg=rg,
            funcao=funcao,
            data_admissao=data_admissao,
            data_nascimento=data_nascimento,
            telefone=telefone,
            email=email,
            senha=senha
        )

        db.session.add(funcionario)
        db.session.commit()

        flash('Funcionário cadastrado com sucesso!', 'success')
        return redirect(url_for('funcionarios'))

    return render_template('cadastrar_funcionario.html')


@app.route('/gerar_unitario')
def gerar_unitario():
    funcionarios = Funcionario.query.all()
    modelos = ModeloNR.query.all()
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    return render_template('gerar_unitario.html', funcionarios=funcionarios, modelos=modelos, data_hoje=data_hoje)


@app.route('/processar_certificado_unitario', methods=['POST'])
def processar_certificado_unitario():
    funcionario_id = request.form['funcionario_id']
    tipo_nr = request.form['tipo_nr']
    tipo_treinamento = request.form['tipo_treinamento']
    data_emissao = datetime.strptime(
        request.form['data_emissao'], '%Y-%m-%d').date()

    funcionario = Funcionario.query.get_or_404(funcionario_id)

    sucesso, resultado = gerar_certificado(
        funcionario, tipo_nr, tipo_treinamento, data_emissao)

    if sucesso:
        flash('Certificado gerado com sucesso!', 'success')
        return send_file(resultado, as_attachment=True)
    else:
        flash(f'Erro: {resultado}', 'error')
        return redirect(url_for('gerar_unitario'))


@app.route('/gerar_lote')
def gerar_lote():
    funcionarios = Funcionario.query.all()
    modelos = ModeloNR.query.all()
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    return render_template('gerar_lote.html', funcionarios=funcionarios, modelos=modelos, data_hoje=data_hoje)


@app.route('/processar_certificados_lote', methods=['POST'])
def processar_certificados_lote():
    funcionarios_ids = request.form.getlist('funcionarios_ids')
    tipo_nr = request.form['tipo_nr']
    tipo_treinamento = request.form['tipo_treinamento']
    data_emissao = datetime.strptime(
        request.form['data_emissao'], '%Y-%m-%d').date()

    resultados = []

    for funcionario_id in funcionarios_ids:
        funcionario = Funcionario.query.get(funcionario_id)
        if funcionario:
            sucesso, resultado = gerar_certificado(
                funcionario, tipo_nr, tipo_treinamento, data_emissao)
            resultados.append({
                'funcionario': funcionario.nome,
                'sucesso': sucesso,
                'resultado': resultado
            })

    flash(f'Processados {len(resultados)} certificados', 'info')
    return render_template('resultado_lote.html', resultados=resultados)


@app.route('/relatorios')
def relatorios():
    # Estatísticas gerais
    total_funcionarios = Funcionario.query.count()
    total_certificados = CertificadoGerado.query.count()

    # Certificados por NR
    certificados_por_nr = db.session.query(
        CertificadoGerado.tipo_nr,
        db.func.count(CertificadoGerado.id).label('total')
    ).group_by(CertificadoGerado.tipo_nr).all()

    # Últimos certificados
    ultimos_certificados = db.session.query(CertificadoGerado, Funcionario).join(
        Funcionario, CertificadoGerado.funcionario_id == Funcionario.id
    ).order_by(CertificadoGerado.data_emissao.desc()).limit(10).all()

    return render_template('relatorios.html',
                           total_funcionarios=total_funcionarios,
                           total_certificados=total_certificados,
                           certificados_por_nr=certificados_por_nr,
                           ultimos_certificados=ultimos_certificados)


@app.route('/configuracoes')
def configuracoes():
    modelos = ModeloNR.query.all()
    return render_template('configuracoes.html', modelos=modelos)


@app.route('/cadastrar_modelo', methods=['POST'])
def cadastrar_modelo():
    tipo_nr = request.form['tipo_nr']
    descricao = request.form['descricao']

    # Verificar se já existe
    if ModeloNR.query.filter_by(tipo_nr=tipo_nr).first():
        flash('Modelo para esta NR já existe!', 'error')
        return redirect(url_for('configuracoes'))

    # Caminho do modelo
    caminho_modelo = f"modelos_nr/{tipo_nr}_modelo.pptx"

    modelo = ModeloNR(
        tipo_nr=tipo_nr,
        caminho_modelo_pptx=caminho_modelo,
        descricao=descricao
    )

    db.session.add(modelo)
    db.session.commit()

    flash('Modelo cadastrado! Lembre-se de colocar o arquivo PowerPoint na pasta modelos_nr/', 'success')
    return redirect(url_for('configuracoes'))


@app.route('/importar_funcionarios', methods=['POST'])
def importar_funcionarios():
    """Rota para importar funcionários em lote"""
    try:
        funcionarios_data = [
            {
                'nome': 'ANDRE ROBERTO DOS SANTOS',
                'cpf': '313.673.508-08',
                'data_nascimento': '12/01/1980',
                'telefone': '11 94870-7283',
                'email': 'andrealtatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Técnico de Segurança'
            },
            {
                'nome': 'BRUNO PINHEIRO DE LIMA',
                'cpf': '401.201.328-93',
                'data_nascimento': '27/04/1990',
                'telefone': '11 95273-9404',
                'email': 'brunoaltatelas@gmail.com',
                'senha': 'Alta972600#',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'CAIO VINICIUS PAES DO NASCIMENTO',
                'cpf': '414.038.588-02',
                'data_nascimento': '30/05/1991',
                'telefone': '11 95487-5236',
                'email': '',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'CARLOS ALBERTO DOS SANTOS',
                'cpf': '288.915.798-90',
                'data_nascimento': '21/11/1978',
                'telefone': '16 98865-1612',
                'email': 'carlosaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Supervisor de Instalação'
            },
            {
                'nome': 'CLEUTON CLEBER VIEIRA ROMANO',
                'cpf': '270.176.758-00',
                'data_nascimento': '05/12/1979',
                'telefone': '19 990058626',
                'email': 'cleutonaltatelas@gmail.com',
                'senha': 'Alta972600#',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'DIOGO PEREIRA CARDOSO',
                'cpf': '058.224.705-56',
                'data_nascimento': '30/12/1991',
                'telefone': '16 98103-7258',
                'email': 'diogoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'EDERSON GONÇALVES VIEIRA DA SILVA',
                'cpf': '495.685.328-97',
                'data_nascimento': '10/09/1999',
                'telefone': '16 99430-4340',
                'email': 'edersongonsalvesaltatelas@gmail.com',
                'senha': 'Alta972600',
                'funcao': 'Auxiliar de Instalação'
            },
            {
                'nome': 'ERDESSON QUIRINO DE LIMA',
                'cpf': '385.283.058-30',
                'data_nascimento': '17/10/1988',
                'telefone': '16 98192-4980',
                'email': 'erdersonaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'EVERTON SAMPAIO MELO DA COSTA',
                'cpf': '258.334.658-00',
                'data_nascimento': '14/01/1976',
                'telefone': '11 96917-5480',
                'email': 'evertonaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Supervisor de Instalação'
            },
            {
                'nome': 'FELIPE ARAUJO DOS SANTOS',
                'cpf': '101.876.985-46',
                'data_nascimento': '13/03/2003',
                'telefone': '16 99292-3212',
                'email': 'felipealtatelas@gmail.com',
                'senha': 'Alta972600',
                'funcao': 'Auxiliar de Instalação'
            },
            {
                'nome': 'FERNANDO SILVA DE SOUZA',
                'cpf': '005.378.972-59',
                'data_nascimento': '25/01/1989',
                'telefone': '16 99278-2701',
                'email': 'fernandoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'FILIPE DELFINO',
                'cpf': '350.969.688-39',
                'data_nascimento': '07/05/1987',
                'telefone': '16 99261-7738',
                'email': 'filipedelfinoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'GABRIEL JACKSON PEIXOTO RIBEIRO',
                'cpf': '438.515.568-28',
                'data_nascimento': '08/07/1996',
                'telefone': '16 99361-7195',
                'email': 'gabrielaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'GUSTAVO ADOLFO CASTANEDA CARDENAS',
                'cpf': '023.066.106-81',
                'data_nascimento': '23/12/1986',
                'telefone': '11 96293-9343',
                'email': 'gustavoaltatelas@gmail.com',
                'senha': 'Alta972600@',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'JARDIEL NUNES DA SILVA',
                'cpf': '070.368.533-36',
                'data_nascimento': '13/09/2000',
                'telefone': '16 98191-9551',
                'email': 'jardielaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Auxiliar de Instalação'
            },
            {
                'nome': 'JUNIEL DE SOUSA',
                'cpf': '011.619.363-86',
                'data_nascimento': '07/09/1984',
                'telefone': '16 99204-7416',
                'email': 'junielaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'KAIQUE DE OLIVEIRA SANTOS',
                'cpf': '435.731.658-85',
                'data_nascimento': '02/12/1997',
                'telefone': '16 99447-8913',
                'email': 'kaiquealtatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Auxiliar de Instalação'
            },
            {
                'nome': 'LEANDRO RODRIGUES DE SOUZA',
                'cpf': '414.455.308-64',
                'data_nascimento': '26/07/1987',
                'telefone': '16 99396-5158',
                'email': 'leandroaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'LEONARDO DOUGLAS DE OLIVEIRA CORREA',
                'cpf': '525.803.638-31',
                'data_nascimento': '05/03/2003',
                'telefone': '11 93397-5926',
                'email': 'leonardoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Auxiliar de Instalação'
            },
            {
                'nome': 'LUCAS EDUARDO RIBEIRO FRANÇA E SILVA',
                'cpf': '468.944.148-07',
                'data_nascimento': '27/10/2006',
                'telefone': '16 98836-9753',
                'email': 'lucasaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Menor Aprendiz'
            },
            {
                'nome': 'LUCIANO DE JESUS',
                'cpf': '264.298.638-16',
                'data_nascimento': '06/11/1975',
                'telefone': '16 99754-1563',
                'email': 'lucianoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Supervisor de Instalação'
            },
            {
                'nome': 'LUIS HENRIQUE ROCETTI DA SILVA',
                'cpf': '412.241.338-97',
                'data_nascimento': '08/03/1992',
                'telefone': '16 99649-4762',
                'email': 'luisaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'MAICON DOUGLAS DOS SANTOS INFORZATO',
                'cpf': '463.539.228-76',
                'data_nascimento': '01/05/1993',
                'telefone': '16 98152-5822',
                'email': 'maiconaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'MATHEUS SOUSA COSTA',
                'cpf': '538.169.808-99',
                'data_nascimento': '01/12/2001',
                'telefone': '16 99111-6444',
                'email': 'matheusaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Auxiliar de Instalação'
            },
            {
                'nome': 'MOEMIA COSTA DE OLIVEIRA',
                'cpf': '362.026.838-05',
                'data_nascimento': '05/02/1987',
                'telefone': '11 96150-8453',
                'email': 'moemia.costa@altatelas.com',
                'senha': 'Alta972600$',
                'funcao': 'Assistente Administrativo'
            },
            {
                'nome': 'PABLO HENRIQUE RIBEIRO FRIZI',
                'cpf': '584.518.788-57',
                'data_nascimento': '22/12/2007',
                'telefone': '16 99449-1102',
                'email': 'pabloaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Menor Aprendiz'
            },
            {
                'nome': 'PAULO FERREIRA CARDOSO',
                'cpf': '427.979.418-96',
                'data_nascimento': '27/10/1997',
                'telefone': '16 99715-6763',
                'email': 'pauloaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'RAFAEL DE SOUZA COSTA',
                'cpf': '106.957.083-41',
                'data_nascimento': '09/05/2005',
                'telefone': '89 9421-1070',
                'email': 'rafaelaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Menor Aprendiz'
            },
            {
                'nome': 'RODRIGO APARECIDO COELHO PAULISTA',
                'cpf': '218.937.248-83',
                'data_nascimento': '02/12/1982',
                'telefone': '16 99627-3207',
                'email': 'rodrigoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'RONALDO HENRIQUE DO CARMO',
                'cpf': '342.202.368-21',
                'data_nascimento': '14/09/1986',
                'telefone': '16 98846-2058',
                'email': 'ronaldoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'VICTOR HUGO VIANA GARCEZ',
                'cpf': '384.657.848-76',
                'data_nascimento': '15/09/2000',
                'telefone': '16 99307-5592',
                'email': 'victorhugoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Auxiliar de Instalação'
            },
            {
                'nome': 'VITOR BRENO DE SOUZA ARAUJO',
                'cpf': '485.789.938-88',
                'data_nascimento': '15/09/2001',
                'telefone': '16 98187-3464',
                'email': 'vitorbrenoaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Auxiliar de Instalação'
            },
            {
                'nome': 'WAGNER ZAMBONI',
                'cpf': '286.246.658-17',
                'data_nascimento': '17/08/1980',
                'telefone': '16 99722-6712',
                'email': 'wagneraltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Supervisor de Instalação'
            },
            {
                'nome': 'WENDEL HENRIQUE ANTONIO DA SILVA',
                'cpf': '504.069.548-95',
                'data_nascimento': '09/12/1998',
                'telefone': '16 99166-2527',
                'email': 'wendelaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Instalador de Telas'
            },
            {
                'nome': 'WILLIAM RODRIGUES DA SILVA',
                'cpf': '524.429.368-01',
                'data_nascimento': '16/03/2001',
                'telefone': '16 99650-8192',
                'email': 'williamaltatelas@gmail.com',
                'senha': 'Alta972600$',
                'funcao': 'Auxiliar de Instalação'
            }
        ]

        sucessos = 0
        erros = 0
        mensagens_erro = []

        for func_data in funcionarios_data:
            try:
                # Verificar se CPF já existe
                cpf_limpo = re.sub(r'[^0-9]', '', func_data['cpf'])
                cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:11]}"

                # Verificar se funcionário já existe e atualizar
                funcionario_existente = Funcionario.query.filter_by(cpf=cpf_formatado).first()
                if funcionario_existente:
                    # Atualizar funcionário existente com nova função
                    funcionario_existente.funcao = func_data.get('funcao', 'Instalador de Telas')
                    funcionario_existente.telefone = func_data['telefone']
                    funcionario_existente.email = func_data['email'] if func_data['email'] else None
                    funcionario_existente.senha = func_data['senha']
                    sucessos += 1
                    continue

                # Converter data de nascimento
                data_nascimento = datetime.strptime(
                    func_data['data_nascimento'], '%d/%m/%Y').date()

                # Verificar se funcionário já existe e atualizar
                funcionario_existente = Funcionario.query.filter_by(cpf=cpf_formatado).first()
                if funcionario_existente:
                    # Atualizar funcionário existente com nova função
                    funcionario_existente.funcao = func_data.get('funcao', 'Instalador de Telas')
                    funcionario_existente.telefone = func_data['telefone']
                    funcionario_existente.email = func_data['email'] if func_data['email'] else None
                    funcionario_existente.senha = func_data['senha']
                    sucessos += 1
                    continue

                # Criar funcionário
                funcionario = Funcionario(
                    nome=func_data['nome'],
                    cpf=cpf_formatado,
                    data_nascimento=data_nascimento,
                    telefone=func_data['telefone'],
                    email=func_data['email'] if func_data['email'] else None,
                    senha=func_data['senha'],
                    funcao=func_data.get('funcao', 'Instalador de Telas'),  # Usar função específica ou padrão
                    data_admissao=datetime.now().date()  # Data atual como admissão
                )

                db.session.add(funcionario)
                sucessos += 1

            except Exception as e:
                erros += 1
                mensagens_erro.append(
                    f"Erro ao processar {func_data['nome']}: {str(e)}")

        db.session.commit()

        mensagem = f"Importação concluída! {sucessos} funcionários adicionados"
        if erros > 0:
            mensagem += f", {erros} erros encontrados"

        flash(mensagem, 'success' if erros == 0 else 'warning')

        if mensagens_erro:
            # Mostrar apenas os primeiros 5 erros
            for msg in mensagens_erro[:5]:
                flash(msg, 'error')

        return redirect(url_for('funcionarios'))

    except Exception as e:
        flash(f'Erro na importação: {str(e)}', 'error')
        return redirect(url_for('funcionarios'))

# Inicializar banco de dados


def criar_tabelas():
    db.create_all()

    # Criar modelos padrão se não existirem
    modelos_padrao = [
        {'tipo_nr': 'NR06', 'descricao': 'Equipamentos de Proteção Individual'},
        {'tipo_nr': 'NR10', 'descricao': 'Segurança em Instalações e Serviços em Eletricidade'},
        {'tipo_nr': 'NR12', 'descricao': 'Segurança no Trabalho em Máquinas e Equipamentos'},
        {'tipo_nr': 'NR18', 'descricao': 'Condições de Segurança na Indústria da Construção'},
        {'tipo_nr': 'NR33',
            'descricao': 'Segurança e Saúde nos Trabalhos em Espaços Confinados'},
        {'tipo_nr': 'NR35', 'descricao': 'Trabalho em Altura'}
    ]

    for modelo_info in modelos_padrao:
        if not ModeloNR.query.filter_by(tipo_nr=modelo_info['tipo_nr']).first():
            modelo = ModeloNR(
                tipo_nr=modelo_info['tipo_nr'],
                caminho_modelo_pptx=f"modelos_nr/{modelo_info['tipo_nr']}_modelo.pptx",
                descricao=modelo_info['descricao']
            )
            db.session.add(modelo)

    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        criar_tabelas()
    app.run(debug=True)
