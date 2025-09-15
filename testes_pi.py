from banco_de_dados import (insert_produto, insert_encomenda, insert_venda, listar_produtos, listar_encomendas, listar_vendas)

# Inserindo produtos

insert_produto('carrinho', 10.50, quantidade=10, encomenda=12, descricao='legal')
insert_produto('coração', 20, )
insert_produto('gatinho', 6, quantidade=6)
insert_produto('folha', 10.0, descricao='uma folha', valor_custo=5.00)
insert_produto('croche', 25.00, quantidade=12, encomenda=1, descricao='croche bonito', valor_custo=12.00)

# inserindo encomendas

# insert_encomenda(prazo='10', comentario='foi encomendado', produtos=[(2,1), (1,2)])
# insert_encomenda(produtos=[(7, 10), (6, 6)])
# insert_encomenda(prazo='dias', quantidade=10, comentario='fazer isso', produtos=[
# 	(1, 5),
# 	(2, 10)
#   ])

# insert_venda('2025-09-12', 20.5, 'primeira venda', [
# 	(1, 20),
# 	(2, 5)
# ])

# Teste selects

# listar_produtos()
# listar_encomendas()
# listar_vendas()







