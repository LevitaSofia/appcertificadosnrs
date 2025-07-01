# 🌐 Sistema de Treinamentos NR - Configuração de Rede

Este sistema permite acesso multi-usuário através da rede local, possibilitando que funcionários acessem de seus celulares, tablets ou computadores.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Todos os dispositivos na mesma rede WiFi
- Firewall configurado para permitir conexões na porta 5000

## 🚀 Iniciando o Servidor

### Método 1: Automático (Windows)
```bash
# Execute o arquivo batch
iniciar_servidor.bat
```

### Método 2: Script Python
```bash
# Execute o script de rede
python iniciar_rede.py
```

### Método 3: Direto
```bash
# Execute o app principal
python app.py
```

## 📱 Acessando de Outros Dispositivos

1. **Descubra o IP do servidor** (será exibido ao iniciar)
2. **No dispositivo cliente**, abra o navegador
3. **Digite**: `http://IP_DO_SERVIDOR:5000`
   - Exemplo: `http://192.168.1.100:5000`

## 🔥 Configuração do Firewall

### Windows
```cmd
# Como administrador
netsh advfirewall firewall add rule name="Python Flask" dir=in action=allow protocol=TCP localport=5000
```

Ou manualmente:
1. Abra "Windows Defender Firewall"
2. Clique em "Permitir um aplicativo através do firewall"
3. Adicione Python.exe à lista

### Linux/Ubuntu
```bash
sudo ufw allow 5000
sudo ufw reload
```

### macOS
Geralmente permite por padrão. Verifique "Preferências do Sistema > Segurança" se houver problemas.

## 📊 Funcionalidades Disponíveis em Rede

- ✅ **Login multi-usuário simultâneo**
- ✅ **Dashboard responsivo (mobile-friendly)**
- ✅ **Cadastro e gestão de funcionários**
- ✅ **Sistema completo de treinamentos**
- ✅ **Geração de certificados**
- ✅ **Avaliações online**
- ✅ **Relatórios em tempo real**

## 🛡️ Segurança

- **Autenticação**: Login obrigatório com CPF e senha
- **Autorização**: Diferentes níveis de acesso (admin/usuário)
- **Sessões**: Controle de sessão com timeout automático
- **Validação**: Validação de dados em frontend e backend

## 📱 Acesso Mobile

O sistema é totalmente responsivo e funciona perfeitamente em:
- 📱 Smartphones (Android/iOS)
- 📱 Tablets
- 💻 Computadores/Notebooks
- 🖥️ Desktops

## 🔧 Configurações Avançadas

### Alterar Porta
Edite `config.py`:
```python
PORT = 8080  # Nova porta
```

### Configurar HTTPS (Produção)
Para ambiente de produção, configure SSL:
```python
app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
```

### Banco de Dados Externo
Para múltiplos servidores, configure um banco central no `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@server:5432/dbname'
```

## 🐛 Solução de Problemas

### Não consegue acessar de outros dispositivos
1. ✅ Verifique se estão na mesma rede WiFi
2. ✅ Confirme o IP do servidor
3. ✅ Configure o firewall
4. ✅ Teste com `telnet IP_SERVIDOR 5000`

### Lentidão no acesso
1. ✅ Verifique a velocidade da rede WiFi
2. ✅ Reduza o número de conexões simultâneas
3. ✅ Configure cache no navegador

### Problemas de login
1. ✅ Confirme que o banco de dados está acessível
2. ✅ Verifique se os funcionários estão cadastrados
3. ✅ Teste localmente primeiro

## 📞 Suporte

Para suporte técnico, verifique:
- Logs do servidor no terminal
- Console do navegador (F12)
- Arquivo de configuração `config.py`

## 🔄 Atualizações

Para atualizar o sistema:
1. Pare o servidor (Ctrl+C)
2. Execute `git pull origin main`
3. Reinstale dependências: `pip install -r requirements.txt`
4. Reinicie o servidor

---

💡 **Dica**: Para melhor performance em rede, use conexão cabeada no servidor principal e WiFi 5GHz para os clientes.
