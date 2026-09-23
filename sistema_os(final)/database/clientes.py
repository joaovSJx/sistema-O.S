from database.connection import conectar
from database.usuarios import usuario_legado_id


def cadastrar_cliente(nome, cpf, telefone, email, endereco, usuario_id=None):
    """Cadastra um cliente. Se já existir um cliente com o mesmo CPF,
    reaproveita o cadastro existente em vez de duplicar.
    Retorna o id do cliente."""
    if not nome or not nome.strip():
        raise ValueError("Informe o nome do cliente.")
    if not cpf or not cpf.strip():
        raise ValueError("Informe o CPF do cliente.")
    if not telefone or not telefone.strip():
        raise ValueError("Informe o telefone do cliente.")
    if not email or not email.strip():
        raise ValueError("Informe o e-mail do cliente.")
    if not endereco or not endereco.strip():
        raise ValueError("Informe o endereço do cliente.")

    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM clientes WHERE cpf = ? AND usuario_id = ?", (cpf, usuario_id))
    existente = cursor.fetchone()
    if existente:
        conexao.close()
        return existente[0]

    cursor.execute('''
        insert into clientes (usuario_id, nome, cpf, telefone, email, endereco)
        values (?, ?, ?, ?, ?, ?)
    ''', (usuario_id, nome, cpf, telefone, email, endereco))
    id_cliente = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return id_cliente


def buscar_cliente_por_cpf(cpf, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, cpf, telefone, email, endereco FROM clientes WHERE cpf = ? AND usuario_id = ?", (cpf, usuario_id))
    cliente = cursor.fetchone()
    conexao.close()
    return cliente


def buscar_cliente_por_id(cliente_id, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, cpf, telefone, email, endereco FROM clientes WHERE id = ? AND usuario_id = ?", (cliente_id, usuario_id))
    cliente = cursor.fetchone()
    conexao.close()
    return cliente


def listar_clientes(usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, cpf, telefone, email, endereco FROM clientes WHERE usuario_id = ? ORDER BY nome", (usuario_id,))
    clientes = cursor.fetchall()
    conexao.close()
    return clientes


def atualizar_cliente(cliente_id, nome, cpf, telefone, email, endereco, usuario_id=None):
    dados = (nome, cpf, telefone, email, endereco)
    if any(not valor or not valor.strip() for valor in dados):
        raise ValueError("Preencha todos os dados do cliente.")
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE clientes SET nome = ?, cpf = ?, telefone = ?, email = ?, endereco = ? WHERE id = ? AND usuario_id = ?",
        (*dados, cliente_id, usuario_id),
    )
    conexao.commit()
    conexao.close()


def excluir_cliente(cliente_id, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM ordens_servico WHERE cliente_id = ? AND usuario_id = ?", (cliente_id, usuario_id))
    if cursor.fetchone():
        conexao.close()
        raise ValueError("Não é possível excluir um cliente que possui ordens de serviço.")
    cursor.execute("DELETE FROM equipamentos WHERE cliente_id = ? AND usuario_id = ?", (cliente_id, usuario_id))
    cursor.execute("DELETE FROM clientes WHERE id = ? AND usuario_id = ?", (cliente_id, usuario_id))
    conexao.commit()
    conexao.close()
