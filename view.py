import controller

from textual import on

from textual.app import (App, ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput, OptionList, Select, SelectionList, TabbedContent, TabPane, DataTable,
                             Collapsible, Switch, Placeholder, Checkbox, Rule)
from textual.screen import (Screen, ModalScreen)
from textual.containers import (
    Container, VerticalGroup, HorizontalGroup, Grid, Center, ScrollableContainer, Horizontal, Vertical, CenterMiddle, ItemGrid, VerticalScroll, HorizontalScroll)
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

class SidebarMenu(Container):
    'Menu lateral vertical do sistema.'

    def compose(self):

        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Produtos", id="bt_produtos", classes="botoes_inicial", variant="primary")
            yield Button("Encomendas", id="bt_encomendas", classes="botoes_inicial", variant="success")
            yield Button("Vendas", id="bt_vendas", classes="botoes_inicial", variant="warning")
            yield Button("Pesquisa", id="bt_pesquisa", classes="botoes_inicial", variant='error', disabled=True)
            yield Button("Tela inicial", id="bt_inicial", classes="botoes_inicial")

        return super().compose()

    def on_button_pressed(self, event: Button.Pressed):
        'Eventos que ocorrem ao apertar os botões.'
        match event.button.id:
            case "bt_produtos":
                self.app.switch_screen("tela_produtos")
            case "bt_encomendas":
                self.app.switch_screen("tela_encomendas")
            case "bt_vendas":
                self.app.switch_screen("tela_vendas")
            case "bt_pesquisa":
                self.app.switch_screen("tela_pesquisa")
            case "bt_inicial":
                self.app.switch_screen("tela_inicial")


class TelaLogin(Screen):
    'Tela de login do sistema.'

    def compose(self):
        'Composição da tela.'
        yield Header()

        with CenterMiddle(id="container_login"):
            with VerticalGroup():
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

        yield Footer(show_command_palette=False)

    def verificar_login(self):
        'Função de validação do login. Ele faz a criptografia para validar a senha.'
        import hashlib
        from hashlib import sha256

        input_login = self.query_one("#input_login", Input).value.strip()
        input_senha = self.query_one("#input_senha", Input).value.strip()

        if not input_login or not input_senha:
            self.notify(title="Epa!", message="Preencha todos os campos obrigatórios", severity="warning")
            return

        try:
            id_vendedor, login, senha, nome, nome_loja = controller.select_vendedor(
                input_login)

            senha_hash = hashlib.sha256(input_senha.encode('utf-8')).digest()

            if input_login == login and senha_hash == senha:
                self.notify(title="Sucesso!", message="Login realizado")
                self.app.switch_screen('tela_inicial')

        except TypeError:
            self.notify(title="Ops!", message="Login ou senha incorretos!", severity='error')

    @on(Switch.Changed)
    async def on_switch(self, event: Switch.Changed):
        'Ações que ocorrem ao clicar no Switch da tela.'
        mostrar_senha = self.query_one("#switch_senha", Switch).value
        input_senha = self.query_one("#input_senha", Input)

        if mostrar_senha == True:
            input_senha.password = False
        else:
            input_senha.password = True

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao clicar nos botões da tela.'
        match event.button.id:
            case 'bt_login':
                self.verificar_login()

            case "bt_sair":
                self.app.exit()

            case "bt_cadastrar":
                self.app.switch_screen("tela_cadastro")


class TelaCadastro(Screen):
    'Tela de cadastro de usuário do sistema.'

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

        yield Footer(show_command_palette=False)

    def limpar_campos(self):
        'Reseta os campos preenchidos da TelaCadastro.'
        self.query_one("#input_login", Input).clear()
        self.query_one("#input_senha", Input).clear()
        self.query_one("#input_nome", Input).clear()
        self.query_one("#input_nome_loja", Input).clear()

    def pegar_dados_vendedor(self):
        'Pega as informações inseridas nos campos de cadastro de usuário.'
        login = self.query_one("#input_login", Input).value.strip()
        senha = self.query_one("#input_senha", Input).value.strip()
        nome = self.query_one("#input_nome", Input).value.strip().capitalize()
        nome_loja = self.query_one("#input_nome_loja", Input).value.strip().capitalize

        return login, senha, nome, nome_loja

    def insert_vendedor(self):
        'Insere os dados de novo usuário no banco de dados do sistema.'
        from hashlib import sha256

        login, senha, nome, nome_loja = self.pegar_dados_vendedor()

        senha_codificada = sha256(senha.encode('utf-8')).digest()

        try:
            controller.insert_vendedor(
                login, senha_codificada, nome, nome_loja)
            self.notify(title="Sucesso!", message="Usuário cadastrado")
            self.app.switch_screen('tela_login')
            self.limpar_campos()

        except:
            self.notify(title="Ops!", message="Algo deu errado", severity="warning")

    @on(Switch.Changed)
    async def on_switch(self, event: Switch.Changed):
        'Ações que ocorrem ao clicar no Switch da tela.'

        mostrar_senha = self.query_one("#switch_senha", Switch).value
        input_senha = self.query_one("#input_senha", Input)

        if mostrar_senha == True:
            input_senha.password = False
        else:
            input_senha.password = True

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao clicar nos botões da tela.'
        match event.button.id:
            case 'bt_voltar':
                self.app.switch_screen('tela_login')

            case "bt_cadastrar":
                login, senha, nome, nome_loja = self.pegar_dados_vendedor()

                if not nome or not login or not senha:
                    self.notify(title="Ops!", message="Insira todos os dados necessários", severity="warning")
                elif "@" not in login or ".com" not in login:
                    self.notify(title="Ops!", message="Insira um e-mail válido!", severity="warning")
                elif len(senha) < 6:
                    self.notify(title="Ops!", message="A senha deve ter no mínimo 6 caracteres!", severity="warning")
                else:
                    self.insert_vendedor()


class TelaInicial(Screen):
    'Tela Inicial do sistema.'

    def compose(self):
        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Produtos", id="bt_produtos", classes="botoes_inicial", variant="primary")
            yield Button("Encomendas", id="bt_encomendas", classes="botoes_inicial", variant="success")
            yield Button("Vendas", id="bt_vendas", classes="botoes_inicial", variant="warning")
            yield Button("Pesquisa", id="bt_pesquisa", classes="botoes_inicial", variant='error', disabled=True)
            yield Button("Sair", id="bt_sair", classes="botoes_inicial")

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao clicar nos botões da tela.'

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


