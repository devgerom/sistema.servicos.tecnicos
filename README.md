# 🔧 Dr. Eletron Refrigeração

Sistema para gestão de clientes e serviços técnicos de refrigeração, climatização e elétrica.

## O que o sistema faz?

- Cadastra clientes
- Cadastra serviços para cada cliente
- Busca clientes pelo nome
- Edita dados de clientes e serviços
- Exclui clientes e serviços

## Como instalar?

### 1. Clonar o projeto

```bash
git clone https://github.com/devgerom/sistema.servicos.tecnicos.git
cd sistema.servicos.tecnicos
2. Criar ambiente virtual
bash
python -m venv .venv
.venv\Scripts\activate  # Windows
3. Instalar dependências
bash
pip install -r requirements.txt
4. Criar o banco de dados
bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
5. Executar
bash
python main.py
Abrir no navegador: http://localhost:5000

Tecnologias usadas
Python + Flask

SQLite + SQLAlchemy

HTML, CSS, JavaScript

Estrutura do projeto
text
app/
├── static/          # CSS, JS, imagens
├── templates/       # HTML
├── models.py        # Banco de dados
└── views.py         # Rotas do sistema
Como usar?
Cadastrar cliente - Preencha nome, endereço e telefone

Cadastrar serviço - Selecione o cliente e os dados do serviço

Buscar - Digite o nome do cliente

Editar/Excluir - Use os botões nos resultados da busca

🤝 Contribuir
Fork o projeto

Crie uma branch (git checkout -b minha-feature)

Commit (git commit -m 'minha feature')

Push (git push origin minha-feature)

Abra um Pull Request

📞 Contato
GitHub: @devgerom
Email: dev.gerom@gmail.com