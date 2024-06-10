import csv
from openpyxl import Workbook
from factory.dados import database
from tkinter import messagebox
def enviar_para_excel():
        arquivo = database.table('admin').all()
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
                    nome_colunas = ['Nome', 'Cachorro', 'Preço', 'Data']
                    escritor = csv.DictWriter(arquivo_csv, fieldnames=nome_colunas)
                    escritor.writeheader()
                    
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
                messagebox.showerror('ERROR','ERRO')
        else:
            with open(nome_arquivo_csv, 'w', newline='') as arquivo_vazio_csv:
                arquivo_vazio_csv.write(' ')