import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os
import pandas as pd  # Importando a biblioteca pandas

class Produto:
    def __init__(self, id, nome, preco, quantidade):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def __str__(self):
        return f"{self.nome} (ID: {self.id}): {self.quantidade} unidades a R${self.preco:.2f} cada"

class Mercado:
    def __init__(self):
        self.produtos = {}
        self.proximo_id = 1  # ID automático começa em 1
        self.carregar_produtos()  # Carrega produtos do Excel ao iniciar

    def carregar_produtos(self):
        # Lendo a planilha Excel e carregando os produtos
        caminho_arquivo = os.path.join(os.getcwd(), "mercadoria.xlsx")
        try:
            df = pd.read_excel(caminho_arquivo)  # Lê a planilha Excel

            for _, row in df.iterrows():  # Itera sobre as linhas do DataFrame
                nome = row['Nome']  # Supondo que a coluna com o nome do produto é chamada 'Nome'
                preco = row['Preço']  # Supondo que a coluna com o preço é chamada 'Preço'
                quantidade = row['Quantidade']  # Supondo que a coluna com a quantidade é chamada 'Quantidade'
                self.adicionar_produto(nome, preco, quantidade)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")

    def adicionar_produto(self, nome, preco, quantidade):
        id = self.proximo_id
        self.produtos[id] = Produto(id, nome, preco, quantidade)
        self.proximo_id += 1  # Incrementa o ID para o próximo produto
        self.salvar_produtos()  # Salva os produtos sempre que um novo produto é adicionado

    def editar_estoque(self, id, nova_quantidade):
        if id in self.produtos:
            self.produtos[id].quantidade = nova_quantidade
            self.salvar_produtos()  # Salva as alterações no Excel
        else:
            raise ValueError("Produto não encontrado")

    def remover_produto(self, id):
        if id in self.produtos:
            del self.produtos[id]
            self.salvar_produtos()  # Salva as alterações no Excel
        else:
            raise ValueError("Produto não encontrado")

    def obter_produtos(self):
        return self.produtos.values()

    def salvar_produtos(self):
        # Salva os produtos no arquivo Excel
        caminho_arquivo = os.path.join(os.getcwd(), "mercadoria.xlsx")
        dados = {
            'Nome': [],
            'Preço': [],
            'Quantidade': []
        }
        for produto in self.produtos.values():
            dados['Nome'].append(produto.nome)
            dados['Preço'].append(produto.preco)
            dados['Quantidade'].append(produto.quantidade)

        df = pd.DataFrame(dados)
        df.to_excel(caminho_arquivo, index=False)

