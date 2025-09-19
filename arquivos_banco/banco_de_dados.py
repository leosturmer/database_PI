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

### Colocar vendedor

def insert_vendedor(self, login, senha, nome, nome_loja=None):
    sql = '''
    INSERT INTO vendedor (login, senha, nome, nome_loja)
        VALUES (?, ?, ?, ?)
    '''

    sql_values_vendedor = [login, senha, nome, nome_loja]

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, sql_values_vendedor)

def update_vendedor(self, id_vendedor, login=None, senha=None, nome=None, nome_loja=None):
    consulta_valores = []
    valores = []

    if login is not None:
        consulta_valores.append('login = ?')
        valores.append(login)

    if senha is not None:
        consulta_valores.append('senha = ?')
        valores.append(senha)

    if nome is not None:
        consulta_valores.append('nome = ?')
        valores.append(nome)

    if nome_loja is not None:
        consulta_valores.append('nome_loja = ?')
        valores.append(nome_loja)

    sql = f'''
    UPDATE vendedor

    SET {', '.join(consulta_valores)}

    WHERE id_vendedor = {id_vendedor}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

### Estoque

def visualizar_estoque(self):
    
    sql = '''
    SELECT nome, valor_unitario, quantidade, imagem, descricao, valor_custo 
    FROM view_produtos
    WHERE quantidade > 0;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

        for nome, valor_unitario, quantidade, imagem, descricao, valor_custo in select_all:
            print(f'''
        Nome do produto: {nome} | Quantidade: {quantidade} 
        Valor unitário: {valor_unitario} | Imagem: {imagem}
        Valor de custo: {valor_custo} | Descrição: {descricao}
        ''')

def visualizar_esgotados(self):
    sql = '''
    SELECT nome, valor_unitario, quantidade, imagem, descricao, valor_custo 
    FROM view_produtos
    WHERE quantidade = 0 OR quantidade = Null;
    '''
    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

        for nome, valor_unitario, quantidade, imagem, descricao, valor_custo in select_all:
            print(f'''
    Nome do produto: {nome} | Quantidade: {quantidade} 
    Valor unitário: {valor_unitario} | Imagem: {imagem}
    Valor de custo: {valor_custo} | Descrição: {descricao}
    ''')

### Produtos

### Cadastro de produtos: 

def insert_produto(self, nome, valor_unitario, quantidade=None, imagem=None, aceita_encomenda=0, descricao=None, valor_custo=None):

    sql = '''INSERT INTO produtos (nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
    sql_values_produtos = [nome, valor_unitario, quantidade,
                        imagem, aceita_encomenda, descricao, valor_custo]

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, sql_values_produtos)


### Pesquisa de produtos:

def listar_produtos(self): # Lista TODOS os produtos da loja
    sql = '''
    SELECT nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo
        FROM view_produtos;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

    for nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        print(f'''
    Nome: {nome} | Custo: {valor_custo} | Valor unitário: {valor_unitario}
    Quantidade: {quantidade} | Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
    Imagem: {imagem}''')

