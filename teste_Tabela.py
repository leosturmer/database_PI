import controller

from textual.app import (App, ComposeResult)

from textual.widgets import DataTable


class NizeApp(App):

    def on_mount(self):
        self.atualizar_tabela_encomendas()



    def atualizar_tabela_encomendas(self):
        tabela = self.query_one(DataTable)

        tabela.add_columns('ID encomenda', 'Produtos', 'Prazo', 'Comentario', 'Status')

        conteudo = controller.listar_encomendas()
        

        for id_encomenda, detalhes in conteudo.items():
            # for nome, quantidade in detalhes['produtos']:
            #     produto = nome
            #     quant = quantidade
               
            nome_produtos = [''.join([f'{nome}, quantidade ({quantidade}) | '])  for nome, quantidade in detalhes['produtos']]  

            if detalhes['status'] == 1:
                status = 'Em produção'
            elif detalhes['status'] == 2:
                status = 'Finalizada'
            elif detalhes['status'] == 3:
                status = 'Vendida'
            elif detalhes['status'] == 4:
                status = 'Cancelada'                    

            tabela.add_row(id_encomenda, ''.join(nome_produtos), detalhes['prazo'], detalhes['comentario'], status)

    def compose(self):

        yield DataTable(zebra_stripes=True, cell_padding=3)


if __name__ == "__main__":
    app = NizeApp()
    app.run()