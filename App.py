from PegaDados import janela_login
from LeDados import main
import os

try:
    nome = janela_login()
    main(nome)
except Exception as e:
    print(f"Erro: {e}")
finally:
    arquivo_para_deletar = "curso.txt"

    if os.path.exists(arquivo_para_deletar):
        os.remove(arquivo_para_deletar)
        print(f"Arquivo '{arquivo_para_deletar}' deletado com sucesso.")

