class Vendedor():
    def __init__(self):
        self.nome = ''

### Produtos
    def cadastrar_produto(self):
        pass

    def pesquisar_produto(self):
        pass

    def atualizar_produto(self):
        pass

    def deletar_produto(self):
        pass
    
### Vendas

    def cadastrar_venda(self):
        pass

    def pesquisar_venda(self): # ?
        pass

    def atualizar_venda(self): # ?
        pass

    def deletar_venda(self): # ?
        pass

### Encomendas

    def cadastrar_encomenda(self):
        pass

    def pesquisar_encomenda(self): # ? 
        pass

    def atualizar_encomenda(self): # ? 
        pass

    def deletar_encomenda(self): #?#
        pass

### Estoque

    def visualizar_estoque(self):
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