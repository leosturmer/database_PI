yield SelectionList(id='select_produtos').add_options((nome, id_produto) for nome, id_produto in self.LISTA_DE_PRODUTOS.items())



    @on(SelectionList.OptionSelected)
    async def on_selected_change(self, event: SelectionList.OptionSelected):
        if event.option:
            self.query_one("#bt_limpar", Button).disabled = False
        

    # @on(Mount)
    # @on(SelectionList.SelectedChanged)
        

        # produto = controller.select_produto_id(id_produto)

        # self.query_one("#stt_produto_selecionado", Static).update(f"Produto selecionado: {produto}")
        # self.query_one("#seletor_produtos", WidgetQuantidade).update(f"{id_produto}")



# case 'bt_confirmar_produtos':
            #     # async def atualizar_select_quantidade(self) -> None:
            #     id_produto_lista = self.query_one(SelectionList).selected

            #     for produto in id_produto_lista:
            #         widget = self.query_one("#collapsible_encomendas", Collapsible)
            #         widget.mount(WidgetQuantidade('oiiiiiii'))

            #     self.notify(f"{id_produto_lista}")


