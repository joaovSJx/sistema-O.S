# Configurações do sistema.

# Credenciais de acesso (login único, conforme solicitado).
LOGIN_USUARIO = "trab"
LOGIN_SENHA = "123456"

# Dados do recebedor do Pix, usados para gerar o BRCode/QRCode nos PDFs.
# Ajuste conforme a chave Pix real da assistência técnica.
# Formatos de chave aceitos pela biblioteca pybrcode:
#   CPF     -> ###.###.###-##
#   CNPJ    -> ##.###.###/####-##
#   Celular -> (##) #####-####
#   E-mail  -> ###@###.###
#   Aleatória -> string com 36 caracteres
PIX_NOME = "lucas"                  # até 25 caracteres (sem acentos)
PIX_CIDADE = "Sao Paulo"           # até 15 caracteres (sem acentos)
PIX_CHAVE = "31999673097"
