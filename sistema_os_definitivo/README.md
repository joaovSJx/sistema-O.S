# Sistema de Ordem de Serviço

Projeto acadêmico de um sistema para assistência técnica, desenvolvido em Python. O objetivo é organizar clientes, equipamentos e ordens de serviço, mantendo os dados em um banco SQLite.

## Tecnologias

- Python
- SQLite
- SQL
- ttkbootstrap (interface gráfica)
- FPDF2 (geração de PDF)
- pybrcode (geração do QR Code Pix)

## Funcionalidades implementadas

- Criação automática do banco de dados SQLite.
- Cadastro de clientes (reaproveitando o cadastro quando o CPF já existe).
- Cadastro de equipamentos vinculados a clientes.
- Cadastro de ordem de serviço.
- Validação de problema e data de entrada.
- Validação do formato da data: `AAAA-MM-DD`.
- Verificação de que o equipamento pertence ao cliente informado.
- Retorno do número da OS criada.
- Consulta de OS:
  - todas as ordens;
  - por número da OS;
  - por status;
  - por nome do cliente;
  - por período de entrada.
- Geração de PDF da ordem de serviço com logo, dados do atendimento, valor, diagnóstico, serviço realizado e espaço para assinaturas.
- Geração automática do QR Code Pix (via `pybrcode`) e inserção dele no PDF, sempre que a OS tiver um valor definido.
- Interface gráfica em ttkbootstrap com duas telas:
  - **Login** (usuário e senha fixos, definidos em `config.py`);
  - **Cadastrar Ordem de Serviço** (cliente + equipamento + OS em um único formulário, já linkado ao banco e ao gerador de PDF/Pix).

## Estrutura do projeto

```text
sistema os/
├── config.py
├── imagens/
│   └── logo.jpeg
├── database/
│   ├── banco.py
│   ├── clientes.py
│   ├── connection.py
│   └── ordens_servico.py
├── documentos/
│   ├── gerados/
│   └── gerar_pdf.py
├── interface/
│   ├── app.py
│   ├── login.py
│   └── cadastro.py
├── pix/
│   └── gerar_pix.py
├── main.py
├── teste_banco.py
└── assistencia.db
```

## Banco de dados

O banco `assistencia.db` possui três tabelas:

- `clientes`: informações dos clientes.
- `equipamentos`: equipamentos vinculados a um cliente.
- `ordens_servico`: registros das OS vinculados ao cliente e ao equipamento.

Os status iniciais previstos são: `Aberta`, `Em análise`, `Em manutenção` e `Concluída`.

## Configuração (`config.py`)

Antes de rodar o sistema, ajuste o `config.py`:

- `LOGIN_USUARIO` / `LOGIN_SENHA`: credenciais fixas de acesso à interface (padrão: `trab` / `123456`).
- `PIX_NOME`, `PIX_CIDADE`, `PIX_CHAVE`: dados do recebedor usados para gerar o QR Code Pix. `PIX_CHAVE` precisa estar em um dos formatos aceitos pela `pybrcode` (CPF, CNPJ, celular, e-mail ou chave aleatória de 36 caracteres).

## Como executar

1. Instale o Python 3.
2. Instale as bibliotecas necessárias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Ajuste as credenciais e a chave Pix em `config.py`.

4. Crie as tabelas (se ainda não existirem) e abra a interface gráfica:

   ```powershell
   python main.py
   ```

   A tela de **login** abrirá primeiro (usuário/senha definidos em `config.py`). Após entrar, a interface atual exibe o cadastro de clientes. As telas de equipamento e ordem de serviço podem ser integradas depois.

5. Use `teste_banco.py` para testar as funções de banco ou gerar um PDF de uma OS existente sem usar a interface:

   ```powershell
   python teste_banco.py
   ```

Os PDFs gerados são salvos na pasta `documentos/gerados/`.

## Funções principais

`database/clientes.py`:

| Função | Finalidade |
|---|---|
| `cadastrar_cliente(nome, cpf, telefone, email, endereco)` | Cadastra um cliente (ou reaproveita um existente pelo CPF) e retorna seu id. |
| `buscar_cliente_por_cpf(cpf)` | Busca um cliente pelo CPF. |
| `buscar_cliente_por_id(cliente_id)` | Busca um cliente pelo id. |
| `listar_clientes()` | Lista todos os clientes. |

`database/ordens_servico.py`:

| Função | Finalidade |
|---|---|
| `cadastrar_equipamento(cliente_id, tipo, marca, modelo, numero_serie, descricao)` | Cadastra um equipamento vinculado a um cliente e retorna seu id. |
| `cadastrar_os(cliente_id, equipamento_id, problema, valor, data_entrada)` | Cadastra uma OS e retorna seu número. |
| `consultar_os()` | Lista todas as OS. |
| `consultar_os_por_id(id_os)` | Busca uma OS pelo número. |
| `consultar_os_por_status(status)` | Busca OS por status. |
| `consultar_os_por_cliente(nome_cliente)` | Busca OS por nome ou parte do nome do cliente. |
| `consultar_os_por_periodo(data_inicio, data_fim)` | Busca OS dentro de um período de entrada. |

`pix/gerar_pix.py`:

| Função | Finalidade |
|---|---|
| `gerar_qrcode_pix(valor, pix_id, descricao, pasta, nome_arquivo)` | Gera o QR Code Pix (BRCode) via `pybrcode` e salva um PNG; retorna `None` se não houver valor. |

`documentos/gerar_pdf.py`:

| Função | Finalidade |
|---|---|
| `gerar_pdf_os(id_os)` | Gera o PDF de uma OS existente, incluindo automaticamente o QR Code Pix quando a OS tiver valor definido. |

## Interface gráfica

`interface/app.py` mantém a única janela do sistema e alterna entre `interface/login.py` e `interface/cadastro.py` (que são frames, não janelas separadas), conforme descrito em "Como executar".

## Próximos passos

- Telas de consulta/listagem de OS e alteração de status.
- Edição de dados de clientes e equipamentos já cadastrados.
