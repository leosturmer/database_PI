import model

# // Inserts

def insert_vendedor(login, senha, nome, nome_loja=None):
    'Encapsula informações para inserir vendedor no banco de dados.'
    novo_vendedor = model.Vendedor(login=login, senha=senha, nome=nome, nome_loja=nome_loja)

    model.insert_vendedor(novo_vendedor)

def insert_produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo):
    'Encapsula informações para inserir produto no banco de dados.'

    novo_produto = model.Produto(id_produto, nome, valor_unitario,
                                 quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model.insert_produto(novo_produto)

def insert_encomenda(status, prazo, comentario, produtos):
    'Encapsula informações para inserir uma encomenda no banco de dados.'

    if comentario == '':
        comentario = None

    encomenda = model.Encomenda(
        status=status, prazo=prazo, comentario=comentario, produtos=produtos)

    model.insert_encomenda(encomenda)

def insert_venda(data, valor_final, status, produtos, comentario):
    'Encapsula informações para inserir uma venda no banco de dados.'

    venda = model.Venda(data=data, valor_final=valor_final,
                        status=status,  produtos=produtos, comentario=comentario)
    model.insert_venda(venda)

# // Selects

def listar_produtos():
    'Encapsula informações para listar produtos do banco de dados.'

    estoque = model.Estoque()
    produtos = model.listar_produtos(estoque)

    return produtos

def listar_produtos_encomenda():
    'Encapsula informações para listar produtos de uma encomenda do banco de dados.'

    estoque = model.Estoque()
    produtos = model.listar_produtos_encomenda(estoque)

    return produtos

def listar_encomendas():
    'Encapsula informações para listar as encomendas do banco de dados.'
    encomendas = model.listar_encomendas()

    return encomendas

def listar_vendas():
    'Encapsula informações para listar as vendas do banco de dados.'
    vendas = model.listar_vendas()
    return vendas

def select_vendedor(login):
    'Encapsula informações para selecionar vendedor no banco de dados.'

    vendedor = model.select_vendedor(login)

    return vendedor

def select_produto_id(id_produto: int):
    'Encapsula informações para selecionar um produto pelo ID no banco de dados.'

    return model.select_produto_id(model.Produto(id_produto))

def select_produto_nome(nome: str):
    'Encapsula informações para selecionar um produto pelo nome no banco de dados.'
    return model.select_produto_nome(nome)
    

def select_encomenda_status(status):
    'Encapsula informações para selecionar uma encomenda pelo status no banco de dados.'

    encomendas = model.select_encomenda_status(status)

    return encomendas

def select_encomenda_id(id_encomenda: int):
    'Encapsula informações para selecionar uma encomenda pelo ID no banco de dados.'

    return model.select_encomenda_id(model.Encomenda(id_encomenda))



# // Updates

def update_produto(id_produto, nome=None, valor_unitario=None,
                            quantidade=None, imagem=None, aceita_encomenda=None, descricao=None, valor_custo=None):
    'Encapsula informações para atualizar um produto pelo ID no banco de dados.'

    produto = model.Produto(id_produto, nome, valor_unitario,
                            quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model.update_produto(produto)

    return produto

def update_encomendas(id_encomenda, status, prazo=None, comentario=None):
    'Encapsula informações para atualizar uma encomenda pelo ID no banco de dados.'

    encomenda = model.Encomenda(status, prazo, comentario)
    model.update_encomendas(id_encomenda, encomenda)

    return encomenda

def update_venda(id_venda, status, data=None, comentario=None):
    'Encapsula informações para selecionar uma venda pelo ID no banco de dados.'

    venda = model.Venda(data=data, status=status, comentario=comentario)
    model.update_venda(id_venda, venda)

    return venda

# // Deletes

def delete_produto(id_produto):
    'Encapsula informações para deletar um produto pelo ID no banco de dados.'

    produto = model.Produto(id_produto)

    return model.delete_produto(produto)

def delete_encomenda(id_encomenda):
    'Encapsula informações para deletar uma encomenda pelo ID no banco de dados.'

    encomenda = model.delete_encomenda(id_encomenda)
    return encomenda

def delete_venda(id_venda):
    'Encapsula informações para selecionar uma venda pelo ID no banco de dados.'

    venda = model.delete_venda(id_venda)
    return venda

# //////////// Não utilizados

# def select_produto_quantidade():
#     produto = model.Produto()

