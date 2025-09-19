import view

from textual.app import (App, ComposeResult)

BINDINGS = []

class NizeApp(App):
    def compose(self) -> ComposeResult:
        self.push_screen('')
