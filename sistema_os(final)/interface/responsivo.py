def centralizar_canvas(canvas, frame, largura, altura):
    """Centraliza um Canvas de medidas-base sem escalar nem distorcer seus itens."""
    estado = {"x": 0, "y": 0}

    def reposicionar(_evento=None):
        x = max(0, (canvas.winfo_width() - largura) // 2)
        y = max(0, (canvas.winfo_height() - altura) // 2)
        canvas.move("all", x - estado["x"], y - estado["y"])
        estado["x"], estado["y"] = x, y

    canvas.bind("<Configure>", reposicionar)
    frame.after_idle(reposicionar)
