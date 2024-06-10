import customtkinter as tk
from tkinter import ttk
from utils.validadores import validar_inteiro , validar_horario
from utils.exportador import enviar_para_excel
from factory.dados import database


class ClientesForm:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.database = database

        # Remover cliente
        self.texto_remover = tk.CTkLabel(self.root, text="REMOVER CLIENTE:", font=('arial', 12, 'bold'))
        self.texto_remover.place(x=230, y=20)

        self.texto_id = tk.CTkLabel(self.root, text="Digite um número de ID válido.", font=('arial', 9, 'bold'), text_color='pink')
        self.texto_id.place(x=230, y=50)

        self.remover_botao = tk.CTkButton(self.root, text="Remover", command=self.remover_cliente, width=50, font=self.app.fonte, text_color="pink", fg_color="gray")
        self.remover_botao.place(x=360, y=80)

        self.valida_int = self.root.register(validar_inteiro)
        self.remove_entry = tk.CTkEntry(self.root, width=120, validate="key", validatecommand=(self.valida_int, "%P"))
        self.remove_entry.place(x=230, y=80)

        # Adicionar cliente
        self.texto_adicionar = tk.CTkLabel(self.root, text="CADASTRAR CLIENTE:", font=('arial', 12, 'bold'))
        self.texto_adicionar.place(x=450, y=20)

        self.botao_adicionar = tk.CTkButton(self.root, text="Enviar", font=self.app.fonte, width=50, command=self.adicionar_cliente, text_color="pink", fg_color="gray")
        self.botao_adicionar.place(x=450, y=230)

        self.botao_csv = tk.CTkButton(self.root, text="Fazer Planilha", width=50, font=self.app.fonte, text_color="pink", fg_color="gray", command= enviar_para_excel)
        self.botao_csv.place(x=230, y=160)

        self.texto_nome = tk.CTkLabel(self.root, text="Nome:", font=('arial', 10, 'bold'), text_color='pink')
        self.texto_nome.place(x=450, y=45)

        self.adicionar_nome_entry = tk.CTkEntry(self.root, placeholder_text="Digite seu nome")
        self.adicionar_nome_entry.place(x=450, y=70)

        self.adicionar_preco_entry = tk.CTkEntry(self.root, placeholder_text="Digite o preço")
        self.adicionar_preco_entry.place(x=450, y=130)

        self.texto_preco = tk.CTkLabel(self.root, text="Preço da tosa:", font=('arial', 10, 'bold'), text_color='pink')
        self.texto_preco.place(x=450, y=100)

        self.adicionar_hora_entry = tk.CTkEntry(self.root, placeholder_text="Digite o dia e hora")
        self.adicionar_hora_entry.place(x=450, y=187)

        self.texto_hora = tk.CTkLabel(self.root, text="Hora:", font=('arial', 10, 'bold'), text_color='pink')
        self.texto_hora.place(x=450, y=158)

        self.lista_botao = tk.CTkOptionMenu(self.root, values=["excluir database", "media preço", "total"],
                                            button_color="white", variable=self.app.opcao_selecionadas, text_color="pink", fg_color="gray", dropdown_text_color='pink')
        self.lista_botao.place(x=230, y=120)
        self.app.opcao_selecionadas.set("Opções:")

    def adicionar_cliente(self):
        try:
            if self.adicionar_nome_entry.get() != "" and self.adicionar_preco_entry.get() != "" and self.adicionar_hora_entry.get() != "":
                cachorro_lista = self.adicionar_janela_cachorro()
                cachorro = {item: value for item, value in cachorro_lista if item is not None and item.strip() != '' and value is not None and value.strip() != ''}
                if not cachorro:
                    return
                id_numero = len(self.app.arvore_view.lista.get_children()) + 1
                nome = self.adicionar_nome_entry.get()
                preco = float(self.adicionar_preco_entry.get())
                horario = self.adicionar_hora_entry.get()
                horario_formatado = validar_horario(horario)
                if horario_formatado:
                    data = {"nome": nome, "cachorro": cachorro, "preco": preco, "data": horario_formatado}
                    self.database.insert(data)
                    cachorro_str = ', '.join([f"{item}: {value}" for item, value in cachorro.items()])
                    self.app.arvore_view.lista.insert("", "end", values=(id_numero, nome, cachorro_str, f'R${preco:,.2f}', horario_formatado))
                    self.carregar_dados()
            else:
                self.app.exibir_erro("ERRO: ALGUM DOS CAMPOS ESTA VÁZIO.")
        except ValueError:
            self.app.exibir_erro("ERRO: Formatação inválida de preço")

    def carregar_dados(self):
        self.app.arvore_view.lista.delete(*self.app.arvore_view.lista.get_children())
        data = self.database.all()
        for item in data:
            id_numero = item.doc_id
            cachorros = item["cachorro"]
            cachorro_str = ', '.join([f"{item} ({value})" for item, value in cachorros.items()])
            self.app.arvore_view.lista.insert("", "end", values=(id_numero, item["nome"], cachorro_str, f'R${item["preco"]:,.2f}', item["data"]), tags="odd")

    def remover_cliente(self):
        try:
            if self.database.all():
                id_numero = int(self.remove_entry.get())
                self.database.remove(doc_ids=[id_numero])
                self.carregar_dados()
            else:
                self.app.exibir_erro("ERRO: ID não encontrado.")
        except ValueError:
            self.app.exibir_erro("ERRO: Digite algum ID.")
        except KeyError:
            self.app.exibir_erro("ERRO: ID não encontrado.")

    def excluir_tudo(self):
        if self.database.all():
            self.database.truncate()
            self.carregar_dados()
        else:
            self.app.exibir_erro("ERRO: Não há nada para excluir")

    def adicionar_janela_cachorro(self) -> list[tuple]:
        self.alergias = []
        self.racas = []

        win = tk.CTkToplevel(self.root)
        win.geometry("300x200")
        win.title('Adicionar Cachorro')
        win.resizable(False, False)

        win.lift(aboveThis=self.root)
        win.focus_force()

        texto_cachorro = tk.CTkLabel(win, text="CADASTRO CACHORRO", font=('arial', 12, 'bold'))
        texto_cachorro.place(x=75, y=5)

        texto_raca = tk.CTkLabel(win, text="Cachorro:", font=('arial', 10, 'bold'), text_color='PINK')
        texto_raca.place(x=53, y=36)

        self.raca_input = tk.CTkEntry(win, placeholder_text="Coloque a raça do cachorro:", width=200)
        self.raca_input.place(x=50, y=60)

        texto_alergia = tk.CTkLabel(win, text="Alergia:", font=('arial', 10, 'bold'), text_color='PINK')
        texto_alergia.place(x=53, y=89)

        self.alergia_input = tk.CTkEntry(win, placeholder_text="Caso haja, digite a alergia:", width=200)
        self.alergia_input.place(x=50, y=115)

        botao_dog = tk.CTkButton(win, text="Enviar", width=50, font=self.app.fonte, text_color="pink", fg_color="gray", command=lambda: self.capturar_dados(win))
        botao_dog.place(x=50, y=150)

        win.wait_window()
        dados_cachorro = list(zip(self.racas, self.alergias))
        return dados_cachorro

    def capturar_dados(self, win):
        raca = self.raca_input.get()
        alergia = self.alergia_input.get()
        if raca:
            self.racas.append(raca)
        if alergia:
            self.alergias.append(alergia)
        if not alergia:
            self.alergias.append('Não')
