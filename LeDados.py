from tkinter import *
import tkinter as tk


def criar_dicionario_disciplinas(nome_do_arquivo="curso.txt"):
    disciplinas = {}

    with open(nome_do_arquivo, "r") as arquivo:
        lista_dados = arquivo.readlines()

    for linha in lista_dados[1:]:
        linha = linha.strip()

        # Ignorar linhas que começam com "-"
        if linha.startswith('-'):
            continue

        # Extrair período e resto da linha
        partes = linha.split(': ')
        periodo, resto_linha = partes[0].split(' ', 1)
        periodo = int(periodo)

        # Extrair nome da disciplina
        nome_disciplina = resto_linha.split('[')[0].strip()

        # Extrair detalhes
        detalhes = linha.split(': ')[1]
        cred, ch, cod, nota = detalhes.split(", ")

        # Organizando creditos
        cred = int(cred.replace("'", "").replace("[", ""))

        # Organizando carga horaria
        ch = ch.replace("'", "")

        # Organizando codigo da disciplina
        cod = cod.replace("'", "").replace("]", "")

        #Organizando nota
        nota = float(nota.replace("]", ""))

        # Montar a lista de informações
        info_disciplina = [periodo, cred, ch, cod, nota]

        # Adicionar ao dicionário
        disciplinas[nome_disciplina] = info_disciplina

    return disciplinas


def verifica_periodos(disciplinas):
    max_periodo = 0

    for chave, valores in disciplinas.items():
        if isinstance(valores[0], int):  # Verifica se valores[0] é do tipo int
            if valores[0] > max_periodo:
                max_periodo = valores[0]

    return max_periodo


def ajeita_checkboxes(disciplina, var, row, disciplinas):
    global checkboxes, entries_notas
    if var.get() == 1:
        checkboxes[disciplina] = [row, 1]
        disciplinas[disciplina].pop()
        nota = float(entries_notas[disciplina].get())
        nova_lista = disciplinas[disciplina]
        nova_lista.append(nota)
        disciplinas[disciplina] = nova_lista
    else:
        checkboxes[disciplina] = [row, 0]
    calcular_cr()


def calcular_cr():
    global checkboxes, entries_notas, disciplinas, cr_var

    total_creditos = 0
    soma_notas_creditos = 0

    for disciplina, info in disciplinas.items():
        if disciplina in checkboxes and checkboxes[disciplina][1] == 1:  # Se o checkbox está marcado
            if info[-1] <= 10:
                credito = info[1]
                total_creditos += credito
                soma_notas_creditos += int(info[-1]) * credito

    if total_creditos > 0:
        cr = soma_notas_creditos / total_creditos
        cr_var.set(f"CR: {cr:.2f}(sem eletivas)")
    else:
        cr_var.set("CR: N/A")


