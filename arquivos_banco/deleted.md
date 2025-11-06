sql_table_deleted_produtos = '''
    CREATE TABLE IF NOT EXISTS deleted_produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nome TEXT NOT NULL,
            valor_unitario REAL NOT NULL,

            quantidade INTEGER NULL,
            imagem TEXT NULL,
            aceita_encomenda INTEGER NULL,
            descricao TEXT NULL,
            valor_custo REAL NULL,

            data_deletado TEXTO NOT NULL
    );
    '''

sql_table_deleted_encomendas = '''
    CREATE TABLE IF NOT EXISTS deleted_encomendas(
        id_encomenda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        prazo TEXT NULL,
        status NOT NULL,
        comentario TEXT NULL,
        data_deletado TEXTO NOT NULL
        );
    '''

sql_table_deleted_vendas = '''
    CREATE TABLE IF NOT EXISTS deleted_vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            data TEXT NOT NULL,
            valor_final REAL NOT NULL,
            status NOT NULL,
            comentario TEXT NULL,
            data_deletado TEXTO NOT NULL
    );
    '''

sql_table_deleted_encomenda_produto = '''
    CREATE TABLE IF NOT EXISTS deleted_encomenda_produto (
        id_encomenda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NULL,
        data_deletado TEXTO NOT NULL,


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
        data_deletado TEXTO NOT NULL,

        FOREIGN KEY (id_venda)
            REFERENCES vendas (id_venda)
        FOREIGN KEY (id_produto)
            REFERENCES produtos (id_produto)


    );
    '''

    conexao.execute(sql_table_deleted_encomendas)
    conexao.execute(sql_table_deleted_produtos)
    conexao.execute(sql_table_deleted_vendas)
    conexao.execute(sql_table_deleted_encomenda_produto)
    conexao.execute(sql_table_deleted_venda_produtos)

def delete_produto(produto: Produto):
    sql_insert = '''
    INSERT INTO deleted_produtos (id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    SELECT id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo
        FROM Produtos

    WHERE id_produto = ?;
    '''

    sql_delete = '''
    DELETE FROM produtos
    WHERE id_produto = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_insert, (produto.id_produto,))
        conexao.execute(sql_delete, (produto.id_produto,))


def delete_encomenda(id_encomenda):
    sql_insert_tabela = '''
    INSERT INTO deleted_encomendas (id_encomenda, prazo, status, comentario)

    SELECT id_encomenda, prazo, status, comentario
        FROM encomendas
        
    WHERE id_encomenda = ?;
    '''

    sql_insert_relacao = '''
    INSERT INTO deleted_encomenda_produto (id_encomenda, id_produto, quantidade)
    
    SELECT id_encomenda, id_produto, quantidade
        FROM encomenda_produto
    
    WHERE id_encomenda = ?;

    '''

    sql_delete_tabela = '''
    DELETE FROM encomendas
    WHERE id_encomenda = ?;
    '''

    sql_delete_relacao = '''
    DELETE FROM encomenda_produto
    WHERE id_encomenda = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_insert_tabela, (id_encomenda, ))
        conexao.execute(sql_insert_relacao, (id_encomenda, ))
        conexao.execute(sql_delete_tabela, (id_encomenda, ))
        conexao.execute(sql_delete_relacao, (id_encomenda, ))


def delete_venda(id_venda):
    sql_insert_tabela = '''
    INSERT INTO deleted_vendas (id_venda, data, valor_final, status, comentario)

    SELECT id_venda, data, valor_final, status, comentario
        FROM vendas
        
    WHERE id_venda = ?;
    '''

    sql_insert_relacao = '''
    INSERT INTO deleted_venda_produto (id_venda, id_produto, quantidade, valor_unitario)
    
    SELECT id_venda, id_produto, quantidade, valor_unitario
        FROM venda_produto
    
    WHERE id_venda = ?;

    '''

    sql_delete_tabela = '''
    DELETE FROM vendas
    WHERE id_venda = ?;
    '''

    sql_delete_relacao = '''
    DELETE FROM venda_produto
    WHERE id_venda = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_insert_tabela, (id_venda, ))
        conexao.execute(sql_insert_relacao, (id_venda, ))
        conexao.execute(sql_delete_tabela, (id_venda, ))
        conexao.execute(sql_delete_relacao, (id_venda, ))