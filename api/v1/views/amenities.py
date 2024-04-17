#!/usr/bin/python3
"""view for amenities"""
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """Retrieves the list of all Amenities objects"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """get an amenity"""

    fetched_obj = storage.get(Amenity, amenity_id)

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):

    fetched_obj = storage.get(Amenity, str(amenity_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """creates an amenity"""

    am_json = request.get_json(silent=True)

    if am_json is None:
        abort(400, 'Not a JSON')
    if "name" not in am_json:
        abort(400, 'Missing name')

    name = am_json['name']
    new_am = Amenity(name=name)
    new_am.save()

    return jsonify(new_am.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    am_json = request.get_json(silent=True)
    if am_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get(Amenity, str(amenity_id))
    if fetched_obj is None:
        abort(404)
    for key, val in am_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict()), 200
