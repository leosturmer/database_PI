
- ##### TELA VENDAS TÁ AUMENTANDO O PREÇO FINAL SEMPRE QUE CLICA EM ADICIONAR

    - Tela de Pesquisa:
        - Produtos:
           não PRODUTOS ---- ao cadastrar, fazer um FETCH pra ver se já tem aquele nome cadastrado.

            - Colocar os filtros do checkbox
            - Fazer as pesquisas no banco de dados pelo input

        - Encomendas:
            - Colocar a tabela
            - Colocar checkboxes
            - Colocar input
            - Colocar botão
            - Colocar os filtros do checkbox
            - Fazer as pesquisas no banco de dados pelo input

        - Vendas:
            - Colocar a tabela
            - Colocar checkboxes
            - Colocar input
            - Colocar botão
            - Colocar os filtros do checkbox
            - Fazer as pesquisas no banco de dados pelo input

##### OUTROS COMENTÁRIOS

    - O valor final da venda não vai no banco. Ele calcula pelos produtos adicionados na venda.
    - Estoque - view pela tabela produtos sem o estoque zerado
    - Na tabela produtos, o "encomenda" é "aceita_encomenda"

###
        if estoque:
            self.checkbox_list_produto.append(1)
        elif fora_estoque:
            self.checkbox_list_produto.append(2)
        elif encomenda:
            self.checkbox_list_produto.append(3)  
        elif nao_encomenda:
            self.checkbox_list_produto.append(4)
        elif estoque and fora_estoque and encomenda and nao_encomenda:
            self.checkbox_list_produto.extend([1, 2, 3, 4])
        elif estoque and fora_estoque and encomenda:
            self.checkbox_list_produto.extend([1, 2, 3])
        elif estoque and encomenda and nao_encomenda:
            self.checkbox_list_produto.extend([1, 3, 4])
        elif estoque and fora_estoque and nao_encomenda:
            self.checkbox_list_produto.extend([1, 2, 4])
        elif fora_estoque and encomenda and nao_encomenda:
            self.checkbox_list_produto.extend([2, 3, 4])
        elif estoque and fora_estoque:
            self.checkbox_list_produto.extend([1, 2])
        elif estoque and encomenda:
            self.checkbox_list_produto.extend([1, 3])
        elif estoque and nao_encomenda:
            self.checkbox_list_produto.extend([1, 4])
        elif fora_estoque and encomenda:
            self.checkbox_list_produto.extend([2, 3])
        elif fora_estoque and nao_encomenda:
            self.checkbox_list_produto.extend([2, 4])
        elif encomenda and nao_encomenda:
            self.checkbox_list_produto.extend([3, 4])

