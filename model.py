import sqlite3
from hashlib import sha256

# ------------------------------ SQL ------------------------------
#
# ----------- Criação das tabelas
#

sql_table_vendedor = '''
    CREATE TABLE IF NOT EXISTS vendedor (
            id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            login TEXT NOT NULL UNIQUE,
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
            aceita_encomenda INTEGER NULL,
            descricao TEXT NULL,
            valor_custo REAL NULL
    );
    '''

sql_table_encomendas = '''
    CREATE TABLE IF NOT EXISTS encomendas (
            id_encomenda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            prazo TEXT NULL,
            status NOT NULL,
            comentario TEXT NULL
    );
    '''

sql_table_vendas = '''
    CREATE TABLE IF NOT EXISTS vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            data TEXT NOT NULL,
            valor_final REAL NOT NULL,
            status NOT NULL,
            comentario TEXT NULL
    );
    '''

# // Tabelas relacionais

sql_table_encomenda_produto = '''
    CREATE TABLE IF NOT EXISTS encomenda_produto (
        id_encomenda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NULL,

        FOREIGN KEY (id_encomenda)
                REFERENCES encomendas (id_encomenda)
        FOREIGN KEY (id_produto)
                REFERENCES produtos (id_produto)
    );
    '''

sql_table_venda_produtos = '''
    CREATE TABLE IF NOT EXISTS venda_produto (
        id_venda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unitario REAL NOT NULL,

        FOREIGN KEY (id_venda)
            REFERENCES vendas (id_venda)
        FOREIGN KEY (id_produto)
            REFERENCES produtos (id_produto)
    );
    '''

# // Views das tabelas

sql_view_produtos = '''
    CREATE VIEW IF NOT EXISTS view_produtos AS
        SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
        FROM produtos;
    '''

sql_view_encomendas = '''
    CREATE VIEW IF NOT EXISTS view_encomendas AS
        SELECT encomendas.id_encomenda, produtos.nome, encomenda_produto.quantidade, encomendas.prazo,  encomendas.status, encomendas.comentario

        FROM encomendas

        INNER JOIN encomenda_produto ON encomendas.id_encomenda = encomenda_produto.id_encomenda

        INNER JOIN produtos ON encomenda_produto.id_produto = produtos.id_produto;
    '''

sql_view_vendas = '''
    CREATE VIEW IF NOT EXISTS view_vendas AS 
        SELECT vendas.id_venda, produtos.nome, venda_produto.quantidade, vendas.data,  venda_produto.valor_unitario, vendas.valor_final, vendas.status, vendas.comentario

        FROM vendas

        INNER JOIN venda_produto ON vendas.id_venda = venda_produto.id_venda
        INNER JOIN produtos ON venda_produto.id_produto = produtos.id_produto;
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

###################################################################################################

# ------------------------------ Classes ------------------------------

# // Classes banco de dados

class Estoque():
    def __init__(self, produtos=[]):
        self.produtos = produtos

class Vendedor():
    def __init__(self, login, senha, nome, nome_loja=None):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.nome_loja = nome_loja

class Produto():
    def __init__(self, id_produto, nome=None, valor_unitario=None, quantidade=0, imagem=None, aceita_encomenda=0, descricao=None, valor_custo=None):
        self.id_produto = id_produto
        self.nome = nome
        self.valor_unitario = valor_unitario
        self.quantidade = quantidade
        self.imagem = imagem
        self.aceita_encomenda = aceita_encomenda
        self.descricao = descricao
        self.valor_custo = valor_custo

class Encomenda():
    def __init__(self, status, prazo=None, comentario=None, produtos=[]):

        self.status = status
        self.prazo = prazo
        self.comentario = comentario
        self.produtos = produtos

class Venda():
    def __init__(self, data, status, valor_final=0, comentario=None, produtos={}):
        self.data = data
        self.status = status
        self.valor_final = valor_final
        self.comentario = comentario
        self.produtos = produtos

###################################################################################################

# ------------------------------ Banco de dados ------------------------------

# ------------ Produtos ------------


def insert_produto(produto: Produto):
    'Insere um produto no banco de dados.'

    sql = '''
    INSERT INTO produtos (id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''

    if produto.imagem == '':
        produto.imagem = None

    if produto.aceita_encomenda == '':
        produto.aceita_encomenda = 2

    if produto.descricao == '':
        produto.descricao = None

    if produto.valor_custo == '':
        produto.valor_custo = None

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, (produto.id_produto, produto.nome, produto.valor_unitario, produto.quantidade,
                        produto.imagem, produto.aceita_encomenda, produto.descricao, produto.valor_custo))

