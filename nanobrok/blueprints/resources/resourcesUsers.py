from flask import request
from flask_restplus import Resource

from nanobrok.ext.database import db
from nanobrok.models import User, UserSchema
from marshmallow import ValidationError
from nanobrok.exceptions import (
    ValidationError as VE,
)

from nanobrok.ext.restapi import ns_user
from .resourcesAuth import token_required_admin
from .resourceUtils import build_message_done
from nanobrok.ext.socketio import remove_key_from_dict

# This file is part of the Nanobrok Open Source Project.
# nanobrok is licensed under the Apache 2.0.

# Copyright 2021 p0cL4bs Team - Marcos Bomfim (mh4x0f)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def register_routes(app):
    ns_user.add_resource(UserResource, "")
    print("ROUTERS Registed: UsesController ")


class UserResource(Resource):
    @ns_user.doc(
        responses={400: "There was an error in your request, please try again."}
    )
    @ns_user.doc(responses={200: "User registered successfully."})
    @token_required_admin
    def post(self, args):
        user_data = request.get_json(silent=True)
        if not user_data:
            raise VE(
                msg="There was an error in your request, please try again.", code=400
            )
        schema = UserSchema()

        try:
            result_userData = schema.load(user_data)
        except ValidationError as err:
            print(err.messages)
            raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        mobile_user = User.query.one()
        User.query.filter_by(public_id=mobile_user.public_id).update(
            remove_key_from_dict(result_userData, {"deviceInfo"})
        )
        db.session.commit()

        return build_message_done(
            200, "User registered successfully.", mobile_user.serialize()
        )


# - CRUD list:
#   GET /users/<id_usuario> @token_required
# class UserItemResource(Resource):
#     @ns_user.doc(responses={200: "User successfully listed."})
#     @ns_user.doc(responses={401: "User does not have permission to access"})
#     @token_required_admin
#     def get(self, current_user, id_user):
#         user = User.query.filter_by(id=id_user).first()

#         return build_message_done(200, "User successfully listed.", user.serialize())
