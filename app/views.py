from app import app, db
from app.models import Cliente, Servico
from flask import render_template, url_for, request
from datetime import datetime
from sqlalchemy import func

@app.route('/')
def homepage():
    # Estatísticas gerais
    total_clientes = Cliente.query.count()
    total_servicos = Servico.query.count()
    
    # Serviços por status
    servicos_pendentes = Servico.query.filter_by(status='pendente').count()
    servicos_andamento = Servico.query.filter_by(status='em_andamento').count()
    servicos_concluidos = Servico.query.filter_by(status='concluido').count()
    servicos_cancelados = Servico.query.filter_by(status='cancelado').count()
    
    # Serviços pendentes recentes (últimos 5)
    servicos_recentes_pendentes = Servico.query.filter_by(status='pendente').order_by(Servico.data_servico.desc()).limit(5).all()
    
    # Total em aberto (pendentes + em andamento)
    total_em_aberto = servicos_pendentes + servicos_andamento
    
    # Calcular faturamento total (serviços concluídos)
    faturamento_total = db.session.query(func.sum(Servico.valor)).filter_by(status='concluido').scalar() or 0
    
    context = {
        'total_clientes': total_clientes,
        'total_servicos': total_servicos,
        'servicos_pendentes': servicos_pendentes,
        'servicos_andamento': servicos_andamento,
        'servicos_concluidos': servicos_concluidos,
        'servicos_cancelados': servicos_cancelados,
        'total_em_aberto': total_em_aberto,
        'faturamento_total': faturamento_total,
        'servicos_recentes_pendentes': servicos_recentes_pendentes
    }
    
    return render_template('index.html', context=context)




@app.route('/clientes', methods=['GET','POST'])
def clientes():
    if request.method == 'POST':
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        telefone = request.form.get('telefone')
        observacoes = request.form.get('observacoes')  # observacoes do serviço
        
        print(f"\n=== TENTANDO CADASTRAR CLIENTE ===")
        print(f"Nome: {nome}")
        print(f"Endereço: {endereco}")
        print(f"Telefone: {telefone}")
        
        try:
            # CRIAR o objeto Cliente
            novo_cliente = Cliente(
                nome=nome,
                endereco=endereco,
                telefone=telefone
            )
            
            # ADICIONAR ao banco
            db.session.add(novo_cliente)
            
            # COMMIT (salvar de fato)
            db.session.commit()
            
            print(f"✅ Cliente {nome} salvo com sucesso! ID: {novo_cliente.id}")
            mensagem = f"✅ Cliente {nome} cadastrado com sucesso!"
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao salvar: {e}")
            mensagem = f"❌ Erro ao cadastrar: {str(e)}"
        
        return render_template('cadastro_clientes.html', mensagem=mensagem)
    
    return render_template('cadastro_clientes.html')




@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':        
        pesquisa = request.form.get('pesquisa')
    else: 
        pesquisa = request.args.get('pesquisa')
    
    clientes_encontrados = []
    if pesquisa:
        # Busca por nome que contenha o texto
        clientes_encontrados = Cliente.query.filter(
            Cliente.nome.contains(pesquisa)
        ).all()
    else:
        # Se não tiver pesquisa, mostra todos os clientes
        clientes_encontrados = Cliente.query.all()
    
    # Para cada cliente, buscar seus serviços
    clientes_com_servicos = []
    for cliente in clientes_encontrados:
        servicos_cliente = Servico.query.filter_by(cliente_id=cliente.id).order_by(Servico.data_servico.desc()).all()
        clientes_com_servicos.append({
            'cliente': cliente,
            'servicos': servicos_cliente
        })
    
    context = {
        'pesquisa': pesquisa,
        'clientes_com_servicos': clientes_com_servicos
    }
    
    return render_template('buscar_clientes.html', context=context)

