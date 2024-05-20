""" APLICATIVO  TRABALHO EXTENSÃO: CADASTRAR CONSULTA,
    CHECAR CONSULTA, REMOVER CONSULTA, MÉDIA, TOTAL
    EXCLUIR DATABASE.
"""

from others_.cadastro import database
from janela import App




app = App(database)
app.mainloop()