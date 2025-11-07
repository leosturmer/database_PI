import model




def insert_vendedor(login, senha, nome, nome_loja=None):
    novo_vendedor = model.Vendedor(login=login, senha=senha, nome=nome, nome_loja=nome_loja)

    model.insert_vendedor(novo_vendedor)



def insert_produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo):

    novo_produto = model.Produto(id_produto, nome, valor_unitario,
                                 quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model.insert_produto(novo_produto)


def listar_produtos():
    estoque = model.Estoque()
    produtos = model.listar_produtos(estoque)

    return produtos


def listar_produtos_encomenda():
    estoque = model.Estoque()
    produtos = model.listar_produtos_encomenda(estoque)

    return produtos

def select_vendedor(login):
    vendedor = model.select_vendedor(login)

    return vendedor


def select_produto_id(id_produto: int):
    return model.select_produto_id(model.Produto(id_produto))


def update_produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo):
    produto = model.Produto(id_produto, nome, valor_unitario,
                            quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model.update_produto(produto)

    return produto


def delete_produto(id_produto):
    produto = model.Produto(id_produto)

    return model.delete_produto(produto)


def insert_encomenda(status, prazo, comentario, produtos):
    if comentario == '':
        comentario = None

    encomenda = model.Encomenda(
        status=status, prazo=prazo, comentario=comentario, produtos=produtos)

    model.insert_encomenda(encomenda)


def select_produto_quantidade():
    produto = model.Produto()


def listar_encomendas():
    encomendas = model.listar_encomendas()

    return encomendas


def listar_vendas():
    vendas = model.listar_vendas()
    return vendas


def select_encomenda_status(status):
    encomendas = model.select_encomenda_status(status)

    return encomendas


def select_encomenda_id(id_encomenda: int):
    return model.select_encomenda_id(model.Encomenda(id_encomenda))


def update_encomendas(id_encomenda, status, prazo=None, comentario=None):
    encomenda = model.Encomenda(status, prazo, comentario)
    model.update_encomendas(id_encomenda, encomenda)

    return encomenda


def update_venda(id_venda, data=None, status=None, comentario=None):
    venda = model.Venda(data, status, comentario)
    model.update_vendas(id_venda, venda)

    return venda


def delete_encomenda(id_encomenda):
    encomenda = model.delete_encomenda(id_encomenda)
    return encomenda


def delete_venda(id_venda):
    venda = model.delete_venda(id_venda)
    return venda


def insert_venda(data, valor_final, status, produtos, comentario):

    venda = model.Venda(data=data, valor_final=valor_final,
                        status=status,  produtos=produtos, comentario=comentario)
    model.insert_venda(venda)
