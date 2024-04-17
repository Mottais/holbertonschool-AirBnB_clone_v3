#!/usr/bin/python3
"""import thing here to avoid circular import"""
from flask import Blueprint


app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

if True:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.amenities import *
    from api.v1.views.cities import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.users import *
