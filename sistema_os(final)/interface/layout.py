from pathlib import Path
import tkinter as tk

from PIL import Image, ImageColor, ImageDraw, ImageTk
import ttkbootstrap as ttk
from interface.responsivo import centralizar_canvas


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
        self._icones = {}
        self.canvas = tk.Canvas(self, width=self.LARGURA, height=self.ALTURA,
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        centralizar_canvas(self.canvas, self, self.LARGURA, self.ALTURA)
        self._montar_fundo()
        self._montar_menu()
        self._montar_cabecalho()

    def _carregar_icone(self, arquivo, tamanho, cor=None, preservar_branco=False,
                         remover_branco=False):
        caminho = Path(__file__).resolve().parents[1] / "imagens" / "icones" / arquivo
        imagem = Image.open(caminho).convert("RGBA")
        if preservar_branco or remover_branco:
            ImageDraw.floodfill(imagem, (0, 0), (255, 255, 255, 0), thresh=12)
        area_visivel = imagem.getchannel("A").getbbox()
        if area_visivel:
            imagem = imagem.crop(area_visivel)
        if cor and preservar_branco:
            pixels = imagem.load()
            vermelho, verde, azul = ImageColor.getrgb(cor)
            for y in range(imagem.height):
                for x in range(imagem.width):
                    r, g, b, a = pixels[x, y]
                    if a and min(r, g, b) < 245:
                        pixels[x, y] = (vermelho, verde, azul, a)
        elif cor:
            transparencia = imagem.getchannel("A")
            imagem_colorida = Image.new("RGBA", imagem.size, cor)
            imagem_colorida.putalpha(transparencia)
            imagem = imagem_colorida
        imagem.thumbnail(tamanho, Image.Resampling.LANCZOS)
        icone = ImageTk.PhotoImage(imagem)
        self._icones[(arquivo, tamanho, cor, preservar_branco, remover_branco)] = icone
        return icone

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

        itens = [
            ("icone_painel.png", "PAINEL", self.app.mostrar_dashboard),
            ("icone_clientes.png", "CLIENTES", self.app.mostrar_clientes),
            ("icone_equipamentos.png", "EQUIPAMENTOS", self.app.mostrar_equipamentos),
            ("icone_os.png", "ORDEM DE SERVIÇO", self.app.mostrar_ordens),
            ("icone_configuracao.png", "CONFIGURAÇÕES", self.app.mostrar_configuracao),
        ]
        for indice, (arquivo, texto, comando) in enumerate(itens):
            y = 163 + indice * 55
            tag = f"menu_{indice}"
            tamanhos = {"icone_painel.png": (48, 48)}
            icone = self._carregar_icone(
                arquivo, tamanhos.get(arquivo, (18, 18)), "#1262B3"
            )
            self.canvas.create_image(31, y, image=icone, anchor="center", tags=tag)
            self.canvas.create_text(55, y, text=texto, fill="#E5EAF0",
                                    font=("Helvetica", 8 if len(texto) > 15 else 9, "bold"),
                                    anchor="w", tags=tag)
            if comando:
                self.canvas.tag_bind(tag, "<Button-1>", lambda _event, cmd=comando: cmd())
                self.canvas.tag_bind(tag, "<Enter>", lambda _event: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda _event: self.canvas.config(cursor=""))

        self.canvas.create_line(17, 684, 103, 684, fill="#496279")
        icone_saida = self._carregar_icone(
            "icone_saida.png", (30, 30), "#1262B3", preservar_branco=True
        )
        self.canvas.create_image(32, 705, image=icone_saida, anchor="center", tags="sair")
        self.canvas.create_text(55, 705, text="SAIR", fill="#E5EAF0",
                               font=("Helvetica", 10, "bold"), anchor="w", tags="sair")
        self.canvas.tag_bind("sair", "<Button-1>", lambda _event: self.app.mostrar_inicial())

    def _montar_cabecalho(self):
        # Nas telas de O.S. e Configurações o conteúdo começa mais à esquerda;
        # o título acompanha a grade principal para manter o alinhamento visual.
        posicao_titulo = 285 if self.pagina in ("ordens", "configuracao") else 365
        self.canvas.create_text(posicao_titulo, 126, text=self.titulo, fill="#142A47",
                               font=("Georgia", 24, "bold"), anchor="w")
        sino = self._carregar_icone("icone_sino.png", (24, 24), self.AZUL)
        usuario_icone = self._carregar_icone(
            "icone_usuario.png", (31, 31), self.AZUL, preservar_branco=True
        )
        self.canvas.create_image(1114, 28, image=sino, anchor="center")
        self.canvas.create_image(1155, 28, image=usuario_icone, anchor="center")

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
