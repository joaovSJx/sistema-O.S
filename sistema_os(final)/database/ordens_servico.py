from database.connection import conectar
from database.usuarios import usuario_legado_id
from datetime import datetime

def cadastrar_os(cliente_id, equipamento_id, problema, valor, data_entrada, usuario_id=None):
    if not problema or not problema.strip():
        raise ValueError("Informe o problema.")

    if not data_entrada or not data_entrada.strip():
        raise ValueError("Informe a data de entrada")

    try:
        datetime.strptime(data_entrada, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data de entrada inválida. Use o formato YYYY-MM-DD.")
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()



    cursor.execute(
        "SELECT 1 FROM equipamentos WHERE id = ? AND cliente_id = ? AND usuario_id = ?",
        (equipamento_id, cliente_id, usuario_id)
    )

    if not cursor.fetchone():
        conexao.close()
        raise ValueError("O equipamento não pertence ao cliente informado.")


    cursor.execute('''
     
    insert into ordens_servico (usuario_id, cliente_id, equipamento_id, problema, valor, data_entrada) values (?,?,?,?,?,?)
    ''', (usuario_id, cliente_id, equipamento_id, problema, valor, data_entrada))
    id_os = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return id_os

def cadastrar_equipamento(cliente_id, tipo, marca, modelo, numero_serie, descricao, usuario_id=None):
    if not cliente_id:
        raise ValueError("Informe o cliente do equipamento.")
    if not tipo or not tipo.strip():
        raise ValueError("Informe o tipo do equipamento.")
    if not marca or not marca.strip():
        raise ValueError("Informe a marca do equipamento.")
    if not modelo or not modelo.strip():
        raise ValueError("Informe o modelo do equipamento.")
    if not numero_serie or not numero_serie.strip():
        raise ValueError("Informe o número de série do equipamento.")
    if not descricao or not descricao.strip():
        raise ValueError("Informe a descrição do equipamento.")

    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT 1 FROM clientes WHERE id = ? AND usuario_id = ?", (cliente_id, usuario_id))
    if not cursor.fetchone():
        conexao.close()
        raise ValueError("Cliente informado não existe.")

    cursor.execute('''
    insert into equipamentos (usuario_id, cliente_id, tipo, marca, modelo, numero_serie, descricao) values (?,?,?,?,?,?,?)
    ''', (usuario_id, cliente_id, tipo, marca, modelo, numero_serie, descricao))
    id_equipamento = cursor.lastrowid
    conexao.commit()
    conexao.close()
    return id_equipamento


def listar_equipamentos(usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    equipamentos = conexao.execute("""
        SELECT e.id, e.cliente_id, c.nome, e.tipo, e.marca, e.modelo,
               e.numero_serie, e.descricao
        FROM equipamentos AS e
        JOIN clientes AS c ON c.id = e.cliente_id
                           AND c.usuario_id = e.usuario_id
        WHERE e.usuario_id = ?
        ORDER BY e.id
    """, (usuario_id,)).fetchall()
    conexao.close()
    return equipamentos


def atualizar_equipamento(equipamento_id, cliente_id, tipo, marca, modelo,
                          numero_serie, descricao, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    dados = (tipo, marca, modelo, numero_serie, descricao)
    if not cliente_id or any(not valor or not valor.strip() for valor in dados):
        raise ValueError("Preencha todos os dados do equipamento.")
    conexao = conectar()
    cursor = conexao.cursor()
    cliente = cursor.execute(
        "SELECT 1 FROM clientes WHERE id = ? AND usuario_id = ?",
        (cliente_id, usuario_id),
    ).fetchone()
    if not cliente:
        conexao.close()
        raise ValueError("Cliente informado não pertence a esta conta.")
    cursor.execute("""
        UPDATE equipamentos
        SET cliente_id = ?, tipo = ?, marca = ?, modelo = ?,
            numero_serie = ?, descricao = ?
        WHERE id = ? AND usuario_id = ?
    """, (cliente_id, tipo, marca, modelo, numero_serie, descricao,
           equipamento_id, usuario_id))
    conexao.commit()
    conexao.close()


def excluir_equipamento(equipamento_id, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    if cursor.execute(
        "SELECT 1 FROM ordens_servico WHERE equipamento_id = ? AND usuario_id = ?",
        (equipamento_id, usuario_id),
    ).fetchone():
        conexao.close()
        raise ValueError("Não é possível excluir um equipamento que possui O.S.")
    cursor.execute(
        "DELETE FROM equipamentos WHERE id = ? AND usuario_id = ?",
        (equipamento_id, usuario_id),
    )
    conexao.commit()
    conexao.close()

def consultar_os(usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(""" 
    SELECT
        os.id,
        c.nome,
        e.tipo,
        e.marca,
        e.modelo,
        os.problema,
        os.status,
        os.valor,
        os.data_entrada

    FROM ordens_servico AS os
    JOIN clientes AS c ON os.cliente_id = c.id AND c.usuario_id = os.usuario_id
    JOIN equipamentos AS e ON os.equipamento_id = e.id AND e.usuario_id = os.usuario_id
    WHERE os.usuario_id = ? """, (usuario_id,))
    ordens = cursor.fetchall()
    conexao.close()
    return ordens

def consultar_os_por_status(status, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT
        os.id,
        c.nome,
        e.tipo,
        e.marca,
        e.modelo,
        os.problema,
        os.status,
        os.valor,
        os.data_entrada

    FROM ordens_servico AS os
    JOIN clientes AS c ON os.cliente_id = c.id AND c.usuario_id = os.usuario_id
    JOIN equipamentos AS e ON os.equipamento_id = e.id AND e.usuario_id = os.usuario_id
    WHERE os.status = ? AND os.usuario_id = ?
    """, (status, usuario_id))
    ordens = cursor.fetchall()
    conexao.close()
    return ordens

def consultar_os_por_id(id_os, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT
        os.id,
        c.nome,
        e.tipo,
        e.marca,
        e.modelo,
        os.problema,
        os.status,
        os.valor,
        os.data_entrada,
        os.diagnostico,
        os.servico_realizado

    FROM ordens_servico AS os
    JOIN clientes AS c ON os.cliente_id = c.id AND c.usuario_id = os.usuario_id
    JOIN equipamentos AS e ON os.equipamento_id = e.id AND e.usuario_id = os.usuario_id
    WHERE os.id = ? AND os.usuario_id = ?
    """, (id_os, usuario_id))
    ordens = cursor.fetchall()
    conexao.close()
    return ordens

def consultar_os_por_cliente(nome_cliente, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT
        os.id,
        c.nome,
        e.tipo,
        e.marca,
        e.modelo,
        os.problema,
        os.status,
        os.valor,
        os.data_entrada

    FROM ordens_servico AS os
    JOIN clientes AS c ON os.cliente_id = c.id AND c.usuario_id = os.usuario_id
    JOIN equipamentos AS e ON os.equipamento_id = e.id AND e.usuario_id = os.usuario_id
    WHERE c.nome LIKE ? AND os.usuario_id = ?
    """, (f"%{nome_cliente}%", usuario_id))
    ordens = cursor.fetchall()
    conexao.close()
    return ordens

def consultar_os_por_periodo(data_inicio, data_fim, usuario_id=None):
    usuario_id = usuario_id or usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT
        os.id,
        c.nome,
        e.tipo,
        e.marca,
        e.modelo,
        os.problema,
        os.status,
        os.valor,
        os.data_entrada

    FROM ordens_servico AS os
    JOIN clientes AS c ON os.cliente_id = c.id AND c.usuario_id = os.usuario_id
    JOIN equipamentos AS e ON os.equipamento_id = e.id AND e.usuario_id = os.usuario_id
    WHERE os.data_entrada BETWEEN ? AND ? AND os.usuario_id = ?
    """, (data_inicio, data_fim, usuario_id))
    ordens = cursor.fetchall()
    conexao.close()
    return ordens