from PegaDados import janela_login
from LeDados import main
import os

try:
    main()
except Exception as e:
    janela_login()
    main()
finally:
    arquivo_para_deletar = "curso.txt"

    if os.path.exists(arquivo_para_deletar):
        os.remove(arquivo_para_deletar)
        print(f"Arquivo '{arquivo_para_deletar}' deletado com sucesso.")

