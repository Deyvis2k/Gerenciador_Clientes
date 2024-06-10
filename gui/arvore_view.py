from tkinter import ttk
class ArvoreView:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.estilo = ttk.Style()

        self.estilo.configure(style="Custom.Treeview.Heading", font=('arial', 9, 'bold'), foreground="purple", relief="flat")
        self.estilo.configure("Custom.Treeview", background="lightgray", foreground="black", font=("arial", 9, 'bold'), fieldbackground="lightgray")

        nome_colunas = ("ID", "Nome", "Cachorro", "Preço", "Data")
        self.lista = ttk.Treeview(self.root, height=5, columns=nome_colunas, show=["headings", "tree"], style="Custom.Treeview")

        self.lista.tag_configure('odd')

        self.lista.heading("#0", text="")
        self.lista.heading("#1", text="ID")
        self.lista.heading("#2", text="Nome")
        self.lista.heading("#3", text="Cachorros(alergia)")
        self.lista.heading("#4", text="Preço")
        self.lista.heading("#5", text="Data")

        self.lista.column("#0", width=0, stretch=False)
        self.lista.column("#1", width=29, stretch=False)
        self.lista.column("#2", width=160, stretch=False)
        self.lista.column("#3", width=180)
        self.lista.column("#4", width=100, stretch=False)
        self.lista.column("#5", width=120, stretch=False)

        self.lista.pack(fill="both", side="bottom")

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.lista.yview)
        self.scrollbar.place(x=585, y=275, height=140)
        self.lista.configure(yscrollcommand=self.scrollbar.set)