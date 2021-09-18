from flask_restplus import Resource
from flask import request
from nanobrok.models import PacketData, PacketType, PacketDataSchema, Event
from nanobrok.exceptions import (
    ValidationError as VE,
)
from nanobrok.blueprints.webui.utils import remove_key_from_dict, build_packet_data
from nanobrok.ext.restapi import ns_transfer
from .resourceUtils import build_message_done
from nanobrok.ext.socketio import socketio
import threading, json
from nanobrok.ext.database import db
from .resourcesAuth import token_required_admin
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
    ns_transfer.add_resource(ConnectionResource, "/ping")
    print("ROUTERS Registed: TransferController ")


class ConnectionResource(Resource):
    @ns_transfer.doc(responses={200: "The android device is connected."})
    @ns_transfer.doc(responses={401: "User does not have permission to access"})
    @ns_transfer.doc(
        responses={400: "Bad Request, request syntax, invalid request message."}
    )
    @ns_transfer.doc(responses={503: "The device connection not found."})
    @token_required_admin
    def get(self, current_user):
        packet_data = None
        ev = threading.Event()

        def ackResponse(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()

        print("sending: event ")
        socketio.emit(
            Event.PING_PONG_CODE.value,
            {"ping": ""},
            namespace=settings.ENDPOINT_IO_TRANSFER,
            callback=ackResponse,
        )
        ev.wait(timeout=5)

        if packet_data != None:
            return build_message_done(200, "The android device is connected.", "")

        raise VE(msg="The device connection not found.", code=503)
