from PegaDados import entra_na_do_seu_curso
from LeDados import main, janela_login
import os

try:
    resultado = janela_login()
    mat = resultado[0]
    sen = resultado[1]
    nome = entra_na_do_seu_curso(mat, sen)
    main(nome)
except Exception as e:
    print(f"Erro: {e}")
finally:
    arquivo_para_deletar = "curso.txt"

    if os.path.exists(arquivo_para_deletar):
        os.remove(arquivo_para_deletar)
        print(f"Arquivo '{arquivo_para_deletar}' deletado com sucesso.")

