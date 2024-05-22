from tinydb import TinyDB 
import time, os
from dataclasses import dataclass

"""'Não há realmente uma necessidade de utilizar dataclass 
    já que só há 1 item para inicilizar. Porém, para motivos de estudos, 
    resolvi utilizá-lo. Apenas isso.
    
    parte puramente de testes, reutilezei o código através de herança em
    janela.py
'"""




database = TinyDB('database.json', indent= 4)
database.default_table_name = 'admin'

@dataclass
class Admin:
    database: TinyDB
    
    #Inseri dados na DATABASE, além de gerar um ID único.
    def inserir_dados(self):
        print()
        nome = input('Digite o nome do cliente: ')
        preco = float(input('Digite o preço da tosa: '))
        horario = input('Digite o horário marcado: ')
        data = {"nome": nome, "preco": preco, "horario": horario}
        self.database.insert(data)
        
    # Visualiza database e lista 4 dados do cliente
    def visualizar_database(self):
        print()
        consultas = self.database.all()
        if consultas:
            for item in consultas:
                print('ID:', item.doc_id)
                print('Nome:', item['nome'])
                print(f'Preço: R$ {item["preco"]:.2f}')
                print('Data:', item['data'])
                print()
        else:
            print('ERRO: Não há nada para listar. Porfavor cadastre novos clientes.')
            
    #Remover clientes utilizando doc_ids que pega o ID do cliente
    def remover_cliente(self):
        try:
         number = int(input('Digite o ID para remover: '))
         self.database.remove(doc_ids= [number])
        except ValueError:
            print('ERRO: ID apenas aceita números.')
            
            
    def calcular_media(self) -> float | None:
        db = database.all()
        if db != [] and len(db) > 1:
            for item in db:
                total_precos = sum(item['preco'] for item in db)
                media = total_precos/len(db)
                print(f'A média de {len(db)} consultas é {media:.2f} ')
                return media
        else:
            print("Não há itens suficientes para fazer a média")
            return None
        
    def total_preco(self) -> float | None:
        db = database.all()
        
        if db != []:
            for item in db:
                total = sum(item['preco'] for item in db)
        
            print(f'O preço total das suas tosas é R${total:.2f}')
        else:
            print('Não há nenhum item')
            return None
            
            
    #Simples método que printa 5 opções
    def escolhas(self):
        print()
        print('OPÇÕES:')
        print('(1) CADASTRO CLIENTE')
        print('(2) EXCLUIR CLIENTE')
        print('(3) VISUALIZAR CONSULTA')
        print('(4) DELETAR TODOS OS CLIENTES')
        print('(5) SAIR')
        print()
        
        
    #Método principal, no qual se responsabiliza por
    #todos os outros métodos.
    def main(self):
        print('-'*15,"SISTEMA CADASTRO", '-' *15)
        self.escolhas()
        while True:
            opcao = input('Selecione uma opção: ')
            if opcao == "1":
                self.inserir_dados()
                print('Cadastrando..')
                time.sleep(1)
                print('Cliente cadastrado com sucesso!')
                
            elif opcao == "2":
                print()
                excluir_cliente = self.database.all()
                if excluir_cliente:
                    self.remover_cliente()
                else:
                    print('ERRO: Não há nada para excluir')
                    
            elif opcao == "3":
                self.visualizar_database()
                
            elif opcao == "4":
                excluir = self.database.all()
                if excluir:
                    print('Excluindo todos os dados..') 
                    time.sleep(3)
                    self.database.truncate()
                    print('Dados excluidos com sucesso.')
                else:
                    print('ERRO: Não há nada para excluir')
                    
            elif opcao == "5":
                print()
                print("Encerrando programa...")
                time.sleep(2)
                print('Até mais!')
                break
            
            elif opcao == "media":
                self.calcular_media()
            
            #Não que o "cls" seja uma opção, tanto que nem listei
            #apenas para o intuito de facilitar minha vida.
            #Utiliza o módulo OS e a função system para limpar.
            #Dependendo do sistema pode dar falha, Linux e Mac utilizam
            # "clear" ao invés de "cls".
            elif opcao == "cls":
                os.system("cls")
                print('-'*15,"SISTEMA CADASTRO", '-' *15)
                self.escolhas()
                
            elif opcao == "total":
                self.total_preco()
            
            
            else:
                print()
                print('ERROR: opção inválida')
                print()

        
if __name__ == '__main__':
    admin = Admin(database)
    admin.main()