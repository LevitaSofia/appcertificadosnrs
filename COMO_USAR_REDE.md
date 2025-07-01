# 🌐 SISTEMA DE TREINAMENTOS NR - PRONTO PARA REDE!

## ✅ Status: CONFIGURADO E PRONTO PARA USO

### 📍 Endereços de Acesso
- **Local (servidor)**: http://127.0.0.1:5000
- **Rede (outros dispositivos)**: http://192.168.18.22:5000

### 🚀 Como Iniciar o Servidor

#### Opção 1: Execução Direta
```bash
python app.py
```

#### Opção 2: Script de Rede (Recomendado)
```bash
python iniciar_rede.py
```

#### Opção 3: Arquivo Batch (Windows)
```bash
iniciar_servidor.bat
```

### 📱 Instruções para Usuários

1. **Conecte-se à mesma rede WiFi** que o servidor
2. **Abra o navegador** no seu dispositivo (celular, tablet, computador)
3. **Digite o endereço**: `http://192.168.18.22:5000`
4. **Faça login** com seu CPF e senha

### 👥 Credenciais de Teste

Os funcionários já estão cadastrados no sistema. Use:
- **CPF**: Números do CPF (ex: 31367350808)
- **Senha**: Alta972600$ (ou variação conforme cadastro)

### 🔧 Funcionalidades Disponíveis

✅ **Multi-usuário simultâneo**
✅ **Interface responsiva (mobile-friendly)**
✅ **Sistema completo de treinamentos**
✅ **Geração de certificados**
✅ **Dashboard em tempo real**
✅ **Controle de acesso por perfil**

### 🛡️ Segurança Implementada

- Autenticação obrigatória
- Controle de sessões
- Validação de dados
- Proteção contra acesso não autorizado

### 🔥 Configuração do Firewall

Se outros dispositivos não conseguirem acessar, configure o firewall:

**Windows (como administrador):**
```cmd
netsh advfirewall firewall add rule name="Sistema NR" dir=in action=allow protocol=TCP localport=5000
```

### 📊 Monitoramento

Para ver quem está acessando o sistema, observe os logs no terminal onde o servidor está rodando.

### 🆘 Suporte

- **Teste de rede**: `python teste_rede.py`
- **Verificar dependências**: `python iniciar_rede.py`
- **Reinstalar dependências**: `pip install -r requirements.txt`

---

**🎉 O sistema está pronto para uso em rede local!**

Para dúvidas, verifique os logs do servidor ou execute os scripts de teste.
