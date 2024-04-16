#!/usr/bin/python3
"""view for state"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get all states"""
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """return json of a state"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """deletes a state using id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state"""
    req = request.get_json()

    if req is None:
        abort(400, 'Not a JSON')
    if 'name' not in req:
        abort(400, 'Missing name')

    new_state = State(name=req['name'])
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')

    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()

    return jsonify(state.to_dict()), 200
