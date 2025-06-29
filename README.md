# Sistema de Certificados NR

Sistema web desenvolvido em Python Flask para geração automatizada de certificados de Normas Regulamentadoras (NR).

## 📋 Características

- ✅ **Geração Automática**: Substitui variáveis em modelos PowerPoint
- ✅ **Gestão de Funcionários**: Cadastro completo com validação de CPF
- ✅ **Múltiplas NRs**: Suporte para NR06, NR10, NR12, NR18, NR33, NR35
- ✅ **Geração em Lote**: Processe múltiplos certificados simultaneamente
- ✅ **Interface Moderna**: Design responsivo com Bootstrap 5
- ✅ **Relatórios**: Acompanhe estatísticas e histórico
- ✅ **Banco SQLite**: Leve e sem necessidade de configuração

## 🚀 Instalação Rápida

### 1. Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalação

```bash
# Clone ou baixe o projeto
cd certificados-nr

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

### 3. Acesse o Sistema

Abra seu navegador e acesse: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
certificados-nr/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── certificados.db       # Banco de dados SQLite (criado automaticamente)
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── cadastrar_funcionario.html
│   ├── funcionarios.html
│   ├── gerar_unitario.html
│   ├── gerar_lote.html
│   ├── relatorios.html
│   ├── configuracoes.html
│   └── resultado_lote.html
├── static/              # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── imagens/         # Fotos dos funcionários
├── modelos_nr/          # Modelos PowerPoint
│   ├── NR06_modelo.pptx
│   ├── NR12_modelo.pptx
│   ├── NR18_modelo.pptx
│   └── NR35_modelo.pptx
└── certificados/        # Certificados gerados
    └── nome_funcionario/
        ├── NR18_2025-06-28.pptx
        └── NR18_2025-06-28.pdf
```

## 🎯 Como Usar

### 1. Configurar Modelos

1. Coloque seus arquivos `.pptx` na pasta `modelos_nr/`
2. Use as variáveis no PowerPoint:
   - `{{NOME}}` - Nome do funcionário
   - `{{CPF}}` - CPF formatado
   - `{{RG}}` - RG
   - `{{CARGO}}` - Função/cargo
   - `{{DATA_ADMISSAO}}` - Data de admissão
   - `{{TIPO_TREINAMENTO}}` - Tipo de treinamento
   - `{{DATA}}` - Data de emissão

### 2. Cadastrar Funcionários

1. Acesse **Funcionários → Cadastrar Funcionário**
2. Preencha todos os dados obrigatórios
3. CPF será validado automaticamente
4. Foto é opcional

### 3. Gerar Certificados

#### Certificado Unitário:
1. Acesse **Certificados → Gerar Unitário**
2. Selecione funcionário, NR e tipo de treinamento
3. Defina a data de emissão
4. Clique em **Gerar e Baixar**

#### Certificados em Lote:
1. Acesse **Certificados → Gerar em Lote**
2. Configure NR, tipo de treinamento e data
3. Selecione os funcionários
4. Clique em **Gerar Certificados em Lote**

### 4. Acompanhar Relatórios

- Acesse **Relatórios** para ver estatísticas
- Visualize gráficos de certificados por NR
- Acompanhe histórico de certificados gerados

## 🔧 Configuração Avançada

### Personalizando Modelos

1. Abra seu arquivo PowerPoint
2. Insira as variáveis onde desejar:
   ```
   Certificamos que {{NOME}}, portador do CPF {{CPF}}, 
   função {{CARGO}}, concluiu com aproveitamento o 
   treinamento {{TIPO_TREINAMENTO}} da {{NR}} em {{DATA}}.
   ```
3. Salve na pasta `modelos_nr/` com o nome `NRxx_modelo.pptx`

### Adicionando Nova NR

1. Acesse **Configurações**
2. Clique em **Adicionar Novo Modelo**
3. Preencha tipo (ex: NR33) e descrição
4. Coloque o arquivo `.pptx` na pasta `modelos_nr/`

### Backup dos Dados

- O arquivo `certificados.db` contém todos os dados
- Faça backup regular deste arquivo
- Para restaurar, substitua o arquivo pelo backup

## 📦 Dependências

- **Flask 2.3.3** - Framework web
- **Flask-SQLAlchemy 3.0.5** - ORM para banco de dados
- **python-pptx 0.6.21** - Manipulação de arquivos PowerPoint
- **pdfkit 1.0.0** - Conversão para PDF (opcional)
- **Werkzeug 2.3.7** - Utilitários web
- **Jinja2 3.1.2** - Template engine
- **pandas 2.0.3** - Manipulação de dados (opcional)

## 🎨 Interface

- **Bootstrap 5** - Framework CSS responsivo
- **Font Awesome 6** - Ícones
- **SweetAlert2** - Alertas elegantes
- **Chart.js** - Gráficos nos relatórios

## 🐛 Solução de Problemas

### Erro: "Modelo não encontrado"
- Verifique se o arquivo `.pptx` está na pasta `modelos_nr/`
- Certifique-se que o nome segue o padrão: `NRxx_modelo.pptx`

### Erro: "CPF inválido"
- Use apenas números ou formato xxx.xxx.xxx-xx
- O sistema valida automaticamente

### Certificado não gerado
- Verifique se todas as variáveis estão corretas no modelo
- Confirme que o funcionário está cadastrado
- Veja o log de erros no terminal

### Problemas de Performance
- Para muitos funcionários, use geração em lote
- Considere usar um servidor mais robusto para produção

## 🔒 Segurança

- Sistema projetado para uso local/rede interna
- Para uso em produção, configure:
  - HTTPS
  - Autenticação de usuários
  - Firewall
  - Backup automatizado

## 📝 Licença

Este projeto foi desenvolvido para automatizar a geração de certificados de treinamento. 

## 🤝 Suporte

Para dúvidas ou problemas:

1. Verifique a seção de **Solução de Problemas**
2. Consulte os logs no terminal
3. Verifique a estrutura de arquivos
4. Teste com poucos funcionários primeiro

## 🚀 Melhorias Futuras

- [ ] Geração de PDF automatizada
- [ ] Envio por email
- [ ] QR Code de validação
- [ ] API REST
- [ ] Múltiplos usuários
- [ ] Integração com Active Directory
- [ ] Relatórios em Excel
- [ ] Notificações automáticas

---

**Desenvolvido para facilitar a gestão de certificados de treinamento em NRs**
