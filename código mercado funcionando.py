import pandas as pd

# Criando uma lista com os dados dos produtos
dados_produtos = [
    {"Nome": "Arroz", "Preço": 4.50, "Quantidade": "5 kg"},
    {"Nome": "Feijão", "Preço": 6.00, "Quantidade": "1 kg"},
    {"Nome": "Macarrão", "Preço": 3.00, "Quantidade": "500 g"},
    {"Nome": "Açúcar", "Preço": 2.50, "Quantidade": "1 kg"},
    {"Nome": "Sal", "Preço": 1.00, "Quantidade": "1 kg"},
    {"Nome": "Óleo de cozinha", "Preço": 5.50, "Quantidade": "900 ml"},
    {"Nome": "Leite", "Preço": 3.80, "Quantidade": "1 L"},
    {"Nome": "Café", "Preço": 8.00, "Quantidade": "500 g"},
    {"Nome": "Pão", "Preço": 2.00, "Quantidade": "1 unidade"},
    {"Nome": "Farinha de trigo", "Preço": 3.20, "Quantidade": "1 kg"},
    {"Nome": "Batata", "Preço": 4.00, "Quantidade": "2 kg"},
    {"Nome": "Cebola", "Preço": 3.00, "Quantidade": "1 kg"},
    {"Nome": "Tomate", "Preço": 5.00, "Quantidade": "1 kg"},
    {"Nome": "Alho", "Preço": 7.00, "Quantidade": "200 g"},
    {"Nome": "Carne bovina", "Preço": 30.00, "Quantidade": "1 kg"},
    {"Nome": "Frango", "Preço": 12.00, "Quantidade": "1 kg"},
    {"Nome": "Ovos", "Preço": 5.00, "Quantidade": "1 dúzia"},
    {"Nome": "Maçã", "Preço": 3.50, "Quantidade": "1 kg"},
    {"Nome": "Banana", "Preço": 2.50, "Quantidade": "1 kg"},
    {"Nome": "Laranja", "Preço": 3.00, "Quantidade": "1 kg"},
]

# Criando um DataFrame a partir da lista
df = pd.DataFrame(dados_produtos)

# Salvando o DataFrame em um arquivo Excel
df.to_excel('mercadoria.xlsx', index=False)

print("Planilha 'mercadoria.xlsx' criada com sucesso!")