def update_produto(produto: Produto):
    'Atualiza um produto no banco de dados.'

    consulta_valores = []
    valores = []

    if produto.nome is not None:
        consulta_valores.append('nome = ?')
        valores.append(produto.nome)

    if produto.valor_unitario is not None:
        consulta_valores.append('valor_unitario = ?')
        valores.append(produto.valor_unitario)

    if produto.quantidade is not None:
        consulta_valores.append('quantidade = ?')
        valores.append(produto.quantidade)

    if produto.imagem is not None:
        consulta_valores.append('imagem = ?')
        valores.append(produto.imagem)

    if produto.aceita_encomenda is not None:
        consulta_valores.append('aceita_encomenda = ?')
        valores.append(produto.aceita_encomenda)

    if produto.descricao is not None:
        consulta_valores.append('descricao = ?')
        valores.append(produto.descricao)

    if produto.valor_custo is not None:
        consulta_valores.append('valor_custo = ?')
        valores.append(produto.valor_custo)

    sql = f'''
    UPDATE produtos

    SET {', '.join(consulta_valores)}

    WHERE id_produto = {produto.id_produto}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

def delete_produto(produto: Produto):
    'Deleta um produto do banco de dados.'
    sql_delete = '''
    DELETE FROM produtos
    WHERE id_produto = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_delete, (produto.id_produto,))

def listar_produtos(estoque: Estoque):
    'Seleciona todos os produtos do banco de dados.'
    sql = '''
    SELECT id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo
        FROM view_produtos;
    '''
    produtos_dict = dict()
    lista_de_produtos = []

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

    for id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        if id_produto not in produtos_dict:
            produtos_dict[id_produto] = {
                'nome': nome,
                'valor_unitario': valor_unitario,
                'quantidade': quantidade,
                'imagem': imagem,
                'aceita_encomenda': aceita_encomenda,
                'descricao': descricao,
                'valor_custo': valor_custo
            }
            lista_de_produtos.append((nome, id_produto))

            estoque.produtos = lista_de_produtos

    return estoque.produtos

def listar_produtos_encomenda(estoque: Estoque):
    'Seleciona todos os produtos que aceiam encomenda no banco de dados.'
    sql = '''
    SELECT id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo
        FROM view_produtos
        
    WHERE aceita_encomenda = 1;
    '''
    produtos_dict = dict()
    lista_de_produtos = dict()

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

    for id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        if id_produto not in produtos_dict:
            produtos_dict[id_produto] = {
                'nome': nome,
                'valor_unitario': valor_unitario,
                'quantidade': quantidade,
                'imagem': imagem,
                'aceita_encomenda': aceita_encomenda,
                'descricao': descricao,
                'valor_custo': valor_custo
            }
            lista_de_produtos[nome] = id_produto

            estoque.produtos = lista_de_produtos

    return estoque.produtos

