# Sistema de Templates NR01 por Cargo

## Visão Geral
O sistema agora possui templates específicos de NR01 para diferentes cargos, mantendo o template original para "Ajudantes de Instalação" e criando versões especializadas para outros cargos.

## Templates Criados

### 1. **Técnico de Segurança do Trabalho**
- **Template Visualização:** `nr01_tecnico_seguranca.html`
- **Template Impressão:** `nr01_tecnico_seguranca_impressao.html`
- **Conteúdo Específico:**
  - Responsabilidades de supervisão e orientação
  - Procedimentos para investigação de acidentes
  - Orientações para supervisão de equipes
  - Responsabilidades técnicas e éticas

### 2. **Supervisor de Instalação**
- **Template Visualização:** `nr01_supervisor_instalacao.html`
- **Template Impressão:** `nr01_supervisor_instalacao_impressao.html`
- **Conteúdo Específico:**
  - Coordenação de equipes de instalação
  - Controle de qualidade dos serviços
  - Procedimentos de segurança para supervisão
  - Responsabilidades de liderança

### 3. **Instalador de Telas**
- **Template Visualização:** `nr01_instalador_telas.html`
- **Template Impressão:** `nr01_instalador_telas_impressao.html`
- **Conteúdo Específico:**
  - Técnicas de instalação de redes
  - EPIs obrigatórios detalhados
  - Procedimentos de segurança específicos
  - Responsabilidades operacionais

### 4. **Ajudante/Auxiliar de Instalação** (Original)
- **Template Visualização:** `nr01.html`
- **Template Impressão:** `nr01_impressao.html`
- **Conteúdo:** Mantido como estava originalmente

## Como Funciona o Sistema

### Seleção Automática de Templates
O sistema utiliza duas funções no `app.py` para determinar qual template usar:

```python
def get_nr01_template_by_cargo(cargo):
    """Determina qual template NR01 usar baseado no cargo do funcionário"""
    
def get_nr01_template_impressao_by_cargo(cargo):
    """Determina qual template de impressão NR01 usar baseado no cargo do funcionário"""
```

### Lógica de Mapeamento
A seleção de template é baseada em palavras-chave no cargo do funcionário:

- **Técnico de Segurança:** Se o cargo contém "técnico de segurança" ou "tecnico de seguranca"
- **Supervisor de Instalação:** Se o cargo contém "supervisor" e "instalação"
- **Instalador de Telas:** Se o cargo contém "instalador" e "tela"
- **Ajudante/Auxiliar:** Se o cargo contém "ajudante" ou "auxiliar" e ("instalação" ou "tela")
- **Outros Cargos:** Usa o template genérico (original)

### Fluxo de Funcionamento

1. **Usuário acessa NR01:** Sistema identifica o cargo do funcionário
2. **Seleção de Template:** Algoritmo determina o template apropriado
3. **Renderização:** Template específico é carregado com dados do funcionário
4. **Impressão:** Template de impressão correspondente é usado para gerar PDF

## Vantagens do Sistema

### ✅ **Flexibilidade**
- Cada cargo tem conteúdo específico para suas responsabilidades
- Fácil adição de novos cargos e templates

### ✅ **Compatibilidade**
- Sistema mantém funcionamento com cargos existentes
- Templates originais preservados para ajudantes

### ✅ **Manutenibilidade**
- Código organizado com funções específicas
- Fácil modificação de mapeamentos

### ✅ **Escalabilidade**
- Simples adicionar novos templates
- Sistema preparado para crescimento

## Adicionando Novos Cargos

Para adicionar um novo cargo:

1. **Criar Templates:**
   - `nr01_[nome_cargo].html` (visualização)
   - `nr01_[nome_cargo]_impressao.html` (impressão)

2. **Atualizar Funções de Mapeamento:**
   ```python
   # Em get_nr01_template_by_cargo()
   elif 'palavra_chave' in cargo_lower:
       return 'nr01_novo_cargo.html'
   
   # Em get_nr01_template_impressao_by_cargo()
   elif 'palavra_chave' in cargo_lower:
       return 'nr01_novo_cargo_impressao.html'
   ```

3. **Testar:**
   - Criar funcionário com novo cargo
   - Verificar se template correto é carregado

## Status Atual

✅ **Templates Criados:** 4 cargos (8 arquivos total)
✅ **Sistema Funcionando:** Seleção automática implementada
✅ **Compatibilidade:** Templates originais mantidos
✅ **Testado:** Sistema rodando sem erros

## Próximos Passos Sugeridos

1. **Testar todos os templates** com funcionários reais
2. **Revisar conteúdo** específico de cada cargo
3. **Adicionar mais cargos** conforme necessário
4. **Otimizar design** se necessário
5. **Criar documentação** para usuários finais

---
**Data de Implementação:** $(date)
**Status:** ✅ Implementado e Funcionando
