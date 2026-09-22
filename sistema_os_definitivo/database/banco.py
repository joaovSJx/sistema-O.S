from database.connection import conectar
from database.usuarios import criar_tabela_usuarios, garantir_usuario_legado


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
        id integer primary key autoincrement,
        usuario_id integer,
        nome text not null,
        cpf text not null,
        telefone text not null,
        email text not null,
        endereco text not null 
        )
        ''')
    conexao.commit()
    conexao.close()

def criar_tabela_equipamentos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        create table if not exists equipamentos (
        id integer primary key autoincrement,
        cliente_id integer not null,
        usuario_id integer,
        tipo text not null,
        marca text not null,
        modelo text not null,
        numero_serie text not null,
        descricao text not null,
        foreign key (cliente_id) references clientes(id)
        )
        ''')
    conexao.commit()
    conexao.close()


def criar_tabela_os():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        create table if not exists ordens_servico(
        id integer primary key autoincrement,
        cliente_id integer not null,
        equipamento_id integer not null,
        usuario_id integer,
        problema text not null,
        diagnostico text,
        servico_realizado text,
        status text not null default 'Aberta',
        valor real,
        data_entrada text not null,
        data_conclusao text,
        observacoes text,
        foreign key (cliente_id) references clientes(id),
        foreign key (equipamento_id) references equipamentos(id) 
        )''')

    conexao.commit()
    conexao.close()


def preparar_banco():
    criar_tabela_usuarios()
    garantir_usuario_legado()
    criar_tabela()
    criar_tabela_equipamentos()
    criar_tabela_os()
    migrar_donos_dos_registros()


def migrar_donos_dos_registros():
    """Adiciona o dono às tabelas antigas e atribui seus dados a trab."""
    from database.usuarios import usuario_legado_id

    usuario_id = usuario_legado_id()
    conexao = conectar()
    cursor = conexao.cursor()
    for tabela in ("clientes", "equipamentos", "ordens_servico"):
        colunas = {linha[1] for linha in cursor.execute(f"PRAGMA table_info({tabela})")}
        if "usuario_id" not in colunas:
            cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN usuario_id INTEGER")
        cursor.execute(
            f"UPDATE {tabela} SET usuario_id = ? WHERE usuario_id IS NULL",
            (usuario_id,),
        )
    conexao.commit()
    conexao.close()