class App:
    def __init__(self, root):
        self.mercado = Mercado()
        self.root = root
        self.root.title("Gerenciador de Mercado")

        # Aumentando o tamanho da fonte padrão
        self.font_size = 14
        self.button_font_size = 12

        # Definindo cores
        self.secondary_color = "#4CAF50"  # Verde escuro para botões

        # Configurando o layout
        self.tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Gerenciamento')
        self.tab_control.add(self.tab2, text='Caixa')
        self.tab_control.add(self.tab3, text='Histórico de Compras')
        self.tab_control.pack(expand=1, fill='both')

        # Configurando as abas
        self.setup_gestao()
        self.setup_caixa()
        self.setup_historico()

        self.historico = []
        self.itens_comprados = []  # Para armazenar itens comprados

    def setup_gestao(self):
        # Entradas para o nome, preço e quantidade
        tk.Label(self.tab1, text="Nome do Produto:", font=("Arial", self.font_size)).grid(row=0, column=0, pady=5)
        self.nome_entry = tk.Entry(self.tab1, font=("Arial", self.font_size))
        self.nome_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.tab1, text="Preço:", font=("Arial", self.font_size)).grid(row=1, column=0, pady=5)
        self.preco_entry = tk.Entry(self.tab1, font=("Arial", self.font_size))
        self.preco_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.tab1, text="Quantidade:", font=("Arial", self.font_size)).grid(row=2, column=0, pady=5)
        self.quantidade_entry = tk.Entry(self.tab1, font=("Arial", self.font_size))
        self.quantidade_entry.grid(row=2, column=1, pady=5)

        # Campo de busca para o filtro
        tk.Label(self.tab1, text="Buscar Produto:", font=("Arial", self.font_size)).grid(row=3, column=0, pady=5)
        self.buscar_entry = tk.Entry(self.tab1, font=("Arial", self.font_size))
        self.buscar_entry.grid(row=3, column=1, pady=5)
        self.buscar_entry.bind("<KeyRelease>", self.filtrar_produtos)  # Atualiza ao digitar

        # Botões no topo sem ícones
        btn_frame = tk.Frame(self.tab1)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)

        tk.Button(btn_frame, text="Adicionar Produto", command=self.adicionar_produto,
                  font=("Arial", self.button_font_size), width=20, bg=self.secondary_color, fg="white").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Editar Estoque", command=self.editar_estoque_produto,
                  font=("Arial", self.button_font_size), width=20, bg=self.secondary_color, fg="white").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Remover Produto", command=self.remover_produto,
                  font=("Arial", self.button_font_size), width=20, bg=self.secondary_color, fg="white").pack(side="left", padx=10)

        # Tabela para exibir produtos
        self.produto_tree = ttk.Treeview(self.tab1, columns=("ID", "Nome", "Preço", "Quantidade"), show='headings')
        self.produto_tree.heading("ID", text="ID")
        self.produto_tree.heading("Nome", text="Nome")
        self.produto_tree.heading("Preço", text="Preço (R$)")
        self.produto_tree.heading("Quantidade", text="Quantidade")
        self.produto_tree.grid(row=5, column=0, columnspan=3, pady=5)

        self.atualizar_tabela_produtos()  # Atualiza a tabela de produtos ao iniciar

    def setup_caixa(self):
        # Entradas para nome/ID e quantidade
        tk.Label(self.tab2, text="Nome ou ID do Produto:", font=("Arial", self.font_size)).grid(row=0, column=0, pady=5)
        self.nome_caixa_entry = tk.Entry(self.tab2, font=("Arial", self.font_size))
        self.nome_caixa_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.tab2, text="Quantidade:", font=("Arial", self.font_size)).grid(row=1, column=0, pady=5)
        self.quantidade_caixa_entry = tk.Entry(self.tab2, font=("Arial", self.font_size))
        self.quantidade_caixa_entry.grid(row=1, column=1, pady=5)

        # Formas de pagamento
        tk.Label(self.tab2, text="Forma de Pagamento:", font=("Arial", self.font_size)).grid(row=2, column=0, pady=5)
        self.forma_pagamento = ttk.Combobox(self.tab2, values=["Dinheiro", "Cartão de Crédito", "Cartão de Débito"], font=("Arial", self.font_size))
        self.forma_pagamento.grid(row=2, column=1, pady=5)
        self.forma_pagamento.set("Dinheiro")  # Valor padrão

        # Botões no topo com símbolos
        btn_frame = tk.Frame(self.tab2)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho,
                  font=("Arial", self.button_font_size), width=20, bg=self.secondary_color, fg="white").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Fechar Compra", command=self.fechar_compra,
                  font=("Arial", self.button_font_size), width=20, bg=self.secondary_color, fg="white").pack(side="left", padx=10)

        # Tabela de carrinho
        self.carrinho_tree = ttk.Treeview(self.tab2, columns=("ID", "Nome", "Quantidade", "Preço Total"), show='headings')
        self.carrinho_tree.heading("ID", text="ID")
        self.carrinho_tree.heading("Nome", text="Nome")
        self.carrinho_tree.heading("Quantidade", text="Quantidade")
        self.carrinho_tree.heading("Preço Total", text="Preço Total (R$)")
        self.carrinho_tree.grid(row=4, column=0, columnspan=2, pady=5)

    def setup_historico(self):
        # Configuração da aba de histórico
        self.historico_listbox = tk.Listbox(self.tab3, font=("Arial", self.font_size), width=50, height=15)
        self.historico_listbox.pack(pady=20)

    def adicionar_produto(self):
        # Lógica para adicionar um produto
        nome = self.nome_entry.get()
        preco = float(self.preco_entry.get())
        quantidade = int(self.quantidade_entry.get())
        self.mercado.adicionar_produto(nome, preco, quantidade)
        self.atualizar_tabela_produtos()

    def editar_estoque_produto(self):
        try:
            id_selecionado = int(self.produto_tree.item(self.produto_tree.selection())['values'][0])
            nova_quantidade = int(self.quantidade_entry.get())
            self.mercado.editar_estoque(id_selecionado, nova_quantidade)
            self.atualizar_tabela_produtos()
        except IndexError:
            messagebox.showerror("Erro", "Nenhum produto selecionado")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida")

    def remover_produto(self):
        try:
            id_selecionado = int(self.produto_tree.item(self.produto_tree.selection())['values'][0])
            self.mercado.remover_produto(id_selecionado)
            self.atualizar_tabela_produtos()
        except IndexError:
            messagebox.showerror("Erro", "Nenhum produto selecionado")

    def atualizar_tabela_produtos(self):
        # Limpa a tabela e insere novamente
        self.produto_tree.delete(*self.produto_tree.get_children())
        for produto in self.mercado.obter_produtos():
            self.produto_tree.insert('', 'end', values=(produto.id, produto.nome, produto.preco, produto.quantidade))

    def filtrar_produtos(self, event):
        filtro = self.buscar_entry.get().lower()
        produtos_filtrados = [p for p in self.mercado.obter_produtos() if filtro in p.nome.lower() or filtro in str(p.id)]
        self.produto_tree.delete(*self.produto_tree.get_children())
        for produto in produtos_filtrados:
            self.produto_tree.insert('', 'end', values=(produto.id, produto.nome, produto.preco, produto.quantidade))

    def adicionar_ao_carrinho(self):
        # Lógica para adicionar ao carrinho
        nome_ou_id = self.nome_caixa_entry.get()
        quantidade = int(self.quantidade_caixa_entry.get())

        for produto in self.mercado.obter_produtos():
            if produto.nome == nome_ou_id or str(produto.id) == nome_ou_id:
                if quantidade <= produto.quantidade:
                    produto.quantidade -= quantidade  # Atualiza estoque
                    total = quantidade * produto.preco
                    self.itens_comprados.append((produto.id, produto.nome, quantidade, total))  # Armazena no carrinho
                    self.carrinho_tree.insert('', 'end', values=(produto.id, produto.nome, quantidade, total))
                    self.mercado.salvar_produtos()  # Salva as mudanças de estoque
                else:
                    messagebox.showerror("Erro", "Quantidade insuficiente em estoque")
                break
        else:
            messagebox.showerror("Erro", "Produto não encontrado")

    def fechar_compra(self):
        if not self.itens_comprados:
            messagebox.showerror("Erro", "Nenhum item no carrinho")
            return

        total_compra = sum(item[3] for item in self.itens_comprados)  # Soma o total
        forma_pagamento = self.forma_pagamento.get()
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cupom = f"Cupom Fiscal - {data_hora}\n\n"

        for item in self.itens_comprados:
            cupom += f"Produto: {item[1]}, Quantidade: {item[2]}, Total: R${item[3]:.2f}\n"

        cupom += f"\nTotal: R${total_compra:.2f}\n"
        cupom += f"Forma de Pagamento: {forma_pagamento}\n"
        self.historico.append(cupom)  # Salva no histórico
        self.historico_listbox.insert(tk.END, f"Compra de R${total_compra:.2f} em {data_hora}")

        self.itens_comprados.clear()  # Limpa o carrinho
        self.carrinho_tree.delete(*self.carrinho_tree.get_children())  # Limpa a tabela do carrinho

        try:
            with open("cupom_fiscal.txt", "w") as f:
                f.write(cupom)
            os.startfile("cupom_fiscal.txt")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível gerar o cupom fiscal: {e}")

    def gerar_cupom_fiscal(self):
        total = sum(item[3] for item in self.itens_comprados)
        cupom = f"Total: {total:.2f}\nItens comprados:\n"
        for item in self.itens_comprados:
            cupom += f"{item[1]} - Quantidade: {item[2]}, Total: R${item[3]:.2f}\n"

        with open("cupom_fiscal.txt", "w") as file:
            file.write(cupom)

        try:
            os.startfile("cupom_fiscal.txt")
        except:
            pass  # Para sistemas onde os.startfile não está disponível

# Código principal para execução da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
