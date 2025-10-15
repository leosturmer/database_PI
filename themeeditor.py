from textual.app import App, ComposeResult

from textual_theme_editor import ThemeEditor
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

class ExampleApp(App):
    def compose(self) -> ComposeResult:
        yield ThemeEditor()

        yield Header(show_clock=True)

        with TabbedContent(initial='tab_cadastrar_venda'):

            with TabPane('Cadastrar venda', id='tab_cadastrar_venda'):
                with ScrollableContainer():
                    with HorizontalGroup(id='cnt_select_produtos'):
                        yield Label('Selecione um produto:')
                        with HorizontalGroup():
                            with VerticalGroup():
                                with HorizontalGroup():
                                    yield Select([(0, 0 ), (0, 0)],
                                                 type_to_search=True,
                                                 id='select_produtos_venda',
                                                 allow_blank=True,
                                                 prompt='Selecione o produto para adicionar à venda'
                                                 )

                                yield Static('lalalalalla', id='static_produto')

                                with HorizontalGroup():
                                    yield Input(placeholder='Quantidade vendida...',
                                                id='quantidade_venda',
                                                max_length=3,
                                                type="integer"
                                                )
                                    yield Button('Adicionar',
                                                 disabled=True,
                                                 id='bt_adicionar_quantidade')



if __name__ == "__main__":
    app = ExampleApp()
    app.run()
