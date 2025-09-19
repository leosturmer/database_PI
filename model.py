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

# Tabelas relacionais

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

# Views das tabelas

sql_view_produtos = '''
    CREATE VIEW IF NOT EXISTS view_produtos AS
        SELECT nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
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


#### Tabelas DELETED


sql_table_deleted_produtos = '''
    CREATE TABLE IF NOT EXISTS deleted_produtos (
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

sql_table_deleted_encomendas = '''
    CREATE TABLE IF NOT EXISTS deleted_encomendas(
        id_encomenda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        prazo TEXT NULL,
        status NOT NULL,
        comentario TEXT NULL
        );
    '''

sql_table_deleted_vendas = '''
    CREATE TABLE IF NOT EXISTS deleted_vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            data TEXT NOT NULL,
            valor_final REAL NOT NULL,
            status NOT NULL,
            comentario TEXT NULL
    );
    '''

sql_table_deleted_encomenda_produto = '''
    CREATE TABLE IF NOT EXISTS deleted_encomenda_produto (
        id_encomenda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
            quantidade INTEGER NULL,

            FOREIGN KEY (id_encomenda)
                    REFERENCES encomendas (id_encomenda)
            FOREIGN KEY (id_produto)
                    REFERENCES produtos (id_produto)
    );
    '''

sql_table_deleted_venda_produtos = '''
    CREATE TABLE IF NOT EXISTS deleted_venda_produto (
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

    conexao.execute(sql_table_deleted_encomendas)
    conexao.execute(sql_table_deleted_produtos)
    conexao.execute(sql_table_deleted_vendas)
    conexao.execute(sql_table_deleted_encomenda_produto)
    conexao.execute(sql_table_deleted_venda_produtos)


# ## Classes banco de dados

class Loja():
    pass

class Vendedor(Loja):
    pass

class Produto():
    def __init__(self):
        self.nome = ''
        self.quantidade = 0
        self.valor_venda = 0.0
        self.imagem = ''
        self.encomenda = ''
        self.descricao = ''
        self.valor_custo = 0.0


class Venda():
    def __init__(self):
        import datetime

        self.data_venda = datetime.datetime.now()
        self.valor_final = 0.0
        self.comentario = ''
        self.produtos = ''


class Encomenda():
    def __init__(self):
        import datetime

        self.prazo = datetime.timedelta()
        self.quantidade = 0
        self.comentario = ''
        self.produtos = ''
        self.status = 0
