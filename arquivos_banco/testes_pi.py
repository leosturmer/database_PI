from banco_de_dados import (insert_vendedor, insert_produto, insert_encomenda, insert_venda, listar_produtos, listar_encomendas, listar_vendas, select_encomenda_prazo, select_encomenda_produto, select_produto_descricao, select_produto_nome, select_produto_quantidade, select_produto_valor, select_venda_data, select_venda_produto, update_encomendas, update_produtos, update_vendas, update_vendedor, visualizar_esgotados, visualizar_estoque, delete_produto, delete_encomenda, delete_venda)

#### Testes do banco

## 

##### INSERTS ######## 

# ##### Inserindo vendedor
# insert_vendedor('email@email.com', 'abc123', 'Vendedor')

# # Inserindo produtos

# insert_produto('carrinho', valor_unitario=10.50, quantidade=10, aceita_encomenda=12, descricao='legal')
# insert_produto('coração', valor_unitario=20, )
# insert_produto('gatinho', valor_unitario=6, quantidade=6)
# insert_produto('folha', valor_unitario=10.0, descricao='uma folha', valor_custo=5.00)
# insert_produto('croche', valor_unitario=25.00, quantidade=12, aceita_encomenda=1, descricao='croche bonito', valor_custo=12.00)

# # ### inserindo encomendas

# insert_encomenda(status=1, prazo='10', comentario='foi encomendado', produtos=[(2,1), (1,2)])
# insert_encomenda(status=2, produtos=[(7, 10), (6, 6)])
# insert_encomenda(status=3, prazo='dias', comentario='fazer isso', produtos=[
#     (1, 5),
#     (2, 10)
#     ])

# # inserindo vendas

# insert_venda(status=1, data='2025-09-12', valor_final= 20.5, comentario='primeira venda', produtos=[
#     (1, 10),
#     (2, 5)
# ])
# insert_venda(status=2, data='2025-10-24', valor_final= 35, produtos=[
#     (5, 5),
#     (4, 4)
# ])
# insert_venda(status=3, data='2025', produtos=[(2, 5)])

# ####### SELECTS ######## 

# listar_produtos()
# listar_encomendas()
# listar_vendas()


# select_produto_nome('nho')
# select_produto_valor(5)
# select_produto_quantidade(12)
# select_produto_descricao('legal')

# visualizar_estoque()
# visualizar_esgotados()


# select_encomenda_prazo('10')
# select_encomenda_produto('nho')

# select_venda_data('2025')
# select_venda_produto('nho')

####### UPDATES ######## 

##### @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ TESTARRRRRRRRRR UPDATEEEEEEEEEEEEEEESSSSSSSSSSSSSSS @@@@@@@@@@@@@@ ##########

# update_produtos(id_produto=2, nome='carrinho de mão')
# update_encomendas(id_encomenda=3, status=0)
# update_vendas(id_venda=2, status=1)
# update_vendedor(id_vendedor=1, login='novoemail@email.com')


# ###### DELETES ######## 

# delete_produto(1)
# delete_encomenda(1)
# delete_venda(1)



