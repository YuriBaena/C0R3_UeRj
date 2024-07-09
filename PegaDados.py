from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def entra_na_do_seu_curso(matricula_pessoal, senha_pessoal):
    discip_cred = {}

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Roda o Chrome em modo headless
    chrome = webdriver.Chrome(options=chrome_options)

    chrome.get("https://www.alunoonline.uerj.br/requisicaoaluno/")
    chrome.maximize_window()
    time.sleep(1)

    matricula_input = chrome.find_element(By.XPATH, '//*[@id="matricula"]')
    matricula_input.send_keys(matricula_pessoal)

    senha_input = chrome.find_element(By.XPATH, '//*[@id="senha"]')
    senha_input.send_keys(senha_pessoal)

    senha_input.send_keys(Keys.ENTER)
    time.sleep(3)

    nome = chrome.find_element(By.XPATH, '//*[@id="table_cabecalho_rodape"]/tbody/tr[3]/td/font')
    nome = " ".join((nome.text.split("- ")[1]).split(" ")[:2])

    # Descobrindo curso
    entra = chrome.find_element(By.XPATH,
                                '/html/body/table/tbody/tr[3]/td/form/table/tbody/tr[4]/td[3]/div[2]/div[15]/a')
    entra.click()

    time.sleep(3)

    curso = chrome.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td/div/div[2]/div[2]/div[1]/div[3]')
    curso = curso.text.split(":")[1]

    # Voltando para pagina principal
    volta = chrome.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/a[1]')
    volta.click()

    time.sleep(2)

    # Disciplinas de Ccomp
    disciplinas = chrome.find_element(By.XPATH,
                                      '/html/body/table/tbody/tr[3]/td/form/table/tbody/tr[4]/td[3]/div[2]/div[3]/a')
    disciplinas.click()

    time.sleep(2)

    for i in range(2, 78):
        periodo = chrome.find_element(By.XPATH,
                                      f'/html/body/table/tbody/tr[3]/td/form/div[1]/div[2]/table/tbody/tr[{i}]/td[2]')

        disciplina = chrome.find_element(By.XPATH,
                                         f'/html/body/table/tbody/tr[3]/td/form/div[1]/div[2]/table/tbody/tr[{i}]/td[1]')
        cred = chrome.find_element(By.XPATH,
                                   f'/html/body/table/tbody/tr[3]/td/form/div[1]/div[2]/table/tbody/tr[{i}]/td[6]')
        ch = chrome.find_element(By.XPATH,
                                 f'/html/body/table/tbody/tr[3]/td/form/div[1]/div[2]/table/tbody/tr[{i}]/td[7]')

        codigo = disciplina.text.split(" ")[0]
        disciplina_nome = " ".join(disciplina.text.split(" ")[1:])
        cred_valor = cred.text
        ch_horas = ch.text + "hrs"
        periodo_valor = periodo.text

        discip_cred[periodo_valor + " " + disciplina_nome] = [cred_valor, ch_horas, codigo]

    chrome.quit()  # Fechar o navegador ao finalizar
    salvar_dict_em_arquivo(discip_cred, "curso.txt")

    return f"{nome} - {curso}"


def salvar_dict_em_arquivo(dicionario, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for chave, valor in dicionario.items():
            arquivo.write(f'{chave}: {valor}\n')


if __name__ == '__main__':
    mat = input("Matricula: ")
    sen = input("Senha: ")
    entra_na_do_seu_curso(mat,sen)
