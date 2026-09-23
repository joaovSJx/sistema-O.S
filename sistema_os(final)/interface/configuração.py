import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from PIL import Image, ImageTk

from interface.layout import TelaSistema


class ConfiguracaoFrame(TelaSistema):
	def __init__(self, parent, app):
		super().__init__(parent, app, "Configuração do Sistema", "configuracao")
		self._montar_conteudo()

	def _painel(self, pai, titulo, linha, coluna, largura=1, altura=1):
		painel = ttk.Frame(pai, padding=0, bootstyle="light")
		painel.grid(row=linha, column=coluna, rowspan=altura, columnspan=largura,
					sticky="nsew", padx=8, pady=8)
		ttk.Label(painel, text=titulo, anchor="center", bootstyle="inverse-primary",
				  font=("Georgia", 15, "bold")).pack(fill="x", ipady=7)
		corpo = ttk.Frame(painel, padding=14)
		corpo.pack(fill="both", expand=True)
		return corpo

	def _montar_conteudo(self):
		"""Desenha a área de configurações diretamente no Canvas da tela."""
		canvas = self.canvas
		azul = "#071D3A"
		texto = "#1B2635"

		def arredondado(x1, y1, x2, y2, raio=12, **opcoes):
			pontos = [x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
					  x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
					  x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1]
			return canvas.create_polygon(pontos, smooth=True, **opcoes)

		def painel(x1, y1, x2, y2, titulo):
			arredondado(x1, y1, x2, y2, 13, fill="#FEFEFE", outline="#CED3D9", width=2)
			# O cabeçalho fica separado para preservar os cantos arredondados do cartão.
			arredondado(x1, y1, x2, y1 + 44, 13, fill=azul, outline="")
			canvas.create_rectangle(x1, y1 + 23, x2, y1 + 44, fill=azul, outline="")
			canvas.create_text((x1 + x2) / 2, y1 + 23, text=titulo, fill="white",
						   font=("Georgia", 20, "bold"))

		def botao(x1, y1, x2, y2, titulo, tag, cor="#1478C9", cor_texto="white"):
			arredondado(x1, y1, x2, y2, 10, fill=cor, outline="#4C80AA", width=1, tags=tag)
			canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=titulo, fill=cor_texto,
						   font=("Helvetica", 13, "bold"), tags=tag)

		# Cartões superiores.
		# Medidas baseadas na referência, proporcionais ao Canvas 1200 x 720.
		painel(285, 172, 724, 432, "DADOS DA ASSISTÊNCIA")
		painel(745, 172, 1181, 432, "PLANO DO SITE")
		painel(285, 454, 724, 647, "DADOS DE ACESSO E LOGO")
		painel(745, 454, 1181, 647, "INFORMAÇÕES DO SISTEMA")

		self.campos_assistencia = {}
		def campo(rotulo, valor, x, y, largura):
			canvas.create_text(x, y, text=rotulo, fill=texto, anchor="w", font=("Helvetica", 14))
			arredondado(x, y + 8, x + largura, y + 48, 9, fill="white", outline="#313A45", width=2)
			entrada = tk.Entry(canvas, font=("Helvetica", 13), bd=0, highlightthickness=0,
							   bg="white", fg="#303640")
			entrada.insert(0, valor)
			canvas.create_window(x + 12, y + 15, anchor="nw", window=entrada, width=largura - 24, height=25)
			self.campos_assistencia[rotulo] = entrada

		campo("Nome", "Trinity Tech", 310, 226, 389)
		campo("Telefone", "(31) 99999-9999", 310, 291, 172)
		campo("E-mail", "trinity.tech@gmail.com", 507, 291, 192)
		campo("Endereço", "R. Padre Pedro Pinto, 1500 - Venda Nova", 310, 356, 389)

		canvas.create_text(770, 230, text="Plano Gold 💎", fill=texto, anchor="w",
						   font=("Georgia", 18, "bold"))
		beneficios = (
			"• Notificações automáticas via WhatsApp / SMS\n"
			"• Anexo de fotos no Check-in/Check-out\n"
			"• Gestão financeira completa\n"
			"• Portal do cliente\n"
			"• Controle de estoque vinculado à O.S."
		)
		canvas.create_text(765, 258, text=beneficios, fill="#252B32", anchor="nw",
						   justify="left", font=("Helvetica", 12))
		botao(770, 364, 1155, 405, "Fazer Upgrade / Comprar Plano Gold", "comprar_plano")
		canvas.create_text(962, 418, text="* Você está usando a versão gratuita *",
						   fill="#303030", font=("Helvetica", 11))

		# O cartão inferior tem menos altura; um logo menor evita que ele invada
		# o cabeçalho e deixa espaço para as duas ações.
		caminho = Path(__file__).resolve().parents[1] / "imagens" / "logo.png"
		imagem = Image.open(caminho).convert("RGBA")
		imagem.thumbnail((82, 62), Image.Resampling.LANCZOS)
		self._logo = ImageTk.PhotoImage(imagem)
		self.logo_item = canvas.create_image(365, 550, image=self._logo)
		canvas.create_line(470, 505, 470, 620, fill="#C9CDD2", width=2)
		botao(310, 590, 420, 621, "Alterar Logo", "alterar_logo")
		botao(515, 545, 700, 584, "Configurar Login", "configurar_login", "#C9CDD3", "#293746")

		canvas.create_text(770, 520, text="Versão do Sistema: 1.0.0", fill="#363C43", anchor="w",
						   font=("Helvetica", 12))
		canvas.create_text(770, 562, text="Integrantes do Grupo:\nLucas Gabriel, João Vitor, Nycole Ashley",
						   fill="#363C43", anchor="w", justify="left", font=("Helvetica", 12))

		acoes = {
			"salvar_dados": self._salvar_dados,
			"comprar_plano": self._comprar_plano,
			"alterar_logo": self._alterar_logo,
			"configurar_login": self._configurar_login,
		}
		for tag, comando in acoes.items():
			canvas.tag_bind(tag, "<Button-1>", lambda _event, acao=comando: acao())
			canvas.tag_bind(tag, "<Enter>", lambda _event: canvas.config(cursor="hand2"))
			canvas.tag_bind(tag, "<Leave>", lambda _event: canvas.config(cursor=""))

	def _salvar_dados(self):
		messagebox.showinfo("Configuração", "Dados da assistência salvos nesta sessão.", parent=self)

	def _comprar_plano(self):
		messagebox.showinfo("Plano Gold", "O upgrade do Plano Gold será disponibilizado em breve.", parent=self)

	def _alterar_logo(self):
		caminho = filedialog.askopenfilename(
			title="Selecionar logo", filetypes=(("Imagens", "*.png *.jpg *.jpeg"), ("Todos os arquivos", "*.*")),
			parent=self,
		)
		if not caminho:
			return
		imagem = Image.open(caminho).convert("RGBA")
		imagem.thumbnail((82, 62), Image.Resampling.LANCZOS)
		self._logo = ImageTk.PhotoImage(imagem)
		self.canvas.itemconfigure(self.logo_item, image=self._logo)
		messagebox.showinfo("Logo", "Logo carregada para esta sessão.", parent=self)

	def _configurar_login(self):
		janela = tk.Toplevel(self)
		janela.title("Configurar Login")
		janela.geometry("360x220")
		janela.transient(self.winfo_toplevel())
		janela.grab_set()
		conteudo = ttk.Frame(janela, padding=20)
		conteudo.pack(fill="both", expand=True)
		ttk.Label(conteudo, text="Usuário").pack(anchor="w")
		ttk.Entry(conteudo).pack(fill="x", pady=(2, 10))
		ttk.Label(conteudo, text="Nova senha").pack(anchor="w")
		ttk.Entry(conteudo, show="*").pack(fill="x", pady=(2, 15))
		ttk.Button(conteudo, text="Salvar", bootstyle="primary",
				   command=lambda: (janela.destroy(), messagebox.showinfo("Login", "Configuração salva nesta sessão.", parent=self))).pack(anchor="e")
