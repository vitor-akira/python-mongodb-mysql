# 📦 Pipeline, MongoDB e MySQL

Este projeto tem como objetivo construir um pipeline de dados utilizando Python, integrando-o com o MongoDB e o MySQL
## 📂 Estrutura do Projeto

```
📦 pipeline-python-mongo-mysql
├── 📁 data              # Dados 
├── 📁 notebooks         # Notebooks Jupyter 
├── 📁 scripts           # Scripts Python 
└── 📄 requirements.txt  # Bibliotecas necessárias
```

## 🛠️ Configuração do Ambiente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2️⃣ Criar um ambiente virtual (WSL/Linux)
```bash
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar as variáveis de ambiente
Crie um arquivo .env na raiz do projeto e adicione suas credenciais do MySQL:
```bash
MONGO_URI=sua_uri
MYSQL_HOST=seu_host
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
```
## 📝 Notas
1. O script apaga e recria o banco de dados e a tabela a cada execução.
2. O arquivo CSV deve estar no diretório data/.
3. A estrutura da tabela deve corresponder às colunas do CSV.