@app.route('/servicos', methods=['GET', 'POST'])
def servicos():
    # Buscar TODOS os clientes do banco de dados
    clientes = Cliente.query.all()
    
    # Buscar serviços recentes (AQUI no Python, não no template!)
    servicos_recentes = Servico.query.order_by(Servico.id.desc()).limit(5).all()
    
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        tipo_servico = request.form.get('tipo_servico')
        descricao = request.form.get('descricao')
        data_servico = request.form.get('data_servico')
        valor = request.form.get('valor')
        status = request.form.get('status')
        observacoes = request.form.get('observacoes')
        
        if not cliente_id:
            mensagem = "⚠️ Por favor, selecione um cliente!"
            return render_template('cadastro_servicos.html', 
                                 mensagem=mensagem, 
                                 clientes=clientes,
                                 servicos_recentes=servicos_recentes)
        
        try:
            data_servico_obj = datetime.strptime(data_servico, '%Y-%m-%d') if data_servico else datetime.now()
            valor_float = float(valor) if valor else None
            
            novo_servico = Servico(
                cliente_id=cliente_id,
                tipo_servico=tipo_servico,
                descricao=descricao,
                data_servico=data_servico_obj,
                valor=valor_float,
                status=status,
                observacoes=observacoes
            )
            
            db.session.add(novo_servico)
            db.session.commit()
            
            # ATUALIZAR a lista de serviços recentes após salvar
            servicos_recentes = Servico.query.order_by(Servico.id.desc()).limit(5).all()
            
            mensagem = f"✅ Serviço de {tipo_servico} cadastrado com sucesso!"
            
        except Exception as e:
            db.session.rollback()
            mensagem = f"❌ Erro ao cadastrar serviço: {str(e)}"
        
        return render_template('cadastro_servicos.html', 
                             mensagem=mensagem, 
                             clientes=clientes,
                             servicos_recentes=servicos_recentes)
    
    # GET - mostrar formulário
    return render_template('cadastro_servicos.html', 
                         clientes=clientes, 
                         servicos_recentes=servicos_recentes)
    
@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        cliente.nome = request.form.get('nome')
        cliente.endereco = request.form.get('endereco')
        cliente.telefone = request.form.get('telefone')
        
        try:
            db.session.commit()
            mensagem = f"✅ Cliente {cliente.nome} atualizado com sucesso!"
            return render_template('editar_cliente.html', cliente=cliente, mensagem=mensagem)
        except Exception as e:
            db.session.rollback()
            mensagem = f"❌ Erro ao atualizar: {str(e)}"
            return render_template('editar_cliente.html', cliente=cliente, mensagem=mensagem)
    
    return render_template('editar_cliente.html', cliente=cliente)


@app.route('/editar_servico/<int:id>', methods=['GET', 'POST'])
def editar_servico(id):
    servico = Servico.query.get_or_404(id)
    clientes = Cliente.query.all()
    
    if request.method == 'POST':
        servico.cliente_id = request.form.get('cliente_id')
        servico.tipo_servico = request.form.get('tipo_servico')
        servico.descricao = request.form.get('descricao')
        servico.data_servico = datetime.strptime(request.form.get('data_servico'), '%Y-%m-%d') if request.form.get('data_servico') else datetime.now()
        servico.valor = float(request.form.get('valor')) if request.form.get('valor') else None
        servico.status = request.form.get('status')
        servico.observacoes = request.form.get('observacoes')
        
        try:
            db.session.commit()
            mensagem = f"✅ Serviço atualizado com sucesso!"
            return render_template('editar_servico.html', servico=servico, clientes=clientes, mensagem=mensagem)
        except Exception as e:
            db.session.rollback()
            mensagem = f"❌ Erro ao atualizar: {str(e)}"
            return render_template('editar_servico.html', servico=servico, clientes=clientes, mensagem=mensagem)
    
    return render_template('editar_servico.html', servico=servico, clientes=clientes)

@app.route('/atualizar_status/<int:id>', methods=['POST'])
def atualizar_status(id):
    servico = Servico.query.get_or_404(id)
    novo_status = request.form.get('status')
    
    if novo_status:
        servico.status = novo_status
        try:
            db.session.commit()
            return {"success": True, "message": "Status atualizado!"}
        except:
            db.session.rollback()
            return {"success": False, "message": "Erro ao atualizar!"}
    
    return {"success": False, "message": "Status não informado!"}



@app.route('/deletar_cliente/<int:id>', methods=['POST'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    # Verificar se o cliente tem serviços
    if cliente.servicos:
        return {"success": False, "message": "Cliente possui serviços. Exclua os serviços primeiro!"}
    
    try:
        db.session.delete(cliente)
        db.session.commit()
        return {"success": True, "message": "Cliente excluído com sucesso!"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Erro: {str(e)}"}
    

@app.route('/deletar_servico/<int:id>', methods=['POST'])
def deletar_servico(id):
    servico = Servico.query.get_or_404(id)
    
    try:
        db.session.delete(servico)
        db.session.commit()
        return {"success": True, "message": "Serviço excluído com sucesso!"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Erro: {str(e)}"}
