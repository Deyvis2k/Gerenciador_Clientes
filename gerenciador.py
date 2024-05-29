import customtkinter as tk
from tinydb import TinyDB
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from openpyxl import Workbook
import csv

database = TinyDB('database.json', indent= 4)
database.default_table_name = 'admin'

class App:
    def __init__(self, database,root):
        super().__init__()
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
        
        self.texto_id = tk.CTkLabel(root, text="Digite um número de ID válido.", font= ('arial', 9, 'bold'), text_color='pink')
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
        
        self.botao_csv = tk.CTkButton(root, text="Fazer Planilha", width=50,font= self.fonte, text_color="pink", fg_color="gray", command= self.enviar_para_excel)
        self.botao_csv.place(x=230,y= 160)
        
        #adicionar clientes - NOME
        self.texto_nome = tk.CTkLabel(root, text="Nome:", font= ('arial', 10, 'bold'),  text_color='pink')
        self.texto_nome.place(x= 450, y= 45)
        
        self.adicionar_nome_entry = tk.CTkEntry(root, placeholder_text="Digite seu nome")
        self.adicionar_nome_entry.place(x=450, y=70)
        
        #adicionar clientes - PREÇO
        #valida_inteiro aplicado nele também
        self.adicionar_preco_entry = tk.CTkEntry(root,placeholder_text="Digite o preço")
        self.adicionar_preco_entry.place(x=450, y=130)
        
        self.texto_preco = tk.CTkLabel(root, text="Preço da tosa:", font= ('arial', 10, 'bold'), text_color='pink')
        self.texto_preco.place(x= 450, y= 100)
        
        #adicionar clientes - data
        self.adicionar_hora_entry = tk.CTkEntry(root, placeholder_text="Digite o dia e hora")
        self.adicionar_hora_entry.place(x=450, y=187)
        
        self.texto_hora = tk.CTkLabel(root, text="Hora:", font= ('arial', 10, 'bold') , text_color='pink')
        self.texto_hora.place(x= 450, y= 158)
        
        #botão opções
        self.lista_botao =  tk.CTkOptionMenu(root, 
                                       values=["listar database","excluir database","media preço","total"],
                                       button_color="white",variable= self.opcao_selecionadas, text_color="pink", fg_color="gray", dropdown_text_color='pink')
        
        self.lista_botao.place(x=230,y=120)
        self.opcao_selecionadas.set("Opções:")
        
        self.opcao_selecionadas.trace_add('write', self.opcoes_botao)
        
        #Treeview - Arvore da database
        self.arvore_frame(root)
        
    def adicionar_cliente(self):
        try:
            if self.adicionar_nome_entry.get() != "" and self.adicionar_preco_entry.get() != "" and self.adicionar_hora_entry.get() != "":
                cachorro_lista = self.adicionar_janela_cachorro()
                cachorro = {item: value for item, value in cachorro_lista if item is not None and item.strip() != '' and value is not None and value.strip() != ''}
                
                if not cachorro:
                    return
                
                id_numero = len(self.lista.get_children()) + 1
                nome = self.adicionar_nome_entry.get()
                preco = float(self.adicionar_preco_entry.get())
                horario = self.adicionar_hora_entry.get()
                horario_formatado = self.formatar_horario(horario)
                
                if horario_formatado != None:
                    data = {"nome": nome,"cachorro": cachorro,"preco": preco, "data": horario_formatado}
                    self.database.insert(data)
                    
                    cachorro_str = ', '.join([f"{item}: {value}" for item, value in cachorro.items()])
                    self.lista.insert("", "end", values=(id_numero, nome, cachorro_str,f'R${preco:,.2f}', horario_formatado))
                    self.carregar_dados()
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
            cachorros = item["cachorro"]
            cachorro_str = ', '.join([f"{item} ({value})" for item, value in cachorros.items()])
            
            self.lista.insert("", "end", values=(id_numero, item["nome"],cachorro_str,f'R${item["preco"]:,.2f}', item["data"]), tags="odd")      
          
    def arvore_frame(self, root):
        self.estilo = ttk.Style()
        
        self.estilo.configure(
            style="Custom.Treeview.Heading",
            font = ('arial',9,'bold'),
            foreground="purple",
            relief="flat"
            )
        
        self.estilo.configure("Custom.Treeview",background = "lightgray", foreground="black", font=("arial",9,'bold'), fieldbackground="lightgray")
        
        nome_colunas = ("ID","Nome","Cachorro","Preço","Data")
        
        self.lista = ttk.Treeview(root, height=5,columns= nome_colunas, show=["headings","tree"],style= "Custom.Treeview")
        
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
        self.lista.column("#3", width=180, stretch=False)
        self.lista.column("#4", width=100, stretch=False)
        self.lista.column("#5", width=120, stretch=False)
        
        self.lista.pack(fill="both", side="bottom")
        
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.lista.yview)
        self.scrollbar.place(x=585, y=275, height=140)  
        self.lista.configure(yscrollcommand=self.scrollbar.set)
               
    #loop para adicionar cachorros até que o usuário saia
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

        botao_dog = tk.CTkButton(win, text="Enviar", width=50, font=self.fonte, text_color="pink", fg_color="gray", command=lambda: self.capturar_dados(win))
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
            
        if alergia == '':
            alergia = 'Não'
            self.alergias.append(alergia)
   
    def enviar_para_excel(self):
        arquivo = self.database.table('admin').all()
        nome_arquivo_csv = 'dados_exportados.csv'
        wb = Workbook()
        ws = wb.active
        
        lista=[]
        lista_preco = []
        
        if arquivo != []:
            total = sum(item['preco'] for item in arquivo)
            media = total / len(arquivo)
            for item  in arquivo:
                nome = item['nome']
                cachorro = item['cachorro']
                cachorro_str = ' & '.join([f"{item}[{value}]" for item, value in cachorro.items()])
                preco = item['preco']
                data = item['data']
                lista.append([nome,f"({cachorro_str})", f'R${preco:.2f}', data])
                    
            lista_preco.append([f'Total: {total:.2f}',f'Média: {media:.2f}'])     
        
            try:
                with open(nome_arquivo_csv, 'w', newline='') as arquivo_csv:
                    for b in lista:
                        arquivo_csv.write(' , '.join(map(str, b)) + "\r")
                        
                with open(nome_arquivo_csv, 'a', newline='') as arquivo_csv:
                    for b in lista_preco:
                        arquivo_csv.write("\r")
                        arquivo_csv.write(' , '.join(b) + "\r")
                                        
                with open(nome_arquivo_csv, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        ws.append(row)
                wb.save('planilha.xlsx')
            except Exception:
                self.exibir_erro('ERROR')
        else:
            with open(nome_arquivo_csv, 'w', newline='') as arquivo_vazio_csv:
                arquivo_vazio_csv.write(' ')
        
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
        elif selecionado == "media preço":
            self.calcular_media()
        elif selecionado == "total":
            self.total_preco()
            
    def exibir_erro(self, texto):
        messagebox.showerror(title= "ERROR", message= texto)
        
    def formatar_horario(self,horarios) -> str | None:
     try:
        hora_formatada = datetime.strptime(horarios, "%d/%m/%Y %H:%M")
        return hora_formatada.strftime("%d/%m/%Y %H:%M")
     except ValueError:
        self.exibir_erro("Erro de Formato, Por favor, insira o horário no formato dia/mes/ano hora:minuto")
        return None
    
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
   core = tk.CTk()
   app = App(database,core)
   app.root.mainloop()