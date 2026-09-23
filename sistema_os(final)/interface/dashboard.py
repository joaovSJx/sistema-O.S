import tkinter as tk
from pathlib import Path

import ttkbootstrap as ttk
from PIL import Image, ImageColor, ImageDraw, ImageTk

from database.ordens_servico import consultar_os, consultar_os_por_status


class DashboardFrame(ttk.Frame):
    """Tela principal do sistema desenhada sobre a imagem de fundo."""

    LARGURA = 1200
    ALTURA = 720
    AZUL_MENU = "#061A34"

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.usuario_id = app.usuario_atual[0] if app.usuario_atual else None
        self.ordens = []
        self.icones = {}
        self.montar_layout()

    def _carregar_icone(self, nome_arquivo, tamanho, cor=None, preservar_branco=False):
        """Abre um ícone e guarda a referência para ele não desaparecer."""
        caminho = (
            Path(__file__).resolve().parents[1]
            / "imagens"
            / "icones"
            / nome_arquivo
        )
        imagem = Image.open(caminho).convert("RGBA")

        
       
        if preservar_branco:
            ImageDraw.floodfill(imagem, (0, 0), (255, 255, 255, 0), thresh=12)

        
        
        area_visivel = imagem.getchannel("A").getbbox()
        if area_visivel:
            imagem = imagem.crop(area_visivel)

        if cor and preservar_branco:
            pixels = imagem.load()
            vermelho_novo, verde_novo, azul_novo = ImageColor.getrgb(cor)
            for y in range(imagem.height):
                for x in range(imagem.width):
                    vermelho, verde, azul, alfa = pixels[x, y]
                    if alfa and min(vermelho, verde, azul) < 245:
                        pixels[x, y] = (vermelho_novo, verde_novo, azul_novo, alfa)
        elif cor:
            transparencia = imagem.getchannel("A")
            imagem_colorida = Image.new("RGBA", imagem.size, cor)
            imagem_colorida.putalpha(transparencia)
            imagem = imagem_colorida

        imagem.thumbnail(tamanho, Image.Resampling.LANCZOS)
        icone = ImageTk.PhotoImage(imagem)
        self.icones[(nome_arquivo, tamanho, cor)] = icone
        return icone

    def _retangulo_arredondado(self, x1, y1, x2, y2, raio, **opcoes):
        """Desenha um retângulo arredondado no Canvas."""
        pontos = [
            x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
            x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
            x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1,
        ]
        return self.canvas.create_polygon(pontos, smooth=True, **opcoes)

    def montar_layout(self):
        self.canvas = tk.Canvas(
            self, width=self.LARGURA, height=self.ALTURA, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        caminho_fundo = (
            Path(__file__).resolve().parents[1]
            / "imagens"
            / "fundo_dashboard.jpeg"
        )
        imagem_fundo = Image.open(caminho_fundo).resize(
            (self.LARGURA, self.ALTURA)
        )
        self.fundo_dashboard = ImageTk.PhotoImage(imagem_fundo)
        self.canvas.create_image(0, 0, image=self.fundo_dashboard, anchor="nw")

        self._montar_menu()
        self._montar_cabecalho()
        self._montar_cartoes()
        self._montar_tabela()
        self._carregar_dados()

    def _montar_menu(self):
        self.canvas.create_rectangle(
            0, 120, 165, self.ALTURA, fill=self.AZUL_MENU, outline=""
        )
        self.canvas.create_line(0, 120, 165, 120, fill="#456078", width=1)
        self.canvas.create_line(164, 120, 164, 690, fill="#456078", width=1)

        caminho_logo = Path(__file__).resolve().parents[1] / "imagens" / "logo.png"
        imagem_logo = Image.open(caminho_logo)
        imagem_logo.thumbnail((55, 55), Image.Resampling.LANCZOS)
        self.logo_dashboard = ImageTk.PhotoImage(imagem_logo)
        self.canvas.create_image(18, 28, image=self.logo_dashboard, anchor="nw")
        self.canvas.create_text(
            82, 53, text="TRINITY TECH", fill="white",
            font=("Helvetica", 10, "bold"), anchor="w",
        )

        itens_menu = [
            ("icone_painel.png", "PAINEL"),
            ("icone_clientes.png", "CLIENTES"),
            ("icone_equipamentos.png", "EQUIPAMENTOS"),
            ("icone_os.png", "ORDEM DE SERVIÇO"),
            ("icone_configuracao.png", "CONFIGURAÇÕES"),
        ]

        y = 163
        comandos = [
            self.app.mostrar_dashboard,
            self.app.mostrar_clientes,
            self.app.mostrar_equipamentos,
            self.app.mostrar_ordens,
            self.app.mostrar_configuracao,
        ]
        for indice, (arquivo_icone, texto) in enumerate(itens_menu):
            tamanhos = {
                "icone_painel.png": (48, 48),
                "icone_clientes.png": (18, 18),
                "icone_equipamentos.png": (18, 18),
                "icone_os.png": (18, 18),
                "icone_configuracao.png": (18, 18),
            }
            icone = self._carregar_icone(
                arquivo_icone, tamanhos[arquivo_icone], "#1262B3"
            )
            tag = f"menu_dashboard_{indice}"
            self.canvas.create_image(
                31, y, image=icone, anchor="center", tags=tag
            )
            self.canvas.create_text(
                55, y, text=texto, fill="#E5EAF0",
                font=("Helvetica", 8 if texto == "ORDEM DE SERVIÇO" else 9, "bold"),
                anchor="w", tags=tag,
            )
            self.canvas.tag_bind(tag, "<Button-1>", lambda _event, comando=comandos[indice]: comando())
            self.canvas.tag_bind(tag, "<Enter>", lambda _event: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(tag, "<Leave>", lambda _event: self.canvas.config(cursor=""))
            y += 55

        self.canvas.create_line(17, 684, 103, 684, fill="#496279", width=1)
        icone_saida = self._carregar_icone(
            "icone_saida.png", (30, 30), "#1262B3", preservar_branco=True
        )
        self.canvas.create_image(
            32, 705, image=icone_saida, anchor="center", tags="sair"
        )
        self.canvas.create_text(
            55, 705, text="SAIR", fill="#E5EAF0",
            font=("Helvetica", 10, "bold"), anchor="w", tags="sair",
        )
        self.canvas.tag_bind("sair", "<Button-1>", lambda evento: self.app.mostrar_inicial())
        self.canvas.tag_bind("sair", "<Enter>", lambda evento: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("sair", "<Leave>", lambda evento: self.canvas.config(cursor=""))

    def _montar_cabecalho(self):
        self._retangulo_arredondado(
            350, 125, 510, 171, 10, fill="#6A7F9F", outline=""
        )
        botao_nova_os = self.canvas.create_text(
            430, 148, text="+ NOVA O.S", fill="white",
            font=("Helvetica", 13, "bold"), anchor="center", tags="nova_os",
        )
        self.canvas.tag_bind("nova_os", "<Button-1>", lambda _event: self.app.mostrar_ordens())
        self.canvas.tag_bind("nova_os", "<Enter>", lambda _event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("nova_os", "<Leave>", lambda _event: self.canvas.config(cursor=""))

        self._retangulo_arredondado(
            893, 112, 1120, 147, 18, fill="white", outline="#17202B", width=2
        )
        self.canvas.create_text(
            908, 130, text="⌕", fill="#17202B",
            font=("Helvetica", 18, "bold"), anchor="w",
        )

        self.busca_os = tk.StringVar(value="Buscar OS...")
        self.entrada_busca = tk.Entry(
            self.canvas,
            textvariable=self.busca_os,
            font=("Helvetica", 11),
            fg="#7B7B7B",
            bg="white",
            bd=0,
            highlightthickness=0,
        )
        self.entrada_busca.bind("<KeyRelease>", self._filtrar_os)
        self.entrada_busca.bind("<FocusIn>", self._limpar_placeholder)
        self.entrada_busca.bind("<FocusOut>", self._restaurar_placeholder)
        self.canvas.create_window(
            936,
            117,
            anchor="nw",
            window=self.entrada_busca,
            width=166,
            height=25,
        )

        icone_sino = self._carregar_icone("icone_sino.png", (24, 24), "#061A34")
        icone_usuario = self._carregar_icone(
            "icone_usuario.png", (31, 31), "#061A34", preservar_branco=True
        )
        self.canvas.create_image(1114, 28, image=icone_sino, anchor="center")
        self.canvas.create_image(1155, 28, image=icone_usuario, anchor="center")

    def _montar_cartoes(self):
        dados_cartoes = [
            ("ABERTAS", "#344B69", "icone_abertas.png"),
            ("EM ANÁLISE", "#C6B800", "icone_analise.png"),
            ("EM MANUTENÇÃO", "#8E0000", "icone_manutencao.png"),
            ("CONCLUÍDAS", "#007416", "icone_concluidas.png"),
        ]
        self.ids_totais = {}
        x = 301

        for titulo, cor, arquivo_icone in dados_cartoes:
            self._retangulo_arredondado(x, 185, x + 188, 293, 13, fill=cor, outline="")
            self.canvas.create_text(
                x + 20, 207, text=titulo, fill="white",
                font=("Helvetica", 12, "bold"), anchor="w",
            )
            self.ids_totais[titulo] = self.canvas.create_text(
                x + 20, 262, text="0", fill="white",
                font=("Helvetica", 36, "bold"), anchor="w",
            )
            icone = self._carregar_icone(arquivo_icone, (56, 56), "white")
            self.canvas.create_image(
                x + 145, 249, image=icone, anchor="center"
            )
            x += 207

    def _montar_tabela(self):
        self.canvas.create_text(
            286, 344, text="ÚLTIMAS ORDENS DE SERVIÇO", fill="#151515",
            font=("Helvetica", 16, "bold"), anchor="w",
        )
        self.canvas.create_rectangle(
            275, 365, 1152, 397, fill="#D1D8E1", outline="#B4BFCC"
        )

        self.colunas = {
            "numero": 310,
            "cliente": 500,
            "equipamento": 690,
            "status": 930,
            "data": 1090,
        }
        titulos = {
            "numero": "Nº OS",
            "cliente": "CLIENTES",
            "equipamento": "EQUIPAMENTO",
            "status": "STATUS",
            "data": "DATA",
        }
        for chave, x in self.colunas.items():
            self.canvas.create_text(
                x, 381, text=titulos[chave], fill="#536476",
                font=("Helvetica", 11, "bold"), anchor="center",
            )
        self.linhas_os = []

    def _carregar_dados(self):
        self.ordens = consultar_os(self.usuario_id)
        totais = {
            "ABERTAS": len(consultar_os_por_status("Aberta", self.usuario_id)),
            "EM ANÁLISE": len(consultar_os_por_status("Em análise", self.usuario_id)),
            "EM MANUTENÇÃO": len(consultar_os_por_status("Em manutenção", self.usuario_id)),
            "CONCLUÍDAS": len(consultar_os_por_status("Concluída", self.usuario_id)),
        }
        for titulo, total in totais.items():
            self.canvas.itemconfig(self.ids_totais[titulo], text=str(total))
        self._preencher_tabela(self.ordens)

    def _preencher_tabela(self, ordens):
        for item in self.linhas_os:
            self.canvas.delete(item)
        self.linhas_os = []

        y = 420
        cores_status = {
            "Aberta": "#344B69",
            "Em análise": "#AD9F00",
            "Em manutenção": "#8E0000",
            "Concluída": "#24724A",
        }
        icone_cliente = self._carregar_icone(
            "cliente_os.png", (18, 18), "#8B8B8B"
        )

        for ordem in reversed(ordens[-5:]):
            id_os, cliente, tipo, marca, modelo, problema, status, valor, data = ordem
            equipamento = f"{tipo} {marca} {modelo}"
            valores = [
                (self.colunas["numero"], f"OS{id_os:05d}", "#202020"),
                (self.colunas["equipamento"], equipamento, "#202020"),
                (self.colunas["status"], status.upper(), cores_status.get(status, "#202020")),
                (self.colunas["data"], data, "#202020"),
            ]

            self.linhas_os.append(self.canvas.create_image(
                435, y, image=icone_cliente, anchor="center"
            ))
            self.linhas_os.append(self.canvas.create_text(
                450, y, text=cliente, fill="#202020",
                font=("Helvetica", 11), anchor="w"
            ))

            for x, texto, cor in valores:
                self.linhas_os.append(self.canvas.create_text(
                    x, y, text=texto, fill=cor, font=("Helvetica", 11), anchor="center"
                ))
            self.linhas_os.append(self.canvas.create_line(
                275, y + 20, 1152, y + 20, fill="#D8DDE3"
            ))
            y += 36

    def _filtrar_os(self, evento=None):
        termo = self.busca_os.get().strip().lower()
        if not termo or termo == "buscar os...":
            ordens_filtradas = self.ordens
        else:
            ordens_filtradas = [
                ordem for ordem in self.ordens
                if termo in str(ordem[0]).lower() or termo in ordem[1].lower()
            ]
        self._preencher_tabela(ordens_filtradas)

    def _limpar_placeholder(self, evento=None):
        if self.busca_os.get() == "Buscar OS...":
            self.busca_os.set("")
            self.entrada_busca.config(fg="#202020")

    def _restaurar_placeholder(self, evento=None):
        if not self.busca_os.get().strip():
            self.busca_os.set("Buscar OS...")
            self.entrada_busca.config(fg="#7B7B7B")
            self._preencher_tabela(self.ordens)
