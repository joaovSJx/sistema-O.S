from pathlib import Path

from database.banco import criar_tabela, criar_tabela_equipamentos, criar_tabela_os
from database.clientes import cadastrar_cliente
from database.connection import conectar
from database.ordens_servico import cadastrar_equipamento, cadastrar_os
from documentos.gerar_pdf import gerar_pdf_os


def testar_geracao_pdf():
    """Cria uma OS de teste, gera o PDF e remove os registros temporários."""
    criar_tabela()
    criar_tabela_equipamentos()
    criar_tabela_os()

    cpf_teste = "99999999999"
    cliente_id = cadastrar_cliente(
        "Cliente Teste PDF",
        cpf_teste,
        "31999999999",
        "teste.pdf@example.com",
        "Rua de Teste, 100",
    )
    equipamento_id = cadastrar_equipamento(
        cliente_id,
        "Notebook",
        "Dell",
        "Inspiron",
        "PDF-TESTE-001",
        "Equipamento criado para teste de PDF",
    )
    os_id = cadastrar_os(
        cliente_id,
        equipamento_id,
        "Tela não liga",
        150.00,
        "2026-09-16",
    )

    conexao = conectar()
    conexao.execute(
        """
        UPDATE ordens_servico
        SET diagnostico = ?, servico_realizado = ?
        WHERE id = ?
        """,
        ("Fonte com defeito", "Substituição da fonte", os_id),
    )
    conexao.commit()
    conexao.close()

    try:
        gerar_pdf_os(os_id)
        caminho_pdf = Path("documentos") / "gerados" / f"Ordem_de_Servico_{os_id}.pdf"
        assert caminho_pdf.is_file(), f"PDF não foi criado: {caminho_pdf}"
        assert caminho_pdf.stat().st_size > 0, "PDF criado está vazio"
        print(f"Teste de geração de PDF aprovado: {caminho_pdf}")
    finally:
        conexao = conectar()
        conexao.execute("DELETE FROM ordens_servico WHERE id = ?", (os_id,))
        conexao.execute("DELETE FROM equipamentos WHERE id = ?", (equipamento_id,))
        conexao.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conexao.commit()
        conexao.close()


if __name__ == "__main__":
    testar_geracao_pdf()