from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from database.usuarios import autenticar_usuario
from interface.responsivo import centralizar_canvas

class LoginFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent); self.app = app; self._montar_layout()
    def _montar_layout(self):
        c = tk.Canvas(self, width=520, height=620, bg="#F4F5F6", highlightthickness=0); c.pack(fill="both", expand=True); centralizar_canvas(c, self, 520, 620)
        def box(a,b,d,e,r=18,**o):
            p=[a+r,b,d-r,b,d,b,d,b+r,d,e-r,d,e,d-r,e,a+r,e,a,e,a,e-r,a,b+r,a,b]
            return c.create_polygon(p,smooth=True,**o)
        box(16,12,504,606,28,fill="white",outline="#0D527F",width=4)
        im=Image.open(Path(__file__).resolve().parents[1]/"imagens"/"logo.png").convert("RGBA"); im.thumbnail((150,130),Image.Resampling.LANCZOS); self.logo=ImageTk.PhotoImage(im)
        c.create_image(260,91,image=self.logo); c.create_text(260,184,text="Trinyti Tech",font=("Segoe Script",29,"bold"),fill="#111827")
        def field(label,y,secret=False):
            c.create_text(70,y,text=label,anchor="w",fill="#61656A",font=("Helvetica",15)); box(54,y+15,465,y+66,16,fill="#F7F7F7",outline="#696969",width=2)
            v=tk.StringVar(); w=tk.Entry(c,textvariable=v,show="*" if secret else "",font=("Helvetica",14),bd=0,highlightthickness=0,bg="#F7F7F7"); c.create_window(70,y+28,anchor="nw",window=w,width=360 if secret else 375,height=28); return v,w
        self.usuario_var,u=field("Usuário ou E-mail",258); self.senha_var,s=field("Senha",349,True)
        self.visivel=False
        def olho(_=None): self.visivel=not self.visivel; s.configure(show="" if self.visivel else "*")
        c.create_text(438,389,text="◉",fill="#172438",font=("Helvetica",16),tags="olho"); c.tag_bind("olho","<Button-1>",olho)
        c.create_text(465,442,text="Esqueceu a senha?",anchor="e",fill="#172438",font=("Georgia",12,"bold"),tags="esqueci")
        c.tag_bind("esqueci","<Button-1>",lambda _:messagebox.showinfo("Recuperar senha","Procure o administrador para redefinir sua senha.",parent=self))
        box(136,480,392,535,10,fill="#104B7B",outline="#0C3E68",width=2,tags="entrar"); c.create_text(264,507,text="Entrar",fill="white",font=("Helvetica",16),tags="entrar")
        c.create_text(260,568,text="Cadastrar-se",fill="#172438",font=("Georgia",13,"bold"),tags="cadastro"); c.create_line(208,576,312,576,fill="#172438",tags="cadastro")
        c.tag_bind("entrar","<Button-1>",lambda _:self._entrar()); c.tag_bind("cadastro","<Button-1>",lambda _:self.app.mostrar_cadastro())
        for tag in ("entrar","cadastro","esqueci","olho"):
            c.tag_bind(tag,"<Enter>",lambda _:c.config(cursor="hand2")); c.tag_bind(tag,"<Leave>",lambda _:c.config(cursor=""))
        u.bind("<Return>",lambda _:self._entrar()); s.bind("<Return>",lambda _:self._entrar()); u.focus_set()
    def _entrar(self):
        registro=autenticar_usuario(self.usuario_var.get().strip(),self.senha_var.get())
        if registro: self.app.usuario_atual=registro; self.app.mostrar_dashboard()
        else: messagebox.showerror("Acesso negado","Usuário, e-mail ou senha inválidos.",parent=self); self.senha_var.set("")
