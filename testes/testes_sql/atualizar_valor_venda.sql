SELECT SUM(produtos.valor_venda * venda_produto.quantidade) as valor_venda
FROM venda_produto
INNER JOIN produtos ON venda_produto.produto = produtos.id_produto
WHERE venda_produto.venda = 2;