class TelaProdutos(Screen):
    'Tela de cadastro, alteração e remoção de produtos do sistema.'

    TITLE = 'Produtos'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.ID_PRODUTO = int()
        self.checkbox_list_produto = list()

    def on_mount(self):
        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)
        tabela.border_title = "Vendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns("Nome", "Quantidade", "Valor unitário", "Valor custo", "Aceita encomenda", "Descrição") 
        self.atualizar_tabela_produtos()

    def on_screen_resume(self):
        'Ações que ocorrem ao voltar para a TelaProdutos.'
        self.limpar_texto_static()
        self.atualizar_select_produtos()
        self.limpar_inputs_produtos()

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        yield SidebarMenu(id="sidebar")

        with TabbedContent(initial='tab_cadastro', id='tabbed_pesquisa'):
            with TabPane("Cadastro de produtos", id="tab_cadastro"):
                with ScrollableContainer(id='tela_produtos'):
                    with Collapsible(title="Expandir para alterar um produto cadastrado", id="collapsible_produtos"):
                        with HorizontalGroup(id='class_select_produtos'):
                            yield Label('Selecione o produto')
                            yield Select(self.LISTA_DE_PRODUTOS,
                                        type_to_search=True,
                                        id='select_produtos',
                                        allow_blank=True,
                                        prompt='Selecione o produto'
                                        )

                        with HorizontalGroup():
                            yield Static(f'\n\nSelecione o produto para visualizar as informações', id='stt_info_produto')
                            yield Button('Preencher campos', variant='primary', id='bt_preencher_campos')

                    yield Rule(orientation='horizontal', line_style='solid')

                    with ScrollableContainer(id='inputs_cadastro'):
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
                                id='input_imagem', disabled=True
                            )
                            yield Label('Aceita encomendas?')
                            yield Switch(value=False, id='select_encomenda')

                        with HorizontalGroup():

                            yield Label("Descrição do produto")
                            yield TextArea(
                                placeholder='Descrição',
                                id='text_descricao')

                    with HorizontalGroup(id='bt_tela_produtos'):
                        yield Button('Cadastrar',  id='bt_cadastrar', disabled=True)
                        yield Button("Alterar", id='bt_alterar', disabled=True)
                        yield Button('Limpar', id='bt_limpar', disabled=True)
                        yield Button('Deletar', id='bt_deletar', disabled=True)
                        yield Button('Voltar', id='bt_voltar')

            with TabPane('Lista de produtos', id='tab_produtos'):
                with VerticalScroll():

                    with HorizontalGroup():
                        yield Checkbox("Em estoque", True, id="cbox_estoque", )
                        yield Checkbox("Fora de estoque", True, id="cbox_fora_estoque")
                        yield Checkbox("Aceita encomenda", False, id="cbox_encomenda")
                        yield Checkbox("Não aceita encomenda", False, id="cbox_nao_encomenda")

                with VerticalScroll():
                    yield DataTable(id='tabela_produtos_pesquisa')
                    yield Button('Voltar', id='bt_voltar')

        yield Footer(show_command_palette=False)

    def pegar_inputs_produtos(self):
        'Pega os campos da TelaProdutos.'
        nome = self.query_one("#input_nome", Input)
        quantidade = self.query_one("#input_quantidade", Input)
        valor_unitario = self.query_one("#input_valor_unitario", Input)
        valor_custo = self.query_one("#input_valor_custo", Input)
        imagem = self.query_one("#input_imagem", Input)
        aceita_encomenda = self.query_one("#select_encomenda", Switch)
        descricao = self.query_one("#text_descricao", TextArea)

        return nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao

    def pegar_valores_inputs(self):
        'Pega os valores inseridos nos campos da TelaProdutos.'
        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_inputs_produtos()

        nome = nome.value.strip().capitalize()
        quantidade = quantidade.value
        valor_unitario = valor_unitario.value
        valor_custo = valor_custo.value
        imagem = imagem.value
        aceita_encomenda = aceita_encomenda.value
        descricao = descricao.text.strip()

        return nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao

    def limpar_inputs_produtos(self):
        'Reseta os valores dos campos da TelaProdutos.'
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
        self.query_one("#bt_deletar", Button).disabled = True
        self.query_one("#select_produtos", Select).value = Select.BLANK

    def atualizar_texto_static(self):
        'Atualiza as informações do produto selecionado na TelaProdutos.'
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

        texto_static.update(
            f'Informações do produto selecionado:\n\n[b]  Nome:[/b] {nome}\n[b]  Quantidade disponível:[/b] {quantidade}\n[b]  Valor unitário:[/b] R$ {valor_unitario}\n  [b]Valor de custo:[/b] R$ {valor_custo}\n  [b]Aceita encomenda:[/b] {aceita_encomenda}\n  [b]Descrição:[/b] {descricao}')

    def limpar_texto_static(self):
        'Reseta as informações do produto selecionado na TelaProdutos.'
        texto_static = self.query_one("#stt_info_produto", Static)
        texto_static.update(f"Selecione o produto para visualizar as informações")

    def cadastrar_produto(self):
        'Cadastra o produto.'
        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

        if nome == '' or quantidade == '' or valor_unitario == '':
            self.notify(
                title="Ops!", message="Insira todos os dados obrigatórios", severity='warning')
        else:
            validacao_nome = controller.select_produto_nome(nome=nome)            
            if validacao_nome != None:
                self.notify(title="Eita!", message="Nome de produto já cadastrado", severity="error")
            else:
                id_produto = None
                controller.insert_produto(
                    id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)
                self.notify(title='Feito!',
                            message=f"{nome} cadastrado com sucesso!")

                self.atualizar_select_produtos()
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

    def atualizar_select_produtos(self):
        'Atualiza o Select de produtos.'
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one(Select).set_options(self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    def preencher_campos(self):
        'Preenche os campos da TelaProdutos com as informações do produto selecionado.'
        id_produto = self.query_one(
            "#select_produtos", Select).value

        self.ID_PRODUTO = id_produto

        _, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
            id_produto)

        input_nome, input_quantidade, input_valor_unitario, input_valor_custo, input_imagem, input_aceita_encomenda, input_descricao = self.pegar_inputs_produtos()
        if imagem is None:
            imagem = ""
        if descricao is None:
            descricao = ""
        if valor_custo is None:
            valor_custo = ""

        input_nome.value = str(nome)
        input_quantidade.value = str(quantidade)
        input_valor_unitario.value = str(valor_unitario)
        input_valor_custo.value = str(valor_custo)
        input_imagem.value = str(imagem)
        input_aceita_encomenda.value = aceita_encomenda
        input_descricao.text = str(descricao)

        self.query_one("#collapsible_produtos", Collapsible).collapsed = True
        self.query_one("#bt_alterar", Button).disabled = False
        self.query_one("#bt_deletar", Button).disabled = False

    def alterar_produto(self):
        id_produto = self.query_one("#select_produtos", Select).value

        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

        controller.update_produto(
            id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

        self.atualizar_select_produtos()

        self.limpar_inputs_produtos()
        self.limpar_texto_static()

        self.notify(title="Feito!", message=f"Produto {nome} alterado com sucesso!")

        self.query_one("#collapsible_produtos", Collapsible).expand = False

    def deletar_produto(self):
        id_produto = self.ID_PRODUTO

        if id_produto > 0:
            controller.delete_produto(id_produto)
            self.notify(title="Já era!", message="Produto excluído com sucesso")

            self.atualizar_select_produtos()
            self.limpar_inputs_produtos()
            self.limpar_texto_static()
            self.ID_PRODUTO = 0

        else:
            self.notify(title="Ops!", message="Você precisa selecionar um produto!", severity='warning')


    
    def pegar_checkbox_produtos(self):
        'Pega os valores dos Checkboxes da TelaVendas.'

        estoque = self.query_one("#cbox_estoque", Checkbox).value
        fora_estoque = self.query_one("#cbox_fora_estoque", Checkbox).value
        encomenda = self.query_one("#cbox_encomenda", Checkbox).value
        nao_encomenda = self.query_one("#cbox_nao_encomenda", Checkbox).value

        if estoque:
            self.checkbox_list_produto.append(1)

        if fora_estoque:
            self.checkbox_list_produto.append(2)

        if encomenda:
            self.checkbox_list_produto.append(3)   
        
        if nao_encomenda:
            self.checkbox_list_produto.append(4)

    def atualizar_tabela_produtos(self): #### Não filtra se dois checkboxes diferentes são apertados.
        'Atualiza as informações para a tabela de produtos da TelaPesquisa.'

        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.pegar_checkbox_produtos()

        for produto in self.LISTA_DE_PRODUTOS:
            id_produto = produto[1]
            _id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, _imagem = controller.select_produto_id(id_produto)

            adicionar_na_tabela = list()

            if int(quantidade) > 0:
                adicionar_na_tabela.append(1)
            else:
                adicionar_na_tabela.append(2)
            
            if aceita_encomenda == True:
                adicionar_na_tabela.append(3)
            else:
                adicionar_na_tabela.append(4)
                            
            if any(item in adicionar_na_tabela for item in self.checkbox_list_produto):                
                if str(valor_custo) == 'None':
                    valor_custo = ''
                else:
                    valor_custo = f"R$ {valor_custo}"
                if str(descricao) == 'None':
                    descricao = ''
                if aceita_encomenda == False:
                    aceita_encomenda = 'Não'
                else:
                    aceita_encomenda = 'Sim'

                tabela.add_row(nome, quantidade, f"R$ {valor_unitario}", valor_custo, aceita_encomenda, descricao)

    def resetar_tabela_produtos(self):
        'Reseta e preenche a tabela de produtos da TelaPesquisa.'
        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)

        tabela.clear()

        self.atualizar_tabela_produtos()

    @on(Checkbox.Changed)
    async def on_checkbox_change(self, event: Checkbox.Changed):
        'Ações que ocorrem ao selecionar um Checkbox.'
        
        if len(self.checkbox_list_produto) > 0:
            self.checkbox_list_produto.clear()  
        self.resetar_tabela_produtos()

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_pesquisar_produto':
                self.resetar_tabela_produtos_pesquisa()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')


    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        'Ações que ocorrem ao preencher o Input.'
        match event.input.value:

            case '':
                self.query_one("#bt_cadastrar", Button).disabled = True
                self.query_one("#bt_limpar", Button).disabled = True
            case str():
                self.query_one("#bt_cadastrar", Button).disabled = False
                self.query_one("#bt_limpar", Button).disabled = False

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        'Ações que ocorrem ao trocar o item selecioando no Select.'
        self.ID_PRODUTO = event.select.value
        if event.select.value == Select.BLANK:
            pass
        else:
            self.atualizar_texto_static()

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao clicar nos botões da tela.'

        match event.button.id:
            case 'bt_cadastrar':
                self.cadastrar_produto()

            case 'bt_limpar':
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

            case 'bt_preencher_campos':
                try:
                    self.preencher_campos()
                except:
                    self.notify(
                        title="Ops!", message="Nenhum produto selecionado!", severity='warning')

            case 'bt_alterar':
                self.alterar_produto()

            case 'bt_deletar':
                self.deletar_produto()


