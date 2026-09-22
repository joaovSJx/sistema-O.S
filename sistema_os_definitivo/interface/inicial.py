import ttkbootstrap as ttk
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk 




class InicialFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._montar_fundo()

    def _montar_fundo(self):
        caminho_fundo = (
        Path(__file__).resolve().parents[1] / "imagens"/ "fundo_inicial.jpeg"
    )

        imagem_fundo = Image.open(caminho_fundo).resize((1200, 720))
        self.imagem_fundo = ImageTk.PhotoImage(imagem_fundo)

        canvas = tk.Canvas(self, width=1200, height=720, highlightthickness=0)
        canvas.place(x=0, y=0)

        canvas.create_image(0, 0, image=self.imagem_fundo, anchor="nw")

        canvas.create_text(
            155, 235,
            text="BEM-VINDO AO TRINYTI TECH", 
            fill="white",
            font=("Helvetica", 11, "bold"),
            anchor="w",
    )

        canvas.create_text(
            155, 275,
            text="Gerencie suas Ordens\nde Serviço de forma\nrápida e eficiente.",
            fill="white",
            font=("Helvetica", 28, "bold"),
            anchor="nw",
            justify="left",
    )

        canvas.create_text(
            155, 420,
            text="Acesse sua conta  ou  Cadastre-se",
            fill="white",
            font=("Helvetica", 12),
            anchor="w",
    )

        botao_entrar = ttk.Button(
            canvas,
            text="ENTRAR NA CONTA",
            bootstyle="info",
            width=20,
            command=self.app.mostrar_login,
    )
        canvas.create_window(255, 480, window=botao_entrar)

        canvas.create_rectangle(
            370, 463, 555, 497,
            outline="#DCE6F0",
            width=1,
            tags="cadastro",
)

        canvas.create_text(
            462, 480,
            text="CADASTRAR-SE",
            fill="white",
            font=("Helvetica", 10),
            tags="cadastro",
)
        canvas.tag_bind("cadastro", "<Button-1>", lambda _event: self.app.mostrar_cadastro())
        canvas.tag_bind("cadastro", "<Enter>", lambda _event: canvas.config(cursor="hand2"))
        canvas.tag_bind("cadastro", "<Leave>", lambda _event: canvas.config(cursor=""))

        canvas.create_text(
            355, 530,
            text="Crie sua conta grátis agora!",
            fill="white",
            font=("Helvetica", 10),
    )

        caminho_ilustracao = (
            Path(__file__).resolve().parents[1] / "imagens" / "imagem_deshboard.jpeg"
    )

        imagem_ilustracao = Image.open(caminho_ilustracao).resize((460, 460))
        self.imagem_ilustracao = ImageTk.PhotoImage(imagem_ilustracao)

        canvas.create_image(
            910, 365,
            image=self.imagem_ilustracao,
    )