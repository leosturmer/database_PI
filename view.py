import controller

from textual import on

from textual.app import (App, ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput, OptionList, Select, SelectionList, TabbedContent, TabPane, DataTable, Collapsible, Switch, Placeholder, Checkbox, Rule)
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

from sqlite3 import IntegrityError

# @@@@@@@@ TELAS DO SISTEMA

class TelaLogin(Screen):

    def compose(self):
        yield Header()
        yield Label("Faça o seu login")
        yield Input(placeholder='Login', id="input_login")
        yield Input(placeholder='Senha', password=True, id="input_senha")

        with HorizontalGroup():
            yield Label("Mostrar senha?")
            yield Switch(id="switch_senha")

        with HorizontalGroup():
            yield Button("Entrar", id="bt_login")

        with HorizontalGroup():
            yield Label("Não tem cadastro?")
            yield Button("Cadastrar", id="bt_cadastrar")

        yield Button("Sair", id="bt_sair")

    def verificar_login(self):
        import hashlib
        from hashlib import sha256

        input_login = self.query_one("#input_login", Input).value.strip()
        input_senha = self.query_one("#input_senha", Input).value.strip()

        if not input_login or not input_senha:
            self.notify("Preencha todos os campos!", severity="warning")
            return

        try:
            id_vendedor, login, senha, nome, nome_loja = controller.select_vendedor(
                input_login)

            senha_hash = hashlib.sha256(input_senha.encode('utf-8')).digest()

            if input_login == login and senha_hash == senha:
                self.notify("Login realizado com sucesso!")
                self.app.switch_screen('tela_inicial')

        except TypeError:
            self.notify("Login ou senha incorretos!", severity='error')

    @on(Switch.Changed)
    async def on_switch(self, event: Switch.Changed):
        mostrar_senha = self.query_one("#switch_senha", Switch).value
        input_senha = self.query_one("#input_senha", Input)

        if mostrar_senha == True:
            input_senha.password = False
        else:
            input_senha.password = True

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_login':
                self.verificar_login()

            case "bt_sair":
                self.app.exit()

            case "bt_cadastrar":
                self.app.switch_screen("tela_cadastro")


class TelaCadastro(Screen):
    def compose(self):
        with HorizontalGroup():
            yield Label("Nome[red]*[/red]")
            yield Input(placeholder="Nome*", id="input_nome")

        with HorizontalGroup():
            yield Label("E-mail[red]*[/red]")
            yield Input(placeholder="Login*", id="input_login")

        with HorizontalGroup():
            yield Label("Senha[red]*[/red]")
            yield Input(placeholder="Mínimo 6 caracteres", password=True, max_length=50, id="input_senha")

        with HorizontalGroup():
            yield Label("Mostrar senha?")
            yield Switch(id="switch_senha")

        with HorizontalGroup():
            yield Label("Sua loja tem nome? (opcional)")
            yield Input(placeholder="Nome da loja", id="input_nome_loja")

        with HorizontalGroup():
            yield Button("Cadastrar", id="bt_cadastrar")
            yield Button("Voltar", id="bt_voltar")

    def limpar_campos(self):
        self.query_one("#input_login", Input).clear()
        self.query_one("#input_senha", Input).clear()
        self.query_one("#input_nome", Input).clear()
        self.query_one("#input_nome_loja", Input).clear()

    def pegar_dados_vendedor(self):
        login = self.query_one("#input_login", Input).value
        senha = self.query_one("#input_senha", Input).value
        nome = self.query_one("#input_nome", Input).value
        nome_loja = self.query_one("#input_nome_loja", Input).value

        return login, senha, nome, nome_loja

    def insert_vendedor(self):
        from hashlib import sha256

        login, senha, nome, nome_loja = self.pegar_dados_vendedor()

        senha_codificada = sha256(senha.encode('utf-8')).digest()

        try:
            controller.insert_vendedor(login, senha_codificada, nome, nome_loja)
            self.notify("Usuário cadastrado com sucesso!")
            self.app.switch_screen('tela_login')
            self.limpar_campos()

        except:
            self.notify("Ops! Algo deu errado", severity="warning")

    @on(Switch.Changed)
    async def on_switch(self, event: Switch.Changed):
        mostrar_senha = self.query_one("#switch_senha", Switch).value
        input_senha = self.query_one("#input_senha", Input)

        if mostrar_senha == True:
            input_senha.password = False
        else:
            input_senha.password = True

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_voltar':
                self.app.switch_screen('tela_login')

            case "bt_cadastrar":
                login, senha, nome, nome_loja = self.pegar_dados_vendedor()

                if not nome or not login or not senha:
                    self.notify(
                        "Ops! Insira todos os dados necessários", severity="error")
                elif "@" not in login or ".com" not in login:
                    self.notify("Insira um e-mail válido!")
                elif len(senha) < 6:
                    self.notify("A senha deve ter no mínimo 6 caracteres!")
                else:
                    self.insert_vendedor()



