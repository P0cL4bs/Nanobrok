import datetime
import uuid
from functools import wraps

import jwt
from dynaconf import settings
from flask import request, session
from flask_restplus import Resource
from werkzeug.security import check_password_hash
from nanobrok.models import User, UserAdm
from nanobrok.exceptions import (
    ValidationError as VE,
)

from nanobrok.ext.restapi import ns_auth
from .resourceUtils import build_message_done
from dynaconf import settings

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
    ns_auth.add_resource(AuthenticateResource, "")
    print("ROUTERS Registed: AuthController ")


def generateTokenJwt(user):
    if user:
        token = jwt.encode(
            {
                "public_id": user.public_id,
                # "exp": datetime.datetime.utcnow() + datetime.timedelta(days=settings.SESSION_LIFETIME),
            },
            settings.SECRET_KEY,
        )
        return token.decode("UTF-8")
    return None


def token_required_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # get token from session web manager
        token = session.get("token")

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            raise VE(msg="Token is missing", code=400)

        try:
            data = jwt.decode(token, settings.SECRET_KEY)
            current_user = UserAdm.query.filter_by(public_id=data["public_id"]).first()
        except Exception as e:
            print(e)
            raise VE(msg="Invalid token", code=400)

        return f(current_user, *args, **kwargs)

    return decorated


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            raise VE(msg="Token is missing", code=400)

        try:
            data = jwt.decode(token, settings.SECRET_KEY)
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            raise VE(msg="Invalid token", code=400)

        return f(current_user, *args, **kwargs)

    return decorated


class AuthenticateResource(Resource):
    @ns_auth.doc(responses={200: "Token successfully generated"})
    @ns_auth.doc(responses={401: "Basic realm=Login required!"})
    def get(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            raise VE(msg="Basic realm=Login required!", code=401)

        user = UserAdm.query.filter_by(username=auth.username).first()

        if not user:
            raise VE(msg="Basic realm=Login required!", code=401)

        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {
                    "public_id": user.public_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=300),
                },
                settings.SECRET_KEY,
            )

            return build_message_done(
                200, "Token successfully generated", token.decode("UTF-8")
            )

        raise VE(msg="Basic realm=Login required!", code=401)
