import customtkinter as tk
from gui.clientes_form import ClientesForm
from gui.arvore_view import ArvoreView
from tkinter import messagebox
from utils.auxiliares import calcular_media, total_preco
from factory.dados import database



class GerenciadorClientes:
    def __init__(self, root):
        tk.set_appearance_mode('dark')
        tk.set_default_color_theme('dark-blue')
        self.root = root
        self.fonte = ('arial',10,'bold')
        self.root.title("GERENCIADOR DE CLIENTES")
        self.root.geometry("600x400")
        self.root.resizable(width=False, height=False)
        self.opcao_selecionadas = tk.StringVar()
        
        self.clientes_form = ClientesForm(self)
        self.arvore_view = ArvoreView(self)

        # Carregar dados iniciais
        self.clientes_form.carregar_dados()
        
        # Trace option menu
        self.opcao_selecionadas.trace_add('write', self.opcoes_botao)

    def opcoes_botao(self, *args):
        selecionado = self.opcao_selecionadas.get()
        if selecionado == "excluir database":
            self.clientes_form.excluir_tudo()
        elif selecionado == "media preço":
            calcular_media(database)
        elif selecionado == "total":
            total_preco(database)

    def exibir_erro(self, texto):
        messagebox.showerror(title="ERROR", message=texto)