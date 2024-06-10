from tkinter import messagebox
from datetime import datetime

def validar_inteiro(valor_se_permitido):
    if valor_se_permitido.isdigit() or valor_se_permitido == "":
        return True
    return False

def validar_horario(horario):
    try:
        hora_formatada = datetime.strptime(horario, "%d/%m/%Y %H:%M")
        return hora_formatada.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        messagebox.showerror("Erro de Formato", "Por favor, insira o horário no formato dia/mes/ano hora:minuto")
        return None