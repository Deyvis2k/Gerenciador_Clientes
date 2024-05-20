import customtkinter as tk
from cadastro import Admin, database
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime


#cores
BLACK = "#000"
WHITE = "#fff"
GRAY = "#808080"
GREEN = "#00ff00"
RED = "#ff0000"
BLUE = "#0000ff"
PINK = "#ffcbdb"
GRAPHITE = "#2e2e2e"

class App(Admin):
    def __init__(self, database,root):
        super().__init__(database)
        self.root = root
        self.fonte = ('arial',10,'bold')
        self.root.title("GERENCIADOR DE CLIENTES")
        self.root.geometry("600x400")
        self.root.resizable(width= False, height= False)
        self.database = database
        self.opcao_selecionadas = tk.StringVar()
        
        
        #remover cliente
        self.texto_remover = tk.CTkLabel(root, text="REMOVER CLIENTE:", font= ('arial', 12, 'bold'))
        self.texto_remover.place(x= 230, y= 20)
        
        self.texto_id = tk.CTkLabel(root, text="Digite um número de ID válido.", font= ('arial', 9, 'bold'), text_color=PINK)
        self.texto_id.place(x= 230, y= 50)
        
        self.remover_botao = tk.CTkButton(root, text="Remover", command = self.remover_cliente, width=50,font= self.fonte, text_color="pink", fg_color="gray")
        self.remover_botao.place(x=360,y= 80)
        
        #validar- remover cliente
        self.valida_int = self.root.register(self.validar_inteiro)
        self.remove_entry = tk.CTkEntry(root, width=120, validate="key", validatecommand=(self.valida_int, "%P"))
        self.remove_entry.place(x=230, y=80)
        
        
        
        #adicionar clientes: 
        self.texto_adicionar = tk.CTkLabel(root, text="CADASTRAR CLIENTE:", font= ('arial', 12, 'bold'))
        self.texto_adicionar.place(x= 450, y= 20)
        
        self.botao_adicionar = tk.CTkButton(root, text="Enviar" ,font= self.fonte, width=50, command= self.adicionar_cliente, text_color="pink", fg_color="gray")
        self.botao_adicionar.place(x = 450, y = 230)
        

        #adicionar clientes - NOME
        self.texto_nome = tk.CTkLabel(root, text="Nome:", font= ('arial', 10, 'bold'),  text_color=PINK)
        self.texto_nome.place(x= 450, y= 45)
        
        self.adicionar_nome_entry = tk.CTkEntry(root, placeholder_text="Digite seu nome")
        self.adicionar_nome_entry.place(x=450, y=70)
        
        #adicionar clientes - PREÇO
        #valida_inteiro aplicado nele também
        self.adicionar_preco_entry = tk.CTkEntry(root,placeholder_text="Digite o preço")
        self.adicionar_preco_entry.place(x=450, y=130)
        
        self.texto_preco = tk.CTkLabel(root, text="Preço da tosa:", font= ('arial', 10, 'bold'), text_color=PINK)
        self.texto_preco.place(x= 450, y= 100)
        
        #adicionar clientes - HORA
        self.adicionar_hora_entry = tk.CTkEntry(root, placeholder_text="Digite a hora(hr:min)")
        self.adicionar_hora_entry.place(x=450, y=187)
        
        self.texto_hora = tk.CTkLabel(root, text="Hora:", font= ('arial', 10, 'bold') , text_color=PINK)
        self.texto_hora.place(x= 450, y= 158)
        
        #botão opções
        self.lista_botao =  tk.CTkOptionMenu(root, hover=True, 
                                       values=["listar database","excluir database"],
                                       button_color="white", variable= self.opcao_selecionadas, text_color="pink", fg_color="gray")
        
        self.lista_botao.place(x=230,y=120)
        
        self.opcao_selecionadas.trace_add('write', self.opcoes_botao)
        
        #Treeview - Arvore da database
        self.arvore_frame(root)
        
    
    def adicionar_cliente(self):
        try:
            if self.adicionar_nome_entry.get() != "" and self.adicionar_preco_entry.get() != "" and self.adicionar_hora_entry.get() != "":
                id_numero = len(self.lista.get_children()) + 1
                nome = self.adicionar_nome_entry.get()
                preco = float(self.adicionar_preco_entry.get())
                horario = self.adicionar_hora_entry.get()
                horario_formatado = self.formatar_horario(horario)
            
                if horario_formatado != None:
                    data = {"nome": nome, "preco": preco, "horario": horario_formatado}
                    self.database.insert(data)
                    self.lista.insert("", "end", values=(id_numero, nome, f'R${preco:.2f}', horario_formatado))
                    
            else:    
                self.exibir_erro("ERRO: ALGUM DOS CAMPOS ESTA VÁZIO.")
        except ValueError:
            self.exibir_erro("ERRO: Formatação inválida de preço")
            
        
          
    def carregar_dados(self):
        for item in self.lista.get_children():
            self.lista.delete(item)

        data = self.database.all()

        for item in data:
            id_numero = item.doc_id
            self.lista.insert("", "end", values=(id_numero, item["nome"], f'R${item["preco"]:.2f}', item["horario"]), tags="odd")      
          
    def arvore_frame(self, root):
        self.estilo = ttk.Style()
        
        self.estilo.configure(
            style="Custom.Treeview.Heading",
            font = ('arial',9,'bold'),
            foreground="purple",
            relief="flat"
            )
        
        self.estilo.configure("Custom.Treeview",background = "lightgray", foreground="black", font=("arial",9,'bold'), fieldbackground="lightgray")
        
        nome_colunas = ("ID","Nome","Preço","Hora")
        
        self.lista = ttk.Treeview(root, height=5,columns= nome_colunas, show=["headings","tree"],style= "Custom.Treeview")
        
        self.lista.tag_configure('odd')
        
        
        self.lista.heading("#0", text="")
        self.lista.heading("#1", text="ID")
        self.lista.heading("#2", text="Nome")
        self.lista.heading("#3", text="Preço")
        self.lista.heading("#4", text="Hora")
        
        self.lista.column("#0", width=0, stretch=False)
        self.lista.column("#1", width=3, anchor="nw")
        self.lista.column("#2", width=65)
        self.lista.column("#3", width=55)
        self.lista.column("#4", width=45)
        
        self.lista.pack(fill="both", side="bottom")
        
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.lista.yview)
        self.scrollbar.place(x=585, y=275, height=140)  
        self.lista.configure(yscrollcommand=self.scrollbar.set)
        
        
        
        
        
        
    def remover_cliente(self):
      try:
        if self.database.all() != []:
                id_numero = int(self.remove_entry.get())
                self.database.remove(doc_ids= [id_numero])
                self.carregar_dados()
        else:             
            self.exibir_erro("ERRO: ID não encontrado.")
      except ValueError:
            self.exibir_erro("ERRO: Digite algum ID.")
      except KeyError:
            self.exibir_erro("ERRO: ID não encontrado.")
            
    def validar_inteiro(self, valor_se_permitido):
        if valor_se_permitido.isdigit() or valor_se_permitido == "":
            return True
        return False
    
      
    def excluir_tudo(self):
        if self.database.all() != []:
            self.database.truncate()
            self.carregar_dados()
        else:
            self.exibir_erro("ERRO: Não há nada para excluir")
            
    def opcoes_botao(self, *args) -> None:
        selecionado = self.lista_botao.get()
        
        if selecionado == "listar database":
            self.carregar_dados()
        elif selecionado == "excluir database":
            self.excluir_tudo()
    
            
    def exibir_erro(self, texto):
        messagebox.showerror(title= "ERROR", message= texto)
        
    def formatar_horario(self,horarios):
     try:
        hora_formatada = datetime.strptime(horarios, '%H:%M')
        return hora_formatada.strftime('%H:%M')
     except ValueError:
        self.exibir_erro("Erro de Formato, Por favor, insira o horário no formato HH:MM")
        return None
        
            
if __name__ == "__main__":
   core = tk.CTk()
   app = App(database, core)
   app.root.mainloop()