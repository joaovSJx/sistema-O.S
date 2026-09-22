from pathlib import Path
import tkinter as tk

from PIL import Image, ImageTk
import ttkbootstrap as ttk


class TelaSistema(ttk.Frame):
    LARGURA = 1200
    ALTURA = 720
    AZUL = "#061A34"
    AZUL_CLARO = "#1769AA"

    def __init__(self, parent, app, titulo, pagina):
        super().__init__(parent)
        self.app = app
        self.titulo = titulo
        self.pagina = pagina
        self._imagens = []
        self.canvas = tk.Canvas(self, width=self.LARGURA, height=self.ALTURA,
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._montar_fundo()
        self._montar_menu()
        self._montar_cabecalho()

    def _montar_fundo(self):
        caminho = Path(__file__).resolve().parents[1] / "imagens" / "fundo_dashboard.jpeg"
        imagem = Image.open(caminho).resize((self.LARGURA, self.ALTURA))
        self._imagens.append(ImageTk.PhotoImage(imagem))
        self.canvas.create_image(0, 0, image=self._imagens[-1], anchor="nw")

    def _montar_menu(self):
        self.canvas.create_rectangle(0, 120, 165, self.ALTURA, fill=self.AZUL, outline="")
        self.canvas.create_line(0, 120, 165, 120, fill="#456078")
        self.canvas.create_line(164, 120, 164, 690, fill="#456078")

        logo = Image.open(Path(__file__).resolve().parents[1] / "imagens" / "logo.png")
        logo.thumbnail((55, 55), Image.Resampling.LANCZOS)
        self._imagens.append(ImageTk.PhotoImage(logo))
        self.canvas.create_image(18, 28, image=self._imagens[-1], anchor="nw")
        self.canvas.create_text(82, 53, text="TRINITY TECH", fill="white",
                               font=("Helvetica", 10, "bold"), anchor="w")

        itens = [("▦", "PAINEL", self.app.mostrar_dashboard),
                 ("♟", "CLIENTES", self.app.mostrar_clientes),
                 ("▣", "EQUIPAMENTOS", self.app.mostrar_equipamentos),
                 ("▤", "ORDEM DE SERVIÇO", self.app.mostrar_ordens),
                 ("⚙", "CONFIGURAÇÕES", self.app.mostrar_configuracao)]
        for indice, (icone, texto, comando) in enumerate(itens):
            y = 163 + indice * 55
            tag = f"menu_{indice}"
            self.canvas.create_text(27, y, text=icone, fill=self.AZUL_CLARO,
                                    font=("Segoe UI Symbol", 17), tags=tag)
            self.canvas.create_text(46, y, text=texto, fill="#E5EAF0",
                                    font=("Helvetica", 8 if len(texto) > 15 else 9, "bold"),
                                    anchor="w", tags=tag)
            if comando:
                self.canvas.tag_bind(tag, "<Button-1>", lambda _event, cmd=comando: cmd())
                self.canvas.tag_bind(tag, "<Enter>", lambda _event: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda _event: self.canvas.config(cursor=""))

        self.canvas.create_line(17, 684, 103, 684, fill="#496279")
        self.canvas.create_text(31, 705, text="⇥", fill=self.AZUL_CLARO,
                               font=("Segoe UI Symbol", 22), tags="sair")
        self.canvas.create_text(55, 705, text="SAIR", fill="#E5EAF0",
                               font=("Helvetica", 10, "bold"), anchor="w", tags="sair")
        self.canvas.tag_bind("sair", "<Button-1>", lambda _event: self.app.mostrar_inicial())

    def _montar_cabecalho(self):
        self.canvas.create_text(320, 126, text=self.titulo, fill="#142A47",
                               font=("Georgia", 24, "bold"), anchor="w")
        self.canvas.create_text(1114, 28, text="●", fill=self.AZUL,
                               font=("Segoe UI Symbol", 19), anchor="center")
        self.canvas.create_text(1155, 28, text="●", fill=self.AZUL,
                               font=("Segoe UI Symbol", 25), anchor="center")
        usuario = self.app.usuario_atual[2] if self.app.usuario_atual else ""
        if usuario:
            self.canvas.create_text(1080, 55, text=f"Usuário: {usuario}", fill="#142A47",
                                    font=("Helvetica", 8, "bold"), anchor="e")

    def area_conteudo(self, x=300, y=155, largura=875, altura=540):
        frame = ttk.Frame(self.canvas)
        self.canvas.create_window(x, y, window=frame, anchor="nw", width=largura, height=altura)
        return frame


def estilo_tabela():
    estilo = ttk.Style()
    estilo.configure("Tabela.Treeview", rowheight=36, font=("Helvetica", 10),
                     background="#FFFFFF", fieldbackground="#FFFFFF")
    estilo.configure("Tabela.Treeview.Heading", background="#183452", foreground="white",
                     font=("Georgia", 11, "bold"))