class TelaEncomendas(Screen):
    'Tela de cadastro, alteração e remoção de encomendas do sistema.'

    TITLE = 'Encomendas'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.ID_PRODUTO = int()
        self.PRODUTOS_QUANTIDADE = dict()
        self.texto_static_produto = 'Selecione um produto para visualizar as informações'
        self.texto_static_encomenda = 'Aqui vão as informações da encomenda'
        self.texto_static_alteracao = 'Selecione uma encomenda para ver as informações'
        self.ENCOMENDA_ALTERACAO = list()
        self.PRODUTO_SELECIONADO = dict()
        self.checkbox_list = list()

    def on_screen_resume(self):
        'Ações que ocorrem ao voltar para a TelaProdutos.'

        self.atualizar_select_produtos()
        self.limpar_inputs()
        self.limpar_inputs_alteracao()
        self.query_one("#coll_encomendas", Collapsible).collapsed = True

    def on_mount(self):
        tabela_cadastro_encomenda = self.query_one(
            "#tabela_cadastro_encomenda", DataTable)
        tabela_cadastro_encomenda.border_title = "Cadastro de encomenda"
        tabela_cadastro_encomenda.cursor_type = 'row'
        tabela_cadastro_encomenda.zebra_stripes = True
        tabela_cadastro_encomenda.add_columns("ID", "Produto", "Quantidade encomendada")

        tabela = self.query_one("#tabela_encomendas", DataTable)
        tabela.border_title = "Encomendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns('ID encomenda', 'Produtos',
                           'Prazo', 'Comentário', 'Status')
        self.atualizar_tabela_encomendas()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield SidebarMenu(id="sidebar")

        with TabbedContent(initial='tab_cadastrar_encomeda'):

            with TabPane('Cadastrar encomenda', id='tab_cadastrar_encomeda'):
                with Collapsible(title="Expandir para adicionar produtos à encomenda"):
                    with HorizontalGroup(id='cnt_select_produtos'):
                        yield Label('Selecione um produto:')
                        yield Select(self.LISTA_DE_PRODUTOS,
                                        type_to_search=True,
                                        id='select_produtos',
                                        allow_blank=True,
                                        prompt='Selecione o produto para adicionar à encomenda'
                                        )

                    with VerticalGroup():
                        with HorizontalGroup():
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
                                
                yield Rule()

                with ScrollableContainer():
                    with HorizontalGroup():
                        yield DataTable(id="tabela_cadastro_encomenda")
                        yield Button("Remover", id="bt_remover", disabled=True)
                    with VerticalGroup():
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
                with Collapsible(title='Expandir tabela de encomendas', id="coll_encomendas"):
                        with HorizontalGroup():
                            yield Checkbox("Em produção", True, id="cbox_producao")
                            yield Checkbox("Finalizada", True, id='cbox_finalizada')
                            yield Checkbox("Vendida", True, id="cbox_vendida")
                            yield Checkbox("Cancelada", True, id="cbox_cancelada")

                        with VerticalScroll():
                            yield DataTable(id='tabela_encomendas')

                            with HorizontalGroup(id="horizontal_alteracao_encomenda"):
                                yield Static(self.texto_static_alteracao, id="static_alteracao_encomenda")
                                
                                yield Button('Preencher dados', id='bt_preencher_dados', disabled=True)

                                with Center(id="tranformar_venda"):
                                    yield Button('Transformar em venda', id='bt_transformar_venda', disabled=True)
                                    yield Label('[blue]Isso não dá baixa no estoque![blue]', id="lbl_transformar_venda")
            
                yield Rule(orientation='horizontal', line_style='solid')

                with VerticalGroup():
                    yield Static("[b]Informações da encomenda selecionada:[/b]", id="stt_alteracao_produto")

                    with HorizontalGroup():
                        yield Label('Prazo de entrega[red]*[/red]')
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

        yield Footer(show_command_palette=False)


    def verificar_data(self, data_inserida, formato="%d/%m/%Y"):
        'Verifica se a data inserida é válida.'
        from datetime import datetime
        try:
            datetime.strptime(data_inserida, formato)
            return True
        except ValueError:
            return self.notify(title="Data inválida", message="Preencha com uma data válida", severity='warning')
        
    def cadastrar_encomenda(self):
        'Cadastra a encomenda no banco de dados.'
        status = self.query_one(
            '#select_status_cadastro', Select).value
        prazo = self.query_one("#prazo_encomenda", Input).value
        comentario = self.query_one("#text_comentario", TextArea).text.strip()
        produtos = self.PRODUTOS_QUANTIDADE
        
        validacao_data = self.verificar_data(prazo)
    
        if len(produtos) == 0:
            self.notify(title="Nenhum produto adicionado", message="Adicione pelo menos um produto!", severity="warning")
        elif len(prazo) < 10:
            self.notify(title="Data inválida!", message="Preencha o prazo no formato DD/MM/AAAA", severity="warning")
        elif validacao_data == True:
            controller.insert_encomenda(
                status=status, prazo=prazo, comentario=comentario, produtos=produtos)

            self.notify(title="Feito!", message='Encomenda cadastrada com sucesso!')
            self.PRODUTOS_QUANTIDADE.clear()
            self.limpar_inputs()
            self.atualizar_tabela_encomendas()
            self.resetar_tabela_encomendas()

    def update_encomenda(self):
        'Envia ao banco de dados as alterações da encomenda.'
        id_encomenda = self.ENCOMENDA_ALTERACAO[0]

        prazo = self.query_one("#prazo_alterado", MaskedInput).value
        status = self.query_one("#select_status_alterado", Select).value
        comentario = self.query_one("#text_comentario_alterado", TextArea).text.strip()

        validacao_data = self.verificar_data(data_inserida=prazo)

        if validacao_data == True:
            controller.update_encomendas(
                id_encomenda=id_encomenda, prazo=prazo, comentario=comentario, status=status)
            
            self.notify(title="Feito!", message="Encomenda alterada com sucesso!")
            self.limpar_inputs_alteracao()
            self.resetar_tabela_encomendas()

    def deletar_encomenda(self):
        'Deleta do banco de dados a encomenda.'
        id_encomenda = self.ENCOMENDA_ALTERACAO[0]
        controller.delete_encomenda(id_encomenda)
        self.notify(title="Feito", message='Encomenda deletada com sucesso!')
        self.ENCOMENDA_ALTERACAO.clear()
        self.limpar_inputs_alteracao()
        self.atualizar_tabela_encomendas()
    
    def atualizar_select_produtos(self):
        'Atualiza o select de produtos quando um novo produto é cadastrado na TelaProdutos.'
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one("#select_produtos", Select).set_options(
            self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    def atualizar_static_produto(self):
        'Atualiza as informações referente ao produto selecionado.'
        try:
            id_produto = self.query_one("#select_produtos", Select).value

            static = self.query_one("#static_produto", Static)

            id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
                id_produto)

            novo_texto = f'[b]Informações do produto:[/b]\n\n[b] Produto selecionado:[/b] {nome}\n[b] Quantidade em estoque: [/b]{quantidade}'

            static.update(novo_texto)
        except Exception as e:
            pass

    def atualizar_static_alteracao(self):
        'Atualiza as informações referente a encomenda selecionada na tela de Atualização de Encomenda.'
        static = self.query_one('#static_alteracao_encomenda', Static)
        novo_texto = f""

        _id_encomenda, produtos, prazo, comentario, status = self.ENCOMENDA_ALTERACAO

        if comentario == None:
            comentario = '--'

        novo_texto = f'''[b]Encomenda:[/b] \n\n[b]Produtos:[/b] {produtos}\n[b]Prazo:[/b] {prazo}\n[b]Status:[/b] {status}\n[b]Comentários:[/b] {comentario}'''

        static.update(novo_texto)

    def atualizar_static_alteracao_produto(self):
        'Atualiza as informações de produtos na tela de alteração de encomendas.'

        static = self.query_one("#stt_alteracao_produto", Static)
        produtos = self.ENCOMENDA_ALTERACAO[1]

        novo_texto = f"[b]Encomenda selecionada:[/b] \n [b]Produtos e quantidades:[/b] {produtos}"
        static.update(novo_texto)
        
    def adicionar_dicionario_encomenda(self):
        'Adiciona os produtos selecionados de uma encomenda para um dict().'
        id_produto = self.query_one("#select_produtos", Select).selection
        quantidade_encomendada = self.query_one(
            "#quantidade_encomenda", Input).value

        
        if id_produto is None:
            self.notify(title="Nenhum produto selecionado", message="Selecione um produto", severity='warning')

        elif quantidade_encomendada == 0 or quantidade_encomendada.startswith("0") or quantidade_encomendada.startswith("-") or quantidade_encomendada == "":
            self.notify(title="Quantidade inválida", message="Adicione uma quantidade válida!", severity='warning')
        else:
            self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_encomendada

    def limpar_statics(self):
        'Limpa os textos dos statics.'
        static = self.query_one("#stt_alteracao_produto", Static)
        produtos = self.ENCOMENDA_ALTERACAO[1]

        novo_texto = f"[b]Encomenda selecionada:[/b] \n [b]Produtos e quantidades:[/b] {produtos}"
        static.update(novo_texto)

    def limpar_inputs(self):
        'Reseta os valores inseridos nos campos da tela de Cadastro de Encomendas.'
        self.query_one("#prazo_encomenda", Input).clear()
        self.query_one("#select_status_cadastro", Select).value = 1
        self.query_one("#text_comentario", TextArea).clear()
        self.query_one("#select_produtos", Select).clear()
        self.query_one('#quantidade_encomenda', Input).clear()
        self.query_one('#static_produto', Static).update(
            self.texto_static_produto)
        self.query_one("#tabela_cadastro_encomenda", DataTable).clear()
        self.query_one("#bt_remover", Button).disabled = True

    def limpar_inputs_alteracao(self):
        'Reseta os valores inseridos nos campos da tela de Atualização de Encomendas.'
        self.query_one("#prazo_alterado", MaskedInput).clear()
        self.query_one("#select_status_alterado", Select).value = 1
        self.query_one("#text_comentario_alterado", TextArea).clear()
        self.query_one("#static_alteracao_encomenda", Static).update(
            self.texto_static_encomenda)
        self.query_one("#stt_alteracao_produto", Static).update("[b]Informações da encomenda selecionada:[/b]")
        
        self.query_one("#bt_alterar", Button).disabled = True
        self.query_one("#bt_deletar", Button).disabled = True

    def pegar_checkbox(self):
        'Pega os valores preenchidos nos campos Checkbox para atualizar a tabela.'
        producao = self.query_one("#cbox_producao", Checkbox).value
        finalizada = self.query_one("#cbox_finalizada", Checkbox).value
        vendida = self.query_one("#cbox_vendida", Checkbox).value
        cancelada = self.query_one("#cbox_cancelada", Checkbox).value

        if producao:
            self.checkbox_list.append(1)

        if finalizada:
            self.checkbox_list.append(2)

        if vendida:
            self.checkbox_list.append(3)

        if cancelada:
            self.checkbox_list.append(4)

    def atualizar_tabela_encomendas(self):
        'Atualiza os valores a serem preenchidos na tabela de encomendas.'
        tabela = self.query_one("#tabela_encomendas", DataTable)

        dados_encomendas = controller.listar_encomendas()

        self.pegar_checkbox()

        for id_encomenda, detalhes in dados_encomendas.items():
            nome_produtos = [''.join([f'{nome}, ({quantidade}) | '])
                             for nome, quantidade in detalhes['produtos']]

            status = detalhes['status']
            comentario = detalhes['comentario']

            if status in self.checkbox_list:

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
                                   detalhes['prazo'], comentario, status)

    def resetar_tabela_encomendas(self):
        'Reseta e atualiza a tela de encomendas.'
        tabela = self.query_one("#tabela_encomendas", DataTable)

        tabela.clear()

        self.atualizar_tabela_encomendas()

    def atualizar_tabela_cadastro_encomenda(self):
        'Atualiza os valores a serem preenchidos na tabela de cadastro da encomenda.'
        
        tabela = self.query_one("#tabela_cadastro_encomenda", DataTable)

        for item in self.PRODUTOS_QUANTIDADE.items():
            id_produto, quantidade = item

            _id_produto, nome, _quantidade, _valor_unitario, _valor_custo, _aceita_encomenda, _descricao, _imagem = controller.select_produto_id(
                id_produto)

            tabela.add_row(_id_produto, nome, quantidade)
        
    def resetar_tabela_cadastro_encomenda(self):
        'Reseta e atualiza a tabela de cadastro da encomenda.'

        tabela = self.query_one("#tabela_cadastro_encomenda", DataTable)
        tabela.clear()
        self.atualizar_tabela_cadastro_encomenda()
        self.query_one("#bt_remover", Button).disabled = True
        self.query_one('#quantidade_encomenda', Input).clear()

    def remover_produto_encomenda(self):
        'Remove um produto adicionado em uma encomenda.'

        id_produto = self.PRODUTO_SELECIONADO[0]
        self.PRODUTOS_QUANTIDADE.pop(id_produto)
        self.resetar_tabela_cadastro_encomenda()
        self.notify(title="Removido!", message="Produto removido da encomenda", severity="warning")

    def preencher_alteracoes_encomenda(self):
        'Preenche os campos com as informações da encomenda a ser alterada.'
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

        self.query_one("#coll_encomendas", Collapsible).collapsed = True
        self.query_one("#bt_alterar", Button).disabled = False
        self.query_one("#bt_deletar", Button).disabled = False
        self.atualizar_static_alteracao_produto()

    def transformar_em_venda(self):
        'Transforma uma encomenda em venda.'
        _id_encomenda, produtos, prazo, comentario, status = self.ENCOMENDA_ALTERACAO
        valor_total_venda = list()
        produtos_quantidade = dict()
        venda_produto_quantidade = dict()

        if status == 'Em produção':
            status = 1
        elif status == 'Finalizada':
            status = 2
        elif status == 'Vendida':
            status = 3
        elif status == 'Cancelada':
            status = 4

        nomes_produtos = produtos.strip(" |").split(" | ") 
        for item in nomes_produtos:
            produto, quantidade = item.split(", ")
            produtos_quantidade[produto] = int(quantidade.strip("()"))
        
        for produto, quantidade in produtos_quantidade.items():
            valor_unitario = controller.select_produto_nome(nome=produto)[3] 
            id_produto = controller.select_produto_nome(nome=produto)[0]
            venda_produto_quantidade[id_produto] = quantidade
            valor_total_venda.append(int(quantidade)*int(valor_unitario))


        valor_final = sum(valor_total_venda)

        controller.insert_venda(data=prazo, valor_final=valor_final, status=status, produtos=venda_produto_quantidade, comentario=comentario)

        self.notify(title="Feito!", message="Encomenda registrada nas vendas")

        produtos_quantidade.clear()
        valor_total_venda.clear()

    @on(Checkbox.Changed)
    async def on_checkbox_change(self, event: Checkbox.Changed):
        'Ações que ocorrem ao selecionar um Checkbox.'
        if len(self.checkbox_list) > 0:
            self.checkbox_list.clear()

        self.resetar_tabela_encomendas()

    @on(DataTable.RowSelected)
    async def on_row_selected(self, event: DataTable.RowSelected):
        'Ações que ocorrem ao selecionar uma linha da tabela.'

        match event.data_table.id:
            case "tabela_cadastro_encomenda":
                self.query_one("#bt_remover", Button).disabled = False 
                encomenda = self.query_one('#tabela_cadastro_encomenda', DataTable)
                self.PRODUTO_SELECIONADO = encomenda.get_row(event.row_key)
        
            case "tabela_encomendas":
                encomenda = self.query_one('#tabela_encomendas', DataTable)
                self.ENCOMENDA_ALTERACAO = encomenda.get_row(event.row_key)
                self.atualizar_static_alteracao()
                self.query_one("#bt_preencher_dados", Button).disabled = False
                self.query_one("#bt_transformar_venda", Button).disabled = False

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        'Ações que ocorrem ao selecionar um item no Select.'
        match event.select.id:
            case 'select_produtos':
                self.ID_PRODUTO = event.select.value
                self.atualizar_static_produto()
                self.query_one('#quantidade_encomenda', Input).clear()
                self.query_one("#bt_remover", Button).disabled = True
                self.query_one("#bt_adicionar_quantidade", Button).disabled = True

            case 'select_id_encomenda':
                self.atualizar_static_alteracao()

    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        'Ações que ocorrem ao alterar um Input.'
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
        'Ações que ocorrem ao alterar um campo TextArea.'
        if event.text_area.id == 'text_comentario':
            self.query_one("#bt_limpar", Button).disabled = False

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao pressionar botões da TelaEncomendas.'
        match event.button.id:
            case 'bt_adicionar_quantidade':

                self.adicionar_dicionario_encomenda()
                self.resetar_tabela_cadastro_encomenda()
                self.query_one('#static_produto', Static).update(self.texto_static_produto)
                self.query_one("#bt_adicionar_quantidade", Button).disabled = True
            
            case 'bt_remover':
                self.remover_produto_encomenda()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')

            case 'bt_cadastrar':
                self.cadastrar_encomenda()

            case 'bt_preencher_dados':
                try:
                    self.preencher_alteracoes_encomenda()
                except:
                    self.notify(title="Ops!", message="Você precisa selecionar uma encomenda", severity='warning')

            case 'bt_transformar_venda':
                self.transformar_em_venda()

            case 'bt_alterar':
                prazo = self.query_one("#prazo_alterado", Input).value

                if len(prazo) < 10:
                    self.notify(title="Data inválida!", message="Preencha o prazo no formato DD/MM/AAAA", severity="warning")
                else:
                    self.update_encomenda()

            case 'bt_deletar':
                self.deletar_encomenda()
                self.resetar_tabela_encomendas()

            case 'bt_limpar':
                self.limpar_inputs()