def select_produto_id(produto: Produto):
    'Seleciona um produto pelo ID no banco de dados.'

    sql = '''
    SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
    FROM view_produtos
    WHERE id_produto = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (produto.id_produto,))
        return cursor.fetchone()

# ------------ Vendedor ------------

def insert_vendedor(vendedor: Vendedor):
    'Insere um vendedor no banco de dados.'
    sql = '''
    INSERT INTO vendedor (login, senha, nome, nome_loja)
        VALUES (?, ?, ?, ?)
    '''

    sql_values_vendedor = [vendedor.login, vendedor.senha, vendedor.nome, vendedor.nome_loja]

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, (sql_values_vendedor))

def select_vendedor(login):
    'Seleciona um vendedor pelo login no banco de dados.'
    sql_vendedor = '''
    SELECT id_vendedor, login, senha, nome, nome_loja
    FROM vendedor
    WHERE login = ?;
    '''

    with sqlite3.connect("nize_database.db") as conexao:
        cursor = conexao.execute(sql_vendedor, (login,))
        vendedor = cursor.fetchone()
        
        return vendedor

# ------------ Encomendas ------------

def insert_encomenda(encomenda: Encomenda):
    'Insere uma encomenda no banco de dados.'

    sql_insert_encomenda = '''INSERT INTO encomendas (status, prazo, comentario) 
            VALUES (?, ?, ?)
            RETURNING id_encomenda
            '''

    sql_insert_encomenda_produto = '''
            INSERT INTO encomenda_produto (id_encomenda, id_produto, quantidade)
            VALUES (?, ?, ?);
            '''

    sql_values_encomenda = [encomenda.status,
                            encomenda.prazo, encomenda.comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql_insert_encomenda, sql_values_encomenda)

        id_encomenda = cursor.fetchone()[0]

        produtos = encomenda.produtos

        lista = []

        for item in produtos.items():
            id_produto, quantidade = item
            lista.append((id_encomenda, id_produto, quantidade))

        cursor.executemany(sql_insert_encomenda_produto, lista)

def select_encomenda_id(id_encomenda):
    'Seleciona uma encomenda pelo ID no banco de dados.'
    sql = '''
    SELECT id_encomenda, prazo, nome, quantidade, comentario, status

    FROM view_encomendas
    WHERE id_encomenda = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (id_encomenda,))
        encomenda = cursor.fetchone()
        return encomenda

def select_encomenda_status(status):
    'Seleciona encomenda pelo status no banco de dados.'
    sql = '''
    SELECT id_encomenda, prazo, nome, quantidade, comentario, status

    FROM view_encomendas
    
    WHERE status = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{status}%',))
        select_all = cursor.fetchall()

        encomendas_dict = {}

        for id_encomenda, prazo, nome, quantidade, comentario, status in select_all:
            if id_encomenda not in encomendas_dict:
                encomendas_dict[id_encomenda] = {
                    'produtos': [],
                    'prazo': prazo,
                    'comentario': comentario,
                    'status': status
                }

            encomendas_dict[id_encomenda]['produtos'].append(
                (nome, quantidade))

        return encomendas_dict

def listar_encomendas():
    sql = '''
    SELECT id_encomenda, prazo, nome, quantidade, comentario, status

    FROM view_encomendas;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

        encomendas_dict = {}

        for id_encomenda, prazo, nome, quantidade, comentario, status in select_all:
            if id_encomenda not in encomendas_dict:
                encomendas_dict[id_encomenda] = {
                    'produtos': [],
                    'prazo': prazo,
                    'comentario': comentario,
                    'status': status
                }

            encomendas_dict[id_encomenda]['produtos'].append(
                (nome, quantidade))

        return encomendas_dict

def update_encomendas(id_encomenda, encomenda: Encomenda):
    'Atualiza uma encomenda no banco de dados.'
    consulta_valores = []
    valores = []

    if encomenda.status is not None:
        consulta_valores.append('status = ?')
        valores.append(encomenda.status)

    if encomenda.prazo is not None:
        consulta_valores.append('prazo = ?')
        valores.append(encomenda.prazo)

    if encomenda.comentario is not None:
        consulta_valores.append('comentario = ?')
        valores.append(encomenda.comentario)

    sql = f'''  
    UPDATE encomendas

    SET {', '.join(consulta_valores)}

    WHERE id_encomenda = {id_encomenda}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

def delete_encomenda(id_encomenda):
    'Deleta uma encomenda do banco de dados.'
    sql_delete_tabela = '''
    DELETE FROM encomendas
    WHERE id_encomenda = ?;
    '''

    sql_delete_relacao = '''
    DELETE FROM encomenda_produto
    WHERE id_encomenda = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_delete_tabela, (id_encomenda, ))
        conexao.execute(sql_delete_relacao, (id_encomenda, ))


