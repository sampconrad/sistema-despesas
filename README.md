# 💰 Sistema de Despesas

Sistema de gestão financeira pessoal, com interface web e API REST servidos à partir de um único arquivo executável.

Desenvolvido com o objetivo de facilitar o controle financeiro pessoal, ele permite cadastrar, editar e excluir despesas, além de exibir uma lista detalhada das informações cadastradas, incluindo aviso de vencimento e detalhes de parcelamento.

- Possui build automatizado - **passos descritos abaixo na seção 🚀 Build Automatizado** - que compilará a aplicação em um único arquivo .exe acessível em  `/dist/SistemaDespesas.exe` para facilitar a utilização do sistema.

## 🎨 Frontend

**📁 [sistema-despesas-client/README.md](sistema-despesas-client/README.md)** - Instruções para executar o frontend em modo desenvolvimento

![image](https://github.com/user-attachments/assets/ed9d9d20-ef52-40a4-a35a-450c099c0170)

### Funcionalidades

- **Operações CRUD completas**: Create, Read, Update, Delete
- **Tipos de despesa**: Selecione entre CRÉDITO FIXO, CRÉDITO PARCELADO, PIX, BOLETO
- **Controle de parcelas**: Acompanhe a condição do parcelamento da Despesa
- **Status de pagamento**: Sinalação de despesas pagas/pendentes
- **Dia de vencimento**: Indique apenas o dia do mês (1-31) no qual a despesa vence
- **Validação em tempo real**: Feedback visual para campos obrigatórios e inválidos
- **Interface responsiva**: Funciona perfeitamente em desktop, tablet e mobile
- **Feedback instantâneo**: Sistema de feedback ao usuário através de toasts e modais
- **Design moderno**: Interface limpa e profissional com Bootstrap 5

### Tecnologias Utilizadas

- **HTML5**
- **CSS3**
- **JavaScript (ES6+)**
- **Bootstrap 5**

## 🐍 Backend API

**📁 [sistema-despesas-api/README.md](sistema-despesas-api/README.md)** - Instruções para executar a API em modo desenvolvimento

![image](https://github.com/user-attachments/assets/e5d8cf35-bce5-4dd3-ab8f-b0baf7a44959)

### Funcionalidades

- **Operações CRUD completas**: Create, Read, Update, Delete
- **Documentação robusta**: Swagger/OpenAPI com exemplos e códigos de status
- **Validações**: Regras de negócio e validação de dados
- **CORS configurado**: Suporte completo para frontend
- **Logs detalhados**: Sistema de logging para monitoramento

### Tecnologias Utilizadas

- **Python 3.8+**
- **Flask**
- **Flask-OpenAPI3**
- **SQLAlchemy**
- **SQLite**
- **Flask-CORS**
- **Pydantic**

## 👨‍💻 Desenvolvimento
Para desenvolvimento e modificações do código, consulte os READMEs específicos:

- **📁 [sistema-despesas-api/README.md](sistema-despesas-api/README.md)** - Instruções para executar a API em modo desenvolvimento
- **📁 [sistema-despesas-client/README.md](sistema-despesas-client/README.md)** - Instruções para executar o frontend em modo desenvolvimento

# 🚀 Build Automatizado

Este guia explica como compilar o Sistema de Despesas em um executável standalone usando o sistema de build automatizado.

### Tecnologias Utilizadas

- **PyInstaller** - Criação do executável
- **Python** - Linguagem principal

## 🗂️ Estrutura do Projeto

```
sistema-despesas/
├── 📁 sistema-despesas-api/     # Backend Flask + API REST
│   ├── app.py                   # Aplicação principal da API
│   ├── model/                   # Modelos de dados (SQLAlchemy)
│   ├── schemas/                 # Schemas Pydantic
│   ├── database/                # Banco SQLite
│   ├── requirements.txt         # Dependências da API
│   └── README.md                # Documentação da API
│
├── 📁 sistema-despesas-client/  # Frontend HTML/CSS/JS
│   ├── index.html               # Interface principal
│   ├── styles.css               # Estilos CSS
│   ├── scripts.js               # JavaScript
│   ├── img/                     # Imagens
│   └── README.md                # Documentação do frontend
│
├── 🚀 Sistema de Build          # Arquivos para criar executável
│   ├── main.py                  # Ponto de entrada do executável
│   ├── build.spec.template      # Template PyInstaller
│   ├── build.bat/ps1            # Scripts de build
│   └── build_requirements.txt   # Dependências do build
│
├── 📋 .gitignore                # Gitignore centralizado
├── 📖 LICENSE                   # Licensa MIT
├── 📖 README.md                 # Este arquivo
└── 📦 dist/                     # Executável gerado
    └──  SistemaDespesas.exe      # Executável standalone
```

## 📋 Pré-requisitos

- **Python 3.8+** instalado no sistema
- **pip** (gerenciador de pacotes Python)
- **Windows 10/11** (para este build específico)

## 🔨 Compilação

1. **Abra o PowerShell ou Prompt de Comando** na pasta raiz `sistema-despesas/`
2. **Execute o script de build:**
   ```bash
   # PowerShell
   .\build.ps1
   
   # ou CMD
   .\build.bat
   ```

## 🎯 Como Usar

### Executável Standalone (Produção)
1. **Navegue até a pasta `dist`**
2. **Dê duplo clique em `SistemaDespesas.exe`**
3. **Aguarde alguns segundos** (inicialização do servidor)
4. **O navegador abrirá automaticamente** em http://localhost:5000

## ⚙️ Processo de Build

O sistema de build automatizado executa as seguintes etapas:

1. **Instala dependências** (`pip install -r build_requirements.txt`)
2. **Copia o template** (`build.spec.template` → `build.spec`)
3. **Cria o executável** (`pyinstaller build.spec --clean`)
5. **Limpa arquivos temporários**

## 📦 Estrutura do Executável

Após o build, você terá:

```
dist/
├── SistemaDespesas.exe    # Executável principal
├── log/                   # Pasta para logs
└── database/              # Pasta para banco SQLite
```

## ⚙️ Configurações

### Alterar Porta
Edite o arquivo `main.py` e modifique a linha:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Desabilitar Abertura Automática do Navegador
Comente ou remova estas linhas em `main.py`:
```python
# threading.Thread(target=open_browser, daemon=True).start()
```

## 📤 Distribuição

O executável é **completamente standalone** e inclui:
- ✅ Python runtime
- ✅ Todas as dependências
- ✅ Frontend integrado
- ✅ Banco SQLite local
- ✅ Servidor web embutido

**Para distribuir:**
1. Execute o build
2. Acessa a pasta `dist/`
3. Envie o arquivo `SistemaDespesas.exe` para qualquer pessoa
4. Ela só precisa executar o `.exe`

## 🔄 Atualizações

Para atualizar o sistema:
1. **Modifique o código** na API ou frontend
2. **Execute o build** novamente: `.\build.ps1`
3. **Substitua o executável** antigo pelo novo

## 🛠️ Solução de Problemas

### Erro: "Porta já em uso"
- Feche outras instâncias do aplicativo
- Ou altere a porta no código

### Executável não abre
- Verifique se o antivírus não está bloqueando
- Execute como administrador se necessário

### Arquivo build.spec não encontrado
- O sistema automaticamente copia `build.spec.template` para `build.spec`
- Se o erro persistir, execute manualmente: `copy build.spec.template build.spec`

## 📚 Documentação

- **[sistema-despesas-api/README.md](sistema-despesas-api/README.md)** - Documentação da API e instruções de desenvolvimento
- **[sistema-despesas-client/README.md](sistema-despesas-client/README.md)** - Documentação do frontend e instruções de desenvolvimento
- **[API Documentation](http://localhost:5000/openapi)** - Documentação da API (quando rodando)

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
