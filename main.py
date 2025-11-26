from view import (TelaProdutos, TelaEncomendas,
                  TelaInicial, TelaVendas, TelaPesquisa, TelaLogin, TelaCadastro)

from textual.app import (App, ComposeResult)
from textual.binding import (Binding)

from textual.theme import Theme

# meu_tema = Theme(
#     name='meu-tema',
#     primary='#086025',
#     secondary='#6D099F',
#     warning='#8F7248',
#     error='#ba3c5b',
#     success='#165028',
#     accent='#ffa62b',
#     foreground='#000000',
#     background='#429F71',
#     surface='#A838DF',
#     panel='#FFFFFF',
#     boost=None,
#     dark=True,
#     luminosity_spread=0.15,
#     text_alpha=0.95,
#     variables={}
# )

class NizeApp(App):
    'Classe App que inicializa o programa.'

    AUTO_FOCUS = None

    CSS_PATH = 'view.tcss'

    SCREENS = {
        'tela_login': TelaLogin,
        'tela_cadastro': TelaCadastro,
        'tela_inicial': TelaInicial,
        'tela_produtos': TelaProdutos,
        'tela_encomendas': TelaEncomendas,
        'tela_vendas': TelaVendas,
        'tela_pesquisa': TelaPesquisa
    }

    def on_mount(self) -> ComposeResult:
        self.theme = 'catppuccin-latte'
        self.push_screen('tela_inicial')
        # self.register_theme(meu_tema)
        # self.theme = 'meu-tema'

if __name__ == "__main__":
    app = NizeApp()
    app.run()
