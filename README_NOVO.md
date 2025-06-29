# Sistema de Certificados NR - Alta Telas

Sistema web completo para geração automática de certificados de Normas Regulamentadoras (NR) com conversão automática para PDF.

## 🚀 Funcionalidades

- ✅ **Cadastro de Funcionários** com dados completos
- ✅ **Importação em Massa** de funcionários da Alta Telas
- ✅ **Geração Unitária** de certificados
- ✅ **Geração em Lote** para múltiplos funcionários
- ✅ **Conversão Automática** PowerPoint → PDF
- ✅ **Organização Automática** em pastas por funcionário
- ✅ **Interface Web Responsiva** com Bootstrap
- ✅ **Sistema de Relatórios** completo
- ✅ **Configuração de Modelos** NR

## 📁 Estrutura do Projeto

```
certificados-nr/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── README.md             # Documentação
├── .gitignore           # Arquivos ignorados pelo Git
├── static/              # Arquivos estáticos (CSS, JS)
│   ├── css/
│   └── js/
├── templates/           # Templates HTML
├── modelos_nr/         # Modelos PowerPoint das NRs
├── certificados/       # Certificados gerados (auto-criado)
└── instance/           # Banco de dados SQLite (auto-criado)
```

## 🏗️ Tecnologias Utilizadas

- **Backend:** Python Flask + SQLAlchemy
- **Frontend:** HTML5 + Bootstrap 5 + JavaScript
- **Banco de Dados:** SQLite
- **Geração PDF:** PowerPoint COM + comtypes/pywin32
- **Templates:** Jinja2

## ⚙️ Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd certificados-nr
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Executar o Sistema
```bash
python app.py
```

O sistema estará disponível em: http://127.0.0.1:5000

## 📋 Modelos PowerPoint

Coloque seus modelos PowerPoint na pasta `modelos_nr/` com as seguintes variáveis:

- `{{NOME}}` - Nome do funcionário
- `{{CPF}}` - CPF do funcionário  
- `{{RG}}` - RG do funcionário
- `{{FUNCAO}}` - Função do funcionário
- `{{TIPO_TREINAMENTO}}` - Tipo de treinamento
- `{{DATA}}` - Data de emissão
- `{{DATA_ADMISSAO}}` - Data de admissão
- `{{NR}}` - Tipo de NR (ex: NR06)
- `{{DESCRICAO_NR}}` - Descrição da NR

## 📄 Geração de Certificados

### Processo Automático:
1. **Carrega** o modelo PowerPoint correspondente
2. **Substitui** as variáveis com dados do funcionário
3. **Converte automaticamente** para PDF
4. **Organiza** na estrutura: `certificados/NOME_FUNCIONARIO/arquivo.pdf`

### Estrutura do Arquivo Gerado:
```
certificados/
└── NOME_FUNCIONARIO/
    └── NOME_FUNCIONARIO_2025-06-28_NR06_Inicial.pdf
```

## 👥 Funcionários Pré-cadastrados

O sistema inclui importação automática de 34 funcionários da Alta Telas com dados completos.

## 🔧 Configuração

### Modelos NR Suportados:
- **NR06** - Equipamentos de Proteção Individual
- **NR10** - Segurança em Instalações Elétricas  
- **NR12** - Segurança em Máquinas e Equipamentos
- **NR18** - Segurança na Construção Civil
- **NR33** - Espaços Confinados
- **NR35** - Trabalho em Altura

### Tipos de Treinamento:
- Treinamento Inicial
- Reciclagem
- Atualização
- Complementar

## 📊 Relatórios

- Total de funcionários cadastrados
- Total de certificados gerados
- Certificados por tipo de NR
- Últimos certificados emitidos

## 🛠️ Desenvolvimento

### Estrutura de Dados:

**Funcionário:**
- Nome, CPF, RG, Função
- Data de nascimento, telefone, email
- Data de admissão, senha

**Certificado:**
- Funcionário, tipo NR, tipo treinamento
- Data de emissão, caminho do arquivo

### APIs Principais:
- `/funcionarios` - Listagem de funcionários
- `/cadastrar_funcionario` - Cadastro individual
- `/importar_funcionarios` - Importação em massa
- `/gerar_unitario` - Geração individual
- `/gerar_lote` - Geração em lote
- `/relatorios` - Dashboard de relatórios

## 🔒 Segurança

- Validação de CPF
- Sanitização de nomes de arquivo
- Tratamento de erros robusto
- Logs detalhados de operações

## 📞 Suporte

Sistema desenvolvido para **Alta Telas Ltda**
- Geração automática de certificados NR
- Organização profissional de arquivos
- Interface intuitiva e responsiva

---

## 🚀 Deploy para Git

### GitHub:
```bash
# Criar repositório no GitHub e depois:
git remote add origin https://github.com/usuario/certificados-nr.git
git branch -M main
git push -u origin main
```

### GitLab:
```bash
# Criar repositório no GitLab e depois:
git remote add origin https://gitlab.com/usuario/certificados-nr.git
git branch -M main
git push -u origin main
```

## 📝 Licença

Sistema proprietário - Alta Telas Ltda © 2025
