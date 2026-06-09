from app import app
from app.models import Cliente

with app.app_context():
    clientes = Cliente.query.all()
    print(f"Total de clientes no banco: {len(clientes)}")
    for cliente in clientes:
        print(f"- ID: {cliente.id}, Nome: {cliente.nome}, Telefone: {cliente.telefone}")