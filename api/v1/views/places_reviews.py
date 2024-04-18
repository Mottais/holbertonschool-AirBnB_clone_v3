#!/usr/bin/python3
"""view for review"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """get all reviews"""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """return json of a review"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """deletes a review using id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a new review"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)


    try:
        req = request.get_json()
        if 'user_id' not in req:
            abort(400, 'Missing user_id')
        if 'text' not in req:
            abort(400, 'Missing text')

        text = req['text']
        user_id = req['user_id']
        user = storage.get(User, user_id)

        if not user:
            abort(404)

        new_review = Review(text=text, user_id=user_id)
        new_review.save()

        return jsonify(new_review.to_dict()), 201
    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    try:
        req = request.get_json()

        for key, value in req.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                        'updated_at']:
                setattr(review, key, value)

        review.save()

        return jsonify(review.to_dict()), 200
    except Exception:
        response = jsonify({"message": "Not a JSON"})
        response.status_code = 400
        return response
