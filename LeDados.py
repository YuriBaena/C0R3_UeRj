from tkinter import *
import tkinter as tk

# Funções de processamento de dados
def criar_dicionario_disciplinas(nome_do_arquivo="curso.txt"):
    disciplinas = {}

    with open(nome_do_arquivo, "r") as arquivo:
        lista_dados = arquivo.readlines()

    for linha in lista_dados[1:]:
        linha = linha.strip()

        if linha.startswith('-'):
            continue

        partes = linha.split(': ')
        periodo, resto_linha = partes[0].split(' ', 1)
        periodo = int(periodo)

        nome_disciplina = resto_linha.split('[')[0].strip()

        detalhes = linha.split(': ')[1]
        cred, ch, cod, nota = detalhes.split(", ")

        cred = int(cred.replace("'", "").replace("[", ""))
        ch = ch.replace("'", "")
        cod = cod.replace("'", "").replace("]", "")
        nota = float(nota.replace("]", ""))

        info_disciplina = [periodo, cred, ch, cod, nota]
        disciplinas[nome_disciplina] = info_disciplina

    return disciplinas

def verifica_periodos(disciplinas):
    max_periodo = 0
    for chave, valores in disciplinas.items():
        if isinstance(valores[0], int):
            if valores[0] > max_periodo:
                max_periodo = valores[0]
    return max_periodo

# Classe para a aplicação gráfica
class Aplicacao(tk.Tk):
    def __init__(self, disciplinas, periodos):
        super().__init__()

        self.disciplinas = disciplinas
        self.periodos = periodos
        self.checkboxes = {}
        self.entries_notas = {}
        self.cr_var = StringVar()

        self.title("C0R3 (coeficiente de rendimento)")
        self.config(background="#596475")
        self.geometry("590x700")

        self.cr_var.set("CR: 0 (sem eletivas)")

        self.setup_ui()
        self.calcular_cr()  # Calcula o CR automaticamente ao iniciar

    def setup_ui(self):
        tudo = Frame(self, bg="#596475")
        tudo.pack(fill=BOTH, expand=True)

        header = Frame(tudo, bg="#34495e", height=50)
        header.pack(fill=X)

        header_label = Label(header, text="Nome do Curso", font=("Helvetica", 18), fg="white", bg="#34495e")
        header_label.pack(pady=10)

        canvas = tk.Canvas(tudo, bg="#7a88a1")
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = tk.Scrollbar(tudo, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        frame_janela = Frame(canvas, bg="#7a88a1")
        canvas_frame_id = canvas.create_window((0, 0), window=frame_janela, anchor="nw")

        frame_janela.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame_id, width=e.width))

        self.create_periodos(frame_janela)

        footer = Frame(self, bg="#34495e", height=30)
        footer.pack(fill=X, side=BOTTOM)

        footer_label = Label(footer, textvariable=self.cr_var, fg="white", bg="#34495e")
        footer_label.pack(pady=5)

    def create_periodos(self, frame_janela):
        for i in range(1, self.periodos + 1):
            framePeriodos = Frame(frame_janela, bg="#464e5c")
            framePeriodos.grid(row=i, column=0, padx=10, pady=3, sticky="nsew")

            framePeriodos.grid_columnconfigure(0, weight=1)
            framePeriodos.grid_columnconfigure(1, weight=1)
            framePeriodos.grid_columnconfigure(2, weight=1)
            framePeriodos.grid_columnconfigure(3, weight=1)

            periodo_label = Label(framePeriodos, text=f"{i}˚ Período", fg="white", bg="#464e5c")
            periodo_label.grid(row=0, column=0, columnspan=4, pady=5, sticky="nsew")

            instrucao1 = Label(framePeriodos, text="FEZ?", fg="#0b1424", bg="#464e5c", font=("Helvetica", 12, "underline"))
            instrucao1.grid(row=1, column=0, sticky="w")

            instrucao2 = Label(framePeriodos, text="DISCIPLINA", fg="#0b1424", bg="#464e5c", font=("Helvetica", 12, "underline"))
            instrucao2.grid(row=1, column=1, sticky="nsew")

            instrucao3 = Label(framePeriodos, text="MÉDIA FINAL:", fg="#0b1424", bg="#464e5c", font=("Helvetica", 12, "underline"))
            instrucao3.grid(row=1, column=3, sticky="nsew")

            j = 2
            for disciplina, info in self.disciplinas.items():
                if info[0] == i:
                    self.create_discipline_widgets(framePeriodos, disciplina, info, j)
                    j += 1

    def create_discipline_widgets(self, framePeriodos, disciplina, info, row):
        x = IntVar()
        if info[-1] != 0:
            x.set(1)
        else:
            x.set(0)

        checkbox = Checkbutton(framePeriodos, variable=x, command=lambda d=disciplina, v=x, r=row: self.ajeita_checkboxes(d, v, r), bg="#464e5c")
        checkbox.grid(row=row, column=0, sticky="nsew")

        label = Label(framePeriodos, text=disciplina, fg="white", bg="#464e5c")
        label.grid(row=row, column=1, sticky="nsew")

        entry_nota = Entry(framePeriodos, bg="#464e5c", fg="white", highlightthickness=0)
        if info[-1] != 0:
            entry_nota.insert(0, info[-1])
            entry_nota.configure(state=DISABLED)
        entry_nota.grid(row=row, column=3, sticky="nsew")

        self.checkboxes[disciplina] = [row, x.get()]
        self.entries_notas[disciplina] = entry_nota

    def ajeita_checkboxes(self, disciplina, var, row):
        if var.get() == 1:
            self.checkboxes[disciplina] = [row, 1]
            self.disciplinas[disciplina].pop()
            nota = float(self.entries_notas[disciplina].get())
            nova_lista = self.disciplinas[disciplina]
            nova_lista.append(nota)
            self.disciplinas[disciplina] = nova_lista
        else:
            self.checkboxes[disciplina] = [row, 0]
        self.calcular_cr()

    def calcular_cr(self):
        total_creditos = 0
        soma_notas_creditos = 0

        for disciplina, info in self.disciplinas.items():
            if disciplina in self.checkboxes and self.checkboxes[disciplina][1] == 1:
                if info[-1] <= 10:
                    credito = info[1]
                    total_creditos += credito
                    soma_notas_creditos += int(info[-1]) * credito

        if total_creditos > 0:
            cr = soma_notas_creditos / total_creditos
            self.cr_var.set(f"CR: {cr:.2f}(sem eletivas)")
        else:
            self.cr_var.set("CR: N/A")

# Função principal para inicializar a aplicação
def main():
    disciplinas = criar_dicionario_disciplinas()
    periodos = verifica_periodos(disciplinas)
    app = Aplicacao(disciplinas, periodos)
    app.mainloop()

if __name__ == '__main__':
    main()
