import controller

from textual.app import (App, ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header, Label, Static, MaskedInput, OptionList, Select, SelectionList)
from textual.screen import (Screen)
from textual.containers import ()


class TelaVendedor(Screen):
    def compose(self):
        yield Label('Usuário:')
        yield MaskedInput(valid_empty=False)
        yield Label('Senha:')
        yield MaskedInput(valid_empty=False)
        yield Label('Nome:')
        yield MaskedInput(valid_empty=False)
        yield Label('Nome da loja:')
        yield MaskedInput(valid_empty=True)



def insert_vendedor(login, senha, nome, nome_loja):
    pass