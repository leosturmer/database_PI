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
        valor_unitario REAL NOT NULL,

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
    valor_unitario REAL NOT NULL,

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


def insert_produto(nome, valor_unitario, quantidade=None, imagem=None, encomenda=0, descricao=None, valor_custo=None):

    sql = f'''INSERT INTO produtos (nome, valor_unitario, quantidade, imagem, encomenda, descricao, valor_custo) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
    sql_values_produtos = [nome, valor_unitario, quantidade,
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


def insert_venda(data, valor_final=0, comentario=None, produtos=[]):
    # Passo 1 - criar a venda
    sql = '''INSERT INTO vendas (data, valor_final, comentario)
        VALUES (?, ?, ?)
        RETURNING id_venda;
        '''

    # passo 2 - inserir produtos da venda (venda_produto)
    sql_values_venda = [data, valor_final, comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, sql_values_venda)
        id_venda = cursor.fetchone()[0]

        sql = f'''
                INSERT INTO venda_produto (venda, produto, quantidade, valor_unitario)
                VALUES (:id_venda, :id_produto, :quantidade, (SELECT produtos.valor_unitario FROM produtos WHERE produtos.id_produto = :id_produto));

                '''

        produtos_quantidades = list()
        for prod_quant in produtos:
            produtos_quantidades.append(
                {
                    'id_venda': id_venda,
                    'id_produto': prod_quant[0],
                    'quantidade': prod_quant[1],
                }
            )

        cursor.executemany(sql, tuple(produtos_quantidades))

        # passo 3.1 - calcular total da venda
        sql_total_venda = '''SELECT SUM(venda_produto.valor_unitario * venda_produto.quantidade) as total_venda
        FROM venda_produto
        WHERE venda_produto.venda = ?;   
    '''
        valor_final = 0

        cursor = conexao.execute(sql_total_venda, (id_venda,))

        valor_final = cursor.fetchone()[0]

    # passo 3.2 atualizar valor_final na tabela vendas com

        sql_update_venda = f'''
        UPDATE vendas
        SET valor_final = {valor_final}
        WHERE id_venda = {id_venda};
    '''

        cursor = conexao.execute(sql_update_venda)


#
# ----------- SELECTS
#

# Selects gerais


def listar_produtos():
    sql = '''
    SELECT nome, valor_unitario, quantidade, imagem, encomenda, descricao, valor_custo
        FROM produtos;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

    for nome, valor_unitario, quantidade, _imagem, encomenda, descricao, valor_custo in select_all:
        print(f'''
Nome: {nome} | Custo: {valor_custo} | Valor unitário: {valor_unitario}
Quantidade: {quantidade} | Aceita encomenda: {encomenda} | Descrição: {descricao}''')


def listar_encomendas():
    sql = '''
    SELECT encomenda_produto.encomenda, encomenda_produto.quantidade, encomendas.prazo, encomendas.comentario, produtos.nome
    FROM encomenda_produto
    JOIN encomendas ON encomenda_produto.encomenda = encomendas.id_encomenda
    JOIN produtos ON encomenda_produto.produto = produtos.id_produto;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

        encomendas_dict = {}

        for encomenda, quantidade, prazo, comentario, nome in select_all:
            if encomenda not in encomendas_dict:
                encomendas_dict[encomenda] = {
                    'produtos': [],
                    'prazo': prazo,
                    'comentario': comentario
                }

            encomendas_dict[encomenda]['produtos'].append((nome, quantidade))

        for encomenda, detalhes in encomendas_dict.items():
            for nome, quantidade in detalhes['produtos']:
                nome_produto = nome
                quantidade_produto = quantidade

            print(f"""
Encomenda id {encomenda}:
Produtos: {nome_produto} | Quantidade: {quantidade_produto}
Prazo de entrega: {detalhes['prazo']} | Comentário: {detalhes['comentario']}""")


def listar_vendas():
    sql = '''
	SELECT venda_produto.venda, venda_produto.quantidade, vendas.data, vendas.valor_final, vendas.comentario, produtos.nome, venda_produto.valor_unitario
  
    FROM venda_produto

    INNER JOIN vendas, produtos
    WHERE (vendas.id_venda = venda_produto.venda) AND (venda_produto.produto = produtos.id_produto);
'''
    vendas_dict = dict()

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

        for venda, quantidade, data, valor_final, comentario, nome, valor_unitario in select_all:
            if venda not in vendas_dict:
                vendas_dict[venda] = {
                    'produtos': [],
                    'data': data,
                    'valor_final': valor_final,
                    'comentario': comentario
                }
            vendas_dict[venda]['produtos'].append(
                (nome, quantidade, valor_unitario))

        for venda, detalhes in vendas_dict.items():
            for nome, quantidade, valor_unitario in detalhes['produtos']:
                nome_produtos = nome
                quantidade_produtos = quantidade
                valor_un_produto = valor_unitario

            print(f'''
Venda id {venda}:
Produto: {nome_produtos} | Quantidade: {quantidade_produtos}
Valor unitário: {valor_un_produto} | Valor final: {valor_final} 
Data da venda: {data} | Comentários: {comentario}
''')


listar_vendas()

# Selects específicos


def select_produto_nome(nome_do_produto):
    sql = '''
    SELECT nome, quantidade, valor_unitario, quantidade, descricao, valor_custo 
    FROM produtos
    WHERE nome LIKE ?;
'''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{nome_do_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, quantidade, descricao, valor_custo in select_all:
            print(nome, quantidade, valor_unitario,
                  quantidade, descricao, valor_custo)


def select_produto_valor(valor_produto):
    sql = '''
    SELECT nome, quantidade, valor_unitario, quantidade, descricao, valor_custo 
    FROM produtos
    WHERE valor_unitario LIKE ?;
'''
    # valor_produto = float(valor_produto)

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{valor_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, quantidade, descricao, valor_custo in select_all:
            print(nome, quantidade, valor_unitario,
                  quantidade, descricao, valor_custo)


def select_produto_quantidade(quantidade_produto):
    sql = '''
    SELECT nome, quantidade, valor_unitario, quantidade, descricao, valor_custo 
    FROM produtos
    WHERE quantidade LIKE ?;
'''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{quantidade_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, quantidade, descricao, valor_custo in select_all:
            print(nome, quantidade, valor_unitario,
                  quantidade, descricao, valor_custo)


def select_produto_descricao(descricao_produto):
    sql = '''
    SELECT nome, quantidade, valor_unitario, quantidade, descricao, valor_custo 
    FROM produtos
    WHERE descricao LIKE ?;
'''
    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{descricao_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, quantidade, descricao, valor_custo in select_all:
            print(nome, quantidade, valor_unitario,
                  quantidade, descricao, valor_custo)


def select_encomenda_produto(nome_produto):
    sql = '''
    SELECT DISTINCT produtos.nome, encomenda_produto.quantidade, encomendas.prazo, encomendas.comentario

    FROM encomenda_produto, produtos

    INNER JOIN encomendas
    WHERE encomendas.id_encomenda = encomenda_produto.encomenda
    AND produtos.nome LIKE ?;
'''
    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{nome_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, prazo, comentario in select_all:
            print(nome, quantidade, prazo, comentario)


def select_encomenda_prazo():
    pass


def select_venda_data():
    pass


def select_venda_produto():
    pass

#
# ----------- UPDATES
#


#
# ----------- DELETES
#
