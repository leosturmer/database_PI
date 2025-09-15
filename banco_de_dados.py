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

# ----------- Inserção de tabelas no banco

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


def insert_produto(nome, valor_venda, quantidade=None, imagem=None, encomenda=0, descricao=None, valor_custo=None):

    sql = f'''INSERT INTO produtos (nome, valor_venda, quantidade, imagem, encomenda, descricao, valor_custo) 
	VALUES (?, ?, ?, ?, ?, ?, ?)
	'''
    sql_values_produtos = [nome, valor_venda, quantidade,
                           imagem, encomenda, descricao, valor_custo]

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, sql_values_produtos)


# a variável "produtos" vai ter que ser passada pelo controller
def insert_encomenda(prazo=None, comentario=None, produtos=[]):

    sql = '''INSERT INTO encomendas (prazo, comentario) 
			VALUES (?, ?)
			RETURNING id_encomenda
			'''

    sql_values_encomenda = [prazo, comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, sql_values_encomenda)
        id_encomenda = cursor.fetchone()[0]

        sql = f'''
		INSERT INTO encomenda_produto (encomenda, produto, quantidade)
		VALUES ({id_encomenda}, ?, ?);
		'''

        cursor.executemany(sql, tuple(produtos))


# a variável "produtos" vai ter que ser passada pelo controller
def insert_venda(data, valor_final, comentario=None, produtos=[]):
    sql = '''INSERT INTO vendas (data, valor_final, comentario)
			VALUES (?, ?, ?)
			RETURNING id_venda;
			'''

    sql_values_venda = [data, valor_final, comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, sql_values_venda)
        id_venda = cursor.fetchone()[0]

        sql = f'''
		INSERT INTO venda_produto (venda, produto, quantidade)
		VALUES ({id_venda}, ?, ?);
		'''
        cursor.executemany(sql, tuple(produtos))

#
# ----------- SELECTS
#

# Produtos

def select_all(tabela):
    sql_select_all = f'''
	SELECT *
	FROM {tabela};
	'''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql_select_all)
        select_all = cursor.fetchall()

        match tabela:
            case 'produtos':
                for _id, nome, valor_venda, quantidade, _imagem, encomenda, descricao, valor_custo in select_all:
                    print(f'''
Nome: {nome} | Custo: {valor_custo} | Valor final: {valor_venda}
Quantidade: {quantidade} | Aceita encomenda: {encomenda} | Descrição: {descricao}''')

            case 'encomendas':
                for _id, prazo, comentario in select_all:
                    print(f'Prazo: {prazo} | Comentário:{comentario}')

            case 'vendas':
                for _id, data, valor_final, comentario in select_all:
                    print(f'''
Data da venda: {data} | Valor: {valor_final} | Comentário: {comentario}''')

def select_pesquisa(tabela, pesquisa):
	sql_select_pesquisa = f'''
	SELECT *
	FROM {tabela}
	WHERE {pesquisa} = ?;
	'''
    
	with sqlite3.connect('nize_database.db') as conexao:
		cursor = conexao.execute(sql_select_pesquisa, (pesquisa,))
		select_all = cursor.fetchall()
        
	match tabela:
            case 'produtos':
                for _id, nome, valor_venda, quantidade, _imagem, encomenda, descricao, valor_custo in select_all:
                    print(f'''
Nome: {nome} | Custo: {valor_custo} | Valor final: {valor_venda}
Quantidade: {quantidade} | Aceita encomenda: {encomenda} | Descrição: {descricao}''')

            case 'encomendas':
                for _id, prazo, comentario in select_all:
                    print(f'Prazo: {prazo} | Comentário:{comentario}')

            case 'vendas':
                for _id, data, valor_final, comentario in select_all:
                    print(f'''
Data da venda: {data} | Valor: {valor_final} | Comentário: {comentario}''')






#
# ----------- UPDATES
#


#
# ----------- DELETES
#
