INSERT INTO venda_produto (venda, produto, quantidade, valor_unitario)
VALUES (1,4,5, (SELECT produtos.valor_unitario FROM produtos WHERE produtos.id_produto = 4));
