import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Conexão com o banco de dados
def init_db():
    conn = sqlite3.connect('oficina.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            fabricante TEXT NOT NULL,
            data_aquisicao DATE NOT NULL,
            status_manutencao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para atualizar o arquivo de equipamentos
def atualizar_arquivo():
    conn = sqlite3.connect('oficina.db')
    c = conn.cursor()
    c.execute("SELECT * FROM equipamentos ORDER BY nome, data_aquisicao")
    equipamentos = c.fetchall()
    conn.close()

    with open('arquivos/equipamentos.txt', 'w') as f:
        for equipamento in equipamentos:
            f.write(f"Nome: {equipamento[1]}, Tipo: {equipamento[2]}, Fabricante: {equipamento[3]}, Data de Aquisição: {equipamento[4]}, Status de Manutenção: {equipamento[5]}\n")


@app.route('/')
def cadastro():
    return render_template('cadastro.html')

@app.route('/add', methods=['POST'])
def add():
    nome = request.form['nome']
    tipo = request.form['tipo']
    fabricante = request.form['fabricante']
    data_aquisicao = request.form['data_aquisicao']
    status_manutencao = request.form['status_manutencao']

    conn = sqlite3.connect('oficina.db')
    c = conn.cursor()
    c.execute("INSERT INTO equipamentos (nome, tipo, fabricante, data_aquisicao, status_manutencao) VALUES (?, ?, ?, ?, ?)",
              (nome, tipo, fabricante, data_aquisicao, status_manutencao))
    conn.commit()
    conn.close()

    # Atualiza o arquivo de equipamentos
    atualizar_arquivo()

    return redirect('/consulta')

# Rota para excluir um equipamento pelo ID
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect('oficina.db')
    c = conn.cursor()
    c.execute("DELETE FROM equipamentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    # Atualiza o arquivo de equipamentos
    atualizar_arquivo()

    return redirect('/consulta')

@app.route('/consulta')
def consulta():
    conn = sqlite3.connect('oficina.db')
    c = conn.cursor()
    c.execute("SELECT * FROM equipamentos ORDER BY nome, data_aquisicao")
    equipamentos = c.fetchall()
    conn.close()
    return render_template('consulta.html', equipamentos=equipamentos)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
