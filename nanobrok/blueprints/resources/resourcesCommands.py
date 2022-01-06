from flask_restplus import Resource
from flask import request
from nanobrok.models import (
    PacketData,
    PacketType,
    PacketDataSchema,
    Event,
    SecCommandType,
    ClipboardSchema,
    MessageToastSchema,
    AlarmSchema,
    TimeLookSchema,
)
from nanobrok.exceptions import (
    ValidationError as VE,
)
from marshmallow import ValidationError
from nanobrok.blueprints.webui.utils import remove_key_from_dict, build_packet_data
from nanobrok.ext.restapi import ns_commands
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
    ns_commands.add_resource(LockNowResource, "/security/locknow")
    ns_commands.add_resource(
        MaxInactivityTimeLockResource, "/security/maxInactivityTimeLock"
    )
    ns_commands.add_resource(CheckIsEnableAdminResource, "/security/checkIsEnableAdmin")
    ns_commands.add_resource(AlarmResource, "/security/alarm")
    ns_commands.add_resource(MessageResource, "/misc/messageToast")
    ns_commands.add_resource(ClipBoardResource, "/misc/clipboard")
    print("ROUTERS Registed: CommandsController ")


class LockNowResource(Resource):
    @ns_commands.doc(responses={200: "commands has executed successfully."})
    @ns_commands.doc(responses={401: "User does not have permission to access"})
    @ns_commands.doc(
        responses={
            503: "Client unavailable, the client is not ready to handle the request"
        }
    )
    @token_required_admin
    def post(self, current_user):

        ev = threading.Event()
        packet_data = None

        def ackResponseLockNow(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()

        packet_data_request = build_packet_data(
            Event.COMMAND_SECURITY_CODE, PacketType.SEND_PACKET_CODE
        )
        db.session.add(packet_data_request)
        db.session.commit()
        print("sending: event packetdata")
        print("Event target => " + Event[packet_data_request.event].name)
        print("data send: {}".format(packet_data_request.serialize()))

        print("sending: event ")
        socketio.emit(
            Event.COMMAND_SECURITY_CODE.value,
            {
                "type": SecCommandType.SET_LOCK_NOW.value,
            },
            namespace=settings.ENDPOINT_IO_CORE,
            callback=ackResponseLockNow,
        )
        ev.wait(timeout=5)

        if packet_data != None:
            packet_data = json.loads(packet_data)
            print("data recv: {}".format(packet_data))
            schema_packet = PacketDataSchema()
            try:
                result_packetData = schema_packet.load(
                    remove_key_from_dict(packet_data, {"data"})
                )
                obj_packetdata = PacketData(**result_packetData)
                db.session.add(obj_packetdata)
                db.session.commit()
                message = packet_data["data"].get("message")
                return build_message_done(200, message, packet_data["data"])
            except Exception as err:
                print(err)
                raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        raise VE(
            msg="Client unavailable, the client is not ready to handle the request",
            code=503,
        )


class MaxInactivityTimeLockResource(Resource):
    @ns_commands.doc(responses={200: "commands has executed successfully."})
    @ns_commands.doc(responses={401: "User does not have permission to access"})
    @ns_commands.doc(
        responses={
            503: "Client unavailable, the client is not ready to handle the request"
        }
    )
    @token_required_admin
    def post(self, current_user):

        timeLookData = request.get_json(silent=True)
        if not timeLookData:
            raise VE(
                msg="There was an error in your request, please try again.", code=400
            )
        schema = TimeLookSchema()

        try:
            result_timeLookData = schema.load(timeLookData)
        except ValidationError as err:
            print(err.messages)
            raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        ev = threading.Event()
        packet_data = None

        def ackResponse(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()

        packet_data_request = build_packet_data(
            Event.COMMAND_SECURITY_CODE, PacketType.SEND_PACKET_CODE
        )
        db.session.add(packet_data_request)
        db.session.commit()
        print("sending: event packetdata")
        print("Event target => " + Event[packet_data_request.event].name)
        print("data send: {}".format(packet_data_request.serialize()))

        print("sending: event ")
        socketio.emit(
            Event.COMMAND_SECURITY_CODE.value,
            {
                "type": SecCommandType.SET_MAX_INACTIVITY_TIME.value,
                "timeMs": result_timeLookData["timeMs"] * 1000,
            },
            namespace=settings.ENDPOINT_IO_CORE,
            callback=ackResponse,
        )
        ev.wait(timeout=5)

        if packet_data != None:
            packet_data = json.loads(packet_data)
            print("data recv: {}".format(packet_data))
            schema_packet = PacketDataSchema()
            try:
                result_packetData = schema_packet.load(
                    remove_key_from_dict(packet_data, {"data"})
                )
                obj_packetdata = PacketData(**result_packetData)
                db.session.add(obj_packetdata)
                db.session.commit()
                message = packet_data["data"].get("message")
                return build_message_done(200, message, packet_data["data"])
            except Exception as err:
                print(err)
                raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        raise VE(
            msg="Client unavailable, the client is not ready to handle the request",
            code=503,
        )


class CheckIsEnableAdminResource(Resource):
    @ns_commands.doc(responses={200: "commands has executed successfully."})
    @ns_commands.doc(responses={401: "User does not have permission to access"})
    @ns_commands.doc(
        responses={
            503: "Client unavailable, the client is not ready to handle the request"
        }
    )
    @token_required_admin
    def post(self, current_user):

        ev = threading.Event()
        packet_data = None

        def ackResponse(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()

        packet_data_request = build_packet_data(
            Event.COMMAND_SECURITY_CODE, PacketType.SEND_PACKET_CODE
        )
        db.session.add(packet_data_request)
        db.session.commit()
        print("sending: event packetdata")
        print("Event target => " + Event[packet_data_request.event].name)
        print("data send: {}".format(packet_data_request.serialize()))

        print("sending: event ")
        socketio.emit(
            Event.COMMAND_SECURITY_CODE.value,
            {"type": SecCommandType.IS_DEVICE_ADMIN.value},
            namespace=settings.ENDPOINT_IO_CORE,
            callback=ackResponse,
        )
        ev.wait(timeout=5)

        if packet_data != None:
            packet_data = json.loads(packet_data)
            print("data recv: {}".format(packet_data))
            schema_packet = PacketDataSchema()
            try:
                result_packetData = schema_packet.load(
                    remove_key_from_dict(packet_data, {"data"})
                )
                obj_packetdata = PacketData(**result_packetData)
                db.session.add(obj_packetdata)
                db.session.commit()
                message = packet_data["data"].get("message")
                return build_message_done(200, message, packet_data["data"])
            except Exception as err:
                print(err)
                raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        raise VE(
            msg="Client unavailable, the client is not ready to handle the request",
            code=503,
        )


class MessageResource(Resource):
    @ns_commands.doc(responses={200: "Message has been sent successfully"})
    @ns_commands.doc(responses={401: "User does not have permission to access"})
    @ns_commands.doc(
        responses={400: "Bad Request, request syntax, invalid request message."}
    )
    @ns_commands.doc(
        responses={
            503: "Client unavailable, the client is not ready to handle the request"
        }
    )
    @token_required_admin
    def post(self, current_user):

        message_data = request.get_json(silent=True)
        if not message_data:
            raise VE(
                msg="There was an error in your request, please try again.", code=400
            )
        schema_message = MessageToastSchema()

        try:
            toast_message = schema_message.load(message_data)
        except ValidationError as err:
            print(err.messages)
            raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        ev = threading.Event()
        packet_data = None

        def ackResponse(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()

        packet_data_request = build_packet_data(
            Event.COMMAND_MISC_TOAST_CODE, PacketType.SEND_PACKET_CODE
        )
        db.session.add(packet_data_request)
        db.session.commit()
        print("sending: event packetdata")
        print("Event target => " + Event[packet_data_request.event].name)
        print("data send: {}".format(packet_data_request.serialize()))

        print("sending: event ")
        socketio.emit(
            Event.COMMAND_MISC_TOAST_CODE.value,
            toast_message,
            namespace=settings.ENDPOINT_IO_CORE,
            callback=ackResponse,
        )
        ev.wait(timeout=5)

        if packet_data != None:
            packet_data = json.loads(packet_data)
            print("data recv: {}".format(packet_data))
            schema_packet = PacketDataSchema()
            try:
                result_packetData = schema_packet.load(
                    remove_key_from_dict(packet_data, {"data"})
                )
                obj_packetdata = PacketData(**result_packetData)
                db.session.add(obj_packetdata)
                db.session.commit()
                message = packet_data["data"].get("message")
                return build_message_done(200, message, packet_data["data"])
            except Exception as err:
                print(err)
                raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        raise VE(
            msg="Client unavailable, the client is not ready to handle the request",
            code=503,
        )


class ClipBoardResource(Resource):
    @ns_commands.doc(responses={200: "Clipboard has been sent successfully"})
    @ns_commands.doc(responses={401: "User does not have permission to access"})
    @ns_commands.doc(
        responses={400: "Bad Request, request syntax, invalid request message."}
    )
    @ns_commands.doc(
        responses={
            503: "Client unavailable, the client is not ready to handle the request"
        }
    )
    def post(self, current_user=None):

        clipboard_data = request.get_json(silent=True)
        if not clipboard_data:
            raise VE(
                msg="There was an error in your request, please try again.", code=400
            )
        schema_clipboard = ClipboardSchema()

        try:
            result_clipboard = schema_clipboard.load(clipboard_data)
        except ValidationError as err:
            print(err.messages)
            raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        ev = threading.Event()
        packet_data = None

        def ackResponse(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()

        packet_data_request = build_packet_data(
            Event.CLIPBOARD_CODE, PacketType.SEND_PACKET_CODE
        )
        db.session.add(packet_data_request)
        db.session.commit()
        print("sending: event packetdata")
        print("Event target => " + Event[packet_data_request.event].name)
        print("data send: {}".format(packet_data_request.serialize()))

        print("sending: event ")
        socketio.emit(
            Event.CLIPBOARD_CODE.value,
            result_clipboard,
            namespace=settings.ENDPOINT_IO_CORE,
            callback=ackResponse,
        )
        ev.wait(timeout=5)

        if packet_data != None:
            packet_data = json.loads(packet_data)
            print("data recv: {}".format(packet_data))
            schema_packet = PacketDataSchema()
            try:
                result_packetData = schema_packet.load(
                    remove_key_from_dict(packet_data, {"data"})
                )
                obj_packetdata = PacketData(**result_packetData)
                db.session.add(obj_packetdata)
                db.session.commit()
                message = packet_data["data"].get("message")
                return build_message_done(200, message, packet_data["data"])
            except Exception as err:
                print(err)
                raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        raise VE(
            msg="Client unavailable, the client is not ready to handle the request",
            code=503,
        )


class AlarmResource(Resource):
    @ns_commands.doc(responses={200: "Alarm has been sent successfully"})
    @ns_commands.doc(responses={401: "User does not have permission to access"})
    @ns_commands.doc(
        responses={400: "Bad Request, request syntax, invalid request message."}
    )
    @ns_commands.doc(
        responses={
            503: "Client unavailable, the client is not ready to handle the request"
        }
    )
    @token_required_admin
    def post(self, current_user):

        message_data = request.get_json(silent=True)
        if not message_data:
            raise VE(
                msg="There was an error in your request, please try again.", code=400
            )
        schema_alarm = AlarmSchema()

        try:
            alarm_data = schema_alarm.load(message_data)
        except ValidationError as err:
            print(err.messages)
            raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        ev = threading.Event()
        packet_data = None

        def ackResponse(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()

        packet_data_request = build_packet_data(
            Event.COMMAND_SECURITY_ALARM_CODE, PacketType.SEND_PACKET_CODE
        )
        db.session.add(packet_data_request)
        db.session.commit()
        print("sending: event packetdata")
        print("Event target => " + Event[packet_data_request.event].name)
        print("data send: {}".format(packet_data_request.serialize()))

        print("sending: event ")
        socketio.emit(
            Event.COMMAND_SECURITY_ALARM_CODE.value,
            alarm_data,
            namespace=settings.ENDPOINT_IO_CORE,
            callback=ackResponse,
        )
        ev.wait(timeout=5)

        if packet_data != None:
            packet_data = json.loads(packet_data)
            print("data recv: {}".format(packet_data))
            schema_packet = PacketDataSchema()
            try:
                result_packetData = schema_packet.load(
                    remove_key_from_dict(packet_data, {"data"})
                )
                obj_packetdata = PacketData(**result_packetData)
                db.session.add(obj_packetdata)
                db.session.commit()
                message = packet_data["data"].get("message")
                return build_message_done(200, message, packet_data["data"])
            except Exception as err:
                print(err)
                raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

        raise VE(
            msg="Client unavailable, the client is not ready to handle the request",
            code=503,
        )
