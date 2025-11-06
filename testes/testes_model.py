import model

# loja = Loja()
# vendedor = Vendedor()

# ##### Testes da model

# ### 

produto1 = model.Produto('carrinho', valor_unitario=10.50, quantidade=10, aceita_encomenda=12, descricao='legal')
produto2 = model.Produto('coração', valor_unitario=20)
produto3 = model.Produto('gatinho', valor_unitario=6, quantidade=6)
produto4 = model.Produto('folha', valor_unitario=10.0, descricao='uma folha', valor_custo=5.00)
produto5 = model.Produto('croche', valor_unitario=25.00, quantidade=12, aceita_encomenda=1, descricao='croche bonito', valor_custo=12.00)
# produto6 = model.Produto()

####### INSERTS ######## 

## Inserindo vendedor
model.insert_vendedor('email@email.com', 'abc123', 'Vendedor')

# Inserindo produtos

model.insert_produto(produto1)
model.insert_produto(produto2)
model.insert_produto(produto3)
model.insert_produto(produto4)
model.insert_produto(produto5)

# ### inserindo encomendas

model.insert_encomenda(status=1, prazo='10', comentario='foi encomendado', produtos=[(2,1), (1,2)])
model.insert_encomenda(status=2, produtos=[(7, 10), (6, 6)])
model.insert_encomenda(status=3, prazo='dias', comentario='fazer isso', produtos=[
    (1, 5),
    (2, 10)
    ])

# inserindo vendas

model.insert_venda(status=1, data='2025-09-12', valor_final= 20.5, comentario='primeira venda', produtos=[
    (1, 10),
    (2, 5)
])
model.insert_venda(status=2, data='2025-10-24', valor_final= 35, produtos=[
    (5, 5),
    (4, 4)
])
model.insert_venda(status=3, data='2025', produtos=[(2, 5)])

# # ####### SELECTS ######## 

# # vendedor.listar_produtos()

# # vendedor.listar_encomendas()

# # vendedor.listar_vendas()


# # vendedor.select_produto_nome('nho')
# # vendedor.select_produto_valor(5)
# # vendedor.select_produto_quantidade(12)
# # vendedor.select_produto_descricao('legal')

# # loja.visualizar_estoque()
# # loja.visualizar_esgotados()

# # ####### UPDATES ######## 



# # ##### @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ TESTARRRRRRRRRR UPDATEEEEEEEEEEEEEEESSSSSSSSSSSSSSS @@@@@@@@@@@@@@ ##########

# # vendedor.update_produtos(id_produto=1, nome='carrinho de mão')
# vendedor.update_encomendas()
# vendedor.update_vendas()
# vendedor.update_vendedor()


# ####### DELETES ######## 

# # vendedor.delete_produto(1)
# # vendedor.delete_encomenda(1)
# # vendedor.delete_venda(1)



