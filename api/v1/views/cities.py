#!/usr/bin/python3
"""State API views"""
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_states(state_id):
    """Retourne les objets City associés à un d'id State passé en paramètre"""
    # Retourne l'objet State de l'id spécifié
    states_get = storage.get(State, state_id)
    if states_get is None:
        abort(404)
    cities_dict = []
    for city_get in states_get.cities:
        cities_dict.append(city_get.to_dict())
    return jsonify(cities_dict)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retourne l'objet City de l'id spécifié au format to_dict()"""
    city_get = storage.get(City, city_id)
    if city_get is None:
        abort(404)
    return jsonify(city_get.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Supprime l'objet City de l'id spécifié format to_dict()"""
    city_delete = storage.get(City, city_id)
    if city_delete is None:
        abort(404)
    storage.delete(city_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new City object"""
    # Retourne l'objet State de l'id spécifié sinon quitte fonction (err404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    # Récupère le contenu JSON de la requête --> ex : {"name": "Alexandria"}
    try:
        data = request.get_json()
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400

        data['state_id'] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201

    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Modifie l'objet City de l'id spécifié"""
    city_get = storage.get(City, city_id)
    if city_get is None:
        abort(404)

    try:
        data = request.get_json()

        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city_get, key, value)

        storage.save()
        return jsonify(city_get.to_dict()), 200

    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response
