from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def obter_gastos():
    conn = sqlite3.connect('gastos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM gastos')
    gastos = c.fetchall()
    conn.close()
    return gastos

@app.route('/')
def index():
    gastos = obter_gastos()
    return render_template('index.html', gastos=gastos)

@app.route('/adicionar_gasto', methods=['POST'])
def adicionar_gasto():
    descricao = request.form.get('descricao')
    valor = float(request.form.get('valor'))

    conn = sqlite3.connect('gastos.db')
    c = conn.cursor()
    c.execute('INSERT INTO gastos (descricao, valor) VALUES (?, ?)', (descricao, valor))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/remover_gasto/<int:gasto_id>', methods=['GET', 'POST'])
def remover_gasto(gasto_id):
    conn = sqlite3.connect('gastos.db')
    c = conn.cursor()
    c.execute('DELETE FROM gastos WHERE id = ?', (gasto_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)