class TelaInicial(Screen):

    def compose(self):
        yield Header()

        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Produtos", id="bt_produtos", classes="botoes_inicial", variant="primary")
            yield Button("Encomendas", id="bt_encomendas", classes="botoes_inicial", variant="success")
            yield Button("Vendas", id="bt_vendas", classes="botoes_inicial", variant="warning")
            yield Button("Relatórios", id="bt_pesquisa", classes="botoes_inicial", variant='error')
            yield Button("Sair", id="bt_sair", classes="botoes_inicial")

        yield Footer()

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


class TelaProdutos(Screen):

    TITLE = 'Produtos'

    def __init__(self, name=None, id=None, classes=None):
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
                             allow_blank=True,
                             prompt='Selecione o produto'
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

            yield Footer()

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


class TelaEncomendas(Screen):

    TITLE = 'Encomendas'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.ID_PRODUTO = int()
        self.PRODUTOS_QUANTIDADE = dict()
        self.texto_static_produto = '\nInformações do produto:\n'
        self.texto_static_encomenda = 'Aqui vão as informações da encomenda'
        self.texto_static_alteracao = 'Selecione uma encomenda para ver as informações'
        self.ENCOMENDA_ALTERACAO = []

    def on_mount(self):
        tabela = self.query_one("#tabela_encomendas", DataTable)
        tabela.border_title = "Encomendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns('ID encomenda', 'Produtos',
                           'Prazo', 'Comentario', 'Status')
        self.atualizar_tabela_encomendas()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with TabbedContent(initial='tab_cadastrar_encomeda'):

            with TabPane('Cadastrar encomenda', id='tab_cadastrar_encomeda'):
                with ScrollableContainer():
                    with HorizontalGroup(id='cnt_select_produtos'):
                        yield Label('Selecione um produto:')
                        with HorizontalGroup():
                            with VerticalGroup():
                                with HorizontalGroup():
                                    yield Select(self.LISTA_DE_PRODUTOS,
                                                 type_to_search=True,
                                                 id='select_produtos',
                                                 allow_blank=True,
                                                 prompt='Selecione o produto para adicionar à encomenda'
                                                 )

                                yield Static(self.texto_static_produto, id='static_produto')

                                with HorizontalGroup():
                                    yield Input(placeholder='Quantidade encomendada...',
                                                id='quantidade_encomenda',
                                                max_length=3,
                                                type="integer"
                                                )
                                    yield Button('Adicionar',
                                                 disabled=True,
                                                 id='bt_adicionar_quantidade')

                    with VerticalGroup():
                        yield Static(self.texto_static_encomenda, id="static_encomenda")
                        with HorizontalGroup():
                            yield Label('Prazo de entrega[red]*[/red]')
                            yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="prazo_encomenda")

                            yield Label('Status da encomenda[red]*[/red]')
                            yield Select([('Em produção', 1),
                                          ('Finalizada', 2),
                                          ('Vendida', 3),
                                          ('Cancelada', 4)],
                                         type_to_search=True,
                                         id='select_status_cadastro',
                                         allow_blank=False
                                         )

                        with HorizontalGroup():
                            yield Label("Comentários")
                            yield TextArea(
                                placeholder='Detalhes da encomenda, dos produtos, da entrega, quem comprou, entre outros',
                                id='text_comentario')

                    with HorizontalGroup(id='bt_tela_encomendas'):
                        yield Button('Cadastrar',  id='bt_cadastrar', disabled=True)
                        yield Button('Limpar', id='bt_limpar', disabled=True)
                        yield Button('Voltar', id='bt_voltar')

            with TabPane('Atualizar encomenda', id='tab_atualizar_encomenda'):
                with Collapsible(title='Expandir tabela de encomendas'):
                    with VerticalScroll():
                        yield DataTable(id='tabela_encomendas')

                yield Rule(orientation='horizontal', line_style='solid')

                with HorizontalGroup():
                    yield Static(self.texto_static_alteracao, id="static_alteracao_encomenda")
                    yield Button('Preencher dados', id='bt_preencher_dados')

                with VerticalGroup():
                    with HorizontalGroup():
                        yield Label('Prazo de entrega')
                        yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="prazo_alterado")

                        yield Label('Status da encomenda')
                        yield Select([('Em produção', 1),
                                      ('Finalizada', 2),
                                      ('Vendida', 3),
                                      ('Cancelada', 4)],
                                     type_to_search=True,
                                     id='select_status_alterado',
                                     allow_blank=False
                                     )

                    with HorizontalGroup():
                        yield Label("Comentários")
                        yield TextArea(
                            placeholder='Detalhes da encomenda, dos produtos, da entrega, quem comprou, entre outros',
                            id='text_comentario_alterado')

                with HorizontalGroup(id='bt_tela_encomendas'):
                    yield Button("Alterar", id='bt_alterar', disabled=True)
                    yield Button('Deletar', id='bt_deletar', disabled=True)
                    yield Button('Voltar', id='bt_voltar')

    def atualizar_select_produtos(self):
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one("#select_produtos", Select).set_options(
            self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    def atualizar_static_produto(self):
        try:
            id_produto = self.query_one("#select_produtos", Select).value

            static = self.query_one("#static_produto", Static)

            id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
                id_produto)

            novo_texto = f'''
            Informações do produto: ID {id_produto}
            Produto selecionado: {nome}   |   Quantidade em estoque: {quantidade} 
                '''

            static.update(novo_texto)
        except:
            pass

    def atualizar_static_encomenda(self):

        novo_texto = 'Encomenda: \n\n'

        try:
            static = self.query_one('#static_encomenda', Static)

            for item in self.PRODUTOS_QUANTIDADE.items():
                id_produto, quantidade = item

                _id_produto, nome, _quantidade, _valor_unitario, _valor_custo, _aceita_encomenda, _descricao, _imagem = controller.select_produto_id(
                    id_produto)

                novo_texto += f'Produto: {nome}, Quantidade: {quantidade}\n'

            static.update(novo_texto)

        except:
            pass

    def atualizar_static_alteracao(self):
        static = self.query_one('#static_alteracao_encomenda', Static)
        novo_texto = f''''''

        id_encomenda, produtos, prazo, comentario, status = self.ENCOMENDA_ALTERACAO

        if comentario == None:
            comentario = ''

        novo_texto = f'''Encomenda: ID {id_encomenda}\n\nProdutos: {produtos}\nPrazo: {prazo}\nStatus: {status}\nComentários: {comentario}'''

        static.update(novo_texto)

    def adicionar_dicionario_encomenda(self):
        id_produto = self.query_one("#select_produtos", Select).selection
        quantidade_encomendada = self.query_one(
            "#quantidade_encomenda", Input).value

        self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_encomendada

    def limpar_inputs(self):
        self.query_one("#prazo_encomenda", Input).clear()
        self.query_one("#select_status_cadastro", Select).value = 1
        self.query_one("#text_comentario", TextArea).clear()
        self.query_one("#select_produtos", Select).clear()
        self.query_one('#quantidade_encomenda', Input).clear()
        self.query_one('#static_produto', Static).update(
            self.texto_static_produto)
        self.query_one('#static_encomenda', Static).update(
            self.texto_static_encomenda)

    def limpar_inputs_alteracao(self):
        self.query_one("#prazo_alterado", MaskedInput).clear()
        self.query_one("#select_status_alterado", Select).value = 1
        self.query_one("#text_comentario_alterado", TextArea).clear()
        self.query_one("#static_alteracao_encomenda", Static).update(
            self.texto_static_encomenda)
        self.query_one("#bt_alterar", Button).disabled = True

    def atualizar_tabela_encomendas(self):
        tabela = self.query_one("#tabela_encomendas", DataTable)

        dados_encomendas = controller.listar_encomendas()

        for id_encomenda, detalhes in dados_encomendas.items():
            nome_produtos = [''.join([f'{nome}, ({quantidade}) | '])
                             for nome, quantidade in detalhes['produtos']]

            status = detalhes['status']

            if detalhes['status'] == 1:
                status = 'Em produção'
            elif detalhes['status'] == 2:
                status = 'Finalizada'
            elif detalhes['status'] == 3:
                status = 'Vendida'
            elif detalhes['status'] == 4:
                status = 'Cancelada'

            if id_encomenda not in tabela.rows:
                tabela.add_row(id_encomenda, ''.join(nome_produtos),
                               detalhes['prazo'], detalhes['comentario'], status)

    def resetar_tabela_encomendas(self):
        tabela = self.query_one("#tabela_encomendas", DataTable)

        tabela.clear()

        self.atualizar_tabela_encomendas()

    def preencher_alteracoes_encomenda(self):
        novo_prazo = self.query_one("#prazo_alterado", MaskedInput)
        novo_status = self.query_one("#select_status_alterado", Select)
        novo_comentario = self.query_one("#text_comentario_alterado", TextArea)

        _id_encomenda, _produtos, prazo, comentario, status = self.ENCOMENDA_ALTERACAO
        comentario = str(comentario)

        if status == 'Em produção':
            status = 1
        elif status == 'Finalizada':
            status = 2
        elif status == 'Vendida':
            status = 3
        elif status == 'Cancelada':
            status = 4

        if comentario == 'None':
            comentario = ''

        novo_prazo.value = prazo
        novo_status.value = status
        novo_comentario.text = comentario

    def update_encomenda(self):
        id_encomenda = self.ENCOMENDA_ALTERACAO[0]

        prazo = self.query_one("#prazo_alterado", MaskedInput).value
        status = self.query_one("#select_status_alterado", Select).value
        comentario = self.query_one("#text_comentario_alterado", TextArea).text

        controller.update_encomendas(
            id_encomenda=id_encomenda, prazo=prazo, comentario=comentario, status=status)

    def deletar_encomenda(self):
        id_encomenda = self.ENCOMENDA_ALTERACAO[0]
        controller.delete_encomenda(id_encomenda)
        self.notify(
            f'Encomenda ID {id_encomenda} deletada com sucesso!', severity='error')

    @on(DataTable.RowSelected)
    async def on_row_selected(self, event: DataTable.RowSelected):
        encomenda = self.query_one('#tabela_encomendas', DataTable)
        self.ENCOMENDA_ALTERACAO = encomenda.get_row(event.row_key)
        self.atualizar_static_alteracao()
        self.query_one("#bt_alterar", Button).disabled = False
        self.query_one("#bt_deletar", Button).disabled = False

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        match event.select.id:
            case 'select_produtos':
                self.ID_PRODUTO = event.select.value
                self.atualizar_static_produto()

            case 'select_id_encomenda':
                self.atualizar_static_alteracao()

    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        match event.input.id:
            case 'quantidade_encomenda':
                self.query_one("#bt_adicionar_quantidade",
                               Button).disabled = False

            case 'prazo_encomenda':
                if event.input.value == '':
                    self.query_one("#bt_cadastrar", Button).disabled = True
                    self.query_one("#bt_limpar", Button).disabled = True
                else:
                    self.query_one("#bt_cadastrar", Button).disabled = False
                    self.query_one("#bt_limpar", Button).disabled = False

    @on(TextArea.Changed)
    async def on_textarea(self, event: TextArea.Changed):
        if event.text_area.id == 'text_comentario':
            self.query_one("#bt_limpar", Button).disabled = False

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_adicionar_quantidade':

                self.adicionar_dicionario_encomenda()
                self.atualizar_static_encomenda()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')

            case 'bt_cadastrar':
                status = self.query_one(
                    '#select_status_cadastro', Select).value
                prazo = self.query_one("#prazo_encomenda", Input).value
                comentario = self.query_one("#text_comentario", TextArea).text

                produtos = self.PRODUTOS_QUANTIDADE

                if produtos == []:
                    self.notify("Adicione pelo menos um produto!")
                elif len(prazo) < 10:
                    self.notify("Preencha o prazo no formato DD/MM/AAAA")
                else:
                    controller.insert_encomenda(
                        status=status, prazo=prazo, comentario=comentario, produtos=produtos)

                    self.notify('Encomenda cadastrada com sucesso!')
                    self.PRODUTOS_QUANTIDADE.clear()
                    self.limpar_inputs()
                    self.atualizar_tabela_encomendas()
                    # self.resetar_tabela_encomendas()

            case 'bt_preencher_dados':
                try:
                    self.preencher_alteracoes_encomenda()
                except:
                    self.notify("Ops! Você precisa selecionar uma encomenda")

            case 'bt_alterar':
                self.update_encomenda()
                self.resetar_tabela_encomendas()
                self.limpar_inputs_alteracao()

            case 'bt_deletar':
                self.deletar_encomenda()
                self.resetar_tabela_encomendas()

            case 'bt_limpar':
                self.limpar_inputs()


