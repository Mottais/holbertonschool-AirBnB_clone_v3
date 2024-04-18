#!/usr/bin/python3
"""State API views"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retourne la liste de tous les objets State format to_dict()"""
    All_Objs_States = storage.all(State).values()
    if All_Objs_States is None:
        abort(404)

    StatesDict = []
    for Obj_state in All_Objs_States:
        StatesDict.append(Obj_state.to_dict())
    return jsonify(StatesDict)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retourne l'objet State de l'id spécifié au format to_dict()"""
    """commande shell :"""
    """curl -X GET http://0.0.0.0:5000/api/v1/states/8f165686-c98...e2d99 ou"""
    """curl -X GET http://127.0.0.1:5000/api/v1/states/8f165686-c98...e2d99"""
    """ou dans un navigateur :"""
    """http://127.0.0.1:5000/api/v1/states/8f165686-c98...e2d99"""

    Obj_state = storage.get(State, state_id)
    if Obj_state is None:
        abort(404)
    return jsonify(Obj_state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Retourne l'objet State de l'id spécifié format to_dict()"""
    # commande shell :
    # curl -X GET http://0.0.0.0:5000/api/v1/states/8f165686-c98...e2d99 ou
    # curl -X GET http://127.0.0.1:5000/api/v1/states/8f165686-c98...e2d99
    # (NB: la méthode [GET] est appliquée par défaut dans un navigateur)
    state_delete = storage.get(State, state_id)
    if state_delete is None:
        abort(404)
    storage.delete(state_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Créé un nouvel objet State"""
    # exemple commande shell : curl -X POST http://0.0.0.0:5000/api/v1/state
    # s/ -H "Content-Type: application/json" -d '{"name": "California"}'

    # Récupère le contenu de la requête --> {"name": "California"}
    try:
        data = request.get_json()

        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400

        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Modifie l'objet State de l'id spécifié"""
    # exemple commande shell : curl -X PUT http://0.0.0.0:5000/api/v1/state
    # s/feadaa73-9e4b-4514-905b-8253f36b46f6 -H "Content-Type: application/js
    # on" -d '{"name": "California is so cool"}'
    Obj_state = storage.get(State, state_id)
    if Obj_state is None:
        abort(404)

    try:
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(Obj_state, key, value)

        storage.save()
        return jsonify(Obj_state.to_dict()), 200

    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response
