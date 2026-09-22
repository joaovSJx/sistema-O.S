import sqlite3

def conectar():
    conexao = sqlite3.connect('assistencia.db')
    conexao.execute("pragma foreign_keys = on") #fiscaliza as chaves estrangeiras
    return conexao