import controller

from textual.app import (App, ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput, OptionList, Select, SelectionList)
from textual.screen import (Screen)
from textual.containers import (
    Container, VerticalGroup, HorizontalGroup, Grid, Center)


class TelaProdutos(Screen):

    def compose(self):
        yield Header(show_clock=True)
        yield Static('Cadastro de produtos')

        yield Input(
            placeholder='Nome do produto*',
            valid_empty=False,
            type='text',
            max_length=50,
            id='input_nome'
        )
        yield Input(
            placeholder='Quantidade*',
            valid_empty=False,
            type='integer',
            max_length=4,
            id='input_quantidade'
        )
        yield Input(
            placeholder='Valor unitário',
            valid_empty=True,
            type='number',
            max_length=7,
            id='input_valor_unitario'
        )
        yield Input(
            placeholder='Valor de custo',
            valid_empty=True,
            type='number',
            max_length=7,
            id='input_valor_custo'
        )
        yield Input(
            placeholder='Imagem',
            valid_empty=True,
            type='text',
            id='input_imagem'
        )
        with HorizontalGroup():
            yield Label('Aceita encomendas?')
            yield Select([
                    ("Sim", 1),
                    ("Não", 2)
                ],
                allow_blank=False, 
                value=2,
                id='select_encomenda'
            )

        yield TextArea(
            placeholder='Descrição',
            compact=True,
            id='text_descricao')

        with HorizontalGroup():
            yield Button('Cadastrar',  id='bt_cadastrar')
            yield Button('Limpar', id='bt_limpar')
            yield Button('Voltar', id='bt_voltar')


    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_cadastrar':
                nome = self.query_one("#input_nome", Input).value
                quantidade = self.query_one("#input_quantidade", Input).value
                valor_unitario = self.query_one("#input_valor_unitario", Input).value
                valor_custo = self.query_one("#input_valor_custo", Input).value
                imagem = self.query_one("#input_imagem", Input).value
                aceita_encomenda = self.query_one("#select_encomenda", Select).value
                descricao = self.query_one("#text_descricao", TextArea).text

                controller.insert_produto(nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao)

            case 'bt_limpar':
                pass
            case 'bt_voltar':
                pass


"""
def insert_produto(nome, valor_unitario, quantidade=0, imagem=None, aceita_encomenda=0, descricao=None, valor_custo=None):

    sql = '''INSERT INTO produtos (nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
    sql_values_produtos = [nome, valor_unitario, quantidade,
                           imagem, aceita_encomenda, descricao, valor_custo]

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, sql_values_produtos)
"""


# class TelaVendedor(Screen):
#     def compose(self):
#         yield Label('Usuário:')
#         yield MaskedInput(valid_empty=False)
#         yield Label('Senha:')
#         yield MaskedInput(valid_empty=False)
#         yield Label('Nome:')
#         yield MaskedInput(valid_empty=False)
#         yield Label('Nome da loja:')
#         yield MaskedInput(valid_empty=True)


# def insert_vendedor(login, senha, nome, nome_loja):
#     pass
