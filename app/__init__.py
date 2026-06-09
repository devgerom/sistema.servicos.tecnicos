from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importar models
from app.models import Cliente, Servico

# Criar banco de dados se não existir
with app.app_context():
    db.create_all()
    print("✅ Banco de dados verificado/criado com sucesso!")

# IMPORTAR AS VIEWS (OBRIGATÓRIO!)
from app.views import homepage, clientes, buscar, servicos