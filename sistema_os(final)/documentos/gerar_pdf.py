from database.ordens_servico import consultar_os_por_id
from fpdf import FPDF
from pathlib import Path

from pix.gerar_pix import gerar_qrcode_pix

RAIZ_PROJETO = Path(__file__).resolve().parents[1]

def gerar_pdf_os(id_os, usuario_id=None):
    ordens = consultar_os_por_id(id_os, usuario_id)

    if not ordens:
            raise ValueError("Ordem de serviço não encontrada.")

    ordem = ordens[0]
    if ordem[7] is None:
            valor_formatado = "Valor não definido"
    else:
            valor_formatado = f"R$ {ordem[7]:.2f}".replace(".", ",")

    diagnostico = ordem[9] or "Não informado"
    servico_realizado = ordem[10] or "Não informado"

    pdf = FPDF()
    
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    caminho_logo = RAIZ_PROJETO / "imagens" / "logo.png"
    pdf.image(str(caminho_logo), x=164, y=18, w=26)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, text="ASSISTÊNCIA TÉCNICA", ln=True)

    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, text="ORDEM DE SERVIÇO", ln=True)

    pdf.set_draw_color(220, 220, 220)
    pdf.line(pdf.l_margin, pdf.get_y() + 4, pdf.w - pdf.r_margin, pdf.get_y() + 4)
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, text=f"OS Nº {ordem[0]}", ln=True)

    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, text=f"Entrada: {ordem[8]}", ln=True)
    pdf.ln(8)

    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, text="CLIENTE E EQUIPAMENTO", ln=True)

    pdf.set_draw_color(225, 225, 225)
    pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
    pdf.ln(5)

    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, text=f"Cliente: {ordem[1]}", ln=True)
    pdf.cell(0, 7, text=f"Equipamento: {ordem[2]} - {ordem[3]} {ordem[4]}", ln=True)
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, text="DETALHES DO ATENDIMENTO", ln=True)

    pdf.set_draw_color(225, 225, 225)
    pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, text="Problema relatado", ln=True)

    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(30, 30, 30)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 7, text=ordem[5])
    pdf.ln(4)

    pdf.set_x(pdf.l_margin)
    pdf.cell(0, 7, text=f"Status: {ordem[6]}", ln=True)
    pdf.cell(0, 7, text=f"Valor: {valor_formatado}", ln=True)
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, text="ANÁLISE E SERVIÇO", ln=True)

    pdf.set_draw_color(225, 225, 225)
    pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, text="Diagnóstico", ln=True)

    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(30, 30, 30)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 7, text=diagnostico)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, text="Serviço realizado", ln=True)

    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(30, 30, 30)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 7, text=servico_realizado)

    pdf.ln(10)

    caminho_qrcode = gerar_qrcode_pix(
        valor=ordem[7],
        pix_id=f"OS{ordem[0]}",
        descricao=f"OS {ordem[0]}",
        nome_arquivo=f"pix_os_{ordem[0]}",
    )

    if pdf.get_y() > 210:
        pdf.add_page()

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, text="PAGAMENTO VIA PIX", ln=True)

    pdf.set_draw_color(225, 225, 225)
    pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
    pdf.ln(5)

    if caminho_qrcode:
        y_qrcode = pdf.get_y()
        pdf.image(caminho_qrcode, x=pdf.l_margin, y=y_qrcode, w=32)

        pdf.set_font("Helvetica", size=10)
        pdf.set_text_color(30, 30, 30)
        pdf.set_xy(pdf.l_margin + 38, y_qrcode + 2)
        pdf.multi_cell(
            0, 6,
            text=f"Escaneie o QR Code com o app do seu banco para pagar {valor_formatado} via Pix.",
        )

        pdf.set_xy(pdf.l_margin, y_qrcode + 36)
    else:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", size=10)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, text="Valor não definido: QR Code do Pix não gerado.", ln=True)

    pdf.ln(8)

    pdf.set_draw_color(225, 225, 225)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 5, text="Documento gerado pelo Sistema de Ordem de Serviço", align="C")
    pdf.cell(0, 5, text=f"OS Nº {ordem[0]}", align="C")

    pdf.set_y(pdf.h - pdf.b_margin - 18)
    pdf.set_draw_color(120, 120, 120)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 70, pdf.get_y())
    pdf.line(pdf.w - pdf.r_margin - 70, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())

    pdf.ln(3)
    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(100, 100, 100)

    pdf.cell(70, 5, text="Assinatura do cliente", align="C")
    pdf.cell(0, 5, text="Assinatura do técnico", align="R")

    pasta_saida = RAIZ_PROJETO / "documentos" / "gerados"
    pasta_saida.mkdir(parents=True, exist_ok=True)
    caminho_pdf = pasta_saida / f"Ordem_de_Servico_{ordem[0]}.pdf"

    pdf.output(str(caminho_pdf))
    print(f"PDF da Ordem de Serviço {ordem[0]} gerado com sucesso!") 
