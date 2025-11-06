CREATE VIEW view_encomendas
AS
SELECT encomendas.prazo, produtos.nome, encomenda_produto.quantidade, encomendas.comentario
FROM encomendas
INNER JOIN encomenda_produto ON encomendas.id_encomenda = encomenda_produto.encomenda
INNER JOIN produtos ON encomenda_produto.produto = produtos.id_produto
;