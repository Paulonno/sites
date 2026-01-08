from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:201206@localhost:5432/agendamento_fotografia'
db = SQLAlchemy(app)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sucesso')
def sucesso():
    return render_template('/sucesso.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    data = request.form['data']
    horario = request.form['horario']

    existe = Agendamento.query.filter_by(
        data=data,
        horario=horario
    ).first()

    if existe:
        return "Horário já reservado!"

    novo = Agendamento(
        nome=request.form.get('nome'),
        telefone=request.form.get('telefone'),
        tipo=request.form.get('tipo'),
        data=data,
        horario=horario
    )

    db.session.add(novo)
    db.session.commit()

    return redirect('/sucesso')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route('/admin')
def admin():
    agendamentos = Agendamento.query.all()
    return render_template('admin.html', agendamentos=agendamentos)

with app.app_context():
    db.create_all()
