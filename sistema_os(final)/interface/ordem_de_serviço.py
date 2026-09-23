import tkinter as tk
import os
from tkinter import messagebox
from datetime import date
from pathlib import Path

import ttkbootstrap as ttk

from database.connection import conectar
from database.ordens_servico import cadastrar_os, consultar_os
from documentos.gerar_pdf import gerar_pdf_os
from interface.layout import TelaSistema, estilo_tabela


class OrdensFrame(TelaSistema):
	def __init__(self, parent, app):
		super().__init__(parent, app, "Ordens de Serviço", "ordens")
		self.ordens = []
		self.usuario_id = app.usuario_atual[0] if app.usuario_atual else None
		self._montar_conteudo()

	def _montar_conteudo(self):
		self._montar_layout_canvas()
		return
		estilo_tabela()
		area = self.area_conteudo(x=305, y=155, largura=890, altura=555)
		topo = ttk.Frame(area)
		topo.pack(fill="x", pady=(0, 13))
		ttk.Button(topo, text="+ NOVA O.S", bootstyle="primary", command=self._abrir_formulario).pack(side="left")
		ttk.Button(topo, text="GERAR PDF", bootstyle="success", command=self._gerar_pdf).pack(side="left", padx=8)
		self.busca = tk.StringVar()
		entrada = ttk.Entry(topo, textvariable=self.busca, width=28)
		entrada.pack(side="right", ipady=5)
		ttk.Label(topo, text="⌕", font=("Segoe UI Symbol", 16)).pack(side="right", padx=(0, 5))
		entrada.bind("<KeyRelease>", lambda _event: self._preencher())

		filtros = ttk.Frame(area)
		filtros.pack(fill="x", pady=(0, 14))
		self.filtro_numero = tk.StringVar()
		self.filtro_cliente = tk.StringVar()
		self.filtro_status = tk.StringVar(value="Todos")
		self.filtro_data = tk.StringVar()
		for rotulo, variavel, largura in (("Filtro: Nº da OS", self.filtro_numero, 13),
										  ("Filtro: Nome do Cliente", self.filtro_cliente, 18),
										  ("Filtro: Status", self.filtro_status, 15),
										  ("Filtro: Período de Entrada", self.filtro_data, 18)):
			bloco = ttk.Frame(filtros)
			bloco.pack(side="left", fill="x", expand=True, padx=(0, 10))
			ttk.Label(bloco, text=rotulo).pack(anchor="w")
			if variavel is self.filtro_status:
				widget = ttk.Combobox(bloco, textvariable=variavel,
									  values=("Todos", "Aberta", "Em análise", "Em manutenção", "Concluída"),
									  state="readonly", width=largura)
			else:
				widget = ttk.Entry(bloco, textvariable=variavel, width=largura)
			widget.pack(fill="x", ipady=4)
			variavel.trace_add("write", lambda *_args: self._preencher())

		moldura = ttk.Frame(area, padding=8, bootstyle="light")
		moldura.pack(fill="both", expand=True)
		colunas = ("numero", "cliente", "equipamento", "problema", "status", "valor", "data", "acoes")
		self.tabela = ttk.Treeview(moldura, columns=colunas, show="headings", style="Tabela.Treeview")
		titulos = ("Nº OS", "CLIENTES", "EQUIPAMENTO", "PROBLEMA", "STATUS", "VALOR", "DATA", "")
		larguras = (78, 115, 135, 135, 95, 85, 70, 50)
		for coluna, titulo, largura in zip(colunas, titulos, larguras):
			self.tabela.heading(coluna, text=titulo)
			self.tabela.column(coluna, width=largura, anchor="center")
		self.tabela.pack(side="left", fill="both", expand=True)
		barra = ttk.Scrollbar(moldura, orient="vertical", command=self.tabela.yview)
		barra.pack(side="right", fill="y")
		self.tabela.configure(yscrollcommand=barra.set)
		self._preencher()

	def _montar_layout_canvas(self):
		self._retangulo_arredondado(325, 158, 475, 202, 11, fill="#536F99", outline="", tags="nova_os")
		self.canvas.create_text(400, 180, text="+ NOVA OS", fill="white", font=("Helvetica", 13, "bold"), tags="nova_os")
		self.canvas.tag_bind("nova_os", "<Button-1>", lambda _event: self._abrir_formulario())

		self._retangulo_arredondado(835, 125, 1135, 162, 19, fill="white", outline="#555555", width=2)
		self.canvas.create_text(855, 143, text="⌕", fill="#555555", font=("Segoe UI Symbol", 18, "bold"))
		self.texto_busca = "Buscar por OS..."
		self.busca = tk.StringVar(value=self.texto_busca)
		entrada = tk.Entry(self.canvas, textvariable=self.busca, font=("Helvetica", 11), fg="#777777", bg="white", bd=0, highlightthickness=0)
		self.canvas.create_window(875, 132, anchor="nw", window=entrada, width=242, height=24)
		entrada.bind("<KeyRelease>", lambda _event: self._preencher())
		entrada.bind("<FocusIn>", self._limpar_busca)
		entrada.bind("<FocusOut>", self._restaurar_busca)

		self.filtro_numero = tk.StringVar()
		self.filtro_cliente = tk.StringVar()
		self.filtro_status = tk.StringVar(value="Todos")
		self.filtro_data = tk.StringVar()
		filtros = [
			("Filtro: Nº da OS", self.filtro_numero, 285, "entrada"),
			("Filtro: Nome do Cliente", self.filtro_cliente, 510, "entrada"),
			("Filtro: Status", self.filtro_status, 735, "status"),
			("Filtro: Período de Entrada", self.filtro_data, 960, "entrada"),
		]
		for rotulo, variavel, x, tipo in filtros:
			self.canvas.create_text(x, 215, text=rotulo, fill="#25374E", font=("Helvetica", 11), anchor="w")
			self._retangulo_arredondado(x, 225, x + 205, 260, 8, fill="white", outline="#777777", width=2)
			if tipo == "status":
				widget = ttk.Combobox(self.canvas, textvariable=variavel, values=("Todos", "Aberta", "Em análise", "Em manutenção", "Concluída"), state="readonly")
			else:
				widget = tk.Entry(self.canvas, textvariable=variavel, font=("Helvetica", 10), bd=0, highlightthickness=0, bg="white")
			self.canvas.create_window(x + 10, 232, anchor="nw", window=widget, width=185, height=22)
			variavel.trace_add("write", lambda *_args: self._preencher())

		self.canvas.create_text(300, 305, text="Listagem", fill="#142A47", font=("Georgia", 18, "bold"), anchor="w")
		self._montar_tabela_canvas()
		self._preencher()

	def _retangulo_arredondado(self, x1, y1, x2, y2, raio, **opcoes):
		pontos = [x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
				  x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
				  x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1]
		return self.canvas.create_polygon(pontos, smooth=True, **opcoes)

	def _montar_tabela_canvas(self):
		self.canvas.create_rectangle(285, 325, 1145, 680, fill="white", outline="#B8C0C8", width=1)
		self.canvas.create_rectangle(285, 325, 1145, 365, fill="#9DB2CB", outline="")
		self.colunas_canvas = [(335, "Nº OS", 92), (435, "CLIENTES", 105), (560, "EQUIPAMENTO", 130),
							(700, "PROBLEMA", 130), (820, "STATUS", 95), (920, "VALOR", 90), (1015, "DATA", 75)]
		for x, titulo, largura in self.colunas_canvas:
			self.canvas.create_text(x, 345, text=titulo, fill="#1B2D45", font=("Georgia", 12, "bold"))
		self.itens_os = []

	def _preencher(self):
		self._preencher_canvas()
		return
		self.ordens = consultar_os(self.usuario_id)
		for item in self.tabela.get_children():
			self.tabela.delete(item)
		numero = self.filtro_numero.get().strip().lower()
		cliente = self.filtro_cliente.get().strip().lower()
		status = self.filtro_status.get()
		data = self.filtro_data.get().strip().lower()
		for ordem in self.ordens:
			id_os, nome, tipo, marca, modelo, problema, situacao, valor, data_entrada = ordem
			if numero and numero not in str(id_os):
				continue
			if cliente and cliente not in nome.lower():
				continue
			if status != "Todos" and situacao != status:
				continue
			if data and data not in data_entrada.lower():
				continue
			equipamento = f"{tipo} {marca} {modelo}"
			valor_formatado = f"R$ {valor or 0:.2f}".replace(".", ",")
			self.tabela.insert("", "end", values=(f"OS{id_os:04d}", nome, equipamento, problema,
												   situacao, valor_formatado, data_entrada, "◉  ✎"))

	def _preencher_canvas(self):
		if not hasattr(self, "itens_os"):
			return
		for item in self.itens_os:
			self.canvas.delete(item)
		self.itens_os = []
		self.ordens = consultar_os(self.usuario_id)
		busca = self.busca.get().strip().lower()
		if busca == self.texto_busca.lower():
			busca = ""
		numero = self.filtro_numero.get().strip().lower()
		cliente = self.filtro_cliente.get().strip().lower()
		status_filtro = self.filtro_status.get()
		data = self.filtro_data.get().strip().lower()
		ordens_filtradas = []
		for ordem in self.ordens:
			id_os, nome, tipo, marca, modelo, problema, situacao, valor, data_entrada = ordem
			texto_busca = f"{id_os} {nome} {tipo} {marca} {modelo}".lower()
			if busca and busca not in texto_busca:
				continue
			if numero and numero not in str(id_os).lower():
				continue
			if cliente and cliente not in nome.lower():
				continue
			if status_filtro != "Todos" and situacao != status_filtro:
				continue
			if data and data not in data_entrada.lower():
				continue
			ordens_filtradas.append(ordem)

		for indice in range(8):
			y1 = 365 + indice * 38
			cor = "#FFFFFF" if indice % 2 == 0 else "#F0F0F0"
			self.itens_os.append(self.canvas.create_rectangle(285, y1, 1145, y1 + 38, fill=cor, outline="#D9DDE0"))

		# As mesmas imagens são reutilizadas em cada linha. Isso mantém todos os
		# ícones visíveis, sem o Python descartar os das linhas anteriores.
		icone_editar = self._carregar_icone("icone_editar_os.png", (22, 22), "#142A47")
		icone_pdf = self._carregar_icone("icone_pdf.png", (23, 23), "#142A47")

		for indice, ordem in enumerate(ordens_filtradas[:8]):
			y = 384 + indice * 38
			id_os, nome, tipo, marca, modelo, problema, situacao, valor, data_entrada = ordem
			equipamento = f"{tipo} {marca} {modelo}"
			valor_formatado = f"R$ {valor or 0:.2f}".replace(".", ",")
			valores = [
				(335, f"OS{id_os:04d}", 12), (435, nome, 16), (560, equipamento, 19),
				(700, problema, 18), (820, situacao, 14), (920, valor_formatado, 13), (1015, data_entrada, 11),
			]
			for x, texto, limite in valores:
				texto = str(texto)
				if len(texto) > limite:
					texto = texto[:limite - 3] + "..."
				self.itens_os.append(self.canvas.create_text(x, y, text=texto, fill="#202020", font=("Helvetica", 11), anchor="center"))
			tag_pdf = f"pdf_{id_os}"
			self.itens_os.append(self.canvas.create_image(1085, y, image=icone_editar))
			self.itens_os.append(self.canvas.create_image(1120, y, image=icone_pdf, tags=tag_pdf))
			self.canvas.tag_bind(tag_pdf, "<Button-1>", lambda _event, id_atual=id_os: self._gerar_pdf_por_id(id_atual))

	def _limpar_busca(self, _event=None):
		if self.busca.get() == self.texto_busca:
			self.busca.set("")

	def _restaurar_busca(self, _event=None):
		if not self.busca.get().strip():
			self.busca.set(self.texto_busca)
			self._preencher_canvas()

	def _gerar_pdf_por_id(self, id_os):
		try:
			gerar_pdf_os(id_os, self.usuario_id)
			caminho_pdf = Path(__file__).resolve().parents[1] / "documentos" / "gerados" / f"Ordem_de_Servico_{id_os}.pdf"
			os.startfile(caminho_pdf)
			messagebox.showinfo("PDF gerado", f"PDF da OS {id_os} gerado com sucesso.", parent=self)
		except (OSError, ValueError) as erro:
			messagebox.showerror("Erro ao gerar PDF", str(erro), parent=self)

	def _gerar_pdf(self):
		selecionados = self.tabela.selection()
		if not selecionados:
			messagebox.showwarning("Gerar PDF", "Selecione uma ordem de serviço.", parent=self)
			return

		valores = self.tabela.item(selecionados[0], "values")
		id_os = int(str(valores[0]).replace("OS", ""))
		try:
			gerar_pdf_os(id_os, self.usuario_id)
			caminho_pdf = Path(__file__).resolve().parents[1] / "documentos" / "gerados" / f"Ordem_de_Servico_{id_os}.pdf"
			os.startfile(caminho_pdf)
			messagebox.showinfo("PDF gerado", f"PDF da OS {id_os} gerado com sucesso.", parent=self)
		except (OSError, ValueError) as erro:
			messagebox.showerror("Erro ao gerar PDF", str(erro), parent=self)

	def _abrir_formulario(self):
		"""Abre o formulário de O.S. desenhado sobre um Canvas.

		Os widgets continuam sendo nativos para manter teclado, seleção e
		validação, mas toda a composição visual segue o desenho de referência.
		"""
		janela = tk.Toplevel(self)
		janela.title("Nova Ordem de Serviço")
		janela.geometry("680x745")
		janela.resizable(False, False)
		janela.configure(bg="#F6F7F8")
		janela.transient(self.winfo_toplevel())
		janela.grab_set()

		canvas = tk.Canvas(janela, width=680, height=745, bg="#F6F7F8",
						   highlightthickness=0)
		canvas.pack(fill="both", expand=True)

		def arredondado(x1, y1, x2, y2, raio=12, **opcoes):
			pontos = [x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
					  x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
					  x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1]
			return canvas.create_polygon(pontos, smooth=True, **opcoes)

		# Moldura, título e divisória.
		arredondado(18, 10, 662, 735, 30, fill="#FDFDFD", outline="#3D6E91", width=3)
		canvas.create_text(46, 51, text="NOVA ORDEM DE SERVIÇO", anchor="w",
						   fill="#101B2B", font=("Georgia", 27, "bold"))
		canvas.create_line(46, 82, 622, 82, fill="#D9DDE0")
		canvas.create_text(636, 42, text="×", fill="#101B2B", font=("Helvetica", 31), tags="fechar")
		canvas.tag_bind("fechar", "<Button-1>", lambda _event: janela.destroy())
		canvas.tag_bind("fechar", "<Enter>", lambda _event: canvas.config(cursor="hand2"))
		canvas.tag_bind("fechar", "<Leave>", lambda _event: canvas.config(cursor=""))

		conexao = conectar()
		clientes = conexao.execute(
			"SELECT id, nome FROM clientes WHERE usuario_id = ? ORDER BY nome", (self.usuario_id,)
		).fetchall()
		equipamentos = conexao.execute(
			"SELECT id, cliente_id, tipo, marca, modelo FROM equipamentos WHERE usuario_id = ? ORDER BY id",
			(self.usuario_id,),
		).fetchall()
		conexao.close()

		clientes_por_nome = {nome: id_cliente for id_cliente, nome in clientes}
		equipamentos_por_nome = {
			f"{tipo} — {marca} {modelo}": (id_equip, cliente_id)
			for id_equip, cliente_id, tipo, marca, modelo in equipamentos
		}

		def campo(x, y, largura, rotulo, icone, widget, altura=39):
			canvas.create_text(x, y, text=rotulo, anchor="w", fill="#2B3B4A",
						   font=("Georgia", 15))
			arredondado(x, y + 13, x + 42, y + 13 + altura, 9, fill="#E9ECEF", outline="")
			canvas.create_text(x + 21, y + 32, text=icone, fill="#122238",
						   font=("Segoe UI Symbol", 17, "bold"))
			arredondado(x + 45, y + 13, x + largura, y + 13 + altura, 10,
						   fill="#FFFFFF", outline="#6D6D6D", width=2)
			canvas.create_window(x + 57, y + 19, anchor="nw", window=widget,
							 width=largura - 70, height=altura - 12)

		canvas.create_text(46, 117, text="Cliente", anchor="w", fill="#111820",
						   font=("Helvetica", 25, "bold"))
		cliente = ttk.Combobox(janela, values=list(clientes_por_nome), state="readonly",
								font=("Helvetica", 12))
		campo(48, 144, 575, "Nome do Cliente", "♙", cliente)

		canvas.create_text(46, 243, text="Equipamento", anchor="w", fill="#111820",
						   font=("Helvetica", 25, "bold"))
		equipamento = ttk.Combobox(janela, state="readonly", font=("Helvetica", 12))
		campo(48, 270, 575, "Tipo de Equipamento", "▣", equipamento)

		def atualizar_equipamentos(_event=None):
			cliente_id = clientes_por_nome.get(cliente.get())
			opcoes = [nome for nome, (_id, dono_id) in equipamentos_por_nome.items()
					  if dono_id == cliente_id]
			equipamento.configure(values=opcoes)
			equipamento.set("")

		cliente.bind("<<ComboboxSelected>>", atualizar_equipamentos)

		canvas.create_text(46, 364, text="Problema ⚠", anchor="w", fill="#111820",
						   font=("Helvetica", 25, "bold"))
		canvas.create_text(52, 395, text="Descrição do Problema", anchor="w", fill="#2B3B4A",
						   font=("Georgia", 15))
		arredondado(48, 414, 623, 521, 12, fill="#FFFFFF", outline="#6D6D6D", width=2)
		problema = tk.Text(janela, font=("Helvetica", 12), wrap="word", bd=0,
						   highlightthickness=0, bg="#FFFFFF")
		canvas.create_window(59, 425, anchor="nw", window=problema, width=551, height=84)

		valor = tk.Entry(janela, font=("Helvetica", 12), bd=0, highlightthickness=0,
						 bg="#FFFFFF")
		data = tk.Entry(janela, font=("Helvetica", 12), bd=0, highlightthickness=0,
						bg="#FFFFFF")
		data.insert(0, date.today().isoformat())
		canvas.create_text(46, 562, text="Valor", anchor="w", fill="#111820",
						   font=("Helvetica", 25, "bold"))
		campo(48, 590, 288, "", "R$", valor)
		canvas.create_text(362, 562, text="Data de entrada", anchor="w", fill="#111820",
						   font=("Helvetica", 25, "bold"))
		campo(363, 590, 260, "", "▣", data)

		def salvar():
			try:
				cliente_id = clientes_por_nome[cliente.get()]
				equipamento_id, dono_id = equipamentos_por_nome[equipamento.get()]
				if cliente_id != dono_id:
					raise ValueError("O equipamento selecionado não pertence ao cliente.")
				cadastrar_os(
					cliente_id, equipamento_id, problema.get("1.0", "end-1c"),
					float(valor.get().replace("R$", "").replace(".", "").replace(",", ".") or 0),
					data.get(), self.usuario_id,
				)
				janela.destroy()
				self._preencher()
			except (KeyError, ValueError) as erro:
				messagebox.showerror("Dados inválidos", str(erro), parent=janela)

		arredondado(150, 670, 379, 717, 10, fill="#0C2749", outline="#496F95", width=2, tags="salvar")
		canvas.create_text(264, 693, text="+ CADASTRAR OS", fill="white",
						   font=("Georgia", 13, "bold"), tags="salvar")
		arredondado(396, 670, 550, 717, 10, fill="#FFFFFF", outline="#999999", width=2, tags="cancelar")
		canvas.create_text(473, 693, text="CANCELAR", fill="#24384D",
						   font=("Georgia", 13, "bold"), tags="cancelar")
		canvas.tag_bind("salvar", "<Button-1>", lambda _event: salvar())
		canvas.tag_bind("cancelar", "<Button-1>", lambda _event: janela.destroy())
		for tag in ("salvar", "cancelar"):
			canvas.tag_bind(tag, "<Enter>", lambda _event: canvas.config(cursor="hand2"))
			canvas.tag_bind(tag, "<Leave>", lambda _event: canvas.config(cursor=""))
