import csv
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

#Olá, só pra avisar que a parte visual (TKINTER) ficou 100% responsavel pelo ChatGPT!

def carregar_exercicios():
    try:
        with open('exercicios.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            exercicios = list(reader)
    except FileNotFoundError:
        exercicios = []
    return exercicios

def salvar_exercicios(exercicios):
    with open('exercicios.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['nome', 'repeticoes', 'carga', 'tipo_carga', 'descricao']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for exercicio in exercicios:
            writer.writerow(exercicio)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Exercícios")
        self.geometry("800x600")
        self.resizable(False, False)

        self.exercicios = carregar_exercicios()

        self.style = ttk.Style(self)
        self.style.theme_use('clam') 

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="Gerenciador de Exercícios", font=("Helvetica", 18)).pack(pady=10)

        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(pady=20)

        ttk.Button(buttons_frame, text="Listar Exercícios", width=20, command=self.listar_exercicios).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(buttons_frame, text="Criar Exercício", width=20, command=self.criar_exercicio).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(buttons_frame, text="Editar Exercício", width=20, command=self.editar_exercicio).grid(row=2, column=0, padx=10, pady=5)
        ttk.Button(buttons_frame, text="Sair", width=20, command=self.quit).grid(row=3, column=0, padx=10, pady=5)

    def listar_exercicios(self):
        listar_window = tk.Toplevel(self)
        listar_window.title("Lista de Exercícios")
        listar_window.geometry("700x500")

        columns = ('Nome', 'Repetições', 'Carga (kg)', 'Tipo de Carga', 'Descrição')
        tree = ttk.Treeview(listar_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        for exercicio in self.exercicios:
            tree.insert('', tk.END, values=(exercicio['nome'], exercicio['repeticoes'], exercicio['carga'],
                                            exercicio['tipo_carga'], exercicio['descricao']))
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(listar_window, text="Fechar", command=listar_window.destroy).pack(pady=10)

    def criar_exercicio(self):
        formulario = FormularioExercicio(self, "Criar Exercício")
        self.wait_window(formulario)
        if formulario.result:
            self.exercicios.append(formulario.result)
            salvar_exercicios(self.exercicios)
            messagebox.showinfo("Sucesso", "Exercício criado com sucesso!")

    def editar_exercicio(self):
        if not self.exercicios:
            messagebox.showwarning("Aviso", "Nenhum exercício cadastrado para editar.")
            return

        editar_window = tk.Toplevel(self)
        editar_window.title("Editar Exercício")
        editar_window.geometry("700x500")

        columns = ('Nome', 'Repetições', 'Carga (kg)', 'Tipo de Carga', 'Descrição')
        tree = ttk.Treeview(editar_window, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        for idx, exercicio in enumerate(self.exercicios):
            tree.insert('', tk.END, iid=idx, values=(exercicio['nome'], exercicio['repeticoes'], exercicio['carga'],
                                                     exercicio['tipo_carga'], exercicio['descricao']))
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def editar_selecionado():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Aviso", "Selecione um exercício para editar.")
                return
            idx = int(selected)
            exercicio = self.exercicios[idx]
            formulario = FormularioExercicio(self, "Editar Exercício", exercicio)
            self.wait_window(formulario)
            if formulario.result:
                self.exercicios[idx] = formulario.result
                salvar_exercicios(self.exercicios)
                tree.item(selected, values=(formulario.result['nome'], formulario.result['repeticoes'],
                                            formulario.result['carga'], formulario.result['tipo_carga'],
                                            formulario.result['descricao']))
                messagebox.showinfo("Sucesso", "Exercício editado com sucesso!")

        
        botoes_frame = ttk.Frame(editar_window)
        botoes_frame.pack(pady=10)
        ttk.Button(botoes_frame, text="Editar Selecionado", command=editar_selecionado).grid(row=0, column=0, padx=10)
        ttk.Button(botoes_frame, text="Fechar", command=editar_window.destroy).grid(row=0, column=1, padx=10)

class FormularioExercicio(tk.Toplevel):
    def __init__(self, parent, title, exercicio=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x500")
        self.resizable(False, False)
        self.result = None

        self.create_widgets(exercicio)

    def create_widgets(self, exercicio):
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nome do Exercício:").pack(anchor=tk.W, pady=5)
        self.nome_var = tk.StringVar(value=exercicio['nome'] if exercicio else "")
        ttk.Entry(frame, textvariable=self.nome_var).pack(fill=tk.X, pady=5)

        ttk.Label(frame, text="Número de Repetições:").pack(anchor=tk.W, pady=5)
        self.repeticoes_var = tk.StringVar(value=exercicio['repeticoes'] if exercicio else "")
        ttk.Entry(frame, textvariable=self.repeticoes_var).pack(fill=tk.X, pady=5)

        ttk.Label(frame, text="Tipo de Carga:").pack(anchor=tk.W, pady=5)
        self.tipo_carga_var = tk.StringVar(value=exercicio['tipo_carga'] if exercicio else "1")
        tipos = [
            ("1. Halteres", "1"),
            ("2. Barra com anilhas", "2"),
            ("3. Máquina com anilha", "3"),
            ("4. Máquina com pino", "4"),
        ]
        for text, value in tipos:
            ttk.Radiobutton(frame, text=text, variable=self.tipo_carga_var, value=value, command=self.atualizar_tipo_carga).pack(anchor=tk.W)

        ttk.Label(frame, text="Carga (kg):").pack(anchor=tk.W, pady=5)
        self.carga_var = tk.StringVar(value=exercicio['carga'] if exercicio else "")
        self.carga_entry = ttk.Entry(frame, textvariable=self.carga_var)
        self.carga_entry.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text="Descrição:").pack(anchor=tk.W, pady=5)
        self.descricao_var = tk.StringVar(value=exercicio['descricao'] if exercicio else "")
        ttk.Entry(frame, textvariable=self.descricao_var).pack(fill=tk.X, pady=5)

        botoes_frame = ttk.Frame(frame)
        botoes_frame.pack(pady=20)
        ttk.Button(botoes_frame, text="Salvar", command=self.salvar).grid(row=0, column=0, padx=10)
        ttk.Button(botoes_frame, text="Cancelar", command=self.destroy).grid(row=0, column=1, padx=10)

        if exercicio:
            self.atualizar_tipo_carga()

    def atualizar_tipo_carga(self):
        tipo = self.tipo_carga_var.get()
        if tipo == '1':
            peso = simpledialog.askfloat("Halteres", "Digite o peso do(s) haltere(s) (em kg):", parent=self)
            if peso is not None:
                halteres = simpledialog.askinteger("Halteres", "O exercício requer 1 ou 2 halteres?", parent=self, minvalue=1, maxvalue=2)
                if halteres:
                    if halteres == 1:
                        carga = peso
                        tipo_carga = f'1 Halter - Peso: {peso}kg'
                    else:
                        carga = 2 * peso
                        tipo_carga = f'2 Halteres - Peso: {peso}kg cada'
                    self.carga_var.set(carga)
                    self.tipo_carga_var.set(tipo)
        elif tipo == '2':
            peso_lado = simpledialog.askfloat("Barra com Anilhas", "Digite o peso de cada lado da barra (em kg):", parent=self)
            peso_barra = simpledialog.askfloat("Barra com Anilhas", "Digite o peso da barra (em kg):", parent=self)
            if peso_lado is not None and peso_barra is not None:
                carga = 2 * peso_lado + peso_barra
                tipo_carga = f'Barra com Anilhas - Peso por lado: {peso_lado}kg, Peso da Barra: {peso_barra}kg'
                self.carga_var.set(carga)
                self.tipo_carga_var.set(tipo)
        elif tipo == '3' or tipo == '4':
            carga = simpledialog.askfloat("Máquina", "Digite o peso total da máquina (em kg):", parent=self)
            if carga is not None:
                tipo_carga = 'Máquina com Anilha' if tipo == '3' else 'Máquina com Pino'
                self.carga_var.set(carga)
                self.tipo_carga_var.set(tipo_carga)

    def salvar(self):
        nome = self.nome_var.get().strip()
        repeticoes = self.repeticoes_var.get().strip()
        carga = self.carga_var.get().strip()
        tipo_carga = self.tipo_carga_var.get().strip()
        descricao = self.descricao_var.get().strip()

        if not nome or not repeticoes or not carga or not tipo_carga:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            repeticoes = int(repeticoes)
            carga = float(carga)
        except ValueError:
            messagebox.showerror("Erro", "Repetições devem ser um número inteiro e carga deve ser um número.")
            return

        exercicio = {
            'nome': nome,
            'repeticoes': repeticoes,
            'carga': carga,
            'tipo_carga': tipo_carga,
            'descricao': descricao
        }

        self.result = exercicio
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
