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
        """Monta a listagem sem deixar o formulário exposto na lateral."""
        canvas = self.canvas

        def arredondado(x1, y1, x2, y2, raio=12, **opcoes):
            pontos = [x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
                      x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
                      x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1]
            return canvas.create_polygon(pontos, smooth=True, **opcoes)

        # Ações superiores no mesmo padrão visual das outras telas.
        arredondado(285, 158, 500, 202, 10, fill="#536F99", outline="", tags="novo_equipamento")
        canvas.create_text(392, 180, text="+ NOVO EQUIPAMENTO", fill="white",
                           font=("Helvetica", 12, "bold"), tags="novo_equipamento")
        canvas.tag_bind("novo_equipamento", "<Button-1>",
                        lambda _event: self._abrir_formulario())
        canvas.tag_bind("novo_equipamento", "<Enter>", lambda _event: canvas.config(cursor="hand2"))
        canvas.tag_bind("novo_equipamento", "<Leave>", lambda _event: canvas.config(cursor=""))

        arredondado(855, 155, 1145, 198, 18, fill="white", outline="#707070", width=2)
        canvas.create_text(878, 176, text="⌕", fill="#52606D", font=("Segoe UI Symbol", 19, "bold"))
        self.busca = tk.StringVar()
        entrada = tk.Entry(canvas, textvariable=self.busca, font=("Helvetica", 11),
                           bd=0, highlightthickness=0, bg="white")
        canvas.create_window(902, 164, anchor="nw", window=entrada, width=224, height=25)
        entrada.bind("<KeyRelease>", lambda _event: self._preencher())

        # Moldura e cabeçalho da tabela, desenhados no Canvas para permitir
        # os mesmos ícones clicáveis usados na tela de Clientes.
        arredondado(285, 225, 1145, 680, 12, fill="#FFFFFF", outline="#C8CDD3", width=2)
        arredondado(285, 225, 1145, 272, 12, fill="#071D3A", outline="")
        canvas.create_rectangle(285, 250, 1145, 272, fill="#071D3A", outline="")
        self.limites_colunas = (285, 355, 510, 620, 730, 865, 980, 1145)
        self.centros_colunas = (320, 432, 565, 675, 797, 922)
        for x in self.limites_colunas[1:-1]:
            canvas.create_line(x, 225, x, 680, fill="#CBD1D7")
        for x, titulo in zip(self.centros_colunas, ("ID", "CLIENTE", "TIPO", "MARCA", "MODELO", "Nº SÉRIE")):
            canvas.create_text(x, 249, text=titulo, fill="white", font=("Helvetica", 12, "bold"))
        canvas.create_text(1062, 249, text="AÇÕES", fill="white", font=("Helvetica", 12, "bold"))
        self.itens_linhas = []
        self._preencher()

    def _preencher(self):
        termo = self.busca.get().strip().lower()
        for item in self.itens_linhas:
            self.canvas.delete(item)
        self.itens_linhas = []

        equipamentos = []
        for equipamento in listar_equipamentos(self.usuario_id):
            if termo and not any(termo in str(valor).lower() for valor in equipamento):
                continue
            equipamentos.append(equipamento)

        for indice in range(7):
            y1 = 272 + indice * 52
            cor = "#FFFFFF" if indice % 2 == 0 else "#F3F5F7"
            self.itens_linhas.append(self.canvas.create_rectangle(
                286, y1, 1144, y1 + 52, fill=cor, outline="#D4D9DE"
            ))
        for x in self.limites_colunas[1:-1]:
            self.itens_linhas.append(self.canvas.create_line(x, 272, x, 636, fill="#D4D9DE"))

        icone_editar = self._carregar_icone("icone_editar_cliente.png", (25, 25), "#2370C2")
        icone_excluir = self._carregar_icone("icone_excluir_cliente.png", (23, 23), "#E43D3D")
        for indice, equipamento in enumerate(equipamentos[:7]):
            y = 298 + indice * 52
            dados = (
                (320, f"EQ{equipamento[0]:03d}", 10),
                (432, equipamento[2], 18),
                (565, equipamento[3], 13),
                (675, equipamento[4], 13),
                (797, equipamento[5], 14),
                (922, equipamento[6], 13),
            )
            for x, valor, limite in dados:
                texto = str(valor)
                if len(texto) > limite:
                    texto = texto[:limite - 3] + "..."
                self.itens_linhas.append(self.canvas.create_text(
                    x, y, text=texto, fill="#202A34", font=("Helvetica", 11), anchor="center"
                ))
            tag_editar = f"editar_equipamento_{equipamento[0]}"
            tag_excluir = f"excluir_equipamento_{equipamento[0]}"
            self.itens_linhas.append(self.canvas.create_image(1063, y, image=icone_editar, tags=tag_editar))
            self.itens_linhas.append(self.canvas.create_image(1108, y, image=icone_excluir, tags=tag_excluir))
            self.canvas.tag_bind(tag_editar, "<Button-1>",
                                 lambda _event, item=equipamento: self._abrir_formulario(item))
            self.canvas.tag_bind(tag_excluir, "<Button-1>",
                                 lambda _event, item=equipamento: self._excluir_equipamento(item))
            for tag in (tag_editar, tag_excluir):
                self.canvas.tag_bind(tag, "<Enter>", lambda _event: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda _event: self.canvas.config(cursor=""))

    def _excluir_equipamento(self, equipamento):
        if not messagebox.askyesno("Excluir equipamento", "Deseja excluir este equipamento?", parent=self):
            return
        try:
            excluir_equipamento(equipamento[0], self.usuario_id)
            self._preencher()
        except ValueError as erro:
            messagebox.showerror("Não foi possível excluir", str(erro), parent=self)

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
        janela.geometry("620x650")
        janela.resizable(False, False)
        janela.configure(bg="#F5F7F9")
        janela.transient(self.winfo_toplevel())
        janela.grab_set()

        canvas = tk.Canvas(janela, width=620, height=650, bg="#F5F7F9", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        def arredondado(x1, y1, x2, y2, raio=12, **opcoes):
            pontos = [x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
                      x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
                      x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1]
            return canvas.create_polygon(pontos, smooth=True, **opcoes)

        titulo = "EDITAR EQUIPAMENTO" if equipamento else "NOVO EQUIPAMENTO"
        arredondado(16, 10, 604, 640, 28, fill="#FEFEFE", outline="#3D6E91", width=3)
        canvas.create_text(43, 50, text=titulo, anchor="w", fill="#102037",
                           font=("Georgia", 25, "bold"))
        canvas.create_line(43, 80, 575, 80, fill="#D9DDE0")
        canvas.create_text(578, 41, text="×", fill="#102037", font=("Helvetica", 29), tags="fechar")
        canvas.tag_bind("fechar", "<Button-1>", lambda _event: janela.destroy())
        canvas.tag_bind("fechar", "<Enter>", lambda _event: canvas.config(cursor="hand2"))
        canvas.tag_bind("fechar", "<Leave>", lambda _event: canvas.config(cursor=""))

        clientes = self._clientes()

        def campo(rotulo, x, y, largura, widget, icone=None):
            canvas.create_text(x, y, text=rotulo, fill="#283A4B", anchor="w",
                               font=("Georgia", 14))
            if icone:
                arredondado(x, y + 12, x + 38, y + 52, 9, fill="#E9ECEF", outline="")
                canvas.create_text(x + 19, y + 32, text=icone, fill="#102037",
                                   font=("Segoe UI Symbol", 15, "bold"))
                inicio = x + 43
            else:
                inicio = x
            arredondado(inicio, y + 12, x + largura, y + 52, 9, fill="white", outline="#68737E", width=2)
            canvas.create_window(inicio + 10, y + 19, anchor="nw", window=widget,
                                 width=x + largura - inicio - 20, height=25)

        canvas.create_text(43, 113, text="Vincule o equipamento ao cliente", anchor="w",
                           fill="#111A24", font=("Helvetica", 20, "bold"))
        cliente = ttk.Combobox(janela, values=list(clientes), state="readonly", font=("Helvetica", 11))
        campo("Cliente", 45, 140, 530, cliente, "♙")

        canvas.create_text(43, 236, text="Dados do equipamento", anchor="w",
                           fill="#111A24", font=("Helvetica", 20, "bold"))
        campos = {}
        for nome, rotulo, x, y, largura in (
            ("tipo", "Tipo", 45, 265, 250),
            ("marca", "Marca", 325, 265, 250),
            ("modelo", "Modelo", 45, 340, 250),
            ("serie", "Nº de série", 325, 340, 250),
        ):
            campos[nome] = tk.Entry(janela, font=("Helvetica", 11), bd=0,
                                    highlightthickness=0, bg="white")
            campo(rotulo, x, y, largura, campos[nome])

        canvas.create_text(45, 422, text="Descrição", fill="#283A4B", anchor="w",
                           font=("Georgia", 14))
        arredondado(45, 434, 575, 522, 10, fill="white", outline="#68737E", width=2)
        descricao = tk.Text(janela, font=("Helvetica", 11), bd=0, highlightthickness=0,
                            bg="white", wrap="word")
        canvas.create_window(57, 445, anchor="nw", window=descricao, width=506, height=66)

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

        arredondado(180, 560, 380, 607, 10, fill="#0C2749", outline="#496F95", width=2, tags="salvar")
        canvas.create_text(280, 583, text="SALVAR EQUIPAMENTO", fill="white",
                           font=("Georgia", 12, "bold"), tags="salvar")
        arredondado(399, 560, 540, 607, 10, fill="#FFFFFF", outline="#999999", width=2, tags="cancelar")
        canvas.create_text(469, 583, text="CANCELAR", fill="#24384D",
                           font=("Georgia", 12, "bold"), tags="cancelar")
        canvas.tag_bind("salvar", "<Button-1>", lambda _event: salvar())
        canvas.tag_bind("cancelar", "<Button-1>", lambda _event: janela.destroy())
        for tag in ("salvar", "cancelar"):
            canvas.tag_bind(tag, "<Enter>", lambda _event: canvas.config(cursor="hand2"))
            canvas.tag_bind(tag, "<Leave>", lambda _event: canvas.config(cursor=""))

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
