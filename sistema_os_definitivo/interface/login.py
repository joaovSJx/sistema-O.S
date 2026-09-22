from pathlib import Path

from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import X, W, SUCCESS, SECONDARY
from tkinter import messagebox

from database.usuarios import autenticar_usuario


class LoginFrame(ttk.Frame):
    """Tela de login com contas persistidas no banco de dados."""

    def __init__(self, parent, app):
        super().__init__(parent, padding=28)
        self.app = app
        self._montar_layout()

    def _montar_layout(self):
        caminho_logo = Path(__file__).resolve().parents[1] / "imagens" / "logo.png"
        imagem_logo = Image.open(caminho_logo)
        imagem_logo.thumbnail((150, 84), Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(imagem_logo)
        ttk.Label(self, image=self.logo_image).pack(pady=(0, 8))

        ttk.Label(
            self, text="Assistência Técnica",
            font=("Helvetica", 18, "bold")
        ).pack(pady=(0, 2))
        ttk.Label(
            self, text="Acesso ao sistema", bootstyle=SECONDARY
        ).pack(pady=(0, 18))

        ttk.Label(self, text="Usuário").pack(anchor=W)
        self.usuario_var = ttk.StringVar()
        entrada_usuario = ttk.Entry(self, textvariable=self.usuario_var)
        entrada_usuario.pack(fill=X, pady=(0, 10))
        entrada_usuario.focus_set()

        ttk.Label(self, text="Senha").pack(anchor=W)
        self.senha_var = ttk.StringVar()
        entrada_senha = ttk.Entry(self, textvariable=self.senha_var, show="*")
        entrada_senha.pack(fill=X, pady=(0, 18))

        ttk.Button(
            self, text="Entrar", bootstyle=SUCCESS, command=self._entrar
        ).pack(fill=X)
        ttk.Button(
            self, text="Criar uma conta", bootstyle=SECONDARY,
            command=self.app.mostrar_cadastro,
        ).pack(fill=X, pady=(8, 0))

        entrada_usuario.bind("<Return>", lambda _evento: self._entrar())
        entrada_senha.bind("<Return>", lambda _evento: self._entrar())

    def _entrar(self):
        usuario = self.usuario_var.get().strip()
        senha = self.senha_var.get().strip()

        registro = autenticar_usuario(usuario, senha)
        if registro:
            self.app.usuario_atual = registro
            self.app.mostrar_dashboard()
        else:
            messagebox.showerror("Acesso negado", "Usuário ou senha inválidos.")
            self.senha_var.set("")
