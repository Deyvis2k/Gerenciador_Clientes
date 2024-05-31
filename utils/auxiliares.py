from tkinter import messagebox

def calcular_media(database):
    db = database.all()
    if db and len(db) > 1:
        total_precos = sum(item['preco'] for item in db)
        media = total_precos / len(db)
        messagebox.showinfo(title="MEDIA", message=f'A média de -{len(db)}- tosas é R${media:,.2f}')
    else:
        messagebox.showerror("Erro", "Não há itens suficientes")

def total_preco(database):
    db = database.all()
    if db:
        total = sum(item['preco'] for item in db)
        messagebox.showinfo(title="TOTAL", message=f'O preço total de -{len(db)}- tosas é R${total:,.2f}')
    else:
        messagebox.showerror("Erro", "Não há nenhum item")