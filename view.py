import controller

from textual.app import (App, ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput, OptionList, Select, SelectionList, TabbedContent, TabPane)
from textual.screen import (Screen)
from textual.containers import (
    Container, VerticalGroup, HorizontalGroup, Grid, Center)
from textual.widget import Widget
from textual.reactive import reactive

class TelaInicial(Screen):
    def compose(self):
        yield Static("Nize", id="titulo_inicial")

        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Produtos", id="bt_produtos", classes="botoes_inicial", variant="primary")
            yield Button("Encomendas", id="bt_encomendas", classes="botoes_inicial", variant="success")
            yield Button("Vendas", id="bt_vendas", classes="botoes_inicial", variant="warning")
            yield Button("Pesquisar", id="bt_pesquisa", classes="botoes_inicial", variant='error')
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
            case "bt_sair":
                self.app.exit()

class WidgetAlteracao(Container):
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

        with TabbedContent(initial='cadastro_produtos'):
            with TabPane('Cadastro de produtos', id='cadastro_produtos'):

                yield WidgetAlteracao()

                with HorizontalGroup():
                    yield Button('Cadastrar',  id='bt_cadastrar')
                    yield Button('Limpar', id='bt_limpar')
                    yield Button('Voltar', id='bt_voltar')
    
            with TabPane('Alteração de produto', id='alteracao_produto'):
                with HorizontalGroup():
                    yield Label('Selecione o produto')
                    yield Select(TelaProdutos.LISTA_DE_PRODUTOS,
                        type_to_search=True,
                        id='select_produtos'
                    )             

                yield WidgetAlteracao()

                with HorizontalGroup():            
                    yield Button('Alterar', id='bt_alterar')
                    yield Button('Voltar', id='bt_voltar')

    def on_select_changed(self, event: Select.Changed):
        id_produto = self.query_one("#select_produtos", Select).value

        produto = controller.select_produto_id(id_produto)

        for nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao in produto:        

            nome = self.query_one("#input_nome", Input).value
            quantidade = self.query_one("#input_quantidade", Input).value
            valor_unitario = self.query_one("#input_valor_unitario", Input).value
            valor_custo = self.query_one("#input_valor_custo", Input).value
            imagem = self.query_one("#input_imagem", Input).value
            aceita_encomenda = self.query_one("#select_encomenda", Select).value
            descricao = self.query_one("#text_descricao", TextArea).text



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
                self.app.switch_screen('tela_inicial')

class TelaEncomendas(Screen):
    pass 

class TelaVendas(Screen):
    pass 

class TelaPesquisa(Screen):
    pass 