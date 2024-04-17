#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """Cré une route pour gérer les erreurs 404"""
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def close_storage(exception):
    """Ferme la connexion à la base de données après chaque requête."""
    storage.close()


if __name__ == "__main__":
    """Récupére les valeurs des variables d'environnement
    ou utilise des valeurs par défaut"""
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    """Lancez l'application Flask"""
    app.run(host=host, port=port, threaded=True)