def main():
    global checkboxes, disciplinas, entries_notas, cr_var

    with open("curso.txt", "r") as arqv:
        nome = arqv.readlines(1)[0]
        arqv.close()

    disciplinas = criar_dicionario_disciplinas()
    periodos = verifica_periodos(disciplinas)
    checkboxes = {}
    entries_notas = {}

    janela = tk.Tk()
    janela.title("C0R3 (coeficiente de rendimento)")
    janela.config(background="#596475")
    janela.geometry("590x700")

    # Criando um frame para conter tudo e expandir conforme o tamanho da janela
    tudo = Frame(janela, bg="#596475")
    tudo.pack(fill=BOTH, expand=True)

    # Header fixo
    header = Frame(tudo, bg="#34495e", height=50)
    header.pack(fill=X)

    header_label = Label(header, text=f"{nome}", font=("Helvetica", 18), fg="white", bg="#34495e")
    header_label.pack(pady=10)

    # Canvas com scrollbar
    canvas = Canvas(tudo, bg="#7a88a1")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(tudo, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame que contém os períodos
    frame_janela = Frame(canvas, bg="#7a88a1")
    canvas_frame_id = canvas.create_window((0, 0), window=frame_janela, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_janela.bind("<Configure>", on_frame_configure)

    def on_canvas_configure(event):
        canvas.itemconfig(canvas_frame_id,
                          width=event.width)  # Ajusta a largura do frame_janela conforme a largura do canvas

    canvas.bind("<Configure>", on_canvas_configure)

    for i in range(1, periodos + 1):
        framePeriodos = Frame(frame_janela, bg="#464e5c")
        framePeriodos.grid(row=i, column=0, padx=10, pady=3, sticky="nsew")

        # Equal column widths
        framePeriodos.grid_columnconfigure(0, weight=1)
        framePeriodos.grid_columnconfigure(1, weight=1)
        framePeriodos.grid_columnconfigure(2, weight=1)
        framePeriodos.grid_columnconfigure(3, weight=1)

        periodo_label = Label(framePeriodos, text=f"{i}˚ Período", fg="white", bg="#464e5c")
        periodo_label.grid(row=0, column=0, columnspan=4, pady=5, sticky="nsew")

        # Labels para instruções
        instrucao1 = Label(framePeriodos, text="FEZ?", fg="#0b1424", bg="#464e5c", font=("Helvetica", 12, "underline"))
        instrucao1.grid(row=1, column=0, sticky="w")

        instrucao2 = Label(framePeriodos, text="DISCIPLINA", fg="#0b1424", bg="#464e5c", font=("Helvetica", 12, "underline"))
        instrucao2.grid(row=1, column=1, sticky="nsew")

        instrucao3 = Label(framePeriodos, text="MÉDIA FINAL:", fg="#0b1424", bg="#464e5c", font=("Helvetica", 12, "underline"))
        instrucao3.grid(row=1, column=3, sticky="nsew")

        j = 2
        for disciplina, info in disciplinas.items():
            if info[0] == i and info[-1] == 0:
                # Checkbutton for checkbox
                x = IntVar()
                checkbox = Checkbutton(framePeriodos, variable=x,
                                       command=lambda d=disciplina, dd=disciplinas , v=x, r=j: ajeita_checkboxes(d, v, r, dd),
                                       bg="#464e5c")
                checkbox.grid(row=j, column=0, sticky="nsew")

                # Label for discipline name
                label = Label(framePeriodos, text=disciplina, fg="white", bg="#464e5c")
                label.grid(row=j, column=1, sticky="nsew")

                # Entry for note
                entry_nota = Entry(framePeriodos, bg="#464e5c", fg="white", highlightthickness=0)
                entry_nota.grid(row=j, column=3, sticky="nsew")

                checkboxes[disciplina] = [j, 0]
                entries_notas[disciplina] = entry_nota

                j += 1

            elif info[0] == i and info[-1] != 0:
                # Checkbutton for checkbox
                x = IntVar()
                checkbox = Checkbutton(framePeriodos, variable=x,
                                       command=lambda d=disciplina, dd=disciplinas , v=x, r=j: ajeita_checkboxes(d, v, r, dd),
                                       bg="#464e5c")
                checkbox.grid(row=j, column=0, sticky="nsew")

                # Label for discipline name
                label = Label(framePeriodos, text=disciplina, fg="white", bg="#464e5c")
                label.grid(row=j, column=1, sticky="nsew")

                # Entry for note
                entry_nota = Entry(framePeriodos, bg="#464e5c", fg="white", highlightthickness=0)
                entry_nota.insert(0, info[-1])
                entry_nota.configure(state=DISABLED)
                entry_nota.grid(row=j, column=3, sticky="nsew")

                checkboxes[disciplina] = [j, 0]
                entries_notas[disciplina] = entry_nota

                j += 1

    # Footer fixo
    footer = Frame(janela, bg="#34495e", height=30)
    footer.pack(fill=X, side=BOTTOM)

    cr_var = StringVar()
    cr_var.set("CR: 0 (sem eletivas)")
    footer_label = Label(footer, textvariable=cr_var, fg="white", bg="#34495e")
    footer_label.pack(pady=5)

    janela.mainloop()

if __name__ == '__main__':
    main()