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
		area = self.area_conteudo(x=300, y=155, largura=895, altura=550)
		area.columnconfigure(0, weight=1)
		area.columnconfigure(1, weight=1)
		area.rowconfigure(0, weight=1)
		area.rowconfigure(1, weight=1)

		dados = self._painel(area, "DADOS DA ASSISTÊNCIA", 0, 0)
		self.campos_assistencia = {}
		for rotulo, valor in (("Nome", "Trinity Tech"), ("Telefone", "(31) 99999-9999"),
							  ("E-mail", "trinity.tech@gmail.com"), ("Endereço", "R. Padre Pedro Pinto, 1500 - Venda Nova")):
			ttk.Label(dados, text=rotulo, font=("Helvetica", 11)).pack(anchor="w")
			campo = ttk.Entry(dados, width=42)
			campo.insert(0, valor)
			campo.pack(fill="x", pady=(0, 4))
			self.campos_assistencia[rotulo] = campo
		ttk.Button(dados, text="Salvar dados", bootstyle="primary",
				   command=self._salvar_dados).pack(anchor="e", pady=(4, 0))

		plano = self._painel(area, "PLANO DO SITE", 0, 1)
		ttk.Label(plano, text="Plano Gold", font=("Georgia", 15, "bold")).pack(anchor="w")
		ttk.Label(plano, text="• Notificações automáticas via WhatsApp / SMS\n• Anexo de fotos no Check-in/Check-out\n• Gestão financeira completa\n• Portal do cliente\n• Controle de estoque vinculado à O.S.", justify="left", font=("Helvetica", 10)).pack(anchor="w", pady=4)
		ttk.Button(plano, text="Fazer Upgrade / Comprar Plano Gold", bootstyle="primary",
			   command=self._comprar_plano).pack(fill="x", pady=4)
		ttk.Label(plano, text="* Você está usando a versão gratuita *").pack()

		acesso = self._painel(area, "DADOS DE ACESSO E LOGO", 1, 0)
		caminho = Path(__file__).resolve().parents[1] / "imagens" / "logo.png"
		imagem = Image.open(caminho).resize((135, 95))
		self._logo = ImageTk.PhotoImage(imagem)
		self.logo_label = ttk.Label(acesso, image=self._logo)
		self.logo_label.pack(side="left", padx=(0, 18))
		ttk.Button(acesso, text="Alterar Logo", bootstyle="primary",
			   command=self._alterar_logo).pack(side="left", anchor="s")
		ttk.Button(acesso, text="Configurar Login", bootstyle="secondary",
			   command=self._configurar_login).pack(side="right", anchor="center")

		info = self._painel(area, "INFORMAÇÕES DO SISTEMA", 1, 1)
		ttk.Label(info, text="Versão do Sistema:\n\nIntegrantes do Grupo:\nLucas Gabriel, João Vitor, Nycole Ashley",
				  justify="left", font=("Helvetica", 11)).pack(anchor="w", pady=8)

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
		imagem.thumbnail((135, 95), Image.Resampling.LANCZOS)
		self._logo = ImageTk.PhotoImage(imagem)
		self.logo_label.configure(image=self._logo)
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
