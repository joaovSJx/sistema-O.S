import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk

from database.clientes import cadastrar_cliente, listar_clientes, atualizar_cliente, excluir_cliente
from interface.layout import TelaSistema, estilo_tabela


class ClientesFrame(TelaSistema):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Clientes", "clientes")
        self.usuario_id = app.usuario_atual[0] if app.usuario_atual else None
        self._montar_conteudo()

    def _montar_conteudo(self):
        estilo_tabela()
        area = self.area_conteudo(x=315, y=155, largura=880, altura=555)
        topo = ttk.Frame(area)
        topo.pack(fill="x", pady=(0, 16))
        ttk.Button(topo, text="+ NOVO CLIENTE", bootstyle="outline-primary",
                   command=self._abrir_formulario).pack(side="left")
        self.busca = tk.StringVar()
        entrada = ttk.Entry(topo, textvariable=self.busca, width=31)
        entrada.pack(side="right", ipady=5)
        ttk.Label(topo, text="⌕", font=("Segoe UI Symbol", 16)).pack(side="right", padx=(0, 5))
        entrada.bind("<KeyRelease>", lambda _event: self._preencher())

        moldura = ttk.Frame(area, padding=10, bootstyle="light")
        moldura.pack(fill="both", expand=True)
        colunas = ("id", "nome", "cpf", "telefone", "email", "acoes")
        self.tabela = ttk.Treeview(moldura, columns=colunas, show="headings",
                                   style="Tabela.Treeview", selectmode="browse")
        cabecalhos = {"id": "ID", "nome": "NOME", "cpf": "CPF", "telefone": "TELEFONE",
                      "email": "E-MAIL", "acoes": "AÇÕES"}
        larguras = {"id": 55, "nome": 165, "cpf": 135, "telefone": 135,
                    "email": 220, "acoes": 90}
        for coluna in colunas:
            self.tabela.heading(coluna, text=cabecalhos[coluna])
            self.tabela.column(coluna, width=larguras[coluna], anchor="center" if coluna != "nome" else "w")
        self.tabela.pack(side="left", fill="both", expand=True)
        barra = ttk.Scrollbar(moldura, orient="vertical", command=self.tabela.yview)
        barra.pack(side="right", fill="y")
        self.tabela.configure(yscrollcommand=barra.set)
        self.tabela.bind("<Double-1>", self._editar_selecionado)
        self.tabela.bind("<Button-1>", self._clicar_acao)
        self._preencher()

    def _preencher(self):
        termo = self.busca.get().strip().lower()
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for cliente in listar_clientes(self.usuario_id):
            if termo and not any(termo in str(valor).lower() for valor in cliente):
                continue
            self.tabela.insert("", "end", iid=str(cliente[0]),
                               values=(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], "✎  🗑"))

    def _selecionado(self):
        selecao = self.tabela.selection()
        return int(selecao[0]) if selecao else None

    def _abrir_formulario(self, cliente=None):
        janela = tk.Toplevel(self)
        janela.title("Editar Cliente" if cliente else "Novo Cliente")
        janela.geometry("450x420")
        janela.transient(self.winfo_toplevel())
        janela.grab_set()
        conteudo = ttk.Frame(janela, padding=24)
        conteudo.pack(fill="both", expand=True)
        ttk.Label(conteudo, text="Editar Cliente" if cliente else "Novo Cliente",
                  font=("Helvetica", 18, "bold")).pack(anchor="w", pady=(0, 18))
        campos = {}
        for nome, rotulo in (("nome", "Nome"), ("cpf", "CPF"), ("telefone", "Telefone"),
                             ("email", "E-mail"), ("endereco", "Endereço")):
            ttk.Label(conteudo, text=rotulo).pack(anchor="w")
            campos[nome] = ttk.Entry(conteudo)
            campos[nome].pack(fill="x", pady=(2, 9))
        if cliente:
            valores = dict(zip(("id", "nome", "cpf", "telefone", "email", "endereco"), cliente))
            for nome, campo in campos.items():
                campo.insert(0, valores[nome])

        def salvar():
            try:
                dados = tuple(campos[nome].get().strip() for nome in campos)
                if cliente:
                    atualizar_cliente(cliente[0], *dados, usuario_id=self.usuario_id)
                else:
                    cadastrar_cliente(*dados, usuario_id=self.usuario_id)
                janela.destroy()
                self._preencher()
            except Exception as erro:
                messagebox.showerror("Dados inválidos", str(erro), parent=janela)

        ttk.Button(conteudo, text="Salvar", bootstyle="primary", command=salvar).pack(side="left", pady=8)
        ttk.Button(conteudo, text="Cancelar", bootstyle="secondary", command=janela.destroy).pack(side="left", padx=8, pady=8)

    def _editar_selecionado(self, _event=None):
        cliente_id = self._selecionado()
        if cliente_id is None:
            return
        cliente = next((item for item in listar_clientes(self.usuario_id) if item[0] == cliente_id), None)
        if cliente:
            self._abrir_formulario(cliente)

    def _clicar_acao(self, evento):
        coluna = self.tabela.identify_column(evento.x)
        item = self.tabela.identify_row(evento.y)
        if not item or coluna != "#6":
            return
        self.tabela.selection_set(item)
        cliente_id = int(item)
        cliente = next((registro for registro in listar_clientes(self.usuario_id) if registro[0] == cliente_id), None)
        if not cliente:
            return
        if evento.x - self.tabela.bbox(item, coluna)[0] < 42:
            self._abrir_formulario(cliente)
            return
        if messagebox.askyesno("Excluir cliente", "Deseja excluir este cliente?", parent=self):
            try:
                excluir_cliente(cliente_id, usuario_id=self.usuario_id)
                self._preencher()
            except ValueError as erro:
                messagebox.showerror("Não foi possível excluir", str(erro), parent=self)