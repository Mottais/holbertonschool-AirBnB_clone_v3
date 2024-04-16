#!/usr/bin/python3
"""defines endpoints and their output """
from flask import Blueprint, jsonify


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', strict_slashes=False)
def get_status():
    """Créez une route /status qui renvoie un JSON
    avec la clé "status" et la valeur "OK"""
    return jsonify({"status": "OK"})
