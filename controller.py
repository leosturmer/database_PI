import model

def insert_vendedor(login, senha, nome, nome_loja):
    novo_vendedor = model.Vendedor(login, senha, nome, nome_loja)

    model.insert_vendedor(novo_vendedor)

    
