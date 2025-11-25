def select_vendedor_id(id_vendedor):
    sql = '''
    SELECT id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo, vendedor FROM produtos
    WHERE id_vendedor = ?
    '''

    with sqlite3.connect("nize_database.db") as conexao:
        cursor = conexao.execute(sql, (id_vendedor,))
        produtos = cursor.fetchall()

        return produtos
    

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
            valor_custo REAL NULL,

            vendedor INT NOT NULL,
            FOREIGN KEY (vendedor) REFERENCES vendedor (id_vendedor)
    );
    '''

sql_table_encomendas = '''
    CREATE TABLE IF NOT EXISTS encomendas (
            id_encomenda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            prazo TEXT NULL,
            status NOT NULL,
            comentario TEXT NULL,

            vendedor INT NOT NULL,
            FOREIGN KEY (vendedor) REFERENCES vendedor (id_vendedor)
    );
    '''

sql_table_vendas = '''
    CREATE TABLE IF NOT EXISTS vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            data TEXT NOT NULL,
            valor_final REAL NOT NULL,
            status NOT NULL,
            comentario TEXT NULL,

            vendedor INT NOT NULL,
            FOREIGN KEY (vendedor) REFERENCES vendedor (id_vendedor)
    );
    '''

# Tabelas relacionais

sql_table_encomenda_produto = '''
    CREATE TABLE IF NOT EXISTS encomenda_produto (
        id_encomenda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
            quantidade INTEGER NULL,
            
            vendedor INT NOT NULL,
            FOREIGN KEY (vendedor) REFERENCES vendedor (id_vendedor)

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

        vendedor INT NOT NULL,
        FOREIGN KEY (vendedor) REFERENCES vendedor (id_vendedor)

        FOREIGN KEY (id_venda)
            REFERENCES vendas (id_venda)
        FOREIGN KEY (id_produto)
            REFERENCES produtos (id_produto)
    );
    '''

# Views das tabelas

sql_view_produtos = '''
    CREATE VIEW IF NOT EXISTS view_produtos AS
        SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem, vendedor
        FROM produtos;
    '''

sql_view_encomendas = '''
    CREATE VIEW IF NOT EXISTS view_encomendas AS
        SELECT encomendas.id_encomenda, produtos.nome, encomenda_produto.quantidade, encomendas.prazo,  encomendas.status, encomendas.comentario, encomendas.vendedor

        FROM encomendas

        INNER JOIN encomenda_produto ON encomendas.id_encomenda = encomenda_produto.id_encomenda

        INNER JOIN produtos ON encomenda_produto.id_produto = produtos.id_produto;
    '''

sql_view_vendas = '''
    CREATE VIEW IF NOT EXISTS view_vendas AS 
        SELECT vendas.id_venda, produtos.nome, venda_produto.quantidade, vendas.data,  venda_produto.valor_unitario, vendas.valor_final, vendas.status, vendas.comentario, vendas.vendedor

        FROM vendas

        INNER JOIN venda_produto ON vendas.id_venda = venda_produto.id_venda
        INNER JOIN produtos ON venda_produto.id_produto = produtos.id_produto;
    '''