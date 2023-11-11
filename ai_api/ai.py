from flask import Flask, jsonify, request
from flask_cors import CORS
from models.nova_ai import NovaAI
from constants.constants import HOST, PORT

ARG_TITLE = "title"
GET = "GET"
POST = "POST"
RELATED_BOOKS_END_POINT = "/ai/query/related-books"

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    """
    Rota principal para verificar o status da API.
    :return: Um JSON indicando que a API está online e o status da solicitação.
    """
    return jsonify({
            "message": "API online",
            "status": 200
        }), 200


@app.route(f"{RELATED_BOOKS_END_POINT}/<title>")
def related_books(title):
    """
    Rota para obter livros relacionados a um título específico.
    :param title: O título para o qual se deseja obter livros relacionados.
    :return: Um JSON contendo o título, os livros relacionados e o status da solicitação.
    """
    if title.strip():
        result = NovaAI.related_books_query(title)
        return jsonify({
            "title": title,
            "related": result,
            "status": 200
        }), 200
    else:
        return jsonify({
            "status": 400
        }), 400
    

@app.route(RELATED_BOOKS_END_POINT, methods = [GET, POST])
def related_books_get_and_post():
    """
    Rota para obter livros relacionados com base nos parâmetros da solicitação.
    :return: Um JSON contendo o título, os livros relacionados e o status da solicitação.
    """
    try:
        title = request.form[ARG_TITLE] if request.method == POST else request.args.get(ARG_TITLE)
        if title.strip():
            result = NovaAI.related_books_query(title)
            return jsonify({
                "title": title,
                "related": result,
                "status": 200
            }), 200
    except:
        pass
    return jsonify({
        "status": 400
    }), 400


def run_api() -> None:
    """
    Inicia o servidor da API.
    :return: None
    """
    app.run(host = HOST, port = PORT, debug = True)


if __name__ == "__main__":
    run_api()