# ------------ Vendas ------------

def insert_venda(venda: Venda):
    'Insere uma venda no banco de dados.'
    sql = '''INSERT INTO vendas (data, status, valor_final, comentario)
        VALUES (?, ?, ?, ?)
        RETURNING id_venda;
        '''
    valor_final = 0

    sql_values_venda = [venda.data, venda.status,
                        venda.valor_final, venda.comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, sql_values_venda)
        id_venda = cursor.fetchone()[0]

        sql = f'''
                INSERT INTO venda_produto (id_venda, id_produto, quantidade, valor_unitario)
                VALUES (:id_venda, :id_produto, :quantidade, (SELECT produtos.valor_unitario FROM produtos WHERE produtos.id_produto = :id_produto));

                '''

        produtos_quantidades = list()

        for prod_quant in venda.produtos.items():
            produtos_quantidades.append(
                {
                    'id_venda': id_venda,
                    'id_produto': prod_quant[0],
                    'quantidade': prod_quant[1],
                }
            )

        cursor.executemany(sql, tuple(produtos_quantidades))

        sql_total_venda = '''SELECT SUM(venda_produto.valor_unitario * venda_produto.quantidade) as total_venda
        FROM venda_produto
        WHERE venda_produto.id_venda = ?;   
    '''

        cursor = conexao.execute(sql_total_venda, (id_venda,))

        valor_final = cursor.fetchone()[0]

        sql_update_venda = f'''
        UPDATE vendas
        SET valor_final = {valor_final}
        WHERE id_venda = {id_venda};
    '''

        cursor = conexao.execute(sql_update_venda)

def listar_vendas():
    'Seleciona todas as vendas do banco de dados.'
    sql = '''
    SELECT id_venda, quantidade, data, valor_final, comentario, nome, valor_unitario, status

    FROM view_vendas;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

        vendas_dict = dict()

        for id_venda, quantidade, data, valor_final, comentario, nome, valor_unitario, status in select_all:
            if id_venda not in vendas_dict:
                vendas_dict[id_venda] = {
                    'produtos': [],
                    'data': data,
                    'valor_final': valor_final,
                    'comentario': comentario,
                    'status': status
                }
            vendas_dict[id_venda]['produtos'].append(
                (nome, quantidade, valor_unitario))

        return vendas_dict

def update_venda(id_venda, venda: Venda):
    'Atualiza uma venda no banco de dados.'
    consulta_valores = []
    valores = []

    if venda.data is not None:
        consulta_valores.append('data = ?')
        valores.append(venda.data)

    if venda.status is not None:
        consulta_valores.append('status = ?')
        valores.append(venda.status)

    if venda.comentario is not None:
        consulta_valores.append('comentario = ?')
        valores.append(venda.comentario)

    sql = f'''  
    UPDATE vendas

    SET {', '.join(consulta_valores)}

    WHERE id_venda = {id_venda}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

def delete_venda(id_venda):
    'Deleta uma venda do banco de dados.'
    sql_delete_tabela = '''
    DELETE FROM vendas
    WHERE id_venda = ?;
    '''

    sql_delete_relacao = '''
    DELETE FROM venda_produto
    WHERE id_venda = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_delete_tabela, (id_venda, ))
        conexao.execute(sql_delete_relacao, (id_venda, ))

# ////////// Não utilizados

# def visualizar_estoque():

#     sql = '''
#     SELECT nome, valor_unitario, quantidade, imagem, descricao, valor_custo 
#     FROM view_produtos
#     WHERE quantidade > 0;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql)
#         select_all = cursor.fetchall()

#         for nome, valor_unitario, quantidade, imagem, descricao, valor_custo in select_all:
#             print(f'''
#         Nome do produto: {nome} | Quantidade: {quantidade} 
#         Valor unitário: {valor_unitario} | Imagem: {imagem}
#         Valor de custo: {valor_custo} | Descrição: {descricao}
#         ''')


