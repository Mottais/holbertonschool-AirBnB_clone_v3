#!/usr/bin/python3
"""defines endpoints and their output """
from flask import Blueprint, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', strict_slashes=False)
def get_status():
    """Créez une route /status qui renvoie un JSON
    avec la clé "status" et la valeur "OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def count_objs():
    """count obj"""
    stats_dict = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(stats_dict)
