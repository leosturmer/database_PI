from view_testes import (TelaProdutos, TelaEncomendas, TelaInicial, TelaVendas, TelaPesquisa)

from textual.app import (App, ComposeResult)
from textual.binding import (Binding)


class NizeApp(App):
    
    SCREENS = {
        'tela_inicial': TelaInicial,
        'tela_produtos': TelaProdutos,
        'tela_encomendas': TelaEncomendas,
        'tela_vendas': TelaVendas,
        'tela_pesquisa': TelaPesquisa
    }


    def on_mount(self) -> ComposeResult:
        self.push_screen('tela_inicial')

if __name__ == "__main__":
    app = NizeApp()
    app.run()