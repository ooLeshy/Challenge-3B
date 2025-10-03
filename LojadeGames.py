import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class SistemaLojaGames:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loja Games")
        self.root.geometry("1920x1200")
        
        self.conectar_banco()
        self.criar_menu_principal()
        
    def conectar_banco(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='loja_games'
            )
            self.cursor = self.conn.cursor()
        except:
            messagebox.showerror("Erro", "Verifique o XAMPP!")

    def criar_menu_principal(self):
        tk.Label(self.root, text="MARIO GAMES", font=('Arial', 50, 'bold')).pack(pady=10)

        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=200)
        
        botoes = [
            ("📥 Cadastrar Jogo", self.janela1_cadastrar_jogo),
            ("📋 Listar Jogos", self.janela2_listar_jogos),
            ("✏️ Editar Jogo", self.janela3_editar_jogo),
            ("🗑️ Excluir Jogo", self.janela4_excluir_jogo),
            ("👥 Cadastrar Cliente", self.janela5_cadastrar_cliente),
            ("📊 Listar Clientes", self.janela6_listar_clientes),
            ("💰 Nova Venda", self.janela7_nova_venda),
            ("📈 Histórico Vendas", self.janela8_historico_vendas),
            ("📦 Estoque", self.janela9_estoque),
            ("🔍 Buscar Jogo", self.janela10_buscar_jogo),
            ("📋 Relatório Vendas", self.janela11_relatorio_vendas),
            ("🚪 Sair", self.root.quit)
        ]
        
        for i, (texto, comando) in enumerate(botoes):
            btn = tk.Button(frame_botoes, text=texto, command=comando,
                          width=20, height=2, bg='#3498db', fg='white',
                          font=('Arial', 10, 'bold'))
            btn.grid(row=i//2, column=i%2, padx=5, pady=3)
            
    # JANELA 1 - Cadastrar Jogo
    def janela1_cadastrar_jogo(self):
        janela = tk.Toplevel()
        janela.title("Cadastrar Jogo")
        janela.geometry("300x200")
        
        tk.Label(janela, text="Nome:").pack()
        nome = tk.Entry(janela)
        nome.pack()
        
        tk.Label(janela, text="Preço:").pack()
        preco = tk.Entry(janela)
        preco.pack()
        
        tk.Label(janela, text="Categoria:").pack()
        categoria = tk.Entry(janela)
        categoria.pack()
        
        tk.Label(janela, text="Estoque:").pack()
        estoque = tk.Entry(janela)
        estoque.pack()
        
        def salvar():
            try:
                self.cursor.execute(
                    "INSERT INTO jogos (nome, preco, categoria, estoque) VALUES (%s, %s, %s, %s)",
                    (nome.get(), float(preco.get()), categoria.get(), int(estoque.get()))
                )
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Jogo cadastrado!")
                janela.destroy()
            except:
                messagebox.showerror("Erro", "Dados inválidos!")
        
        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    # JANELA 2 - Listar Jogos
    def janela2_listar_jogos(self):
        janela = tk.Toplevel()
        janela.title("Lista de Jogos")
        janela.geometry("1100x300")
        
        tree = ttk.Treeview(janela, columns=('ID', 'Nome', 'Preço', 'Categoria', 'Estoque'), show='headings')
        for col in tree['columns']:
            tree.heading(col, text=col)
        
        self.cursor.execute("SELECT * FROM jogos")
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=row)
        
        tree.pack(fill='both', expand=True)

    # JANELA 3 - Editar Jogo
    def janela3_editar_jogo(self):
        janela = tk.Toplevel()
        janela.title("Editar Jogo")
        janela.geometry("300x250")
        
        tk.Label(janela, text="ID do Jogo:").pack()
        id_entry = tk.Entry(janela)
        id_entry.pack()
        
        tk.Label(janela, text="Novo Nome:").pack()
        nome = tk.Entry(janela)
        nome.pack()
        
        tk.Label(janela, text="Novo Preço:").pack()
        preco = tk.Entry(janela)
        preco.pack()
        
        def buscar():
            self.cursor.execute("SELECT * FROM jogos WHERE id = %s", (id_entry.get(),))
            jogo = self.cursor.fetchone()
            if jogo:
                nome.delete(0, tk.END)
                nome.insert(0, jogo[1])
                preco.delete(0, tk.END)
                preco.insert(0, jogo[2])
            else:
                messagebox.showwarning("Aviso", "Jogo não encontrado!")
        
        def salvar_edicao():
            try:
                self.cursor.execute(
                    "UPDATE jogos SET nome=%s, preco=%s WHERE id=%s",
                    (nome.get(), float(preco.get()), id_entry.get())
                )
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Jogo atualizado!")
                janela.destroy()
            except:
                messagebox.showerror("Erro", "Erro ao atualizar!")
        
        tk.Button(janela, text="Buscar", command=buscar).pack()
        tk.Button(janela, text="Salvar Alterações", command=salvar_edicao).pack(pady=10)

    # JANELA 4 - Excluir Jogo
    def janela4_excluir_jogo(self):
        janela = tk.Toplevel()
        janela.title("Excluir Jogo")
        janela.geometry("300x150")
        
        tk.Label(janela, text="ID do Jogo para excluir:").pack()
        id_entry = tk.Entry(janela)
        id_entry.pack()
        
        def excluir():
            if messagebox.askyesno("Confirmar", "Tem certeza?"):
                self.cursor.execute("DELETE FROM jogos WHERE id = %s", (id_entry.get(),))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Jogo excluído!")
                janela.destroy()
        
        tk.Button(janela, text="Excluir", command=excluir).pack(pady=10)

    # JANELA 5 - Cadastrar Cliente
    def janela5_cadastrar_cliente(self):
        janela = tk.Toplevel()
        janela.title("Cadastrar Cliente")
        janela.geometry("300x150")
        
        tk.Label(janela, text="Nome:").pack()
        nome = tk.Entry(janela)
        nome.pack()
        
        tk.Label(janela, text="Email:").pack()
        email = tk.Entry(janela)
        email.pack()
        
        def salvar():
            self.cursor.execute(
                "INSERT INTO clientes (nome, email) VALUES (%s, %s)",
                (nome.get(), email.get())
            )
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            janela.destroy()
        
        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    # JANELA 6 - Listar Clientes
    def janela6_listar_clientes(self):
        janela = tk.Toplevel()
        janela.title("Lista de Clientes")
        janela.geometry("800x300")
        
        tree = ttk.Treeview(janela, columns=('ID', 'Nome', 'Email'), show='headings')
        for col in tree['columns']:
            tree.heading(col, text=col)
        
        self.cursor.execute("SELECT * FROM clientes")
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=row)
        
        tree.pack(fill='both', expand=True)

    # JANELA 7 - Nova Venda
    def janela7_nova_venda(self):
        janela = tk.Toplevel()
        janela.title("Nova Venda")
        janela.geometry("400x300")
        
        # Cliente
        tk.Label(janela, text="ID Cliente:").pack()
        cliente_id = tk.Entry(janela)
        cliente_id.pack()
        
        # Jogo
        tk.Label(janela, text="ID Jogo:").pack()
        jogo_id = tk.Entry(janela)
        jogo_id.pack()
        
        tk.Label(janela, text="Quantidade:").pack()
        quantidade = tk.Entry(janela)
        quantidade.pack()
        
        def finalizar_venda():
            try:
                # Buscar preço do jogo
                self.cursor.execute("SELECT preco, estoque FROM jogos WHERE id = %s", (jogo_id.get(),))
                jogo = self.cursor.fetchone()
                
                if jogo and jogo[1] >= int(quantidade.get()):
                    total = float(jogo[0]) * int(quantidade.get())
                    
                    # Registrar venda
                    self.cursor.execute(
                        "INSERT INTO vendas (cliente_id, total) VALUES (%s, %s)",
                        (cliente_id.get(), total)
                    )
                    
                    # Atualizar estoque
                    self.cursor.execute(
                        "UPDATE jogos SET estoque = estoque - %s WHERE id = %s",
                        (int(quantidade.get()), jogo_id.get())
                    )
                    
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", f"Venda realizada! Total: R$ {total}")
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Estoque insuficiente!")
            except:
                messagebox.showerror("Erro", "Dados inválidos!")
        
        tk.Button(janela, text="Finalizar Venda", command=finalizar_venda).pack(pady=10)

    # JANELA 8 - Histórico de Vendas
    def janela8_historico_vendas(self):
        janela = tk.Toplevel()
        janela.title("Histórico de Vendas")
        janela.geometry("800x300")
        
        tree = ttk.Treeview(janela, columns=('ID', 'Cliente ID', 'Data', 'Total'), show='headings')
        for col in tree['columns']:
            tree.heading(col, text=col)
        
        self.cursor.execute("SELECT * FROM vendas ORDER BY data_venda DESC")
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=row)
        
        tree.pack(fill='both', expand=True)

    # JANELA 9 - Controle de Estoque
    def janela9_estoque(self):
        janela = tk.Toplevel()
        janela.title("Controle de Estoque")
        janela.geometry("800x300")
        
        tree = ttk.Treeview(janela, columns=('ID', 'Jogo', 'Estoque'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Jogo', text='Jogo')
        tree.heading('Estoque', text='Estoque')
        
        self.cursor.execute("SELECT id, nome, estoque FROM jogos ORDER BY estoque")
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=row)
        
        tree.pack(fill='both', expand=True)

    # JANELA 10 - Buscar Jogo
    def janela10_buscar_jogo(self):
        janela = tk.Toplevel()
        janela.title("Buscar Jogo")
        janela.geometry("900x300")
        
        tk.Label(janela, text="Nome do jogo:").pack()
        busca_entry = tk.Entry(janela)
        busca_entry.pack()
        
        tree = ttk.Treeview(janela, columns=('ID', 'Nome', 'Preço', 'Estoque'), show='headings')
        for col in tree['columns']:
            tree.heading(col, text=col)
        
        def buscar():
            for item in tree.get_children():
                tree.delete(item)
            
            self.cursor.execute("SELECT * FROM jogos WHERE nome LIKE %s", (f'%{busca_entry.get()}%',))
            for row in self.cursor.fetchall():
                tree.insert('', 'end', values=row)
        
        tk.Button(janela, text="Buscar", command=buscar).pack()
        tree.pack(fill='both', expand=True)

    # JANELA 11 - Relatório de Vendas
    def janela11_relatorio_vendas(self):
        janela = tk.Toplevel()
        janela.title("Relatório de Vendas")
        janela.geometry("400x200")
        
        # Total de vendas
        self.cursor.execute("SELECT SUM(total) FROM vendas")
        total_vendas = self.cursor.fetchone()[0] or 0
        
        # Quantidade de vendas
        self.cursor.execute("SELECT COUNT(*) FROM vendas")
        qtd_vendas = self.cursor.fetchone()[0]
        
        tk.Label(janela, text="RELATÓRIO GERAL", font=('Arial', 14, 'bold')).pack(pady=10)
        tk.Label(janela, text=f"Total de Vendas: R$ {total_vendas:.2f}").pack()
        tk.Label(janela, text=f"Quantidade de Vendas: {qtd_vendas}").pack()
        tk.Label(janela, text=f"Ticket Médio: R$ {total_vendas/qtd_vendas if qtd_vendas > 0 else 0:.2f}").pack()

    def executar(self):
        self.root.mainloop()

# Executar o sistema
if __name__ == "__main__":
    app = SistemaLojaGames()
    app.executar()
