#!/usr/bin/python3
"""view for user"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get all users"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """return json of a user"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """deletes a user using id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a new user"""

    try:
        req = request.get_json()
        if 'email' not in req:
            abort(400, 'Missing email')
        if 'password' not in req:
            abort(400, 'Missing password')

        email = req['email']
        password = req['password']

        new_user = User(email=email, password=password)
        new_user.save()

        return jsonify(new_user.to_dict()), 201

    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    try:
        req = request.get_json()

        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)

        user.save()

        return jsonify(user.to_dict()), 200

    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response
