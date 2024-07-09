import tkinter as tk
from tkinter import Frame, Label, Entry, Button, BOTTOM, X
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def entra_na_do_seu_curso(matricula_pessoal, senha_pessoal):


    def entra():
        chrome.get("https://www.alunoonline.uerj.br/requisicaoaluno/")
        time.sleep(1)

        matricula_input = chrome.find_element(By.XPATH, '//*[@id="matricula"]')
        matricula_input.send_keys(matricula_pessoal)

        senha_input = chrome.find_element(By.XPATH, '//*[@id="senha"]')
        senha_input.send_keys(senha_pessoal)

        senha_input.send_keys(Keys.ENTER)
        time.sleep(3)

    def nome_curso():
        nome = chrome.find_element(By.XPATH, '//*[@id="table_cabecalho_rodape"]/tbody/tr[3]/td/font')
        nome = " ".join((nome.text.split("- ")[1]).split(" ")[:2])

        entra = chrome.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td/form/table/tbody/tr[4]/td[3]/div[2]/div[15]/a')
        entra.click()
        time.sleep(3)

        curso = chrome.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td/div/div[2]/div[2]/div[1]/div[3]')
        curso = curso.text.split(":")[1]

        volta = chrome.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/a[1]')
        volta.click()
        time.sleep(2)

        return (nome, curso)

    def entra_disciplinas():
        disciplinas = chrome.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td/form/table/tbody/tr[4]/td[3]/div[2]/div[3]/a')
        disciplinas.click()
        time.sleep(2)

    def disciplina(i):
        continua = True
        periodo = chrome.find_element(By.XPATH, f'/html/body/table/tbody/tr[3]/td/form/div[1]/div[2]/table/tbody/tr[{i}]/td[2]')

        if not periodo.text.isnumeric():
            continua = False
            return continua

        disciplina = chrome.find_element(By.XPATH, f'/html/body/table/tbody/tr[3]/td/form/div[1]/div[2]/table/tbody/tr[{i}]/td[1]')
        cred = chrome.find_element(By.XPATH, f'/html/body/table/tbody/tr[3]/td/form/div[1]/div[2]/table/tbody/tr[{i}]/td[6]')
        ch = chrome.find_element(By.XPATH, f'/html/body/table/tbody/tr[3]/td/form/div[1]/div[2]/table/tbody/tr[{i}]/td[7]')

        codigo = disciplina.text.split(" ")[0]
        disciplina_nome = " ".join(disciplina.text.split(" ")[1:])
        cred_valor = cred.text
        ch_horas = ch.text + "hrs"
        periodo_valor = periodo.text

        discip_cred[periodo_valor + " " + disciplina_nome] = [cred_valor, ch_horas, codigo]

        return continua

    def sai_salva():
        chrome.quit()  # Fechar o navegador ao finalizar
        salvar_dict_em_arquivo(discip_cred)

    discip_cred = {}

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Roda o Chrome em modo headless
    chrome = webdriver.Chrome(options=chrome_options)

    entra()
    nome, curso = nome_curso()
    entra_disciplinas()

    i = 2
    while True:
        continua = disciplina(i)
        if not continua:
            break
        i += 1

    sai_salva()

    return f"{nome} - {curso}"

def salvar_dict_em_arquivo(dicionario):
    with open("curso.txt", 'w') as arquivo:
        for chave, valor in dicionario.items():
            arquivo.write(f'{chave}: {valor}\n')

def janela_login():
    global nome
    # Criando a janela de login
    login_janela = tk.Tk()
    login_janela.title("Login")
    login_janela.config(background="#596475")

    # Frame para conter tudo
    tudo = Frame(login_janela, bg="#596475")
    tudo.pack(padx=20, pady=40)

    # Cabeçalho
    header = Frame(tudo, bg="#34495e")
    header.pack(fill=X)

    header_label = Label(header, text="Login", font=("Helvetica", 18), fg="white", bg="#34495e")
    header_label.pack(pady=10)

    # Campos de entrada
    matricula_label = Label(tudo, text="Matrícula:", fg="white", bg="#596475")
    matricula_label.pack(pady=5)

    matricula_entry = Entry(tudo, bg="#464e5c", fg="white", highlightthickness=0)
    matricula_entry.pack(pady=5)

    senha_label = Label(tudo, text="Senha:", fg="white", bg="#596475")
    senha_label.pack(pady=5)

    senha_entry = Entry(tudo, bg="#464e5c", fg="white", highlightthickness=0, show="*")
    senha_entry.pack(pady=5)

    # Botão de login
    def on_login_click():
        global nome
        mat = matricula_entry.get()
        sen = senha_entry.get()
        nome = entra_na_do_seu_curso(mat, sen)
        login_janela.destroy()

    login_button = Button(tudo, text="Login", bg="#34495e", highlightbackground="#596475", command=on_login_click)
    login_button.pack(pady=10, ipadx=10)

    # Rodapé
    footer = Frame(login_janela, bg="#34495e", height=30)
    footer.pack(fill=X, side=BOTTOM)

    footer_label = Label(footer, text="Sistema de Gestão Acadêmica", fg="white", bg="#34495e")
    footer_label.pack(pady=5)

    login_janela.mainloop()

    return nome
