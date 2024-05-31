""" APLICATIVO  TRABALHO EXTENSÃO: CADASTRAR CONSULTA,
    CHECAR CONSULTA, REMOVER CONSULTA, MÉDIA, TOTAL
    EXCLUIR DATABASE.
"""
from gui.app import GerenciadorClientes
import customtkinter as tk

if __name__ == "__main__":
    root = tk.CTk()
    app = GerenciadorClientes(root)
    root.mainloop()