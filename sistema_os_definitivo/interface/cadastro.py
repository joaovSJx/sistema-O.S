import ttkbootstrap as ttk
from ttkbootstrap.constants import LEFT, W, X, YES, SUCCESS, SECONDARY
from tkinter import messagebox

from database.usuarios import cadastrar_usuario


class CadastroFrame(ttk.Frame):
    """Tela de criação de uma conta individual para acesso ao sistema."""

    def __init__(self, parent, app):
        super().__init__(parent, padding=24)
        self.app = app
        self._montar_layout()

    def _campo(self, rotulo, ocultar=False):
        ttk.Label(self, text=rotulo).pack(anchor=W)
        variavel = ttk.StringVar()
        ttk.Entry(self, textvariable=variavel, show="*" if ocultar else "").pack(fill=X, pady=(0, 12))
        return variavel

    def _montar_layout(self):
        cabecalho = ttk.Frame(self)
        cabecalho.pack(fill=X)
        ttk.Label(
            cabecalho, text="Criar conta", font=("Helvetica", 18, "bold")
        ).pack(side=LEFT, anchor=W)
        ttk.Button(
            cabecalho, text="Sair", bootstyle=SECONDARY, command=self._sair
        ).pack(side="right")

        ttk.Label(
            self,
            text="Crie uma conta individual para acessar o sistema.",
            bootstyle=SECONDARY,
        ).pack(anchor=W, pady=(4, 24))

        self.nome = self._campo("Nome completo")
        self.usuario = self._campo("Usuário")
        self.email = self._campo("E-mail")
        self.senha = self._campo("Senha", ocultar=True)
        self.confirmacao = self._campo("Confirmar senha", ocultar=True)

        botoes = ttk.Frame(self)
        botoes.pack(fill=X, pady=(12, 0))
        ttk.Button(
            botoes,
            text="Criar conta",
            bootstyle=SUCCESS,
            command=self._cadastrar,
        ).pack(side=LEFT, expand=YES, fill=X, padx=(0, 6))
        ttk.Button(
            botoes,
            text="Limpar",
            bootstyle=SECONDARY,
            command=self._limpar,
        ).pack(side=LEFT, expand=YES, fill=X, padx=(6, 0))

    def _cadastrar(self):
        try:
            senha = self.senha.get()
            if senha != self.confirmacao.get():
                raise ValueError("As senhas não coincidem.")
            cadastrar_usuario(
                nome=self.nome.get(), usuario=self.usuario.get(),
                email=self.email.get(), senha=senha,
            )
            messagebox.showinfo(
                "Sucesso", "Conta criada com sucesso. Agora faça login."
            )
            self.app.mostrar_login()
        except ValueError as erro:
            messagebox.showerror("Dados inválidos", str(erro))
        except Exception as erro:
            messagebox.showerror("Erro inesperado", str(erro))

    def _sair(self):
        self.app.mostrar_login()

    def _limpar(self):
        for campo in (self.nome, self.usuario, self.email, self.senha, self.confirmacao):
            campo.set("")
