import controller

from textual import on

from textual.app import (App, ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput, OptionList, Select, SelectionList, TabbedContent, TabPane, DataTable)
from textual.screen import (Screen)
from textual.containers import (
    Container, VerticalGroup, HorizontalGroup, Grid, Center, ScrollableContainer)
from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message


class TelaInicial(Screen):
    def compose(self):
        yield Static("Nize", id="titulo_inicial")

        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Produtos", id="bt_produtos", classes="botoes_inicial", variant="primary")
            yield Button("Encomendas", id="bt_encomendas", classes="botoes_inicial", variant="success")
            yield Button("Vendas", id="bt_vendas", classes="botoes_inicial", variant="warning")
            yield Button("Pesquisar", id="bt_pesquisa", classes="botoes_inicial", variant='error')
            yield Button("Estoque", classes="botoes_inicial", id="bt_estoque")
            yield Button("Sair", id="bt_sair", classes="botoes_inicial")

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_produtos":
                self.app.switch_screen("tela_produtos")
            case "bt_encomendas":
                self.app.switch_screen("tela_encomendas")
            case "bt_vendas":
                self.app.switch_screen("tela_vendas")
            case "bt_pesquisa":
                self.app.switch_screen("tela_pesquisa")
            case "bt_estoque":
                self.app.switch_screen("tela_estoque")
            case "bt_sair":
                self.app.exit()


class WidgetProdutos(ScrollableContainer):
    def compose(self):

        yield Input(
            placeholder='Nome do produto*',
            valid_empty=False,
            type='text',
            max_length=50,
            id='input_nome',
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


class TelaProdutos(Screen):

    LISTA_DE_PRODUTOS = controller.listar_produtos()

    def compose(self):
        yield Header(show_clock=True)

        with TabbedContent(initial='cadastro_produtos', id='abas_produtos'):
            with TabPane('Cadastro de produtos', id='cadastro_produtos'):

                yield WidgetProdutos()

                with HorizontalGroup():
                    yield Button('Cadastrar',  id='bt_cadastrar')
                    yield Button('Limpar', id='bt_limpar')
                    yield Button('Voltar', id='bt_voltar')

            with TabPane('Alteração de produto', id='alteracao_produto'):
                with HorizontalGroup():
                    yield Label('Selecione o produto')
                    yield Select(self.LISTA_DE_PRODUTOS,
                                 type_to_search=True,
                                 id='select_produtos',
                                 allow_blank=False
                                 )
                    yield Button('OK', id='bt_OK')

                # yield WidgetProdutos(id='inputs_alteracao')
                yield Input(
                    placeholder='Nome do produto*',
                    valid_empty=False,
                    type='text',
                    max_length=50,
                    id='input_nome',
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
                    yield Button('Alterar', id='bt_alterar')
                    yield Button('Voltar', id='bt_voltar')

    def pegar_inputs_produtos(self):
        nome = self.query_one("#input_nome", Input)
        quantidade = self.query_one("#input_quantidade", Input)
        valor_unitario = self.query_one("#input_valor_unitario", Input)
        valor_custo = self.query_one("#input_valor_custo", Input)
        imagem = self.query_one("#input_imagem", Input)
        aceita_encomenda = self.query_one("#select_encomenda", Select)
        descricao = self.query_one("#text_descricao", TextArea)

        return nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao

    def pegar_valores_inputs(self):
        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_inputs_produtos()

        nome = nome.value
        quantidade = quantidade.value
        valor_unitario = valor_unitario.value
        valor_custo = valor_custo.value
        imagem = imagem.value
        aceita_encomenda = aceita_encomenda.value
        descricao = descricao.text

        return nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao

    def limpar_inputs_produtos(self):
        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_inputs_produtos()
        nome.clear()
        quantidade.clear()
        valor_unitario.clear()
        valor_custo.clear()
        imagem.clear()
        aceita_encomenda.value = 2
        descricao.clear()

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_cadastrar':
                id_produto = None
                nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()
                self.limpar_inputs_produtos()

                controller.insert_produto(
                    id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

                self.atualizar()

            case 'bt_limpar':
                self.limpar_inputs_produtos()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')

            case 'bt_OK':
                id_produto = self.query_one("#select_produtos", Select).value

                _, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo = controller.select_produto_id(
                    id_produto)

                input_nome, input_quantidade, input_valor_unitario, input_valor_custo, input_imagem, input_aceita_encomenda, input_descricao = self.pegar_inputs_produtos()

                input_nome.value = str(nome)
                input_quantidade.value = str(quantidade)
                input_valor_unitario.value = str(valor_unitario)
                input_valor_custo.value = str(valor_custo)
                input_imagem.value = str(imagem)
                input_aceita_encomenda.value = aceita_encomenda
                input_descricao.text = str(descricao)

                self.notify("opa!")

            case 'bt_alterar':
                pass

    def action_atualizar_inputs(self):
        pass

    def atualizar(self):
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one(Select).set_options(self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS


class TelaEstoque(Screen):

    ROWS = [
        ('id_produto', 'nome', 'valor_unitario', 'quantidade',
         'imagem', 'aceita_encomenda', 'descricao', 'valor_custo')
    ]

    def compose(self):

        yield Header()

        yield DataTable()


class TelaEncomendas(Screen):
    pass


class TelaVendas(Screen):
    pass


class TelaPesquisa(Screen):
    pass
