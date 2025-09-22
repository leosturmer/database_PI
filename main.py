from view import (TelaProdutos, TelaEncomendas, TelaInicial, TelaVendas, TelaPesquisa, TelaEstoque)

from textual.app import (App, ComposeResult)
from textual.binding import (Binding)


class NizeApp(App):

    CSS_PATH = 'view.tcss'
    
    SCREENS = {
        'tela_inicial': TelaInicial,
        'tela_produtos': TelaProdutos,
        'tela_encomendas': TelaEncomendas,
        'tela_estoque': TelaEstoque,
        'tela_vendas': TelaVendas,
        'tela_pesquisa': TelaPesquisa
    }


    def on_mount(self) -> ComposeResult:
        self.push_screen('tela_inicial')

if __name__ == "__main__":
    app = NizeApp()
    app.run()