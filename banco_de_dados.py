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

# Views das tabelas

sql_view_produtos = '''
    CREATE VIEW IF NOT EXISTS view_produtos AS
        SELECT nome, valor_unitario, quantidade, imagem, encomenda, descricao, valor_custo
        FROM produtos;
    '''

sql_view_encomendas = '''
    CREATE VIEW IF NOT EXISTS view_encomendas AS
        SELECT encomendas.id_encomenda, encomendas.prazo, produtos.nome, encomenda_produto.quantidade, encomendas.comentario
        FROM encomendas
        INNER JOIN encomenda_produto ON encomendas.id_encomenda = encomenda_produto.encomenda
        INNER JOIN produtos ON encomenda_produto.produto = produtos.id_produto;
    '''

sql_view_vendas = '''
    CREATE VIEW IF NOT EXISTS view_vendas AS 
        SELECT vendas.id_venda, venda_produto.venda, venda_produto.quantidade, vendas.data, vendas.valor_final, vendas.comentario, produtos.nome, venda_produto.valor_unitario

        FROM vendas

        INNER JOIN venda_produto ON vendas.id_venda = venda_produto.venda
        INNER JOIN produtos ON venda_produto.produto = produtos.id_produto;
    '''

# ----------- Inserção de tabelas no banco

with sqlite3.connect('nize_database.db') as conexao:
    conexao.execute(sql_table_vendedor)
    conexao.execute(sql_table_produtos)
    conexao.execute(sql_table_encomendas)
    conexao.execute(sql_table_vendas)
    conexao.execute(sql_table_encomenda_produto)
    conexao.execute(sql_table_venda_produtos)
    conexao.execute(sql_view_produtos)
    conexao.execute(sql_view_encomendas)
    conexao.execute(sql_view_vendas)

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
        FROM view_produtos;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

    for nome, valor_unitario, quantidade, _imagem, encomenda, descricao, valor_custo in select_all:
        print(f'''
    Nome: {nome} | Custo: {valor_custo} | Valor unitário: {valor_unitario}
    Quantidade: {quantidade} | Aceita encomenda: {encomenda} | Descrição: {descricao}''')


def listar_encomendas():  # print só está mostrando um produto
    sql = '''
    SELECT id_encomenda, prazo, nome, quantidade, comentario

    FROM view_encomendas;
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

            nome_produtos = [', '.join([f'{nome}, ({quantidade})'])
                             for nome, quantidade in detalhes['produtos']]

            print(f"""
    Encomenda id {encomenda}:
    Produtos: {', '.join(nome_produtos)}
    Prazo de entrega: {detalhes['prazo']} | Comentário: {detalhes['comentario']}""")


def listar_vendas():  # print só está mostrando um produto
    sql = '''
    SELECT venda, quantidade, data, valor_final, comentario, nome, valor_unitario

    FROM view_vendas;
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
            nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])
                             for nome, quantidade, valor_unitario in detalhes['produtos']]

            print(f'''
    Venda id {venda}:
    Produtos: 
    {'\n'.join(nome_produtos)}
    Valor unitário: {valor_unitario} | Valor final: {valor_final} 
    Data da venda: {data} | Comentários: {comentario}
    ''')

# Selects específicos


def select_produto_nome(nome_do_produto):
    sql = '''
    SELECT nome, quantidade, valor_unitario, quantidade, descricao, valor_custo 
    FROM view_produtos
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
    FROM view_produtos
    WHERE valor_unitario LIKE ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{valor_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, quantidade, descricao, valor_custo in select_all:
            print(nome, quantidade, valor_unitario,
                  quantidade, descricao, valor_custo)


def select_produto_quantidade(quantidade_produto):
    sql = '''
    SELECT nome, quantidade, valor_unitario, quantidade, descricao, valor_custo 
    FROM view_produtos
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
    FROM view_produtos
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
    SELECT prazo, nome, quantidade, comentario

    FROM view_encomendas
    WHERE nome LIKE ?;
'''
    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{nome_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, prazo, comentario in select_all:
            print(
                f'Produto: {nome} | Quantidade: {quantidade} | Prazo: {prazo} | Comentário: {comentario}')


def select_encomenda_prazo(prazo_encomenda):  # Não deu certo o SQL
    sql = '''
    SELECT prazo, nome, quantidade, comentario

    FROM view_encomendas
    
    WHERE prazo LIKE ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{prazo_encomenda}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, prazo, comentario in select_all:
            print(
                f'Nome: {nome} | Quantidade: {quantidade} | Prazo: {prazo} | Comentário: {comentario}')


def select_venda_data(data_venda):  # Não deu certo o SQL
    sql = '''
    SELECT id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario

    FROM view_vendas 

    WHERE data LIKE ?;
    '''
    vendas_dict = dict()

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{data_venda}%',))
        select_all = cursor.fetchall()

        for id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario in select_all:
            if id_venda not in vendas_dict:
                vendas_dict[id_venda] = {
                    'produtos': [],
                    'data': data,
                    'valor_final': valor_final,
                    'comentario': comentario,
                }
            vendas_dict[id_venda]['produtos'].append(
                (nome, quantidade, valor_unitario))

        for id_venda, detalhes in vendas_dict.items():
            nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])
                             for nome, quantidade, valor_unitario in detalhes['produtos']]

            print(f'''
    Venda ID {id_venda}:
    Produtos:
    {'\n'.join(nome_produtos)} 
    Valor final: {valor_final}
    Data da venda: {data} | Comentários: {comentario}
    ''')


def select_venda_produto(nome_produto):  # Não deu certo o SQL
    sql = '''
    SELECT id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario

    FROM view_vendas 

    WHERE nome LIKE ?;
    '''

    vendas_dict = dict()

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{nome_produto}%',))
        select_all = cursor.fetchall()

        for id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario in select_all:
            if id_venda not in vendas_dict:
                vendas_dict[id_venda] = {
                    'produtos': [],
                    'data': data,
                    'valor_final': valor_final,
                    'comentario': comentario,
                }
            vendas_dict[id_venda]['produtos'].append(
                (nome, quantidade, valor_unitario))

        for id_venda, detalhes in vendas_dict.items():
            nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])
                             for nome, quantidade, valor_unitario in detalhes['produtos']]

            print(f'''
    Venda ID {id_venda}:
    Produtos:
    {'\n'.join(nome_produtos)} 
    Valor final: {valor_final}
    Data da venda: {data} | Comentários: {comentario}
    ''')

#
# ----------- UPDATES
#


#
# ----------- DELETES
#
