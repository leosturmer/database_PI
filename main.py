from view import (TelaProdutos)

from textual.app import (App, ComposeResult)
from textual.binding import (Binding)


class NizeApp(App):
    
    SCREENS = {
        'tela_produtos': TelaProdutos
    }


    def on_mount(self) -> ComposeResult:
        self.push_screen('tela_produtos')

if __name__ == "__main__":
    app = NizeApp()
    app.run()