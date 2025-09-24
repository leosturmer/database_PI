import controller

from textual import on

from textual.app import (App, ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput, OptionList, Select, SelectionList, TabbedContent, TabPane, DataTable, Collapsible, Switch, Placeholder)
from textual.screen import (Screen)
from textual.containers import (
    Container, VerticalGroup, HorizontalGroup, Grid, Center, ScrollableContainer, Horizontal, Vertical, CenterMiddle, ItemGrid, VerticalScroll)
from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message
from textual.errors import (
    TextualError, RenderError, DuplicateKeyHandlers, NoWidget)
from textual.scroll_view import ScrollView
from textual.scrollbar import ScrollBar


# @@@@@@@@@@@ CONTAINERS

class ContainerProdutos(ScrollableContainer):
    def compose(self):
        with HorizontalGroup():
            yield Label("Nome do produto[red]*[/red]")
            yield Input(
                placeholder='Nome do produto*',
                type='text',
                max_length=50,
                id='input_nome',

            )
            yield Label("Quantidade[red]*[/red]")
            yield Input(
                placeholder='Quantidade*',
                type='integer',
                max_length=4,
                id='input_quantidade'
            )

        with HorizontalGroup():
            yield Label("Valor unitário[red]*[/red]")
            yield Input(
                placeholder='Valor unitário*',
                type='number',
                max_length=7,
                id='input_valor_unitario'
            )

            yield Label("Valor de custo")
            yield Input(
                placeholder='Valor de custo',
                type='number',
                max_length=7,
                id='input_valor_custo'
            )

        with HorizontalGroup():
            yield Label('Imagem')
            yield Input(
                placeholder='Imagem',
                type='text',
                id='input_imagem'
            )
            yield Label('Aceita encomendas?')
            yield Switch(value=False, id='select_encomenda')

        with HorizontalGroup():

            yield Label("Descrição do produto")
            yield TextArea(
                placeholder='Descrição',
                id='text_descricao')

class ContainerEncomendas(Widget):
    def compose(self):
        with Horizontal():
            yield Label("Quantidade[red]*[/red]")
            yield Input(
                placeholder='Quantidade*',
                type='integer',
                max_length=4,
                id='input_quantidade'
            )
            yield Label('Prazo de entrega[red]*[/red]')
            yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA')

        with Horizontal():
            yield Label('Status da encomenda[red]*[/red]')
            yield Select([('Em produção', 1),
                          ('Finalizada', 2),
                          ('Vendida', 3),
                          ('Cancelada', 4)],
                         type_to_search=True,
                         id='select_status',
                         allow_blank=False
                         )

        with Horizontal():
            yield Label("Comentários")
            yield TextArea(
                placeholder='Detalhes da encomenda, dos produtos, da entrega, quem comprou, entre outros',
                id='text_descricao')


# @@@@@@@@ TELAS DO SISTEMA

class TelaInicial(Screen):

    def compose(self):
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


