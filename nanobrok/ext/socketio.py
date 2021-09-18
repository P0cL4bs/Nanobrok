from flask_socketio import SocketIO, emit, Namespace, disconnect
from flask import request
from dynaconf import settings
import functools
from nanobrok.models import (
    DeviceInfo,
    User,
    UserSchemaSocketIO,
    WifiInfo,
    WifiInfoSchema,
    _get_date,
)
from nanobrok.ext.database import db
from nanobrok.exceptions import ValidationError
import json, jwt
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

socketio = None
socketio_transfer = None

# sio = socketio.Server(async_mode='threading')
def remove_key_from_dict(d, keys):
    return {k: v for k, v in d.items() if k not in keys}


def authenticated_only_socketio(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if len(args) == 0 or not request.args.get("token"):
            disconnect()
            return
        token_encoded = request.args.get("token")
        try:
            data = jwt.decode(token_encoded, settings.SECRET_KEY)
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            disconnect()
            return

        return f(*args, current_user, **kwargs)

    return wrapped


class NamespaceCore(Namespace):
    @authenticated_only_socketio
    def on_connect(self, current_user):
        print("client connected! ")
        current_user = User.query.filter_by(public_id=current_user.public_id).first()
        current_user.is_connected = True
        current_user.lest_sync = _get_date()
        db.session.commit()

    @authenticated_only_socketio
    def on_disconnect(self, current_user):
        print("client disconnected!")
        current_user = User.query.filter_by(public_id=current_user.public_id).first()
        current_user.lest_seen = _get_date()
        current_user.is_connected = False
        db.session.commit()

    @authenticated_only_socketio
    def on_ping(self, user_data, current_user):
        print("currentuser: " + str(current_user))
        print("data on_ping -> {}".format(user_data))
        socketio.emit("pong", {"data": "pong"}, namespace=settings.ENDPOINT_IO_CORE)

    @authenticated_only_socketio
    def on_join(self, user_data, current_user):
        print("join: currentuser: " + str(current_user))

        schema_user = UserSchemaSocketIO()
        schema_wifi = WifiInfoSchema()
        try:
            result_user = schema_user.load(json.loads(user_data)["user"])
            result_wifiInfo = schema_wifi.load(json.loads(user_data)["wifiInfo"])
        except ValidationError as err:
            print(err.messages)
            disconnect()
            return

        User.query.filter_by(public_id=current_user.public_id).update(
            remove_key_from_dict(result_user, {"deviceInfo"})
        )
        DeviceInfo.query.filter_by(id=current_user.deviceInfo.id).update(
            result_user.get("deviceInfo")
        )

        wifiInfo = WifiInfo(**result_wifiInfo)
        db.session.add(wifiInfo)
        db.session.commit()
        print("join: done")


class NamespaceTransfer(Namespace):
    @authenticated_only_socketio
    def on_connect(self, current_user):
        print("NamespaceTransfer: client connected! ")
        current_user = User.query.filter_by(public_id=current_user.public_id).first()
        current_user.is_connected = True
        db.session.commit()

    @authenticated_only_socketio
    def on_disconnect(self, current_user):
        print("NamespaceTransfer: client disconnected!")
        current_user = User.query.filter_by(public_id=current_user.public_id).first()
        current_user.is_connected = False
        db.session.commit()


def init_app(app):
    global socketio
    # socketio = SocketIO(app,engineio_logger=True)
    socketio = SocketIO(
        app,
        engineio_logger=settings.ENGINEIO_LOGGER,
        ping_interval=120,
        ping_timeout=120,
    )
    # register NameSpace socketio
    socketio.on_namespace(NamespaceCore(settings.ENDPOINT_IO_CORE))
    socketio.on_namespace(NamespaceTransfer(settings.ENDPOINT_IO_TRANSFER))
