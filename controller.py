import model

def insert_vendedor(login, senha, nome, nome_loja):
    novo_vendedor = model.Vendedor(login, senha, nome, nome_loja)

    model.insert_vendedor(novo_vendedor)

    
def insert_produto(nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo):
    
    novo_produto = model.Produto(nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model.insert_produto(novo_produto)


def listar_produtos():
    estoque = model.Estoque()
    produtos = model.listar_produtos(estoque)

    return produtos

def select_produto_id(id_produto):
    
    model.select_produto_id(id_produto)

    produto = model.Produto()

    return(produto)