class TelaVendas(Screen):
    'Tela de vendas do sistema'
    TITLE = 'Vendas'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.ID_PRODUTO = int()
        self.PRODUTOS_QUANTIDADE = dict()
        self.PRODUTOS_BAIXA = dict()
        self.PRODUTO_SELECIONADO = dict()
        self.texto_static_produto = 'Selecione um produto para visualizar as informações'
        self.texto_static_venda = 'Adicione produtos para ver o valor total da venda'
        self.texto_static_alteracao = 'Selecione uma venda para ver as informações'
        self.VENDA_ALTERACAO = list()
        self.VALOR_TOTAL_VENDA = list()
        self.checkbox_list = list()

    def on_screen_resume(self):
        'Ações que ocorrem ao voltar para a TelaVendas.'
        self.atualizar_select_produtos()
        self.limpar_inputs()
        self.limpar_inputs_alteracao()
        self.resetar_tabela_cadastro_venda()
        self.resetar_tabela_vendas()
        self.PRODUTOS_BAIXA.clear()
        self.PRODUTOS_QUANTIDADE.clear()

    def on_mount(self):
        'Ações que ocorrem ao montar a TelaVendas.'
        tabela_cadastro_venda = self.query_one(
            "#tabela_cadastro_venda", DataTable)
        tabela_cadastro_venda.border_title = "Cadastro de venda"
        tabela_cadastro_venda.cursor_type = 'row'
        tabela_cadastro_venda.zebra_stripes = True
        tabela_cadastro_venda.add_columns("ID", "Produto", "Quantidade vendida", "Dar baixa", "Valor unitário", "Valor total")


        tabela = self.query_one("#tabela_vendas", DataTable)
        tabela.border_title = "Vendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns('ID venda', 'Produtos',
                           'Data', 'Comentário', 'Status', 'Valor final')
        self.atualizar_tabela_vendas()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield SidebarMenu(id="sidebar")

        with TabbedContent(initial='tab_cadastrar_venda'):

            with TabPane('Cadastrar venda', id='tab_cadastrar_venda'):
                with HorizontalGroup(id='cnt_select_produtos'):     
                    with Collapsible(title="Expandir para adicionar produtos à venda"):
                        with HorizontalGroup(id='cnt_select_produtos'):                  
                            with VerticalGroup():
                                with HorizontalGroup():
                                    yield Label('Selecione um produto:')
                                    yield Select(self.LISTA_DE_PRODUTOS,
                                            type_to_search=True,
                                            id='select_produtos_venda',
                                            allow_blank=True,
                                            prompt='Selecione o produto para adicionar à venda'
                                            )

                                with HorizontalGroup():
                                    yield Static(self.texto_static_produto, id='static_produto')
                                    with VerticalGroup():
                                        with HorizontalGroup():
                                            yield Label("Dar baixa no estoque?")
                                            yield Switch(disabled=False, id="switch_baixa")
                                    
                                        with HorizontalGroup():
                                            yield Input(placeholder='Quantidade vendida...',
                                                        id='quantidade_venda',
                                                        max_length=3,
                                                        type="integer"
                                                        )
                                            yield Button('Adicionar',
                                                            disabled=True,
                                                            id='bt_adicionar_quantidade')
                yield Rule()

                with ScrollableContainer():
                    with VerticalGroup():
                        yield DataTable(id="tabela_cadastro_venda")
                        with HorizontalGroup():
                            yield Static(self.texto_static_venda, id="static_venda")
                            yield Button("Remover", id="bt_remover", disabled=True)

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
                with Collapsible(title='Expandir tabela de venda', id="coll_vendas"):
                    with ScrollableContainer():
                        with HorizontalGroup():
                            yield Checkbox("Em andamento", True, id="cbox_andamento")
                            yield Checkbox("Aguardando pagamento", True, id='cbox_pagamento')
                            yield Checkbox("Finalizada", True, id="cbox_finalizada")
                            yield Checkbox("Cancelada", True, id="cbox_cancelada")

                    
                        yield DataTable(id='tabela_vendas', )

                        with HorizontalGroup():
                            yield Static(self.texto_static_alteracao, id="static_alteracao_venda")
                            yield Button('Preencher dados', id='bt_preencher_dados')

                yield Rule(orientation='horizontal', line_style='solid')

                with VerticalGroup():
                    yield Static("[b]Informações da venda selecionada:[/b]", id="stt_alteracao_produto")
                    with HorizontalGroup():
                        yield Label('Data da venda[red]*[/red]')
                        yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="data_alterada")

                        yield Label('Status da venda[red]*[/red]')
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

        yield Footer(show_command_palette=False)

    def verificar_data(self, data_inserida, formato="%d/%m/%Y"):
        'Verifica se a data inserida é válida.'
        from datetime import datetime
        try:
            datetime.strptime(data_inserida, formato)
            return True
        except ValueError:
            return self.notify(title="Data inválida", message="Insira uma data válida!", severity="warning")
        
    def cadastrar_venda(self):
        'Insere uma venda no banco de dados.'
        status = self.query_one(
            '#select_status_venda', Select).value
        data = self.query_one("#data_venda", MaskedInput).value
        comentario = self.query_one("#text_comentario", TextArea).text.strip()
        dar_baixa = self.query_one("#switch_baixa", Switch)
        produtos = self.PRODUTOS_QUANTIDADE

        verificacao_data = self.verificar_data(data_inserida=data)

        valor_final = sum(self.VALOR_TOTAL_VENDA)

        if len(produtos) == 0:
            self.notify(title="Nenhum produto selecionado", message="Adicione pelo menos um produto!", severity='warning')
        elif len(data) < 10:
            self.notify(title="Data inválida!", message="Preencha o prazo no formato DD/MM/AAAA", severity="warning")
        elif verificacao_data == True:
            controller.insert_venda(
                data=data, valor_final=valor_final, status=status, comentario=comentario, produtos=produtos)

            for produto in produtos.items():
                if produto[0] in self.PRODUTOS_BAIXA:
                    quantidade_estoque = controller.select_produto_id(
                        id_produto=produto[0])[2]

                    quantidade_atualizada = int(
                        quantidade_estoque) - int(produto[1])
                    controller.update_produto(
                        id_produto=produto[0], quantidade=quantidade_atualizada)

            self.notify(title="Feito!", message='Venda cadastrada com sucesso!')
            self.PRODUTOS_QUANTIDADE.clear()
            self.PRODUTOS_BAIXA.clear()
            dar_baixa.value = False
            self.limpar_inputs()
            self.atualizar_tabela_vendas()
            self.resetar_tabela_vendas()

    def update_venda(self):
        'Atualiza uma venda no banco de dados.'
        id_venda = self.VENDA_ALTERACAO[0]

        data = self.query_one('#data_alterada', MaskedInput).value
        status = self.query_one('#select_status_venda_alterada', Select).value
        comentario = self.query_one('#text_comentario_alterado', TextArea).text.strip()
        
        validacao_data = self.verificar_data(data_inserida=data)

        if validacao_data == True:
            controller.update_venda(
            id_venda=id_venda, status=status, data=data, comentario=comentario)
            self.notify(title="Feito!", message="Venda alterada com sucesso!")
            self.resetar_tabela_vendas()
            self.limpar_inputs_alteracao()

    def     da(self):
        'Deleta uma venda do banco de dados.'
        id_venda = self.VENDA_ALTERACAO[0]
        controller.delete_venda(id_venda)
        self.notify(title="Já era!", message='Venda deletada com sucesso!')
        self.VENDA_ALTERACAO.clear()

    def atualizar_select_produtos(self):
        'Atualiza o select de produtos com os novos produtos inseridos na TelaProdutos.'
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one("#select_produtos_venda", Select).set_options(
            self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    def atualizar_static_produto(self):
        'Atualiza as informações do produto selecionado na TelaVendas.'
        try:
            id_produto = self.query_one("#select_produtos_venda", Select).value

            static = self.query_one("#static_produto", Static)

            id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
                id_produto)

            novo_texto = f'[b]Informações do produto:[/b]\n\n[b] Produto selecionado:[/b] {nome}\n[b] Quantidade em estoque: [/b]{quantidade}'

            static.update(novo_texto)
        except:
            pass

    def atualizar_static_venda(self):
        'Atualiza as informações dos produtos inseridos em uma venda na TelaVendas.'
        self.VALOR_TOTAL_VENDA.clear()
        static = self.query_one('#static_venda', Static)

        for item in self.PRODUTOS_QUANTIDADE.items():
            id_produto, quantidade = item

            if id_produto in self.PRODUTOS_BAIXA.keys():
                match self.PRODUTOS_BAIXA[id_produto]:
                    case True:
                        dar_baixa = "Sim"
                    case False:
                        dar_baixa = "Não"

            _id_produto, nome, _quantidade, valor_unitario, _valor_custo, _aceita_encomenda, _descricao, _imagem = controller.select_produto_id(
                id_produto)

            valor_produtos = (valor_unitario * int(quantidade))

            self.VALOR_TOTAL_VENDA.append(valor_produtos)

        valor_total = sum(self.VALOR_TOTAL_VENDA)

        static.update(
            f'[b]Total da venda:[/b] R$ {valor_total:.2f}')

    def atualizar_static_alteracao(self):
        'Atualiza as informações da tela de alteração de venda.'
        static = self.query_one('#static_alteracao_venda', Static)

        _id_venda, produtos, prazo, comentario, status, valor_final = self.VENDA_ALTERACAO

        if comentario == None:
            comentario = ''

        static.update(f'[b]Venda:[/b]\n\n [b]Produtos:[/b] {produtos}\n [b]Prazo:[/b] {prazo}\n [b]Status:[/b] {status}\n [b]Comentários:[/b] {comentario}\n [b]Valor total:[/b] R$ {valor_final}')

    def atualizar_static_alteracao_produto(self):
        'Atualiza as informações de produtos na tela de alteração de produto.'

        static = self.query_one("#stt_alteracao_produto", Static)
        _id_venda, produtos, data, comentario, status, valor_final = self.VENDA_ALTERACAO

        novo_texto = f"[b]Venda selecionada:[/b]\n\n [b]Produtos e quantidades:[/b] {produtos}\n [b]Valor final:[/b] R$ {valor_final}"
        static.update(novo_texto)

    def atualizar_tabela_cadastro_venda(self):
        'Atualiza os valores a serem preenchidos na tabela de cadastro da venda.'
        
        tabela = self.query_one("#tabela_cadastro_venda", DataTable)

        for item in self.PRODUTOS_QUANTIDADE.items():
            id_produto, quantidade = item

            if id_produto in self.PRODUTOS_BAIXA.keys():
                match self.PRODUTOS_BAIXA[id_produto]:
                    case True:
                        dar_baixa = "Sim"
                    case False:
                        dar_baixa = "Não"

            _id_produto, nome, _quantidade, valor_unitario, _valor_custo, _aceita_encomenda, _descricao, _imagem = controller.select_produto_id(
                id_produto)

            valor_produtos = (valor_unitario * int(quantidade))

            tabela.add_row(_id_produto, nome, quantidade, dar_baixa, f"R$ {valor_unitario}", f"R$ {valor_produtos}")

    def resetar_tabela_cadastro_venda(self):
        'Reseta e atualiza a tabela de cadastro da venda.'

        tabela = self.query_one("#tabela_cadastro_venda", DataTable)
        tabela.clear()
        self.atualizar_tabela_cadastro_venda()
        self.query_one("#bt_remover", Button).disabled = True
        self.query_one('#quantidade_venda', Input).clear()

    def adicionar_dicionario_venda(self):
        'Adiciona produtos de uma venda em um dict().'
       
        try:
            id_produto = self.query_one(
                "#select_produtos_venda", Select).selection
            quantidade_vendida = self.query_one(
                "#quantidade_venda", Input).value

            if quantidade_vendida == "" or quantidade_vendida.startswith("0") or quantidade_vendida.startswith("-"):
                self.notify(title='Quantidade inválida', message="Insira uma quantidade válida!", severity="warning")
                return

            dar_baixa = self.query_one("#switch_baixa", Switch).value

            quantidade_estoque = controller.select_produto_id(id_produto)[2]

            match dar_baixa:
                case True:
                    if int(quantidade_vendida) > int(quantidade_estoque):
                        self.notify(
                            "Quantidade maior do que a disponível no estoque!", severity="warning")

                    if int(quantidade_vendida) > int(quantidade_estoque) and id_produto in self.PRODUTOS_BAIXA.keys():
                        self.PRODUTOS_BAIXA.pop(id_produto)
                        self.PRODUTOS_QUANTIDADE.pop(id_produto)
                        self.resetar_tabela_cadastro_venda()
                        self.atualizar_static_venda()

                    if int(quantidade_vendida) <= int(quantidade_estoque):
                        if id_produto not in self.PRODUTOS_BAIXA.keys():
                            self.PRODUTOS_BAIXA[id_produto] = True
                            self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida
                            self.resetar_tabela_cadastro_venda()
                            self.atualizar_static_venda()


                        if id_produto in self.PRODUTOS_BAIXA.keys():
                            self.PRODUTOS_BAIXA[id_produto] = True
                            self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida
                            self.resetar_tabela_cadastro_venda()
                            self.atualizar_static_venda()

                case False:
                    if id_produto not in self.PRODUTOS_BAIXA.keys():
                        self.PRODUTOS_BAIXA[id_produto] = False
                        self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida
                        self.resetar_tabela_cadastro_venda()
                        self.atualizar_static_venda()

                    if id_produto in self.PRODUTOS_BAIXA.keys():
                        self.PRODUTOS_BAIXA[id_produto] = False
                        self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida
                        self.resetar_tabela_cadastro_venda()
                        self.atualizar_static_venda()

        except TypeError as e:
            self.notify(title="Nenhum produto selecionado", message="Selecione um produto!", severity="warning")

    def remover_produto_venda(self):
        'Remove um produto adicionado em uma venda.'

        id_produto = self.PRODUTO_SELECIONADO[0]
        self.PRODUTOS_QUANTIDADE.pop(id_produto)
        self.PRODUTOS_BAIXA.pop(id_produto)
        self.atualizar_static_venda()
        self.resetar_tabela_cadastro_venda()
        self.notify(title="Removido!", message="Produto removido da venda", severity="warning")


    def limpar_inputs(self):
        'Reseta os campos e informações da TelaVendas.'
        self.VALOR_TOTAL_VENDA.clear()
        self.PRODUTOS_QUANTIDADE.clear()
        self.PRODUTOS_BAIXA.clear()

        self.query_one("#data_venda", Input).clear()
        self.query_one("#select_status_venda", Select).value = 1
        self.query_one("#text_comentario", TextArea).clear()
        self.query_one("#select_produtos_venda", Select).clear()
        self.query_one('#quantidade_venda', Input).clear()
        self.query_one("#switch_baixa", Switch).value = False
        self.query_one('#static_produto', Static).update(
            self.texto_static_produto)
        self.query_one('#static_venda', Static).update(
            self.texto_static_venda)
        self.query_one("#tabela_cadastro_venda", DataTable).clear()
        
    def limpar_inputs_alteracao(self):
        'Reseta os campos e informações de alterações da TelaVendas.'
        self.query_one("#data_alterada", MaskedInput).clear()
        self.query_one("#select_status_venda_alterada", Select).value = 1
        self.query_one("#text_comentario_alterado", TextArea).clear()
        self.query_one("#static_alteracao_venda", Static).update(
            self.texto_static_venda)
        self.query_one("#stt_alteracao_produto", Static).update("[b]Informações da venda selecionada:[/b]")
        self.query_one("#bt_alterar", Button).disabled = True
        self.query_one("#bt_deletar", Button).disabled = True

    def pegar_checkbox_venda(self):
        'Pega os valores dos Checkboxes da TelaVendas.'
        andamento = self.query_one("#cbox_andamento", Checkbox).value
        pagamento = self.query_one("#cbox_pagamento", Checkbox).value
        finalizada = self.query_one("#cbox_finalizada", Checkbox).value
        cancelada = self.query_one("#cbox_cancelada", Checkbox).value

        if andamento:
            self.checkbox_list.append(1)

        if pagamento:
            self.checkbox_list.append(2)

        if finalizada:
            self.checkbox_list.append(3)

        if cancelada:
            self.checkbox_list.append(4)
    
    def atualizar_tabela_vendas(self):
        'Atualiza os valores a serem preenchidos na tabela da TelaVendas.'
        tabela = self.query_one("#tabela_vendas", DataTable)

        dados_vendas = controller.listar_vendas()

        self.pegar_checkbox_venda()

        for id_encomenda, detalhes in dados_vendas.items():
            nome_produtos = [''.join([f'{nome}, ({quantidade}) | \n '])
                             for nome, quantidade, _valor_unitario in detalhes['produtos']]

            status = detalhes['status']
            valor_final = detalhes['valor_final']

            if status in self.checkbox_list:

                if detalhes['status'] == 1:
                    status = 'Em produção'
                elif detalhes['status'] == 2:
                    status = 'Aguardando pagamento'
                elif detalhes['status'] == 3:
                    status = 'Finalizada'
                elif detalhes['status'] == 4:
                    status = 'Cancelada'

                if id_encomenda not in tabela.rows:
                    tabela.add_row(id_encomenda, ''.join(nome_produtos),
                                   detalhes['data'], detalhes['comentario'], status, f"R$ {valor_final}")

    def resetar_tabela_vendas(self):
        'Reseta e preenche a tabela da TelaVendas.'
        tabela = self.query_one("#tabela_vendas", DataTable)

        tabela.clear()

        self.atualizar_tabela_vendas()

    def preencher_alteracoes_venda(self):
        'Preenche os valores de uma venda na parte de Atualização de Venda na TelaVendas.'
        novo_prazo = self.query_one("#data_alterada", MaskedInput)
        novo_status = self.query_one("#select_status_venda_alterada", Select)
        novo_comentario = self.query_one("#text_comentario_alterado", TextArea)

        _id_encomenda, _produtos, prazo, comentario, status, _valor_total = self.VENDA_ALTERACAO

        comentario = str(comentario)

        if status == 'Em produção':
            status = 1
        elif status == 'Aguardando pagamento':
            status = 2
        elif status == 'Finalizada':
            status = 3
        elif status == 'Cancelada':
            status = 4

        if comentario == 'None':
            comentario = ''

        novo_prazo.value = prazo
        novo_status.value = status
        novo_comentario.text = comentario

        self.query_one("#coll_vendas", Collapsible).collapsed = True
        self.atualizar_static_alteracao_produto()
  
    @on(Checkbox.Changed)
    async def on_checkbox_change(self, event: Checkbox.Changed):
        'Ações que ocorrem ao selecionar um Checkbox.'
        if len(self.checkbox_list) > 0:
            self.checkbox_list.clear()

        self.resetar_tabela_vendas()

    @on(DataTable.RowSelected)
    async def on_row_selected(self, event: DataTable.RowSelected):
        'Ações que ocorrem ao selecionar as linhas de uma tabela.'
        match event.data_table.id:
            case "tabela_vendas":

                encomenda = self.query_one('#tabela_vendas', DataTable)
                self.VENDA_ALTERACAO = encomenda.get_row(event.row_key)
                self.atualizar_static_alteracao()
                self.query_one("#bt_alterar", Button).disabled = False
                self.query_one("#bt_deletar", Button).disabled = False

            case "tabela_cadastro_venda":
                self.query_one("#bt_remover", Button).disabled = False 
                encomenda = self.query_one('#tabela_cadastro_venda', DataTable)
                self.PRODUTO_SELECIONADO = encomenda.get_row(event.row_key)

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        'Ações que ocorrem ao selecionar um item do Select.'
        match event.select.id:
            case 'select_produtos_venda':
                self.ID_PRODUTO = event.select.value
                self.atualizar_static_produto()

            case 'select_id_venda':
                self.atualizar_static_alteracao()

    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        'Ações que ocorrem ao preencher um Input.'
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
        'Ações que ocorrem ao preencher uma TextArea.'
        if event.text_area.id == 'text_comentario':
            self.query_one("#bt_limpar", Button).disabled = False

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao pressionar um botão na TelaVendas.'
        match event.button.id:
            case 'bt_adicionar_quantidade':
                self.adicionar_dicionario_venda()

            case 'bt_remover':
                self.remover_produto_venda()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')

            case 'bt_cadastrar':
                self.cadastrar_venda()

            case 'bt_preencher_dados':
                try:
                    self.preencher_alteracoes_venda()
                except ValueError:
                    self.notify(title="Ops!", message= "Você precisa selecionar uma venda", severity='warning')

            case 'bt_alterar':
                self.update_venda()

            case 'bt_deletar':
                self.delete_venda()
                self.resetar_tabela_vendas()

            case 'bt_limpar':
                self.limpar_inputs()


