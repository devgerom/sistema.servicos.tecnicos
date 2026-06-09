// app/static/js/main.js

// Função para deletar cliente
function deletarCliente(id, nome) {
    if (confirm(`⚠️ Tem certeza que deseja excluir o cliente "${nome}"?\n\nEsta ação não poderá ser desfeita!`)) {
        fetch(`/deletar_cliente/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
                location.reload();
            } else {
                alert('❌ ' + data.message);
            }
        })
        .catch(error => {
            alert('❌ Erro ao deletar cliente: ' + error);
        });
    }
}

// Função para deletar serviço
function deletarServico(id) {
    if (confirm('⚠️ Tem certeza que deseja excluir este serviço?\n\nEsta ação não poderá ser desfeita!')) {
        fetch(`/deletar_servico/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
                location.reload();
            } else {
                alert('❌ ' + data.message);
            }
        })
        .catch(error => {
            alert('❌ Erro ao deletar serviço: ' + error);
        });
    }
}

// Função para atualizar status (opcional - via AJAX sem recarregar)
function atualizarStatus(servicoId, novoServico) {
    fetch(`/atualizar_status/${servicoId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `status=${novoServico}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('❌ ' + data.message);
        }
    })
    .catch(error => {
        alert('❌ Erro ao atualizar status: ' + error);
    });
}

// Máscara para telefone (opcional)
function mascaraTelefone(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length <= 10) {
        value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    } else {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    }
    input.value = value;
}

// Aplicar máscara de telefone nos campos
document.addEventListener('DOMContentLoaded', function() {
    const telefoneInputs = document.querySelectorAll('input[type="tel"]');
    telefoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            mascaraTelefone(this);
        });
    });
});