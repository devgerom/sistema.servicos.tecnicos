from app import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    data_cadastro = db.Column(db.DateTime, default=datetime.now)
    
    # Relacionamento com serviços
    servicos = db.relationship('Servico', backref='cliente', lazy=True)
    
    def __repr__(self):
        return f'<Cliente {self.nome}>'

class Servico(db.Model):
    __tablename__ = 'servicos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    tipo_servico = db.Column(db.String(50))
    descricao = db.Column(db.Text)
    data_servico = db.Column(db.DateTime, default=datetime.now)
    valor = db.Column(db.Float)
    status = db.Column(db.String(20), default='pendente')
    observacoes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Servico {self.tipo_servico}>'