class TelaPesquisa(Screen):
    TITLE = 'Pesquisa'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.checkbox_list_produto = list()


    def on_mount(self):
        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)
        tabela.border_title = "Vendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns("Nome", "Quantidade", "Valor unitário", "Valor custo", "Aceita encomenda", "Descrição") 
        self.resetar_tabela_produtos()

    def on_screen_resume(self):
        self.resetar_tabela_produtos()
        

    def compose(self):
        yield Header(show_clock=True)

        yield SidebarMenu(id="sidebar")

        with TabbedContent(initial='tab_produtos', id='tabbed_pesquisa'):
            with TabPane('Produtos', id='tab_produtos'):
                with VerticalScroll():

                    with HorizontalGroup():
                        yield Checkbox("Em estoque", True, id="cbox_estoque")
                        yield Checkbox("Fora de estoque", True, id="cbox_fora_estoque")
                        yield Checkbox("Aceita encomenda", True, id="cbox_encomenda")
                        yield Checkbox("Não aceita encomenda", True, id="cbox_nao_encomenda")

                with HorizontalGroup():
                    yield Select(prompt='Filtrar por:', options=[
                        ('nome', 1), 
                        ("quantidade", 2), 
                        ('valor unitário', 3), 
                        ('valor de custo', 4), 
                        ('descrição', 5)
                        ], id="select_produtos_pesquisa")
                    yield Input(id="input_produto_pesquisa")
                    yield Button("Pesquisar", id="bt_pesquisar_produto")

                with VerticalScroll():
                    yield DataTable(id='tabela_produtos_pesquisa')


            with TabPane('Encomendas', id='tab_encomendas'):
                with VerticalScroll():

                    with HorizontalGroup():
                        yield Checkbox("Em produção", True, id="cbox_producao")
                        yield Checkbox("Finalizada", True, id='cbox_finalizada')
                        yield Checkbox("Vendida", True, id="cbox_vendida")
                        yield Checkbox("Cancelada", True, id="cbox_cancelada")
            
                    yield DataTable(id='tabela_encomendas_pesquisa')

            with TabPane('Vendas', id='tab_vendas'):
                with VerticalScroll():

                    with HorizontalGroup():
                        yield Checkbox("Em produção", True, id="cbox_producao")
                        yield Checkbox("Finalizada", True, id='cbox_finalizada')
                        yield Checkbox("Vendida", True, id="cbox_vendida")
                        yield Checkbox("Cancelada", True, id="cbox_cancelada")
            
                    yield DataTable(id='tabela_vendas_pesquisa')

        yield Button('Voltar', id='bt_voltar')

        yield Footer(show_command_palette=False)

    def pegar_checkbox_produtos(self):
        'Pega os valores dos Checkboxes da TelaVendas.'

        estoque = self.query_one("#cbox_estoque", Checkbox).value
        fora_estoque = self.query_one("#cbox_fora_estoque", Checkbox).value
        encomenda = self.query_one("#cbox_encomenda", Checkbox).value
        nao_encomenda = self.query_one("#cbox_nao_encomenda", Checkbox).value

        if estoque:
            self.checkbox_list_produto.append(1)

        if fora_estoque:
            self.checkbox_list_produto.append(2)

        if encomenda:
            self.checkbox_list_produto.append(3)   
        
        if nao_encomenda:
            self.checkbox_list_produto.append(4)

    def atualizar_tabela_produtos(self): #### Não filtra se dois checkboxes diferentes são apertados.
        'Atualiza as informações para a tabela de produtos da TelaPesquisa.'

        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.pegar_checkbox_produtos()

        for produto in self.LISTA_DE_PRODUTOS:
            id_produto = produto[1]
            _id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, _imagem = controller.select_produto_id(id_produto)

            adicionar_na_tabela = list()

            if int(quantidade) > 0:
                adicionar_na_tabela.append(1)
            elif int(quantidade) == 0: 
                adicionar_na_tabela.append(2)
            
            if aceita_encomenda == True:
                adicionar_na_tabela.append(3)
            elif aceita_encomenda == False:
                adicionar_na_tabela.append(4)
                
            if any(item in self.checkbox_list_produto for item in adicionar_na_tabela):                
                if str(valor_custo) == 'None':
                    valor_custo = ''
                else:
                    valor_custo = f"R$ {valor_custo}"
                if str(descricao) == 'None':
                    descricao = ''
                if aceita_encomenda == False:
                    aceita_encomenda = 'Não'
                else:
                    aceita_encomenda = 'Sim'

                tabela.add_row(nome, quantidade, f"R$ {valor_unitario}", valor_custo, aceita_encomenda, descricao)

    def resetar_tabela_produtos(self):
        'Reseta e preenche a tabela de produtos da TelaPesquisa.'
        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)

        tabela.clear()

        self.atualizar_tabela_produtos()

    def fazer_pesquisa(self):
        select = self.query_one("#select_produtos_pesquisa", Select).value
        pesquisa = self.query_one("#input_produto_pesquisa", Input).value

        match select:
            case 1:
                return controller.select_produto_nome_all(nome=pesquisa)
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass

        
        
    @on(Checkbox.Changed)
    async def on_checkbox_change(self, event: Checkbox.Changed):
        'Ações que ocorrem ao selecionar um Checkbox.'

        if len(self.checkbox_list_produto) > 0:
            self.checkbox_list_produto.clear()
        
        self.resetar_tabela_produtos()


    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_pesquisar_produto':
                self.resetar_tabela_produtos_pesquisa()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')
