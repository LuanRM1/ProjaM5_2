from flask import Flask, render_template, request
from datetime import datetime
from tinydb import TinyDB, Query
import requests

# Cria a instância do Flask no App
app = Flask(__name__)

# Inicializa o banco de dados TinyDB
db = TinyDB("db.json")


def insert_data():
    db.insert(
        {
            "endereco": request.environ.get("REMOTE_ADDR", "N/A"),
            "metodo": request.method,
            "hora": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # Formata a data e hora para string
        }
    )


@app.route("/echo", methods=["POST"])
def echo():
    message = request.json
    insert_data()
    return {"resposta": message["dados"]}


@app.route("/ping")
def ping():
    insert_data()
    return {"resposta": "pong"}


@app.route("/info")
def info():
    itens = db.all()
    print("passo aki")
    return itens


@app.route("/dash")
def retorna_acessos():

    itens = requests.get("http://localhost:8000/info").json()
    page = render_template("item-log.html", itens=itens)
    print(page)

    return page


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
