from database.connection import conectar


def criar_tabela_usuarios():
    conexao = conectar()
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
        """
    )
    conexao.commit()
    conexao.close()


def cadastrar_usuario(nome, usuario, email, senha):
    valores = (nome.strip(), usuario.strip().lower(), email.strip().lower(), senha)
    if any(not valor for valor in valores):
        raise ValueError("Preencha todos os campos do cadastro.")
    if len(valores[1]) < 3:
        raise ValueError("O usuário deve ter pelo menos 3 caracteres.")
    if len(senha) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres.")

    conexao = conectar()
    try:
        conexao.execute(
            "INSERT INTO usuarios (nome, usuario, email, senha) VALUES (?, ?, ?, ?)",
            valores,
        )
        conexao.commit()
    except Exception as erro:
        if "UNIQUE" in str(erro).upper():
            raise ValueError("Este usuário ou e-mail já está cadastrado.") from erro
        raise
    finally:
        conexao.close()


def autenticar_usuario(usuario, senha):
    conexao = conectar()
    registro = conexao.execute(
        "SELECT id, nome, usuario, email FROM usuarios WHERE (usuario = ? OR email = ?) AND senha = ?",
        (usuario.strip().lower(), usuario.strip().lower(), senha),
    ).fetchone()
    conexao.close()
    return registro


def garantir_usuario_legado():
    """Mantém o acesso antigo disponível depois da atualização do sistema."""
    conexao = conectar()
    existente = conexao.execute(
        "SELECT id FROM usuarios WHERE usuario = ?", ("trab",)
    ).fetchone()
    if not existente:
        conexao.execute(
            "INSERT INTO usuarios (nome, usuario, email, senha) VALUES (?, ?, ?, ?)",
            ("Administrador", "trab", "admin@trinitytech.local", "123456"),
        )
        conexao.commit()
    conexao.close()


def usuario_legado_id():
    conexao = conectar()
    registro = conexao.execute(
        "SELECT id FROM usuarios WHERE usuario = ?", ("trab",)
    ).fetchone()
    conexao.close()
    return registro[0] if registro else None
