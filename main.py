""" APLICATIVO  TRABALHO EXTENSÃO: CADASTRAR CONSULTA,
    CHECAR CONSULTA, REMOVER CONSULTA, MÉDIA, TOTAL
    EXCLUIR DATABASE.
"""
import customtkinter as tk
from gerenciador import database
from gerenciador import App



core = tk.CTk()
app = App(database,core)
app.root.mainloop()