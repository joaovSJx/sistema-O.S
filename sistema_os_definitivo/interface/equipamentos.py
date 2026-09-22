import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk

from database.connection import conectar
from database.ordens_servico import (
    atualizar_equipamento,
    cadastrar_equipamento,
    excluir_equipamento,
    listar_equipamentos,
)
from interface.layout import TelaSistema, estilo_tabela


class EquipamentosFrame(TelaSistema):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Equipamentos", "equipamentos")
        self.usuario_id = app.usuario_atual[0] if app.usuario_atual else None
        self._montar_conteudo()

    def _montar_conteudo(self):
        estilo_tabela()
        area = self.area_conteudo(x=315, y=155, largura=880, altura=555)
        topo = ttk.Frame(area)
        topo.pack(fill="x", pady=(0, 14))
        ttk.Button(topo, text="+ NOVO EQUIPAMENTO", bootstyle="outline-primary",
                   command=self._abrir_formulario).pack(side="left")
        self.busca = tk.StringVar()
        entrada = ttk.Entry(topo, textvariable=self.busca, width=31)
        entrada.pack(side="right", ipady=5)
        ttk.Label(topo, text="⌕", font=("Segoe UI Symbol", 16)).pack(side="right", padx=5)
        entrada.bind("<KeyRelease>", lambda _event: self._preencher())

        moldura = ttk.Frame(area, padding=10, bootstyle="light")
        moldura.pack(fill="both", expand=True)
        colunas = ("id", "cliente", "tipo", "marca", "modelo", "serie", "acoes")
        self.tabela = ttk.Treeview(moldura, columns=colunas, show="headings",
                                   style="Tabela.Treeview", selectmode="browse")
        titulos = {"id": "ID", "cliente": "CLIENTE", "tipo": "TIPO", "marca": "MARCA",
                   "modelo": "MODELO", "serie": "Nº SÉRIE", "acoes": "AÇÕES"}
        larguras = {"id": 60, "cliente": 155, "tipo": 105, "marca": 105,
                    "modelo": 125, "serie": 110, "acoes": 85}
        for coluna in colunas:
            self.tabela.heading(coluna, text=titulos[coluna])
            self.tabela.column(coluna, width=larguras[coluna], anchor="center")
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
        for equipamento in listar_equipamentos(self.usuario_id):
            if termo and not any(termo in str(valor).lower() for valor in equipamento):
                continue
            self.tabela.insert(
                "", "end", iid=str(equipamento[0]),
                values=(equipamento[0], equipamento[2], equipamento[3], equipamento[4],
                        equipamento[5], equipamento[6], "✎  🗑"),
            )

    def _clientes(self):
        conexao = conectar()
        clientes = conexao.execute(
            "SELECT id, nome FROM clientes WHERE usuario_id = ? ORDER BY nome",
            (self.usuario_id,),
        ).fetchall()
        conexao.close()
        return {f"{cliente_id} - {nome}": cliente_id for cliente_id, nome in clientes}

    def _abrir_formulario(self, equipamento=None):
        janela = tk.Toplevel(self)
        janela.title("Editar Equipamento" if equipamento else "Novo Equipamento")
        janela.geometry("470x520")
        janela.transient(self.winfo_toplevel())
        janela.grab_set()
        conteudo = ttk.Frame(janela, padding=22)
        conteudo.pack(fill="both", expand=True)
        ttk.Label(conteudo, text="Editar Equipamento" if equipamento else "Novo Equipamento",
                  font=("Helvetica", 18, "bold")).pack(anchor="w", pady=(0, 15))

        clientes = self._clientes()
        ttk.Label(conteudo, text="Cliente").pack(anchor="w")
        cliente = ttk.Combobox(conteudo, values=list(clientes), state="readonly")
        cliente.pack(fill="x", pady=(2, 9))
        campos = {}
        for nome, rotulo in (("tipo", "Tipo"), ("marca", "Marca"), ("modelo", "Modelo"),
                             ("serie", "Nº de série")):
            ttk.Label(conteudo, text=rotulo).pack(anchor="w")
            campos[nome] = ttk.Entry(conteudo)
            campos[nome].pack(fill="x", pady=(2, 8))
        ttk.Label(conteudo, text="Descrição").pack(anchor="w")
        descricao = tk.Text(conteudo, height=4, relief="solid", borderwidth=1)
        descricao.pack(fill="x", pady=(2, 14))

        if equipamento:
            cliente.set(next((nome for nome, id_cliente in clientes.items()
                              if id_cliente == equipamento[1]), ""))
            for nome, valor in (("tipo", equipamento[3]), ("marca", equipamento[4]),
                                ("modelo", equipamento[5]), ("serie", equipamento[6])):
                campos[nome].insert(0, valor)
            descricao.insert("1.0", equipamento[7])

        def salvar():
            try:
                cliente_id = clientes[cliente.get()]
                valores = {nome: campo.get().strip() for nome, campo in campos.items()}
                texto_descricao = descricao.get("1.0", "end").strip()
                if equipamento:
                    atualizar_equipamento(equipamento[0], cliente_id, valores["tipo"],
                                          valores["marca"], valores["modelo"], valores["serie"],
                                          texto_descricao, self.usuario_id)
                else:
                    cadastrar_equipamento(cliente_id, valores["tipo"], valores["marca"],
                                          valores["modelo"], valores["serie"], texto_descricao,
                                          self.usuario_id)
                janela.destroy()
                self._preencher()
            except (KeyError, ValueError) as erro:
                messagebox.showerror("Dados inválidos", str(erro), parent=janela)

        ttk.Button(conteudo, text="Salvar", bootstyle="primary", command=salvar).pack(side="left")
        ttk.Button(conteudo, text="Cancelar", bootstyle="secondary",
                   command=janela.destroy).pack(side="left", padx=8)

    def _equipamento_selecionado(self):
        selecao = self.tabela.selection()
        if not selecao:
            return None
        equipamento_id = int(selecao[0])
        return next((item for item in listar_equipamentos(self.usuario_id)
                     if item[0] == equipamento_id), None)

    def _editar_selecionado(self, _event=None):
        equipamento = self._equipamento_selecionado()
        if equipamento:
            self._abrir_formulario(equipamento)

    def _clicar_acao(self, evento):
        coluna = self.tabela.identify_column(evento.x)
        item = self.tabela.identify_row(evento.y)
        if not item or coluna != "#7":
            return
        self.tabela.selection_set(item)
        equipamento = self._equipamento_selecionado()
        if not equipamento:
            return
        inicio = self.tabela.bbox(item, coluna)[0]
        if evento.x - inicio < 42:
            self._abrir_formulario(equipamento)
        elif messagebox.askyesno("Excluir equipamento", "Deseja excluir este equipamento?", parent=self):
            try:
                excluir_equipamento(equipamento[0], self.usuario_id)
                self._preencher()
            except ValueError as erro:
                messagebox.showerror("Não foi possível excluir", str(erro), parent=self)