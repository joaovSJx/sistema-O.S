import tkinter as tk
from tkinter import font as tkfont
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
        # Controles e tabela desenhados no Canvas para reproduzir o modelo.
        self._retangulo_arredondado(365, 140, 520, 180, 10, fill="white", outline="#4A76A7", width=2, tags="novo")
        self.canvas.create_text(442, 160, text="+ NOVO CLIENTE", fill="#2E68A7",
                                font=("Georgia", 11, "bold"), tags="novo")
        self.canvas.tag_bind("novo", "<Button-1>", lambda _event: self._abrir_formulario())
        self.canvas.tag_bind("novo", "<Enter>", lambda _event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("novo", "<Leave>", lambda _event: self.canvas.config(cursor=""))

        self._retangulo_arredondado(850, 140, 1130, 180, 20, fill="white", outline="#303030", width=2)
        self.canvas.create_text(870, 160, text="⌕", fill="#303030", font=("Segoe UI Symbol", 19, "bold"))
        self.texto_busca = "Buscar nome, CPF ou e-mail..."
        self.busca = tk.StringVar(value=self.texto_busca)
        entrada = tk.Entry(self.canvas, textvariable=self.busca, font=("Helvetica", 11),
                            fg="#777777", bg="white", bd=0, highlightthickness=0)
        entrada.bind("<KeyRelease>", lambda _event: self._preencher())
        entrada.bind("<FocusIn>", self._limpar_busca)
        entrada.bind("<FocusOut>", self._restaurar_busca)
        self.canvas.create_window(892, 147, anchor="nw", window=entrada, width=220, height=26)

        self._montar_tabela_canvas()
        self._preencher()

    def _preencher(self):
        termo = self.busca.get().strip().lower()
        if termo == self.texto_busca.lower():
            termo = ""
        self.clientes_exibidos = [
            cliente for cliente in listar_clientes(self.usuario_id)
            if not termo or any(termo in str(valor).lower() for valor in cliente)
        ]
        for item in self.itens_linhas:
            self.canvas.delete(item)
        self.itens_linhas = []

        for indice in range(10):
            y1 = 250 + indice * 35
            cor = "#FFFFFF" if indice % 2 == 0 else "#E3E3E3"
            self.itens_linhas.append(self.canvas.create_rectangle(320, y1, 1139, y1 + 35, fill=cor, outline="#BBBBBB"))

        for x in (385, 565, 734, 905, 1061):
            self.itens_linhas.append(self.canvas.create_line(x, 250, x, 600, fill="#A9A9A9"))

        icone_editar = self._carregar_icone(
            "icone_editar_cliente.png", (22, 22), "#2370C2"
        )
        icone_excluir = self._carregar_icone(
            "icone_excluir_cliente.png", (20, 20), "#E43D3D"
        )
        for indice, cliente in enumerate(self.clientes_exibidos[:9]):
            y = 267 + indice * 35
            id_cliente, nome, cpf, telefone, email, endereco = cliente
            dados = [
                (352, f"{id_cliente:03d}", 58),
                (475, nome, 165),
                (650, cpf, 150),
                (820, telefone, 150),
                (983, email, 145),
            ]
            for x, texto, largura in dados:
                self.itens_linhas.append(self.canvas.create_text(
                    x, y, text=self._texto_da_coluna(texto, largura),
                    fill="#202020", font=("Georgia", 10), anchor="center"
                ))
            tag_editar = f"editar_{id_cliente}"
            tag_excluir = f"excluir_{id_cliente}"
            self.itens_linhas.append(self.canvas.create_image(
                1088, y, image=icone_editar, tags=tag_editar
            ))
            self.itens_linhas.append(self.canvas.create_image(
                1115, y, image=icone_excluir, tags=tag_excluir
            ))
            self.canvas.tag_bind(tag_editar, "<Button-1>", lambda _event, c=cliente: self._abrir_formulario(c))
            self.canvas.tag_bind(tag_excluir, "<Button-1>", lambda _event, c=cliente: self._excluir_cliente(c))

    def _montar_tabela_canvas(self):
        self._retangulo_arredondado(315, 197, 1145, 610, 13, fill="#183452", outline="")
        self._retangulo_arredondado(321, 203, 1139, 604, 9, fill="white", outline="")
        self._retangulo_arredondado(321, 203, 1139, 250, 9, fill="#183452", outline="")
        limites = (320, 385, 565, 734, 905, 1061, 1139)
        for x in limites[1:-1]:
            self.canvas.create_line(x, 203, x, 600, fill="#9FA6AF")
        cabecalhos = ((352, "ID"), (475, "NOME"), (650, "CPF"), (820, "TELEFONE"), (983, "E-MAIL"))
        for x, texto in cabecalhos:
            self.canvas.create_text(x, 231, text=texto, fill="white", font=("Georgia", 13, "bold"))
        self.itens_linhas = []

    def _texto_da_coluna(self, texto, largura):
        """Encurta textos grandes para que nunca atravessem a coluna."""
        fonte = tkfont.Font(family="Georgia", size=10)
        texto = str(texto)
        if fonte.measure(texto) <= largura:
            return texto
        while texto and fonte.measure(texto + "...") > largura:
            texto = texto[:-1]
        return texto + "..."

    def _retangulo_arredondado(self, x1, y1, x2, y2, raio, **opcoes):
        pontos = [x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
                  x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
                  x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1]
        return self.canvas.create_polygon(pontos, smooth=True, **opcoes)

    def _excluir_cliente(self, cliente):
        if messagebox.askyesno("Excluir cliente", "Deseja excluir este cliente?", parent=self):
            try:
                excluir_cliente(cliente[0], usuario_id=self.usuario_id)
                self._preencher()
            except ValueError as erro:
                messagebox.showerror("Não foi possível excluir", str(erro), parent=self)

    def _limpar_busca(self, _event=None):
        if self.busca.get() == self.texto_busca:
            self.busca.set("")

    def _restaurar_busca(self, _event=None):
        if not self.busca.get().strip():
            self.busca.set(self.texto_busca)
            self._preencher()

    def _selecionado(self):
        selecao = self.tabela.selection()
        return int(selecao[0]) if selecao else None

    def _abrir_formulario(self, cliente=None):
        janela = tk.Toplevel(self)
        janela.title("Editar Cliente" if cliente else "Novo Cliente")
        janela.geometry("570x450")
        janela.resizable(False, False)
        janela.transient(self.winfo_toplevel())
        janela.grab_set()
        fundo_modal = tk.Canvas(
            janela, width=570, height=450, highlightthickness=0, bg="#F6F7F9"
        )
        fundo_modal.pack(fill="both", expand=True)

        def retangulo_arredondado(x1, y1, x2, y2, raio, **opcoes):
            pontos = [
                x1 + raio, y1, x2 - raio, y1, x2, y1, x2, y1 + raio,
                x2, y2 - raio, x2, y2, x2 - raio, y2, x1 + raio, y2,
                x1, y2, x1, y2 - raio, x1, y1 + raio, x1, y1,
            ]
            return fundo_modal.create_polygon(pontos, smooth=True, **opcoes)

        # O modal inteiro é composto no Canvas; somente as entradas são widgets.
        retangulo_arredondado(12, 12, 558, 438, 18, fill="#244E80", outline="")
        retangulo_arredondado(16, 16, 554, 434, 15, fill="white", outline="")
        fundo_modal.create_text(
            45, 55, text="Editar Cliente" if cliente else "Novo Cliente",
            fill="#142A47", font=("Georgia", 19, "bold"), anchor="w"
        )

        def criar_campo(rotulo, x, y, largura):
            fundo_modal.create_text(
                x, y, text=rotulo, fill="#5F6368", font=("Helvetica", 11), anchor="w"
            )
            retangulo_arredondado(
                x, y + 12, x + largura, y + 52, 9,
                fill="white", outline="#C7CDD5", width=2
            )
            campo = tk.Entry(
                fundo_modal, font=("Helvetica", 12), bd=0,
                highlightthickness=0, bg="white"
            )
            fundo_modal.create_window(
                x + 12, y + 21, anchor="nw", window=campo,
                width=largura - 24, height=24
            )
            return campo

        campos = {}
        campos["nome"] = criar_campo("Nome", 45, 95, 220)
        campos["cpf"] = criar_campo("CPF", 300, 95, 220)
        campos["telefone"] = criar_campo("Telefone", 45, 177, 220)
        campos["email"] = criar_campo("E-mail", 300, 177, 220)

        fundo_modal.create_text(
            45, 259, text="Endereço", fill="#5F6368",
            font=("Helvetica", 11), anchor="w"
        )
        retangulo_arredondado(45, 271, 520, 337, 9, fill="white", outline="#C7CDD5", width=2)
        endereco = tk.Text(
            fundo_modal, font=("Helvetica", 12), bd=0, highlightthickness=0, bg="white"
        )
        fundo_modal.create_window(57, 281, anchor="nw", window=endereco, width=451, height=45)

        if cliente:
            valores = dict(zip(("id", "nome", "cpf", "telefone", "email", "endereco"), cliente))
            for nome, campo in campos.items():
                campo.insert(0, valores[nome])
            endereco.insert("1.0", valores["endereco"])

        def salvar():
            try:
                dados = (
                    campos["nome"].get().strip(),
                    campos["cpf"].get().strip(),
                    campos["telefone"].get().strip(),
                    campos["email"].get().strip(),
                    endereco.get("1.0", "end").strip(),
                )
                if cliente:
                    atualizar_cliente(cliente[0], *dados, usuario_id=self.usuario_id)
                else:
                    cadastrar_cliente(*dados, usuario_id=self.usuario_id)
                janela.destroy()
                self._preencher()
            except Exception as erro:
                messagebox.showerror("Dados inválidos", str(erro), parent=janela)

        retangulo_arredondado(45, 365, 177, 407, 9, fill="#2C6DB4", outline="", tags="salvar")
        fundo_modal.create_text(
            111, 386, text="Salvar", fill="white", font=("Helvetica", 12, "bold"), tags="salvar"
        )
        retangulo_arredondado(192, 365, 324, 407, 9, fill="#E4E7EB", outline="#A9B0B8", width=1, tags="cancelar")
        fundo_modal.create_text(
            258, 386, text="Cancelar", fill="#555B63", font=("Helvetica", 12), tags="cancelar"
        )
        fundo_modal.tag_bind("salvar", "<Button-1>", lambda _event: salvar())
        fundo_modal.tag_bind("cancelar", "<Button-1>", lambda _event: janela.destroy())
        fundo_modal.tag_bind("salvar", "<Enter>", lambda _event: fundo_modal.config(cursor="hand2"))
        fundo_modal.tag_bind("salvar", "<Leave>", lambda _event: fundo_modal.config(cursor=""))
        fundo_modal.tag_bind("cancelar", "<Enter>", lambda _event: fundo_modal.config(cursor="hand2"))
        fundo_modal.tag_bind("cancelar", "<Leave>", lambda _event: fundo_modal.config(cursor=""))

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