class TelaProdutos(Screen):

    TITLE = 'Produtos'

    LISTA_DE_PRODUTOS = controller.listar_produtos()

    def compose(self):

        yield Header(show_clock=True)

        with VerticalGroup():

            with HorizontalGroup(id='class_select_produtos'):
                yield Label('Selecione o produto')
                yield Select(self.LISTA_DE_PRODUTOS,
                            type_to_search=True,
                            id='select_produtos',
                            allow_blank=True
                            )
                yield Button('OK', id='bt_select_produto')

            yield Static(f"Informações do produto:\n\nSelecione o produto\ne clique OK\npara visualizar", id='stt_info_produto')

        with ScrollableContainer(id='tela_produtos'):

            yield ContainerProdutos(id='inputs_cadastro')

            with HorizontalGroup(id='bt_tela_produtos'):
                yield Button('Cadastrar',  id='bt_cadastrar')
                yield Button("Alterar", id='bt_alterar')
                yield Button('Limpar', id='bt_limpar')
                yield Button('Deletar', id='bt_deletar')
                yield Button('Voltar', id='bt_voltar')


    def pegar_inputs_produtos(self):
        nome = self.query_one("#input_nome", Input)
        quantidade = self.query_one("#input_quantidade", Input)
        valor_unitario = self.query_one("#input_valor_unitario", Input)
        valor_custo = self.query_one("#input_valor_custo", Input)
        imagem = self.query_one("#input_imagem", Input)
        aceita_encomenda = self.query_one("#select_encomenda", Switch)
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
        aceita_encomenda.value = False
        descricao.clear()

    def atualizar_texto_static(self):
        texto_static = self.query_one("#stt_info_produto", Static)

        id_produto = self.query_one("#select_produtos", Select).value

        id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(id_produto)

        if descricao == "None":
            descricao = 'Sem descrição'
        if aceita_encomenda == 0:
            aceita_encomenda = 'Não'
        else:
            aceita_encomenda = 'Sim'

        texto_static.update(f'''Informações do produto selecionado: ID: {id_produto}

        Nome: {nome} | Quantidade disponível: {quantidade} | Valor unitário: {valor_unitario}
        Aceita encomenda: {aceita_encomenda} | Valor de custo: {valor_custo}
        Descrição: {descricao}''')

    def limpar_texto_static(self):
        texto_static = self.query_one("#stt_info_produto", Static)
        texto_static.update(f"Informações do produto:\n\nSelecione o produto\ne clique OK\npara visualizar")

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_cadastrar':
                
                nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

                if nome == '' or quantidade == '' or valor_unitario == '':
                    self.notify("Insira os dados obrigatórios")
                else:
                    id_produto = None
                    controller.insert_produto(
                        id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)
                    self.notify(f"{nome} cadastrado com sucesso!")

                    self.atualizar_select_produtos()

            case 'bt_limpar':
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

            case 'bt_select_produto':
                try:
                    id_produto = self.query_one(
                        "#select_produtos", Select).value

                    _, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
                        id_produto)
                    input_nome, input_quantidade, input_valor_unitario, input_valor_custo, input_imagem, input_aceita_encomenda, input_descricao = self.pegar_inputs_produtos()

                    input_nome.value = str(nome)
                    input_quantidade.value = str(quantidade)
                    input_valor_unitario.value = str(valor_unitario)
                    input_valor_custo.value = str(valor_custo)
                    input_imagem.value = str(imagem)
                    input_aceita_encomenda.value = aceita_encomenda
                    input_descricao.text = str(descricao)

                    self.atualizar_texto_static()

                except:
                    self.notify("Ops! Você precisa selecionar um produto")

            case 'bt_alterar':
                try:
                    id_produto = self.query_one(
                        "#select_produtos", Select).value

                    nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

                    controller.update_produto(
                        id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)
                    self.atualizar_select_produtos()

                    self.notify(f"Produto {nome} alterado com sucesso!")
                except:
                    self.notify("Ops! Você precisa selecionar um produto!")

            case 'bt_deletar':
                try:
                    id_produto = self.query_one(
                        "#select_produtos", Select).value

                    controller.delete_produto(id_produto)
                    self.atualizar_select_produtos()

                    self.notify(f"Produto excluído!")
                    self.limpar_inputs_produtos()
                    self.limpar_texto_static()

                except:
                    self.notify("Ops! Você precisa selecionar um produto!")


    def atualizar_select_produtos(self):
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one(Select).set_options(self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS


class TelaEncomendas(Screen):
    TITLE = 'Encomendas'

    LISTA_DE_PRODUTOS = controller.listar_produtos()

    def compose(self):
        with ScrollableContainer():
            yield Header(show_clock=True)

            with HorizontalGroup(id='cnt_select_produtos'):
                yield Label('Selecione o produto')
                yield Select(self.LISTA_DE_PRODUTOS,
                             type_to_search=True,
                             id='select_produtos',
                             allow_blank=True
                             )
                yield Button('OK', id='bt_select_produto')

            with Container(id='tela_encomendas'):
                yield Static(content='''
                Informações do produto:
                Nome do produto: {nome_do_produto}
                Valor unitário: {valor_unitario}               
                ''', id='static_encomendas', )

                yield ContainerEncomendas(id='inputs_encomenda')

                with HorizontalGroup(id='bt_tela_encomendas'):
                    yield Button('Cadastrar',  id='bt_cadastrar')
                    yield Button("Alterar", id='bt_alterar')
                    yield Button('Limpar', id='bt_limpar')
                    yield Button('Deletar', id='bt_deletar')
                    yield Button('Voltar', id='bt_voltar')

    def atualizar_texto_static(self):
        pass

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_cadastrar':
                pass
                #     id_produto = None
                #     nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

                #     if nome == '' or quantidade == '' or valor_unitario == '':
                #         self.notify("Insira os dados obrigatórios")
                #     else:
                #         controller.insert_produto(
                #             id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)
                #         self.notify(f"{nome} cadastrado com sucesso!")

                #     self.atualizar_select_produtos()

            case 'bt_limpar':
                pass
                # self.limpar_inputs_produtos()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')
                # self.limpar_inputs_produtos()

            case 'bt_select_produto':
                pass
                # try:
                #     id_produto = self.query_one("#select_produtos", Select).value

                #     _, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
                #         id_produto)
                #     input_nome, input_quantidade, input_valor_unitario, input_valor_custo, input_imagem, input_aceita_encomenda, input_descricao = self.pegar_inputs_produtos()

                #     input_nome.value = str(nome)
                #     input_quantidade.value = str(quantidade)
                #     input_valor_unitario.value = str(valor_unitario)
                #     input_valor_custo.value = str(valor_custo)
                #     input_imagem.value = str(imagem)
                #     input_aceita_encomenda.value = aceita_encomenda
                #     input_descricao.text = str(descricao)
                # except:
                #     self.notify("Ops! Você precisa selecionar um produto")

            case 'bt_alterar':
                pass
                # try:
                #     id_produto = self.query_one("#select_produtos", Select).value

                #     nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

                #     controller.update_produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)
                #     self.atualizar_select_produtos()

                #     self.notify(f"Produto {nome} alterado com sucesso!")
                # except:
                #     self.notify("Ops! Você precisa selecionar um produto!")

            case 'bt_deletar':
                pass
                # try:
                #     id_produto = self.query_one("#select_produtos", Select).value

                #     controller.delete_produto(id_produto)
                #     self.atualizar_select_produtos()

                #     self.notify(f"Produto excluído!")

                # except:
                #     self.notify("Ops! Você precisa selecionar um produto!")


class TelaVendas(Screen):
    TITLE = 'Vendas'

    pass


class TelaPesquisa(Screen):
    TITLE = 'Pesquisa'

    pass


class TelaEstoque(Screen):
    TITLE = 'Estoque'

    ROWS = [
        ('id_produto', 'nome', 'valor_unitario', 'quantidade',
         'imagem', 'aceita_encomenda', 'descricao', 'valor_custo')
    ]

    def compose(self):

        yield Header()

        yield DataTable()