# def visualizar_esgotados():
#     sql = '''
#     SELECT nome, valor_unitario, quantidade, imagem, descricao, valor_custo 
#     FROM view_produtos
#     WHERE quantidade = 0 OR quantidade = Null;
#     '''
#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql)
#         select_all = cursor.fetchall()

#         for nome, valor_unitario, quantidade, imagem, descricao, valor_custo in select_all:
#             print(f'''
#     Nome do produto: {nome} | Quantidade: {quantidade} 
#     Valor unitário: {valor_unitario} | Imagem: {imagem}
#     Valor de custo: {valor_custo} | Descrição: {descricao}
#     ''')

# def select_encomenda_produto(nome_produto):
#     sql = '''
#     SELECT id_encomenda, prazo, nome, quantidade, comentario, status

#     FROM view_encomendas
#     WHERE nome LIKE ?;
#     '''
#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{nome_produto}%',))
#         select_all = cursor.fetchall()

#         for id_encomenda, prazo, nome, quantidade, comentario, status in select_all:
#             print(
#                 f'ID: {id_encomenda} | Produto: {nome} | Quantidade: {quantidade} | Prazo: {prazo} | Status: {status} | Comentário: {comentario}')


# def select_encomenda_prazo(prazo_encomenda):
#     sql = '''
#     SELECT id_encomenda, prazo, nome, quantidade, comentario, status

#     FROM view_encomendas
    
#     WHERE prazo LIKE ?;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{prazo_encomenda}%',))
#         select_all = cursor.fetchall()

#         for id_encomenda, prazo, nome, quantidade, comentario, status in select_all:
#             print(
#                 f'ID: {id_encomenda} | Nome: {nome} | Quantidade: {quantidade} | Prazo: {prazo} | Status: {status} | Comentário: {comentario}')

# ---------- Vendas



# def update_quantidade(quantidade_vendida, produto: Produto):
#     'Atualiza a quantidade de um produto no banco de dados.'
#     sql = '''UPDATE quantidade 
#     SET quantidade = ?
#     WHERE id_produto = ?;'''

#     sql_quantidade = "SELECT quantidade FROM produtos WHERE id_produto = ?;"
    
#     sql_subtracao = "SELECT ? - ? as difference;"


#     with sqlite3.connect('nize_database.db') as conexao:
#         quantidade_total = conexao.execute(sql_quantidade)

#         cursor = conexao.execute()


#     # https://www.beekeeperstudio.io/blog/sqlite-subtract

#     #         sql_total_venda = '''SELECT SUM(venda_produto.valor_unitario * venda_produto.quantidade) as total_venda
#     #     FROM venda_produto
#     #     WHERE venda_produto.id_venda = ?;   
#     # '''

def select_produto_nome(nome_do_produto):
    'Seleciona um produto pelo nome.'
    
    sql = '''
    SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
    FROM view_produtos
    WHERE nome = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'{nome_do_produto}',))
        produto = cursor.fetchone()
        return produto

# def select_produto_nome(nome_do_produto):
#     'Seleciona um produto pelo nome.'

#     sql = '''
#     SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
#     FROM view_produtos
#     WHERE nome LIKE ?;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{nome_do_produto}%',))
#         select_all = cursor.fetchall()

#         for id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
#             print(f'''
#             Produto ID: {id_produto}
#             Nome: {nome} | Quantidade: {quantidade}
#             Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
#             Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
#             ''')


# def select_produto_valor(valor_produto):  
    
#     sql = '''
#     SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
#     FROM view_produtos
#     WHERE valor_unitario LIKE ?;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{valor_produto}%',))
#         select_all = cursor.fetchall()

#         for id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
#             print(f'''
#             Produto ID: {id_produto}
#             Nome: {nome} | Quantidade: {quantidade}
#             Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
#             Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
#             ''')


