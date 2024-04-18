#!/usr/bin/python3
"""view for place"""
from models.city import City
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """get all places"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """return json of a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """deletes a place using id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a new place"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        req = request.get_json()

        if 'user_id' not in req:
            response = jsonify({"message": "Missing user_id"})
            response.status_code = 400
            return response
        user_id = req['user_id']
        user = storage.get(User, user_id)
        if not user:
            return jsonify(error="Not found"), 404

        if 'name' not in req:
            response = jsonify({"message": "Missing name"})
            response.status_code = 400
            return response
        name = req['name']

        new_place = Place(name=name, user_id=user_id, city_id=city_id)
        new_place.save()
        return jsonify(new_place.to_dict()), 201

    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    try:
        req = request.get_json()

        for key, value in req.items():
            if key not in ['id', 'user_id', 'created_at', 'updated_at']:
                setattr(place, key, value)

        place.save()

        return jsonify(place.to_dict()), 200

    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response