class TelaVendas(Screen):
    TITLE = 'Vendas'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.ID_PRODUTO = int()
        self.PRODUTOS_QUANTIDADE = dict()
        self.texto_static_produto = '\nInformações do produto:\n'
        self.texto_static_venda = 'Aqui vão as informações da venda'
        self.texto_static_alteracao = 'Selecione uma venda para ver as informações'
        self.VENDA_ALTERACAO = []
        self.VALOR_TOTAL_VENDA = []

    def on_mount(self):
        tabela = self.query_one("#tabela_vendas", DataTable)
        tabela.border_title = "Vendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns('ID venda', 'Produtos',
                           'Data', 'Comentario', 'Status', 'Valor final')  # ATUALIZAR ESSES AQUIIIII
        self.atualizar_tabela_vendas()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with TabbedContent(initial='tab_cadastrar_venda'):

            with TabPane('Cadastrar venda', id='tab_cadastrar_venda'):
                with ScrollableContainer():
                    with HorizontalGroup(id='cnt_select_produtos'):
                        yield Label('Selecione um produto:')
                        with HorizontalGroup():
                            with VerticalGroup():
                                with HorizontalGroup():
                                    yield Select(self.LISTA_DE_PRODUTOS,
                                                 type_to_search=True,
                                                 id='select_produtos_venda',
                                                 allow_blank=True,
                                                 prompt='Selecione o produto para adicionar à venda'
                                                 )

                                yield Static(self.texto_static_produto, id='static_produto')

                                with HorizontalGroup():
                                    yield Input(placeholder='Quantidade vendida...',
                                                id='quantidade_venda',
                                                max_length=3,
                                                type="integer"
                                                )
                                    yield Button('Adicionar',
                                                 disabled=True,
                                                 id='bt_adicionar_quantidade')

                    with VerticalGroup():
                        yield Static(self.texto_static_venda, id="static_venda")
                        with HorizontalGroup():
                            yield Label('Data da venda[red]*[/red]')
                            yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="data_venda")

                            yield Label('Status da venda[red]*[/red]')
                            yield Select([('Em andamento', 1),
                                          ('Aguardando pagamento', 2),
                                          ('Finalizada', 3),
                                          ('Cancelada', 4)],
                                         type_to_search=True,
                                         id='select_status_venda',
                                         allow_blank=False
                                         )

                        with HorizontalGroup():
                            yield Label("Comentários")
                            yield TextArea(
                                placeholder='Detalhes da venda, dos produtos, da entrega, quem comprou, entre outros',
                                id='text_comentario')

                    with HorizontalGroup(id='bt_tela_vendas'):
                        yield Button('Cadastrar',  id='bt_cadastrar', disabled=True)
                        yield Button('Limpar', id='bt_limpar', disabled=True)
                        yield Button('Voltar', id='bt_voltar')

            with TabPane('Atualizar venda', id='tab_atualizar_venda'):
                with Collapsible(title='Expandir tabela de venda'):
                    with VerticalScroll():
                        yield DataTable(id='tabela_vendas')

                yield Rule(orientation='horizontal', line_style='solid')

                with HorizontalGroup():
                    yield Static(self.texto_static_alteracao, id="static_alteracao_venda")
                    yield Button('Preencher dados', id='bt_preencher_dados')

                with VerticalGroup():
                    with HorizontalGroup():
                        yield Label('Data da venda')
                        yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="data_alterada")

                        yield Label('Status da venda')
                        yield Select([('Em andamento', 1),
                                      ('Aguardando pagamento', 2),
                                      ('Finalizada', 3),
                                      ('Cancelada', 4)],
                                     type_to_search=True,
                                     id='select_status_venda_alterada',
                                     allow_blank=False
                                     )

                    with HorizontalGroup():
                        yield Label("Comentários")
                        yield TextArea(
                            placeholder='Detalhes da venda, dos produtos, da entrega, quem comprou, entre outros',
                            id='text_comentario_alterado')

                with HorizontalGroup(id='bt_tela_encomendas'):
                    yield Button("Alterar", id='bt_alterar', disabled=True)
                    yield Button('Deletar', id='bt_deletar', disabled=True)
                    yield Button('Voltar', id='bt_voltar')

    def atualizar_select_produtos(self):
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one("#select_produtos_venda", Select).set_options(
            self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    def atualizar_static_produto(self):
        try:
            id_produto = self.query_one("#select_produtos_venda", Select).value

            static = self.query_one("#static_produto", Static)

            id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
                id_produto)

            novo_texto = f'''
            Informações do produto: ID {id_produto}
            Produto selecionado: {nome}   |   Quantidade em estoque: {quantidade} 
            Valor unitário: {valor_unitario}
                '''

            static.update(novo_texto)
        except:
            pass

    def atualizar_static_venda(self):

        novo_texto = 'Venda: \n\n'

        try:
            static = self.query_one('#static_venda', Static)

            for item in self.PRODUTOS_QUANTIDADE.items():
                id_produto, quantidade = item

                _id_produto, nome, _quantidade, valor_unitario, _valor_custo, _aceita_encomenda, _descricao, _imagem = controller.select_produto_id(
                    id_produto)

                valor_produtos = (valor_unitario * int(quantidade))

                novo_texto += f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: {valor_unitario:.2f} | Valor total: {valor_produtos:.2f}\n'

            self.VALOR_TOTAL_VENDA.append(valor_produtos)
            valor_total = sum(self.VALOR_TOTAL_VENDA)

            static.update(
                f'{novo_texto} \n ------------------- Total da venda: {valor_total:.2f}')

        except:
            pass

    def atualizar_static_alteracao(self):
        static = self.query_one('#static_alteracao_venda', Static)
        novo_texto = ''

        id_encomenda, produtos, prazo, comentario, status, valor_final = self.VENDA_ALTERACAO

        if comentario == None:
            comentario = ''

        novo_texto = f'''Venda: ID {id_encomenda}\n\nProdutos: {produtos}\nPrazo: {prazo}\nStatus: {status}\nComentários: {comentario}\nValor total: {valor_final:.2f}'''
        # TEM QUE IR VALOR UNITÁRIO E VALOR FINAL
        static.update(novo_texto)

    def adicionar_dicionario_venda(self):
        id_produto = self.query_one("#select_produtos_venda", Select).selection
        quantidade_vendida = self.query_one(
            "#quantidade_venda", Input).value

        self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida

    def limpar_inputs(self):
        self.query_one("#data_venda", Input).clear()
        self.query_one("#select_status_venda", Select).value = 1
        self.query_one("#text_comentario", TextArea).clear()
        self.query_one("#select_produtos_venda", Select).clear()
        self.query_one('#quantidade_venda', Input).clear()
        self.query_one('#static_produto', Static).update(
            self.texto_static_produto)
        self.query_one('#static_venda', Static).update(
            self.texto_static_venda)

    def limpar_inputs_alteracao(self):
        self.query_one("#data_alterada", MaskedInput).clear()
        self.query_one("#select_status_venda_alterada", Select).value = 1
        self.query_one("#text_comentario_alterado", TextArea).clear()
        self.query_one("#static_alteracao_venda", Static).update(
            self.texto_static_venda)
        self.query_one("#bt_alterar", Button).disabled = True

    def atualizar_tabela_vendas(self):
        tabela = self.query_one("#tabela_vendas", DataTable)

        dados_vendas = controller.listar_vendas()

        for id_encomenda, detalhes in dados_vendas.items():
            nome_produtos = [''.join([f'{nome}, ({quantidade}), R${valor_unitario} | '])
                             for nome, quantidade, valor_unitario in detalhes['produtos']]

            status = detalhes['status']
            valor_final = detalhes['valor_final']

            if detalhes['status'] == 1:
                status = 'Em produção'
            elif detalhes['status'] == 2:
                status = 'Finalizada'
            elif detalhes['status'] == 3:
                status = 'Vendida'
            elif detalhes['status'] == 4:
                status = 'Cancelada'

            if id_encomenda not in tabela.rows:
                tabela.add_row(id_encomenda, ''.join(nome_produtos),
                               detalhes['data'], detalhes['comentario'], status, valor_final)

    def resetar_tabela_vendas(self):
        tabela = self.query_one("#tabela_vendas", DataTable)

        tabela.clear()

        self.atualizar_tabela_vendas()

    def preencher_alteracoes_venda(self):
        novo_prazo = self.query_one("#data_alterada", MaskedInput)
        novo_status = self.query_one("#select_status_venda_alterada", Select)
        novo_comentario = self.query_one("#text_comentario_alterado", TextArea)

        _id_encomenda, _produtos, prazo, comentario, status = self.VENDA_ALTERACAO
        comentario = str(comentario)

        if status == 'Em produção':
            status = 1
        elif status == 'Finalizada':
            status = 2
        elif status == 'Vendida':
            status = 3
        elif status == 'Cancelada':
            status = 4

        if comentario == 'None':
            comentario = ''

        novo_prazo.value = prazo
        novo_status.value = status
        novo_comentario.text = comentario

    def update_venda(self):
        id_venda = self.VENDA_ALTERACAO[0]

        status = self.query_one('#select_status_venda_alterada', Select).value
        data = self.query_one('#data_alterada', Input).value
        comentario = self.query_one('#text_comentario_alterado', TextArea).text

        controller.update_venda(
            id_venda=id_venda, data=data, status=status,  comentario=comentario)

    def delete_venda(self):
        id_venda = self.VENDA_ALTERACAO[0]
        controller.delete_venda(id_venda)
        self.notify(
            f'Venda ID {id_venda} deletada com sucesso!', severity='error')

    @on(DataTable.RowSelected)
    async def on_row_selected(self, event: DataTable.RowSelected):
        encomenda = self.query_one('#tabela_vendas', DataTable)
        self.VENDA_ALTERACAO = encomenda.get_row(event.row_key)
        self.atualizar_static_alteracao()
        self.query_one("#bt_alterar", Button).disabled = False
        self.query_one("#bt_deletar", Button).disabled = False

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        match event.select.id:
            case 'select_produtos_venda':
                self.ID_PRODUTO = event.select.value
                self.atualizar_static_produto()

            case 'select_id_venda':
                self.atualizar_static_alteracao()

    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        match event.input.id:
            case 'quantidade_venda':
                self.query_one("#bt_adicionar_quantidade",
                               Button).disabled = False

            case 'data_venda':
                if event.input.value == '':
                    self.query_one("#bt_cadastrar", Button).disabled = True
                    self.query_one("#bt_limpar", Button).disabled = True
                else:
                    self.query_one("#bt_cadastrar", Button).disabled = False
                    self.query_one("#bt_limpar", Button).disabled = False

    @on(TextArea.Changed)
    async def on_textarea(self, event: TextArea.Changed):
        if event.text_area.id == 'text_comentario':
            self.query_one("#bt_limpar", Button).disabled = False

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_adicionar_quantidade':

                self.adicionar_dicionario_venda()
                self.atualizar_static_venda()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')

            case 'bt_cadastrar':
                status = self.query_one(
                    '#select_status_venda', Select).value
                data = self.query_one("#data_venda", MaskedInput).value
                comentario = self.query_one("#text_comentario", TextArea).text

                produtos = self.PRODUTOS_QUANTIDADE

                valor_final = sum(self.VALOR_TOTAL_VENDA)

                if produtos == {}:
                    self.notify("Adicione pelo menos um produto!")
                elif len(data) < 10:
                    self.notify("Preencha o prazo no formato DD/MM/AAAA")
                else:
                    controller.insert_venda(
                        data=data, valor_final=valor_final, status=status, comentario=comentario, produtos=produtos)

                    self.notify('Venda cadastrada com sucesso!')
                    self.PRODUTOS_QUANTIDADE.clear()
                    self.limpar_inputs()
                    self.atualizar_tabela_vendas()
                    self.resetar_tabela_vendas()

            case 'bt_preencher_dados':
                try:
                    self.preencher_alteracoes_venda()
                except:
                    self.notify("Ops! Você precisa selecionar uma venda")

            case 'bt_alterar':
                self.update_venda()
                self.resetar_tabela_vendas()
                self.limpar_inputs_alteracao()

            case 'bt_deletar':
                self.delete_venda()
                self.resetar_tabela_vendas()

            case 'bt_limpar':
                self.limpar_inputs()


