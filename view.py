import controller

from textual import on

from textual.app import (App, ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput, OptionList, Select, SelectionList, TabbedContent, TabPane, DataTable, Collapsible, Switch, Placeholder, Checkbox)
from textual.screen import (Screen, ModalScreen)
from textual.containers import (
    Container, VerticalGroup, HorizontalGroup, Grid, Center, ScrollableContainer, Horizontal, Vertical, CenterMiddle, ItemGrid, VerticalScroll)
from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message
from textual.errors import (
    TextualError, RenderError, DuplicateKeyHandlers, NoWidget)
from textual.scroll_view import ScrollView
from textual.scrollbar import ScrollBar
from textual.suggester import SuggestFromList
from textual.events import Mount


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


class ContainerEncomendas(ScrollableContainer):
    def compose(self):
        with Horizontal():

            yield Label('Prazo de entrega[red]*[/red]')
            yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="prazo_encomenda")

            yield Label('Status da encomenda[red]*[/red]')
            yield Select([('Em produção', 1),
                          ('Finalizada', 2),
                          ('Vendida', 3),
                          ('Cancelada', 4)],
                         type_to_search=True,
                         id='select_status_encomenda',
                         allow_blank=False
                         )

        with Horizontal():
            yield Label("Comentários")
            yield TextArea(
                placeholder='Detalhes da encomenda, dos produtos, da entrega, quem comprou, entre outros',
                id='text_comentario')


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

    def __init__(self, name = None, id = None, classes = None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.ID_PRODUTO = int()

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        with ScrollableContainer(id='tela_produtos'):
            with HorizontalGroup(id='class_select_produtos'):
                yield Label('Selecione o produto')
                yield Select(self.LISTA_DE_PRODUTOS,
                             type_to_search=True,
                             id='select_produtos',
                             allow_blank=True
                             )

            with HorizontalGroup():
                yield Static(f"""Informações do produto:
                                 
        Selecione o produto para visualizar
                                    
        """, id='stt_info_produto')
                yield Button('Preencher campos', variant='primary', id='bt_preencher_campos')

            yield ContainerProdutos(id='inputs_cadastro')

            with HorizontalGroup(id='bt_tela_produtos'):
                yield Button('Cadastrar',  id='bt_cadastrar', disabled=True)
                yield Button("Alterar", id='bt_alterar', disabled=True)
                yield Button('Limpar', id='bt_limpar', disabled=True)
                yield Button('Deletar', id='bt_deletar', disabled=True)
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

        self.query_one("#bt_cadastrar", Button).disabled = True
        self.query_one("#bt_limpar", Button).disabled = True
        self.query_one("#bt_alterar", Button).disabled = True
        self.query_one("#select_produtos", Select).value = Select.BLANK

    def atualizar_texto_static(self):
        id_produto = self.query_one("#select_produtos", Select).value

        texto_static = self.query_one("#stt_info_produto", Static)

        id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
            id_produto)

        if str(valor_custo) == 'None':
            valor_custo = 'Não informado'
        if str(descricao) == 'None':
            descricao = 'Sem descrição'
        if aceita_encomenda == False:
            aceita_encomenda = 'Não'
        else:
            aceita_encomenda = 'Sim'

        texto_static.update(f'''Informações do produto selecionado: ID: {id_produto}

        Nome: {nome} | Quantidade disponível: {quantidade} | Valor unitário: {valor_unitario}
        Aceita encomenda: {aceita_encomenda} | Valor de custo: {valor_custo}
        Descrição: {descricao}''')

    def limpar_texto_static(self):
        texto_static = self.query_one("#stt_info_produto", Static)
        texto_static.update(
            f"""Informações do produto:
                                 
        Selecione o produto para visualizar
                                    
        """)

    def atualizar_select_produtos(self):
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one(Select).set_options(self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        if event.input.value == '':
            self.query_one("#bt_cadastrar", Button).disabled = True
            self.query_one("#bt_limpar", Button).disabled = True
        else:
            self.query_one("#bt_cadastrar", Button).disabled = False
            self.query_one("#bt_limpar", Button).disabled = False

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        self.ID_PRODUTO = event.select.value    
        if event.select.value == Select.BLANK:
            pass
        else:       
            self.atualizar_texto_static()

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_cadastrar':
                nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

                if nome == '' or quantidade == '' or valor_unitario == '':
                    self.notify(
                        title="Ops!", message="Você precisa inserir os dados obrigatórios!", severity='warning')
                else:
                    id_produto = None
                    controller.insert_produto(
                        id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)
                    self.notify(title='Feito!',
                                message=f"{nome} cadastrado com sucesso!")

                    self.atualizar_select_produtos()

                    self.limpar_inputs_produtos()
                    self.limpar_texto_static()

            case 'bt_limpar':
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

            case 'bt_preencher_campos':

                try:
                    id_produto = self.query_one(
                        "#select_produtos", Select).value

                    self.id_produto = id_produto

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

                    self.query_one("#bt_alterar", Button).disabled = False
                    self.query_one("#bt_deletar", Button).disabled = False

                except:
                    self.notify(
                        title="Ops!", message="Nenhum produto selecionado!", severity='warning')

            case 'bt_alterar':
                id_produto = self.query_one(
                    "#select_produtos", Select).value

                nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

                controller.update_produto(
                    id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

                self.atualizar_select_produtos()

                self.limpar_inputs_produtos()
                self.limpar_texto_static()

                self.notify(f"Produto {nome} alterado com sucesso!")

            case 'bt_deletar':
                id_produto = self.ID_PRODUTO

                if id_produto > 0:
                    controller.delete_produto(id_produto)
                    self.notify(f"Produto excluído!", severity='error')

                    self.atualizar_select_produtos()
                    self.limpar_inputs_produtos()
                    self.limpar_texto_static()

                else:
                    self.notify("Ops! Você precisa selecionar um produto!")


class NovaTelaEncomendas(Screen):
    TITLE = 'Encomendas'

    def __init__(self, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
 
        self.ID_PRODUTO = int()

    def compose(self):
        yield Header(show_clock=True)

        yield ContainerEncomendas()

        yield Button("Registrar nova encomenda")
        yield Button("Alterar encomenda existente")

        yield Static("Selecione a encomenda para adicionar produtos")
        yield Select(name='Selecione a encomenda', options=[("opcao", 1)])
        yield Static("Aqui vai o ID da encomenda")

        yield Select(name="Selecione o produto", id="select_produto", options=[("opcao", 1)])
        yield Input(placeholder="Quantidade", max_length=2)
        yield Button("Inserir produto")

        yield Static("Aqui vão todas as informações da encomenda")


class WidgetQuantidade(Static):
    def compose(self):
        # id_produto = self.query_one("#select_produtos", SelectionList).selected

        yield Select(options=[('opcao', 1)])


class TelaEncomendas(Screen):
    TITLE = 'Encomendas'

    def __init__(self, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
 
        self.ID_PRODUTO = int()
        self.LISTA_DE_PRODUTOS = controller.listar_produtos_encomenda()

    # def on_screen_resume(self):
    #     self.criar_lista_produtos()

    # def criar_lista_produtos(self):
    #     scroll_produtos = self.query_one("#scroll_produtos", VerticalScroll)
        
    #     for produto in self.LISTA_DE_PRODUTOS:
    #         scroll_produtos.mount(Checkbox(produto))

    def compose(self) -> ComposeResult:
        
        with ScrollableContainer():
            yield Header(show_clock=True)

            with HorizontalGroup(id='cnt_select_produtos'):
                yield Label('Selecione os produtos')

                with Collapsible(title="Clique para expandir", id="collapsible_encomendas"):
                    with HorizontalGroup():
                        with VerticalScroll():
                            yield SelectionList(id='select_produtos').add_options((nome, id_produto) for nome, id_produto in self.LISTA_DE_PRODUTOS.items())
                    yield WidgetQuantidade()


            with Container(id='tela_encomendas'):
                yield Static(content='''
                Informações do produto:
                Nome do produto: {nome_do_produto}
                Valor unitário: {valor_unitario}               
                ''', id='static_encomendas')

                yield ContainerEncomendas(id='inputs_encomenda')

                with HorizontalGroup(id='bt_tela_encomendas'):
                    yield Button('Cadastrar',  id='bt_cadastrar', disabled=True)
                    yield Button("Alterar", id='bt_alterar', disabled=True)
                    yield Button('Limpar', id='bt_limpar', disabled=True)
                    yield Button('Deletar', id='bt_deletar', disabled=True)
                    yield Button('Voltar', id='bt_voltar')


    def limpar_inputs(self):
        self.query_one("#prazo_encomenda", Input).clear()
        self.query_one("#select_status_encomenda", Select).value = 1
        self.query_one("#text_comentario", TextArea).clear()
        self.query_one("#select_produtos", SelectionList).deselect_all()


    @on(Mount)
    @on(SelectionList.SelectedChanged)
    def atualizar_select_quantidade(self) -> None:
        id_produto = self.query_one(SelectionList).selected

        self.query_one(WidgetQuantidade).update(f"{id_produto}")

    @on(SelectionList.OptionSelected)
    async def on_selected_change(self, event: SelectionList.OptionSelected):
        if event.option:
            self.query_one("#bt_limpar", Button).disabled = False
        

    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        if event.input.value == '':
            self.query_one("#bt_cadastrar", Button).disabled = True
            self.query_one("#bt_limpar", Button).disabled = True
        else:
            self.query_one("#bt_cadastrar", Button).disabled = False
            self.query_one("#bt_limpar", Button).disabled = False

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')
                # self.limpar_inputs_produtos()
                # self.limpar_texto_static()

            case 'bt_cadastrar':
                # ######## Retorna uma lista com os IDs dos produtos selecionados
                status = self.query_one('#select_status_encomenda', Select).value
                prazo = self.query_one("#prazo_encomenda", Input).value
                comentario = self.query_one("#text_comentario", TextArea).text
                
                id_produtos_selecionados = self.query_one('#select_produtos', SelectionList).selected

                if id_produtos_selecionados == []:
                    self.notify("Selecione pelo menos um produto!")
                elif len(prazo) < 10:
                    self.notify("Preencha o prazo no formato DD/MM/AAAA") 
                else:
                    controller.insert_encomenda(status=status, prazo=prazo, comentario=comentario, produtos=id_produtos_selecionados)


            case 'bt_limpar':
                self.limpar_inputs()

            # case 'bt_cadastrar':
            #     nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

            #     if nome == '' or quantidade == '' or valor_unitario == '':
            #         self.notify(
            #             title="Ops!", message="Você precisa inserir os dados obrigatórios!", severity='warning')
            #     else:
            #         id_produto = None
            #         controller.insert_produto(
            #             id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)
            #         self.notify(title='Feito!',
            #                     message=f"{nome} cadastrado com sucesso!")

            #         self.atualizar_select_produtos()

            #         self.limpar_inputs_produtos()
            #         self.limpar_texto_static()

            # case 'bt_limpar':
            #     self.limpar_inputs_produtos()
            #     self.limpar_texto_static()



            # case 'bt_preencher_campos':

            #     try:
            #         id_produto = self.query_one(
            #             "#select_produtos", Select).value

            #         self.id_produto = id_produto

            #         _, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
            #             id_produto)

            #         input_nome, input_quantidade, input_valor_unitario, input_valor_custo, input_imagem, input_aceita_encomenda, input_descricao = self.pegar_inputs_produtos()

            #         input_nome.value = str(nome)
            #         input_quantidade.value = str(quantidade)
            #         input_valor_unitario.value = str(valor_unitario)
            #         input_valor_custo.value = str(valor_custo)
            #         input_imagem.value = str(imagem)
            #         input_aceita_encomenda.value = aceita_encomenda
            #         input_descricao.text = str(descricao)

            #         self.query_one("#bt_alterar", Button).disabled = False
            #         self.query_one("#bt_deletar", Button).disabled = False

            #     except:
            #         self.notify(
            #             title="Ops!", message="Nenhum produto selecionado!", severity='warning')

            # case 'bt_alterar':
            #     id_produto = self.query_one(
            #         "#select_produtos", Select).value

            #     nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

            #     controller.update_produto(
            #         id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

            #     self.atualizar_select_produtos()

            #     self.limpar_inputs_produtos()
            #     self.limpar_texto_static()

            #     self.notify(f"Produto {nome} alterado com sucesso!")

            # case 'bt_deletar':
            #     id_produto = self.ID_PRODUTO

            #     if id_produto > 0:
            #         controller.delete_produto(id_produto)
            #         self.notify(f"Produto excluído!", severity='error')

            #         self.atualizar_select_produtos()
            #         self.limpar_inputs_produtos()
            #         self.limpar_texto_static()

            #     else:
            #         self.notify("Ops! Você precisa selecionar um produto!")



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
