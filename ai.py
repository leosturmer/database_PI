
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Static, Header, Footer
from textual.screen import Screen

class CadastroScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Tela de Cadastro")
        yield Button("Voltar", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.push_screen("MenuScreen")

class AlterarScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Tela de Alteração")
        yield Button("Voltar", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.push_screen("MenuScreen")

class MenuScreen(Static):
    def compose(self) -> ComposeResult:
        yield Static("Menu Principal")
        yield Button("Cadastrar", id="cadastrar")
        yield Button("Alterar", id="alterar")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cadastrar":
            self.app.switch_screen("CadastroScreen")
        elif event.button.id == "alterar":
            self.app.switch_screen("AlterarScreen")

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield MenuScreen()

if __name__ == "__main__":
    app = MyApp()
    app.run()
