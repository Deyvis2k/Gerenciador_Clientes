import tkinter as tk
from cadastro import database
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

class App(tk.Tk):
    def __init__(self, database):
        super().__init__()
        self.fonte = ('arial',8,'bold')
        self.title("GERENCIADOR DE CLIENTES")
        self.geometry("600x400")
        self.wm_resizable(width= False, height= False)
        self.database = database
        self.configure(bg="lightgray")
        self.style = ttk.Style()
        
        #remover cliente
        self.texto_remover = tk.Label(self, text="REMOVER CLIENTE:", font= ('arial', 10, 'bold'), fg=BLUE , bg= "lightgray")
        self.texto_remover.place(x= 250, y= 52)
        
        self.texto_id = tk.Label(self, text="Digite um número de ID válido.", font= ('arial', 7, 'bold'), bg= "lightgray")
        self.texto_id.place(x= 240, y= 80)
        
        self.remover_botao = tk.Button(self, text="Remover", command = self.remover_cliente, width=7,font= self.fonte, bg=PINK)
        self.remover_botao.place(x=373,y= 99)
        
        #validar- remover cliente -------------------------------------------------------------------
        self.valida_int = self.register(self.validar_inteiro)
        self.remove_entry = tk.Entry(self, bg = PINK, width=20, validate="key", validatecommand=(self.valida_int, "%P"))
        self.remove_entry.place(x=245, y=101)
        
        
        #total/media: -------------------------------------------------------------------
        self.remover_botao = tk.Button(self, text="Total Preço", command = self.total_preco, width=10,font= self.fonte, bg=PINK)
        self.remover_botao.place(x=245,y= 190)
        
        self.remover_botao = tk.Button(self, text="Media Preço", command = self.calcular_media, width=10,font= self.fonte, bg=PINK)
        self.remover_botao.place(x=245,y= 220)
        
        
        
        #agradecimentos - -------------------------------------------------------------------
        
        self.titulo_agradecimento = tk.Label(self,text="Agradecimento:", font=('arial', 10, 'normal'), fg='purple', bg='lightgray')
        self.titulo_agradecimento.place(x=1,y=15)
        
        self.imagem_piaget_label = tk.Button(self,text="alunos",font=('arial', 8, 'normal'), command=self.agradecimentos) # type: ignore
        self.imagem_piaget_label.place(x=15, y=40)
        
        
        #adicionar clientes: -------------------------------------------------------------------
        self.texto_adicionar = tk.Label(self, text="CADASTRAR CLIENTE:", font= ('arial', 10, 'bold'), fg=BLUE , bg= "lightgray")
        self.texto_adicionar.place(x= 450, y= 50)
        
        self.botao_adicionar = tk.Button(self, text="Enviar" ,font= self.fonte, width=11, fg= BLACK, bg = PINK, command= self.adicionar_cliente)
        self.botao_adicionar.place(x = 450, y = 230)
        

        #adicionar clientes - NOME -------------------------------------------------------------------
        self.texto_nome = tk.Label(self, text="insira o nome do cliente:", font= ('arial', 9, 'bold'), fg=BLACK, bg= "lightgray")
        self.texto_nome.place(x= 450, y= 80)
        
        self.adicionar_nome_entry = tk.Entry(self, bg = PINK, width=24)
        self.adicionar_nome_entry.place(x=450, y=100)
        
        #adicionar clientes - PREÇO -------------------------------------------------------------------
        self.adicionar_preco_entry = tk.Entry(self, bg = PINK, width=24, )
        self.adicionar_preco_entry.place(x=450, y=150)
        
        self.texto_preco = tk.Label(self, text="insira o preço da tosa:", font= ('arial', 9, 'bold'), fg=BLACK, bg= "lightgray")
        self.texto_preco.place(x= 450, y= 128)
        
        #adicionar clientes - HORA -------------------------------------------------------------------
        self.adicionar_hora_entry = tk.Entry(self, bg = PINK, width=24)
        self.adicionar_hora_entry.place(x=450, y=200)
        
        self.texto_hora = tk.Label(self, text="insira a hora da tosa:", font= ('arial', 9, 'bold'), fg=BLACK, bg= "lightgray")
        self.texto_hora.place(x= 450, y= 176)
        
        self.botao_load = tk.Button(self, text="Carregar Dados", command= self.carregar_dados, bg=PINK, fg=BLACK, font= ('arial', 8, 'bold'))
        self.botao_load.place(x = 245, y = 130)
        
        self.botao_load = tk.Button(self, text="Excluir DB", command= self.excluir_tudo,  bg=PINK, fg=BLACK, font= ('arial', 8, 'bold'))
        self.botao_load.place(x = 245, y = 160)
        
        self.arvore_frame()
        
    
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
                    self.lista.insert("", "end", values=(id_numero, nome, f'R${preco:,.2f}', horario_formatado))
            else:    
                self.exibir_erro("ERRO: ALGUM DOS CAMPOS ESTA VÁZIO.")
        except ValueError:
            self.exibir_erro("ERRO: Formatação errada de preço.")
        
        
          
    def carregar_dados(self):
        for item in self.lista.get_children():
            self.lista.delete(item)

        data = self.database.all()

        for item in data:
            id_numero = item.doc_id
            self.lista.insert("", "end", values=(id_numero, item["nome"], f'R${item["preco"]:,.2f}', item["data"]))      
          
    def arvore_frame(self):
        self.style.configure("Custom.Treeview.Heading",background = "black", foreground="purple", font=("arial",10,'bold'))
        self.style.configure("Custom.Treeview",background = "lightgray", foreground="black", font=("arial",9,'bold'), fieldbackground="lightgray")
        
        self.lista = ttk.Treeview(self,columns=("col1","col2","col3","col4"),style="Custom.Treeview", height=5)
        self.lista.heading("#0", text="")
        self.lista.heading("#1", text="ID")
        self.lista.heading("#2", text="Nome")
        self.lista.heading("#3", text="Preço")
        self.lista.heading("#4", text="Hora")
        
        self.lista.column("#0", width=0, stretch=False)
        self.lista.column("#1", width=28)
        self.lista.column("#2", width=102)
        self.lista.column("#3", width=60)
        self.lista.column("#4", width=50)
        
        # self.lista.place(x=2,relheight=2, relwidth=0.37)  
        
        
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.lista.yview)
        self.lista.configure(yscrollcommand=self.scrollbar.set)
        
        self.lista.pack(fill='both', side="bottom") 
        self.scrollbar.place(x=582, y=275, height=120)  
        
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
            
    def validar_inteiro(self, valor_se_permitido) -> bool:
        if valor_se_permitido.isdigit() or valor_se_permitido == "":
            return True
        return False
    
    def validar_float(self, valor_float):
        if valor_float == "":
            return True
        try:
            float(valor_float.replace('.'))
            return True
        except ValueError or KeyError:
            self.exibir_erro("ERROR")
            
    def agradecimentos(self):
        return messagebox.showinfo(title='Criado por:', message=" Deyvis Campos \n Dennis Campos \n Nicolas de Jesus \n Nícollas Almeida \n Kalvin Fernandes \n Karl Heinz")
            
    
    def excluir_tudo(self):
        if self.database.all() != []:
            self.database.truncate()
            self.carregar_dados()
        else:
            self.exibir_erro("ERRO: Não há nada para excluir")
            
    def formatar_horario(self,horarios) -> str | None:
     try:
        hora_formatada = datetime.strptime(horarios, '%H:%M')
        return hora_formatada.strftime('%H:%M')
     except ValueError:
        self.exibir_erro("Erro de Formato, Por favor, insira o horário no formato HH:MM")
        return None
    
            
    def exibir_erro(self, texto):
        messagebox.showerror(title= "ERROR", message= texto)
        
        
    def calcular_media(self) -> float | None:
        db = database.all()
        if db != [] and len(db) > 1:
            for item in db:
                total_precos = sum(item['preco'] for item in db)
                media = total_precos/len(db)
            messagebox.showinfo(title="MEDIA", message=f'A média de -{len(db)}- tosas é R${media:,.2f}')
        else:
            self.exibir_erro("Não há itens suficientes")
            return None
        
    def total_preco(self) -> float | None:
        db = database.all()
        
        if db != []:
            for item in db:
                total = sum(item['preco'] for item in db)
            messagebox.showinfo(title="TOTAL", message=f'O preço total de -{len(db)}- tosas é R${total:,.2f}')
        else:
            self.exibir_erro("Não há nenhum item")
            return None    
    
        
            
if __name__ == "__main__":
   app = App(database)
   app.mainloop()