# def select_produto_quantidade(quantidade_produto):
#     sql = '''
#     SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
#     FROM view_produtos
#     WHERE quantidade LIKE ?;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{quantidade_produto}%',))
#         select_all = cursor.fetchall()

#         for id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
#             print(f'''
#             Produto ID: {id_produto}
#             Nome: {nome} | Quantidade: {quantidade}
#             Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
#             Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
#             ''')


# def select_produto_descricao(descricao_produto):
#     sql = '''
#     SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
#     FROM view_produtos
#     WHERE descricao LIKE ?;
#     '''
#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{descricao_produto}%',))
#         select_all = cursor.fetchall()

#         for id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
#             print(f'''
#             Produto ID: {id_produto}
#             Nome: {nome} | Quantidade: {quantidade}
#             Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
#             Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
#             ''')


# def select_venda_data(data_venda):
#     sql = '''
#     SELECT id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status

#     FROM view_vendas 

#     WHERE data LIKE ?;
#     '''
#     vendas_dict = dict()

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{data_venda}%',))
#         select_all = cursor.fetchall()

#         for id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status in select_all:
#             if id_venda not in vendas_dict:
#                 vendas_dict[id_venda] = {
#                     'produtos': [],
#                     'data': data,
#                     'valor_final': valor_final,
#                     'comentario': comentario,
#                     'status': status
#                 }
#             vendas_dict[id_venda]['produtos'].append(
#                 (nome, quantidade, valor_unitario))

#         for id_venda, detalhes in vendas_dict.items():
#             nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])
#                              for nome, quantidade, valor_unitario in detalhes['produtos']]

#             print(f'''
#     Venda ID {id_venda}:
#     Produtos:
#     {'\n'.join(nome_produtos)} 
#     Valor final: {valor_final} | Status: {status}
#     Data da venda: {data} | Comentários: {comentario}
#     ''')


# def select_venda_produto(nome_produto):
#     sql = '''
#     SELECT id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status

#     FROM view_vendas 

#     WHERE nome LIKE ?;
#     '''

#     vendas_dict = dict()

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{nome_produto}%',))
#         select_all = cursor.fetchall()

#         for id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status in select_all:
#             if id_venda not in vendas_dict:
#                 vendas_dict[id_venda] = {
#                     'produtos': [],
#                     'data': data,
#                     'valor_final': valor_final,
#                     'comentario': comentario,
#                     'status': status
#                 }
#             vendas_dict[id_venda]['produtos'].append(
#                 (nome, quantidade, valor_unitario))

#         for id_venda, detalhes in vendas_dict.items():
#             nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])

#                              for nome, quantidade, valor_unitario in detalhes['produtos']]

#             print(f'''
#     Venda ID {id_venda}:
#     Produtos:
#     {'\n'.join(nome_produtos)} 
#     Valor final: {valor_final} | Status: {status}
#     Data da venda: {data} | Comentários: {comentario}
#     ''')


# ------------ Updates ------------

# def update_vendedor(id_vendedor, login=None, senha=None, nome=None, nome_loja=None):
    # consulta_valores = []
    # valores = []

    # if login is not None:
    #     consulta_valores.append('login = ?')
    #     valores.append(login)

    # if senha is not None:
    #     consulta_valores.append('senha = ?')
    #     valores.append(senha)

    # if nome is not None:
    #     consulta_valores.append('nome = ?')
    #     valores.append(nome)

    # if nome_loja is not None:
    #     consulta_valores.append('nome_loja = ?')
    #     valores.append(nome_loja)

    # sql = f'''
    # UPDATE vendedor

    # SET {', '.join(consulta_valores)}

    # WHERE id_vendedor = {id_vendedor}
    # '''

    # with sqlite3.connect('nize_database.db') as conexao:
    #     conexao.execute(sql, valores)


# ------------ Deletes ------------


# def delete_vendedor(login):
#     sql_delete = '''
#     DELETE FROM produtos
#     WHERE login = ?;
#     '''
#     with sqlite3.connect("nize_database.db") as conexao:
#         conexao.execute(sql_delete, (login))