def select_produto_nome(self, nome_do_produto): ### Pesquisa produto pelo nome
    sql = '''
    SELECT nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
    FROM view_produtos
    WHERE nome LIKE ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{nome_do_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
            print(f'''
            Nome: {nome} | Quantidade: {quantidade}
            Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
            Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
            ''')

def select_produto_valor(self, valor_produto): ### Pesquisa produto pelo valor
    sql = '''
    SELECT nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
    FROM view_produtos
    WHERE valor_unitario LIKE ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{valor_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
            print(f'''
            Nome: {nome} | Quantidade: {quantidade}
            Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
            Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
            ''')

def select_produto_quantidade(self, quantidade_produto): ### Pesquisa produto pela quantidade
    sql = '''
    SELECT nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
    FROM view_produtos
    WHERE quantidade LIKE ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{quantidade_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
            print(f'''
            Nome: {nome} | Quantidade: {quantidade}
            Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
            Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
            ''')

def select_produto_descricao(self, descricao_produto): ### Pesquisa produto pela descrição
    sql = '''
    SELECT nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
    FROM view_produtos
    WHERE descricao LIKE ?;
    '''
    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{descricao_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
            print(f'''
            Nome: {nome} | Quantidade: {quantidade}
            Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
            Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
            ''')

### Atualização de produtos
def update_produtos(self, id_produto, nome=None, valor_unitario=None, quantidade=None, imagem=None, aceita_encomenda=0, descricao=None, valor_custo=None):

    consulta_valores = []
    valores = []

    if nome is not None:
        consulta_valores.append('nome = ?')
        valores.append(nome)

    if valor_unitario is not None:
        consulta_valores.append('valor_unitario = ?')
        valores.append(valor_unitario)

    if quantidade is not None:
        consulta_valores.append('quantidade = ?')
        valores.append(quantidade)

    if imagem is not None:
        consulta_valores.append('imagem = ?')
        valores.append(imagem)

    if aceita_encomenda is not None:
        consulta_valores.append('aceita_encomenda = ?')
        valores.append(aceita_encomenda)

    if descricao is not None:
        consulta_valores.append('descricao = ?')
        valores.append(descricao)

    if valor_custo is not None:
        consulta_valores.append('valor_custo = ?')
        valores.append(valor_custo)

    sql = f'''
    UPDATE produtos

    SET {', '.join(consulta_valores)}

    WHERE id_produto = {id_produto}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

### Remoção de produtos (FAZER)

def delete_produto(self, id_produto):
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
        conexao.execute(sql_insert, (id_produto,))
        conexao.execute(sql_delete, (id_produto,))

### Encomendas

### Cadastro de encomenda

def insert_encomenda(self, status, prazo=None, comentario=None, produtos=[]):

    sql = '''INSERT INTO encomendas (status, prazo, comentario) 
                        VALUES (?, ?, ?)
                        RETURNING id_encomenda
                        '''

    sql_values_encomenda = [status, prazo, comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, sql_values_encomenda)
        id_encomenda = cursor.fetchone()[0]

        sql = f'''
                INSERT INTO encomenda_produto (id_encomenda, id_produto, quantidade)
                VALUES ({id_encomenda}, ?, ?);
                '''

        cursor.executemany(sql, tuple(produtos))

### Pesquisa de encomenda

def listar_encomendas(self):
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

            encomendas_dict[id_encomenda]['produtos'].append((nome, quantidade))

        for id_encomenda, detalhes in encomendas_dict.items():

            nome_produtos = [', '.join([f'{nome}, ({quantidade})'])
                            for nome, quantidade in detalhes['produtos']]

            print(f"""
    Encomenda id {id_encomenda}:
    Produtos: {', '.join(nome_produtos)}
    Prazo de entrega: {detalhes['prazo']} | Status: {status} | Comentário: {detalhes['comentario']}""")

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@
# NÃO ESTÁ FUNCIONANDO DIREITO
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@

def select_encomenda_produto(self, nome_produto):
    sql = '''
    SELECT prazo, nome, quantidade, comentario, status

    FROM view_encomendas
    WHERE nome LIKE ?;
    '''
    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{nome_produto}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, prazo, comentario, status in select_all:
            print(
                f'Produto: {nome} | Quantidade: {quantidade} | Prazo: {prazo} | Status: {status} | Comentário: {comentario}')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@
# NÃO ESTÁ FUNCIONANDO DIREITO
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@

def select_encomenda_prazo(self, prazo_encomenda):
    sql = '''
    SELECT prazo, nome, quantidade, comentario, status

    FROM view_encomendas
    
    WHERE prazo LIKE ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{prazo_encomenda}%',))
        select_all = cursor.fetchall()

        for nome, quantidade, prazo, comentario, status in select_all:
            print(
                f'Nome: {nome} | Quantidade: {quantidade} | Prazo: {prazo} | Status: {status} | Comentário: {comentario}')

### Atualização de encomendas

def update_encomendas(self, id_encomenda, prazo=None, comentario=None, status=None):
    consulta_valores = []
    valores = []

    if prazo is not None:
        consulta_valores.append('prazo = ?')
        valores.append(prazo)

    if comentario is not None:
        consulta_valores.append('comentario = ?')
        valores.append(comentario)

    if status is not None:
        consulta_valores.append('status = ?')
        valores.append(status)

    sql = f'''  
    UPDATE encomendas

    SET {', '.join(consulta_valores)}

    WHERE id_encomenda = {id_encomenda}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

### Remoção de encomendas (FAZER)

def delete_encomenda(self, id_encomenda):
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

### Vendas

### Cadastro de vendas

def insert_venda(self, data, status, valor_final=0, comentario=None, produtos=[]):
    sql = '''INSERT INTO vendas (data, status, valor_final, comentario)
        VALUES (?, ?, ?, ?)
        RETURNING id_venda;
        '''

    sql_values_venda = [data, status, valor_final, comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, sql_values_venda)
        id_venda = cursor.fetchone()[0]

        sql = f'''
                INSERT INTO venda_produto (id_venda, id_produto, quantidade, valor_unitario)
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

        sql_total_venda = '''SELECT SUM(venda_produto.valor_unitario * venda_produto.quantidade) as total_venda
        FROM venda_produto
        WHERE venda_produto.id_venda = ?;   
    '''
        valor_final = 0

        cursor = conexao.execute(sql_total_venda, (id_venda,))

        valor_final = cursor.fetchone()[0]

        sql_update_venda = f'''
        UPDATE vendas
        SET valor_final = {valor_final}
        WHERE id_venda = {id_venda};
    '''

        cursor = conexao.execute(sql_update_venda)

### Pesquisa de vendas


def listar_vendas(self):  
    sql = '''
    SELECT id_venda, quantidade, data, valor_final, comentario, nome, valor_unitario, status

    FROM view_vendas;
    '''
    vendas_dict = dict()

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

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

        for id_venda, detalhes in vendas_dict.items():
            nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])
                            for nome, quantidade, valor_unitario in detalhes['produtos']]

            print(f'''
    Venda id {id_venda}:
    Produtos: 
    {'\n'.join(nome_produtos)}
    Valor unitário: {valor_unitario} | Valor final: {valor_final} 
    Status: {status} | Data da venda: {data} | Comentários: {comentario}
    ''')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@
# NÃO ESTÁ FUNCIONANDO DIREITO
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@         
    
def select_venda_data(self, data_venda): 
    sql = '''
    SELECT id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status

    FROM view_vendas 

    WHERE data LIKE ?;
    '''
    vendas_dict = dict()

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{data_venda}%',))
        select_all = cursor.fetchall()

        for id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status in select_all:
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

        for id_venda, detalhes in vendas_dict.items():
            nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])
                            for nome, quantidade, valor_unitario in detalhes['produtos']]

            print(f'''
    Venda ID {id_venda}:
    Produtos:
    {'\n'.join(nome_produtos)} 
    Valor final: {valor_final} | Status: {status}
    Data da venda: {data} | Comentários: {comentario}
    ''')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@
# NÃO ESTÁ FUNCIONANDO DIREITO
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@

def select_venda_produto(self, nome_produto):
    sql = '''
    SELECT id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status

    FROM view_vendas 

    WHERE nome LIKE ?;
    '''

    vendas_dict = dict()

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{nome_produto}%',))
        select_all = cursor.fetchall()

        for id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status in select_all:
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

        for id_venda, detalhes in vendas_dict.items():
            nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])

                            for nome, quantidade, valor_unitario in detalhes['produtos']]

            print(f'''
    Venda ID {id_venda}:
    Produtos:
    {'\n'.join(nome_produtos)} 
    Valor final: {valor_final} | Status: {status}
    Data da venda: {data} | Comentários: {comentario}
    ''')

### Atualização de encomendas

def update_vendas(self, id_venda=None, data=None, comentario=None, status=None):  # Ver se coloco STATUS na venda
    consulta_valores = []
    valores = []

    if data is not None:
        consulta_valores.append('data = ?')
        valores.append(data)

    if comentario is not None:
        consulta_valores.append('comentario = ?')
        valores.append(comentario)

    if status is not None:
        consulta_valores.append('status = ?')
        valores.append(status)

    sql = f'''  
    UPDATE vendas

    SET {', '.join(consulta_valores)}

    WHERE id_venda = {id_venda}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

### Remoção de encomendas (FAZER)

def delete_venda(self, id_venda):
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






# class Produto():
#     def __init__(self):
#         self.nome = ''
#         self.quantidade = 0
#         self.valor_venda = 0.0
#         self.imagem = ''
#         self.encomenda = ''
#         self.descricao = ''
#         self.valor_custo = 0.0


# class Venda():
#     def __init__(self):
#         import datetime

#         self.data_venda = datetime.datetime.now()
#         self.valor_final = 0.0
#         self.comentario = ''
#         self.produtos = ''


# class Encomenda():
#     def __init__(self):
#         import datetime

#         self.prazo = datetime.timedelta()
#         self.quantidade = 0
#         self.comentario = ''
#         self.produtos = ''
#         self.status = 0
