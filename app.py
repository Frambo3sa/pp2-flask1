import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# Banco de dados
class Filme(db.Model):  # tabela
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    genero = db.Column(db.String(100), nullable=False)
    duracao = db.Column(db.Float, nullable=False)
    data_lancamento = db.Column(db.String(10), nullable=True)  # Mudar para String para simplificar
    diretor = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

# Rotas
@app.route('/', methods=["GET", "POST"])  # Inserir filmes e lista
def home():
    if request.method == "POST":
        try:
            filme = Filme(
                title=request.form.get("title"),
                genero=request.form.get("genero"),
                duracao=float(request.form.get("duracao")),  # Converter para float
                data_lancamento=request.form.get("data_lancamento"),
                diretor=request.form.get("diretor")
            )
            db.session.add(filme)
            db.session.commit()
        except Exception as e:
            print("Falha ao adicionar o Filme:", e)

    filmes = Filme.query.all()
    return render_template("index.html", filmes=filmes)

# Rota de alterar o filme
@app.route('/update', methods=["POST"])
def update():
    try:
        oldtitle = request.form.get("oldtitle")
        filme = Filme.query.filter_by(title=oldtitle).first()
        if filme:
            filme.title = request.form.get("newtitle", filme.title)
            filme.genero = request.form.get("newgenero", filme.genero)
            filme.duracao = float(request.form.get("newduracao", filme.duracao))  # Converter para float
            filme.data_lancamento = request.form.get("newdata", filme.data_lancamento)
            filme.diretor = request.form.get("newdiretor", filme.diretor)
            db.session.commit()
    except Exception as e:
        print("Não foi possível alterar o Filme:", e)
    return redirect("/")

# Deletar filme
@app.route('/delete', methods=["POST"])
def delete():
    title = request.form.get("title")
    filme = Filme.query.filter_by(title=title).first()
    if filme:
        db.session.delete(filme)
        db.session.commit()
    return redirect("/")

@app.route('/filmao', methods=["POST"])
def outrapag():
    return render_template("filmao.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)