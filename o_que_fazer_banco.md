#### O que fazer no banco também:

##### CONFERÊNCIAS

- Só deixar inserir uma venda/encomenda se o produto existir;
- Só deixar inserir quando estiver com todos campos NULL corretos;


##### A DEFINIR

- Status da venda? realizado, não realizado, etc 0123
- Status da encomenda? Se foi finalizado etc

STATUS DE VENDA:
1. Em andamento
1. Finalizado
1. Produto encomendado
1. Cancelada

STATUS DA ENCOMENDA:
1. Em produção
2. Cancelado
3. Finalizado


##### OUTROS COMENTÁRIOS
- O valor final da venda não vai no banco. Ele calcula pelos produtos adicionados na venda.
- Estoque - view pela tabela produtos sem o estoque zerado
