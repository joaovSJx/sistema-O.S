from pathlib import Path
import re, tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from database.usuarios import cadastrar_usuario
from interface.responsivo import centralizar_canvas

class CadastroFrame(ttk.Frame):
    def __init__(self,parent,app): super().__init__(parent); self.app=app; self.campos={}; self._montar()
    def _montar(self):
        c=tk.Canvas(self,width=520,height=720,bg="#F4F5F6",highlightthickness=0); c.pack(fill="both",expand=True); centralizar_canvas(c,self,520,720)
        def box(a,b,d,e,r=18,**o):
            p=[a+r,b,d-r,b,d,b,d,b+r,d,e-r,d,e,d-r,e,a+r,e,a,e,a,e-r,a,b+r,a,b]; return c.create_polygon(p,smooth=True,**o)
        box(16,10,504,710,28,fill="white",outline="#0D527F",width=4); c.create_text(50,48,text="↩",fill="#0D527F",font=("Helvetica",27,"bold"),tags="voltar")
        c.tag_bind("voltar","<Button-1>",lambda _:self.app.mostrar_login())
        im=Image.open(Path(__file__).resolve().parents[1]/"imagens"/"logo.png").convert("RGBA"); im.thumbnail((142,122),Image.Resampling.LANCZOS); self.logo=ImageTk.PhotoImage(im)
        c.create_image(260,88,image=self.logo); c.create_text(260,181,text="Trinyti Tech",font=("Segoe Script",28,"bold"),fill="#111827"); c.create_text(54,236,text="Criar Conta",anchor="w",fill="#172438",font=("Georgia",18,"bold"))
        def field(name,placeholder,y,secret=False):
            box(46,y,474,y+50,16,fill="#F7F7F7",outline="#696969",width=2); v=tk.StringVar(value=placeholder); w=tk.Entry(c,textvariable=v,font=("Helvetica",14),fg="#96999C",bd=0,highlightthickness=0,bg="#F7F7F7"); c.create_window(63,y+13,anchor="nw",window=w,width=392,height=27)
            def focus(_):
                if v.get()==placeholder: v.set(""); w.configure(fg="#1F2933",show="*" if secret else "")
            def blur(_):
                if not v.get().strip(): v.set(placeholder); w.configure(fg="#96999C",show="")
            w.bind("<FocusIn>",focus); w.bind("<FocusOut>",blur); self.campos[name]=(v,placeholder)
        field("nome","Nome Completo",270); field("email","E-mail Profissional",350); field("senha","Crie uma Senha",430,True); field("confirmacao","Confirme sua Senha",510,True)
        box(145,590,370,647,10,fill="#104B7B",outline="#0C3E68",width=2,tags="cadastrar"); c.create_text(257,618,text="Cadastrar",fill="white",font=("Georgia",16,"bold"),tags="cadastrar")
        c.create_text(260,674,text="Já tem uma conta?",fill="#4C535A",font=("Helvetica",11)); c.create_text(370,674,text="Entrar",fill="#172438",font=("Georgia",12,"bold"),tags="entrar")
        c.tag_bind("cadastrar","<Button-1>",lambda _:self._cadastrar()); c.tag_bind("entrar","<Button-1>",lambda _:self.app.mostrar_login())
    def _valor(self,n): v,p=self.campos[n]; return "" if v.get()==p else v.get().strip()
    def _cadastrar(self):
        try:
            senha=self._valor("senha")
            if senha!=self._valor("confirmacao"): raise ValueError("As senhas não coincidem.")
            email=self._valor("email"); usuario=re.sub(r"[^a-z0-9_]","",email.split("@",1)[0].lower())
            cadastrar_usuario(self._valor("nome"),usuario,email,senha); messagebox.showinfo("Sucesso","Conta criada com sucesso. Agora faça login.",parent=self); self.app.mostrar_login()
        except ValueError as e: messagebox.showerror("Dados inválidos",str(e),parent=self)
        except Exception as e: messagebox.showerror("Erro inesperado",str(e),parent=self)
