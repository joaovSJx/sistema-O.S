# Sistema de Ordem de Serviço

Aplicação desktop para gestão de assistências técnicas. O sistema permite cadastrar clientes e equipamentos, abrir e acompanhar ordens de serviço, consultar indicadores no painel e gerar documentos em PDF com QR Code para pagamento via Pix.

## Funcionalidades

- Cadastro e autenticação de usuários.
- Cadastro, edição e busca de clientes.
- Cadastro e consulta de equipamentos vinculados a clientes.
- Abertura e acompanhamento de ordens de serviço.
- Filtros por número da OS, cliente, status e período de entrada.
- Painel com totais de OS abertas, em análise, em manutenção e concluídas.
- Geração de PDF da ordem de serviço.
- Inclusão de QR Code Pix no PDF quando a OS possui valor definido.
- Banco de dados local SQLite, criado e preparado automaticamente na inicialização.

## Requisitos

- Python 3.10 ou superior.
- Tkinter instalado no sistema operacional, necessário para a interface gráfica.
- Um ambiente com suporte a janelas gráficas; o projeto não é uma aplicação web.

No Ubuntu/Debian, caso o Tkinter não esteja instalado:

```bash
sudo apt update
sudo apt install python3-tk
```

## Instalação

Clone ou copie o projeto e entre na pasta da aplicação:

```bash
cd "sistema_os(final)"
```

É recomendado usar um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows, a ativação equivalente é:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Como executar

Ainda dentro de `sistema_os(final)`, execute:

```bash
python main.py
```

Na primeira execução, o sistema cria o arquivo `assistencia.db` e as tabelas necessárias. O arquivo fica no diretório em que o comando foi executado; por isso, execute o programa a partir de `sistema_os(final)` para manter os dados no local esperado.

## Primeiro acesso

O usuário legado criado automaticamente é:

| Campo | Valor |
| --- | --- |
| Usuário | `trab` |
| Senha | `123456` |

Depois de entrar, é possível cadastrar outros usuários pela tela inicial. Não use a credencial padrão em um ambiente real: a autenticação ainda é local e o armazenamento de senhas não utiliza hash. As credenciais legadas ficam definidas em [config.py](sistema_os(final)/config.py).

## Configuração do Pix

Edite [config.py](sistema_os(final)/config.py) antes de gerar documentos para substituir os dados de demonstração:

```python
PIX_NOME = "Nome da assistência"
PIX_CIDADE = "Sua Cidade"
PIX_CHAVE = "sua-chave-pix"
```

Os valores devem respeitar as regras do padrão Pix e da biblioteca `pybrcode`: nome com até 25 caracteres, cidade com até 15 caracteres e uma chave Pix válida. O QR Code só é incluído quando a OS tem um valor maior que zero.

## Fluxo recomendado

1. Faça login ou crie uma conta.
2. Cadastre o cliente com seus dados de contato.
3. Cadastre o equipamento e vincule-o ao cliente.
4. Abra uma nova OS, selecione o cliente e o equipamento e informe o problema.
5. Atualize status, diagnóstico, serviço realizado e valor conforme o atendimento evoluir.
6. Gere o PDF pela listagem de ordens de serviço.

Os status disponíveis são `Aberta`, `Em análise`, `Em manutenção` e `Concluída`.

## Arquivos gerados e dados locais

- `assistencia.db`: banco SQLite local, criado em tempo de execução.
- `documentos/gerados/Ordem_de_Servico_<id>.pdf`: PDF de cada OS.
- `documentos/gerados/pix_os_<id>.png`: imagem do QR Code usada no PDF.

Esses arquivos são dados da aplicação e devem ser incluídos em uma rotina de backup se o sistema for usado em produção. O banco não é remoto nem compartilhado entre computadores.

## Estrutura do projeto

```text
sistema_os(final)/
├── main.py                  # Inicializa o banco e abre a aplicação
├── config.py                # Credenciais legadas e configuração do Pix
├── requirements.txt         # Dependências Python
├── database/                # Conexão, tabelas e consultas SQLite
├── interface/               # Telas da aplicação Tkinter/ttkbootstrap
├── documentos/              # Geração e saída dos PDFs
├── pix/                     # Geração dos QR Codes Pix
└── imagens/                 # Logo, fundo e ícones da interface
```

## Solução de problemas

### `ModuleNotFoundError`

Confirme que o ambiente virtual está ativado e reinstale as dependências:

```bash
python -m pip install -r requirements.txt
```

### A janela não abre

Verifique se o Tkinter está instalado e se você está executando o programa em um ambiente com interface gráfica. Em servidores sem display, a aplicação desktop não poderá ser aberta diretamente.

### O Pix não aparece no PDF

Confira `PIX_NOME`, `PIX_CIDADE` e `PIX_CHAVE` em [config.py](sistema_os(final)/config.py) e verifique se a OS possui um valor maior que zero.

## Tecnologias

- Python
- Tkinter e ttkbootstrap
- SQLite
- Pillow
- fpdf2
- pybrcode

## Status do projeto

Projeto acadêmico em evolução, com foco no fluxo básico de atendimento de uma assistência técnica. Antes de disponibilizá-lo para uso real, revise autenticação, armazenamento de senhas, backup e permissões de acesso aos dados.