class TelaPesquisa(Screen):
    TITLE = 'Pesquisa'

    # def __init__(self, name = None, id = None, classes = None):
    #     super().__init__(name, id, classes)
    #     self.LISTA_DE_PRODUTOS = controller.listar_produtos()

    # def on_mount(self):
    #     tabela_estoque = self.query_one("#tabela_estoque", DataTable)
    #     tabela_estoque.border_title = "Produtos"
    #     tabela_estoque.cursor_type = 'row'
    #     tabela_estoque.zebra_stripes = True

    #     tabela_estoque.add_columns('ID produto', 'Produto',
    #                        'Valor unitario', 'Valor de custo', 'Quantidade disponível', 'Aceita encomenda', 'Descrição')
    #     self.atualizar_tabela_estoque()

    #     tabela_encomendas = self.query_one("#tabela_encomendas", DataTable)
    #     tabela_encomendas.border_title = "Encomendas"
    #     tabela_encomendas.cursor_type = 'row'
    #     tabela_encomendas.zebra_stripes = True

    #     tabela_encomendas.add_columns('ID encomenda', 'Produtos',
    #                        'Prazo', 'Comentario', 'Status')
    #     self.atualizar_tabela_encomendas()

    #     tabela_vendas = self.query_one("#tabela_vendas", DataTable)
    #     tabela_vendas.border_title = "Vendas"
    #     tabela_vendas.cursor_type = 'row'
    #     tabela_vendas.zebra_stripes = True

    #     tabela_vendas.add_columns('ID venda', 'Produtos',
    #                        'Data', 'Comentario', 'Status', 'Valor final')  # ATUALIZAR ESSES AQUIIIII
    #     self.atualizar_tabela_vendas()

    def compose(self):
        yield Header(show_clock=True)

        with TabbedContent(initial='tab_produtos', id='tabbed_pesquisa'):
            with TabPane('Produtos', id='tab_produtos'):
                with VerticalScroll():
                    yield SelectionList[int](('Todas as encomendas', 1), ('Em andamento', 2), ("Produtos fora de estoque", 3))

                with VerticalScroll():
                    yield DataTable(id='tabela_produtos')

                with HorizontalGroup():
                    yield Select(prompt='Filtrar por:', options=[('nome', 1), ("quantidade", 2), ('valor unitário', 3), ('valor de custo', 4), ('aceita encomenda', 5), ('descrição', 6)])
                    yield Input()
                    yield Button("Pesquisar", disabled=True)

            with TabPane('Encomendas', id='tab_encomendas'):
                with VerticalScroll():
                    yield DataTable(id='tabela_encomendas')

            with TabPane('Vendas', id='tab_vendas'):
                with VerticalScroll():
                    yield DataTable(id='tabela_vendas')

        yield Button('Voltar', id='bt_voltar')

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')

    # def atualizar_tabela_estoque(self):
    #     tabela = self.query_one("#tabela_estoque", DataTable)

    #     id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo = controller.listar_produtos()

    #     if id_produto not in tabela.rows:
    #             tabela.add_row(id_produto, nome, valor_unitario, valor_custo, quantidade, aceita_encomenda, descricao)

    # def atualizar_tabela_encomendas(self):
    #     tabela = self.query_one("#tabela_encomendas", DataTable)

    #     dados_encomendas = controller.listar_encomendas()

    #     for id_encomenda, detalhes in dados_encomendas.items():
    #         nome_produtos = [''.join([f'{nome}, ({quantidade}) | '])
    #                          for nome, quantidade in detalhes['produtos']]

    #         status = detalhes['status']

    #         if detalhes['status'] == 1:
    #             status = 'Em produção'
    #         elif detalhes['status'] == 2:
    #             status = 'Finalizada'
    #         elif detalhes['status'] == 3:
    #             status = 'Vendida'
    #         elif detalhes['status'] == 4:
    #             status = 'Cancelada'

    #         if id_encomenda not in tabela.rows:
    #             tabela.add_row(id_encomenda, ''.join(nome_produtos),
    #                            detalhes['prazo'], detalhes['comentario'], status)

    # def atualizar_tabela_vendas(self):
    #     tabela = self.query_one("#tabela_vendas", DataTable)

    #     dados_vendas = controller.listar_vendas()

    #     for id_encomenda, detalhes in dados_vendas.items():
    #         nome_produtos = [''.join([f'{nome}, ({quantidade}), R${valor_unitario} | '])
    #                          for nome, quantidade, valor_unitario in detalhes['produtos']]

    #         status = detalhes['status']
    #         valor_final = detalhes['valor_final']

    #         if detalhes['status'] == 1:
    #             status = 'Em produção'
    #         elif detalhes['status'] == 2:
    #             status = 'Finalizada'
    #         elif detalhes['status'] == 3:
    #             status = 'Vendida'
    #         elif detalhes['status'] == 4:
    #             status = 'Cancelada'

    #         if id_encomenda not in tabela.rows:
    #             tabela.add_row(id_encomenda, ''.join(nome_produtos),
    #                            detalhes['data'], detalhes['comentario'], status, valor_final)
