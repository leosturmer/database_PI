#### O que fazer no banco também:

- Arrumar os SQL que não estão funcionando direito (searchs de encomenda e venda)

- Ver como a MODEL e VIEW vão inserir os produtos na venda e encomenda
- Ver como a MODEL e VIEW vão inserir as datas e prazos nas vendas

- Ver se tem como uma ENCOMENDA FINALIZADA se transformar em uma VENDA

- Fazer def filtrar_encomenda_status
- Fazer def filtrar_venda_status

- Ver as questões de diferenciar maiúsculo e minúsculo


- TEM QUE DIMINUIR DO ESTOQUE QUANDO REALIZAR UMA VENDAAAAAAA!!!!!!!!!!!!!


##### CONFERÊNCIAS

- Só deixar inserir uma venda/encomenda se o produto existir;
- Só deixar inserir quando estiver com todos campos NULL corretos;

##### Quais são os status

STATUS DE VENDA:
1. Em produção / encomendado
1. Cancelada
1. Aguardando pagamento
1. Finalizado

STATUS DA ENCOMENDA:
1. Em produção
1. Cancelado
1. Vendido (transforma em VENDA)
1. Finalizado



##### OUTROS COMENTÁRIOS

- O valor final da venda não vai no banco. Ele calcula pelos produtos adicionados na venda.
- Estoque - view pela tabela produtos sem o estoque zerado

- Na tabela produtos, o "encomenda" é "aceita_encomenda"
