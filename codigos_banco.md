### Banco de dados PI - SQLITE - Nize

CREATE DATABASE nize_database;
USE nize_database;

CREATE TABLE vendedor (
	id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	login TEXT NOT NULL,
	senha TEXT NOT NULL,
	nome TEXT NOT NULL,
	nome_loja TEXT NULL
);

CREATE TABLE produtos (
	id_produto INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome TEXT NOT NULL,
	valor_venda REAL NOT NULL,
	quantidade INTEGER NULL,
	imagem TEXT NULL
	producao INTEGER NULL,
	descricao TEXT NULL,
	valor_custo REAL NULL,
);

CREATE TABLE encomenda (
	id_encomenda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	prazo TEXT NULL,
	quantidade INTEGER NULL,
	comentario TEXT NULL
);

CREATE TABLE encomenda_produto (
	quantidade INTEGER NULL,
	
	FOREIGN KEY encomenda
		REFERENCES encomenda (id_encomenda)
	FOREIGN KEY produto
		REFERENCES produtos (id_produto)
);

CREATE TABLE vendas (
	id_venda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	data TEXT NOT NULL,
	valor_final REAL NOT NULL, # para deixar salvo junto do ID da venda
	comentario TEXT NULL
);

CREATE TABLE venda_produto (
	quantidade INTEGER NOT NULL,

	FOREIGN KEY venda
REFERENCES vendas (id_venda)
	FOREIGN KEY produto
REFERENCES produtos (id_produto)
);



#### A DEFINIR

- Status da venda? realizado, não realizado, etc 0123
- Valor final? devo deixar salvo?
- Deixar salvo registro de todas as vendas?


#### OUTROS COMENTÁRIOS
- O valor final da venda não vai no banco. Ele calcula pelos produtos adicionados na venda.
- Estoque - view pela tabela produtos sem o estoque zerado


