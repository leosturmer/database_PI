
produtos = {1: "2", 5: "1"}

baixa = [5]


for produto in produtos.items():
    if produto[0] in baixa:
        print(produto)

