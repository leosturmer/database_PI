import sqlite3

#
# ----------- Criação das tabelas
#

sql_table_vendedor = '''
CREATE TABLE IF NOT EXISTS vendedor (
	id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	login TEXT NOT NULL,
	senha TEXT NOT NULL,
	nome TEXT NOT NULL,
	nome_loja TEXT NULL
);
'''

sql_table_produtos = '''
CREATE TABLE IF NOT EXISTS produtos (
	id_produto INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome TEXT NOT NULL,
	valor_venda REAL NOT NULL,

	quantidade INTEGER NULL,
	imagem TEXT NULL,
	encomenda INTEGER NULL,
	descricao TEXT NULL,
	valor_custo REAL NULL
);
'''

sql_table_encomendas = '''
CREATE TABLE IF NOT EXISTS encomendas (
	id_encomenda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	prazo TEXT NULL,
	quantidade INTEGER NULL,
	comentario TEXT NULL
);
'''

sql_table_vendas = '''
CREATE TABLE IF NOT EXISTS vendas (
	id_venda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	data TEXT NOT NULL,
	valor_final REAL NOT NULL,
	comentario TEXT NULL
);
'''

# Tabelas relacionais
sql_table_encomenda_produto = '''
CREATE TABLE IF NOT EXISTS encomenda_produto (
    encomenda INTEGER NOT NULL,
    produto INTEGER NOT NULL,
	quantidade INTEGER NULL,
	
	FOREIGN KEY (encomenda)
		REFERENCES encomendas (id_encomenda)
	FOREIGN KEY (produto)
		REFERENCES produtos (id_produto)
);
'''

sql_table_venda_produtos = '''
CREATE TABLE IF NOT EXISTS venda_produto (
    venda INTEGER NOT NULL,
    produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,

    FOREIGN KEY (venda)
        REFERENCES vendas (id_venda)
	FOREIGN KEY (produto)
        REFERENCES produtos (id_produto)
);
'''

#
# ----------- Inserção de tabelas no banco
#

with sqlite3.connect('nize_database.db') as conexao:
    conexao.execute(sql_table_vendedor)
    conexao.execute(sql_table_produtos)
    conexao.execute(sql_table_encomendas)
    conexao.execute(sql_table_vendas)
    conexao.execute(sql_table_encomenda_produto)
    conexao.execute(sql_table_venda_produtos)

#
# ----------- INSERTS
#

sql_insert_vendedor = '''
INSERT INTO vendedor (login, senha, nome, nome_loja)
	VALUES (?, ?, ?, ?)
'''

def insert_produto(nome, valor_venda, quantidade=0, imagem='', encomenda=0, descricao='', valor_custo=0):

	valores=['?', '?']
	lista_colunas = ['nome', 'valor_venda']
	lista_valores = [nome, valor_venda]

	if (quantidade>0):
		lista_colunas.append('quantidade')
		valores.append('?')
		lista_valores.append(quantidade)

	if (len(imagem)>0):
		lista_colunas.append(imagem)
		valores.append('?')
		lista_valores.append(imagem)
	
	if (encomenda>0):
		lista_colunas.append('encomenda')
		valores.append('?')
		lista_valores.append(encomenda)
    
	if (len(descricao)>0):
		lista_colunas.append('descricao')
		valores.append('?')
		lista_valores.append(descricao)
	
	if (valor_custo>0):
		lista_colunas.append('valor_custo')
		valores.append('?')
		lista_valores.append(valor_custo)

	colunas = ','.join(lista_colunas)

	sql = f'INSERT INTO produtos ({colunas}) VALUES ({','.join(valores)})'

	with sqlite3.connect('nize_database.db') as conexao:
		conexao.execute(sql, tuple(lista_valores))

sql_insert_encomenda = '''
INSERT INTO encomendas (prazo, quantidade, comentario)
	VALUES (?, ?, ?)
'''

def insert_encomenda(prazo, quantidade, comentario, produtos): # a variável "produtos" vai ter que ser passada pelo controller

	valores = []
	lista_colunas = []
	lista_valores = []

	if(len(prazo)>0):
		valores.append('?')
		lista_colunas.append('prazo')
		lista_valores.append(prazo)

	if (quantidade>0):
		valores.append('?')
		lista_colunas.append('quantidade')
		lista_valores.append(quantidade)

	if (len(comentario)>0):
		valores.append('?')
		lista_colunas.append('comentario')
		lista_valores.append(comentario)

	colunas = ','.join(lista_colunas)

	sql = f'''INSERT INTO encomendas ({colunas}) 
			VALUES ({','.join(valores)})
			RETURNING id_encomenda
			'''
	
	with sqlite3.connect('nize_database.db') as conexao:
		cursor = conexao.execute(sql, tuple(lista_valores))
		id_encomenda = cursor.fetchone()[0]

		sql = f'''
		INSERT INTO encomenda_produto (encomenda, produto, quantidade)
		VALUES ({id_encomenda}, ?, ?);
		'''

		cursor.executemany(sql, produtos)

def insert_venda(data, valor_final, comentario, produtos): # a variável "produtos" vai ter que ser passada pelo controller

	valores = ['?']
	lista_colunas = ['data']
	lista_valores = [data]

	if(valor_final>0):
		valores.append('?')
		lista_colunas.append('valor_final')
		lista_valores.append(valor_final)

	if (len(comentario)>0):
		valores.append('?')
		lista_colunas.append('comentario')
		lista_valores.append(comentario)

	colunas = ','.join(lista_colunas)

	sql = f'''INSERT INTO vendas ({colunas})
			VALUES ({','.join(valores)})
			RETURNING id_venda;
			'''

	with sqlite3.connect('nize_database.db') as conexao:
		cursor = conexao.execute(sql, tuple(lista_valores))
		id_venda = cursor.fetchone()[0] # pegamos o id_venda da nova venda inserida

		sql = f'''
		INSERT INTO venda_produto (venda, produto, quantidade)
		VALUES ({id_venda}, ?, ?);
		'''
		cursor.executemany(sql, produtos)
	
'''

# ------------------------ TESTES 


# Controller faz esta chamada

# insert_venda('2025-09-12', 20.5, 'primeira venda', [
# 	(1, 20),
# 	(2, 5)
# ])

# insert_encomenda(prazo='dias', quantidade=10, comentario='fazer isso', produtos=[
# 	(1, 5),
# 	(2, 10)
# ])

# insert_produto('folha', 10.0, descricao='uma folha', valor_custo=5.00)
# insert_produto('croche', 25.00, quantidade=12, encomenda=1, descricao='croche bonito', valor_custo=12.00)
'''

#
# ----------- SELECTS
#



#
# ----------- UPDATES
#



#
# ----------- DELETES
#