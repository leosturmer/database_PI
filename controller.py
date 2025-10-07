import model

def insert_vendedor(login, senha, nome, nome_loja):
    novo_vendedor = model.Vendedor(login, senha, nome, nome_loja)

    model.insert_vendedor(novo_vendedor)

    
def insert_produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo):
    
    novo_produto = model.Produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model.insert_produto(novo_produto)


def listar_produtos():
    estoque = model.Estoque()
    produtos = model.listar_produtos(estoque)

    return produtos

def listar_produtos_encomenda():
    estoque = model.Estoque()
    produtos = model.listar_produtos_encomenda(estoque)

    return produtos

def select_produto_id(id_produto: int):
      
    return model.select_produto_id(model.Produto(id_produto))

def update_produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo):
    produto = model.Produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model.update_produto(produto)

    return produto

def delete_produto(id_produto):
    produto = model.Produto(id_produto)

    return model.delete_produto(produto)

def insert_encomenda(status, prazo, comentario, produtos):
    if comentario == '':
        comentario = None

    encomenda = model.Encomenda(status=status, prazo=prazo, comentario=comentario, produtos=produtos)

    model.insert_encomenda(encomenda)


def select_produto_quantidade():
    produto = model.Produto()

def listar_encomendas():
    encomendas = model.listar_encomendas()

    return encomendas

def select_encomenda_status(status):
    encomendas = model.select_encomenda_status(status)
    
    return encomendas

def select_encomenda_id(id_encomenda: int):
    return model.select_encomenda_id(model.Encomenda(id_encomenda))
