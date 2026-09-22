import tkinter as tk
from tkinter import messagebox
from datetime import date

import ttkbootstrap as ttk

from database.connection import conectar
from database.ordens_servico import cadastrar_os, consultar_os
from interface.layout import TelaSistema, estilo_tabela


class OrdensFrame(TelaSistema):
	def __init__(self, parent, app):
		super().__init__(parent, app, "Ordens de Serviço", "ordens")
		self.ordens = []
		self.usuario_id = app.usuario_atual[0] if app.usuario_atual else None
		self._montar_conteudo()

	def _montar_conteudo(self):
		estilo_tabela()
		area = self.area_conteudo(x=305, y=155, largura=890, altura=555)
		topo = ttk.Frame(area)
		topo.pack(fill="x", pady=(0, 13))
		ttk.Button(topo, text="+ NOVA O.S", bootstyle="primary", command=self._abrir_formulario).pack(side="left")
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

	def _preencher(self):
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

	def _abrir_formulario(self):
		janela = tk.Toplevel(self)
		janela.title("Nova Ordem de Serviço")
		janela.geometry("520x510")
		janela.transient(self.winfo_toplevel())
		janela.grab_set()
		conteudo = ttk.Frame(janela, padding=24)
		conteudo.pack(fill="both", expand=True)
		ttk.Label(conteudo, text="Nova Ordem de Serviço", font=("Helvetica", 18, "bold")).pack(anchor="w", pady=(0, 16))

		conexao = conectar()
		clientes = conexao.execute("SELECT id, nome FROM clientes WHERE usuario_id = ? ORDER BY nome", (self.usuario_id,)).fetchall()
		equipamentos = conexao.execute("SELECT id, cliente_id, tipo, marca, modelo FROM equipamentos WHERE usuario_id = ? ORDER BY id", (self.usuario_id,)).fetchall()
		conexao.close()
		clientes_por_nome = {f"{id_cliente} - {nome}": id_cliente for id_cliente, nome in clientes}
		ttk.Label(conteudo, text="Cliente").pack(anchor="w")
		cliente = ttk.Combobox(conteudo, values=list(clientes_por_nome), state="readonly")
		cliente.pack(fill="x", pady=(2, 10))
		equipamentos_por_nome = {f"{id_equip} - {tipo} {marca} {modelo}": (id_equip, cliente_id)
								 for id_equip, cliente_id, tipo, marca, modelo in equipamentos}
		ttk.Label(conteudo, text="Equipamento").pack(anchor="w")
		equipamento = ttk.Combobox(conteudo, values=list(equipamentos_por_nome), state="readonly")
		equipamento.pack(fill="x", pady=(2, 10))
		ttk.Label(conteudo, text="Problema").pack(anchor="w")
		problema = ttk.Entry(conteudo)
		problema.pack(fill="x", pady=(2, 10))
		ttk.Label(conteudo, text="Valor").pack(anchor="w")
		valor = ttk.Entry(conteudo)
		valor.pack(fill="x", pady=(2, 10))
		ttk.Label(conteudo, text="Data de entrada (AAAA-MM-DD)").pack(anchor="w")
		data = ttk.Entry(conteudo)
		data.insert(0, date.today().isoformat())
		data.pack(fill="x", pady=(2, 15))

		def salvar():
			try:
				cliente_id = clientes_por_nome[cliente.get()]
				equipamento_id, dono_id = equipamentos_por_nome[equipamento.get()]
				if cliente_id != dono_id:
					raise ValueError("O equipamento selecionado não pertence ao cliente.")
				cadastrar_os(cliente_id, equipamento_id, problema.get(), float(valor.get().replace(",", ".") or 0), data.get(), self.usuario_id)
				janela.destroy()
				self._preencher()
			except (KeyError, ValueError) as erro:
				messagebox.showerror("Dados inválidos", str(erro), parent=janela)

		ttk.Button(conteudo, text="Salvar", bootstyle="primary", command=salvar).pack(side="left")
		ttk.Button(conteudo, text="Cancelar", bootstyle="secondary", command=janela.destroy).pack(side="left", padx=8)
