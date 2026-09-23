from pathlib import Path

from pybrcode.pix import generate_simple_pix

from config import PIX_CHAVE, PIX_CIDADE, PIX_NOME

RAIZ_PROJETO = Path(__file__).resolve().parents[1]

def gerar_qrcode_pix(valor, pix_id=None, descricao=None,
                      pasta=None, nome_arquivo="pix_qrcode"):

    if valor is None:
        return None

    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return None

    if valor <= 0:
        return None

    if pix_id:
        pix_id = str(pix_id)[:25]

    chave_pix = PIX_CHAVE
    if chave_pix.isdigit() and len(chave_pix) == 11:
        chave_pix = f"({chave_pix[:2]}) {chave_pix[2:7]}-{chave_pix[7:]}"

    pix = generate_simple_pix(
        fullname=PIX_NOME,
        key=chave_pix,
        city=PIX_CIDADE,
        value=valor,
        pix_id=pix_id,
        description=descricao,
        mult_transaction=False,
    )

    pasta_saida = Path(pasta) if pasta else RAIZ_PROJETO / "documentos" / "gerados"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    pix.imageToPath(str(pasta_saida), filename=nome_arquivo)
    caminho_png = pasta_saida / f"{nome_arquivo}.png"

    return str(caminho_png)
