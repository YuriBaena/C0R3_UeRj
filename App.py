from PegaDados import janela_login
from LeDados import main

try:
    main()
except Exception as e:
    janela_login()
    main()