import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, YES


class App(ttk.Window):
    """Janela única do sistema. As telas (login, cadastro) são apenas
    frames trocados dentro desta mesma janela, evitando problemas de
    se criar mais de uma janela raiz (Tk) na mesma aplicação."""

    def __init__(self):
        super().__init__(title="Sistema OS", themename="flatly")
        self.usuario_atual = None
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES)
        self.mostrar_inicial()

    def _limpar_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_inicial(self):
        self.usuario_atual = None
        self._limpar_container()
        self.title("Sistema de Ordem de Serviço")
        self.geometry("1200x720")
        self.minsize(1200, 720)
        self.resizable(True, True)
        self.place_window_center()

        from interface.inicial import InicialFrame
        InicialFrame(self.container, self).pack(fill=BOTH, expand=YES)


    def mostrar_dashboard(self):
        self._limpar_container()
        self.title("Sistema de Ordem de Serviço - Painel")
        self.geometry("1200x720")
        self.minsize(1200, 720)
        self.resizable(True, True)
        self.place_window_center()

        from interface.dashboard import DashboardFrame
        DashboardFrame(self.container, self).pack(fill=BOTH, expand=YES)


    def mostrar_login(self):
        self._limpar_container()
        self.title("Sistema OS - Login")
        self.geometry("520x620")
        self.minsize(520, 620)
        self.resizable(True, True)
        self.place_window_center()

        from interface.login import LoginFrame
        LoginFrame(self.container, self).pack(fill=BOTH, expand=YES)

    def mostrar_cadastro(self):
        self._limpar_container()
        self.title("Sistema OS - Cadastrar Cliente")
        self.minsize(520, 720)
        self.resizable(True, True)
        self.geometry("520x720")
        self.place_window_center()

        from interface.cadastro import CadastroFrame
        CadastroFrame(self.container, self).pack(fill=BOTH, expand=YES)

    def mostrar_clientes(self):
        self._limpar_container()
        self.title("Sistema OS - Clientes")
        self.geometry("1200x720")
        self.minsize(1200, 720)
        self.resizable(True, True)
        self.place_window_center()
        from interface.clientes import ClientesFrame
        ClientesFrame(self.container, self).pack(fill=BOTH, expand=YES)

    def mostrar_equipamentos(self):
        self._limpar_container()
        self.title("Sistema OS - Equipamentos")
        self.geometry("1200x720")
        self.minsize(1200, 720)
        self.resizable(True, True)
        self.place_window_center()
        from interface.equipamentos import EquipamentosFrame
        EquipamentosFrame(self.container, self).pack(fill=BOTH, expand=YES)

    def mostrar_ordens(self):
        self._limpar_container()
        self.title("Sistema OS - Ordens de Serviço")
        self.geometry("1200x720")
        self.minsize(1200, 720)
        self.resizable(True, True)
        self.place_window_center()
        from interface.ordem_de_serviço import OrdensFrame
        OrdensFrame(self.container, self).pack(fill=BOTH, expand=YES)

    def mostrar_configuracao(self):
        self._limpar_container()
        self.title("Sistema OS - Configuração")
        self.geometry("1200x720")
        self.minsize(1200, 720)
        self.resizable(True, True)
        self.place_window_center()
        from interface.configuração import ConfiguracaoFrame
        ConfiguracaoFrame(self.container, self).pack(fill=BOTH, expand=YES)


def iniciar_app():
    App().mainloop()
