from flask_restplus import Resource
from nanobrok.models import (
    LocationSchema,
    Location,
    PacketData,
    PacketType,
    PacketDataSchema,
    Event,
)
from nanobrok.exceptions import (
    ValidationError as VE,
)
from nanobrok.blueprints.webui.utils import remove_key_from_dict, build_packet_data
from nanobrok.ext.restapi import ns_location
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
    ns_location.add_resource(LocationResource, "")
    print("ROUTERS Registed: LocationController ")


class LocationResource(Resource):
    @ns_location.doc(responses={200: "Location successfully."})
    @ns_location.doc(responses={401: "User does not have permission to access"})
    @ns_location.doc(
        responses={400: "Bad Request, request syntax, invalid request message."}
    )
    @ns_location.doc(
        responses={
            503: "Client unavailable, the client is not ready to handle the request"
        }
    )
    @token_required_admin
    def post(self, current_user):

        ev = threading.Event()
        packet_data = None

        def ackResponseLocation(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()

        packet_data_request = build_packet_data(
            Event.GET_GEOLOCATION, PacketType.SEND_PACKET_CODE
        )
        db.session.add(packet_data_request)
        db.session.commit()
        print("sending: event packetdata")
        print("Event target => " + Event[packet_data_request.event].name)
        print("data send: {}".format(packet_data_request.serialize()))

        print("sending: event ")
        socketio.emit(
            Event[packet_data_request.event].value,
            {"data": "packet geolocation"},
            namespace=settings.ENDPOINT_IO_CORE,
            callback=ackResponseLocation,
        )
        ev.wait(timeout=10.0)
        if packet_data != None:
            packet_data = json.loads(packet_data)
            print("data recv: {}".format(packet_data))
            schema_packet = PacketDataSchema()
            schema_location = LocationSchema()
            try:
                result_packetData = schema_packet.load(
                    remove_key_from_dict(packet_data, {"data"})
                )
                result_location = schema_location.load(packet_data.get("data"))
                obj_packetdata = PacketData(**result_packetData)
                obj_location = Location(**result_location)
                db.session.add(obj_packetdata)
                if obj_location.latitude != None:
                    db.session.add(obj_location)
                db.session.commit()
            except Exception as err:
                print(err)
                raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)
            return build_message_done(
                200, "User successfully listed.", obj_location.serialize()
            )

        raise VE(
            msg="Client unavailable, the client is not ready to handle the request",
            code=503,
        )
