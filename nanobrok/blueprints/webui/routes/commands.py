from flask import abort, render_template, request, flash, session, url_for, redirect
from nanobrok.models import (
    Event,
    User,
    PacketData,
    PacketDataSchema,
    Audio,
    AudioSchema,
    PacketType,
    PermissionSchema,
    PermissionCheckShema,
    AudioTimeRecordSchema,
)
from nanobrok.ext.socketio import socketio
import threading, json
from dynaconf import settings
from nanobrok.ext.database import db
from nanobrok.blueprints.resources.resourceUtils import build_message_done
from nanobrok.blueprints.webui.utils import remove_key_from_dict
from ..utils import build_packet_data, checkUserIsAuthenticated
from flask_login import login_required
from marshmallow import ValidationError
from nanobrok.exceptions import (
    ValidationError as VE,
)
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


@login_required
def route_page_commands():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    records_audios = []
    if "records_audios" in session:
        records_audios = session["records_audios"]
    return render_template(
        "pages/commands/index.html", mobile_user=mobile_user, audios=records_audios
    )


@login_required
def route_commands_permision():

    permissionData = request.get_json(force=True)
    if not permissionData:
        raise VE(msg="There was an error in your request, please try again.", code=400)
    schema = PermissionCheckShema()

    try:
        permissionDataLoaded = schema.load(permissionData)
    except ValidationError as err:
        print(err.messages)
        raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

    ev = threading.Event()
    result = None
    result_permissionData = {"status": False}

    def callBackAckResponse(data):
        nonlocal result
        nonlocal ev

        result = data
        ev.set()

    send_packet = build_packet_data(
        Event.COMMAND_PERMISSION_CHECK_CODE,
        PacketType.SEND_PACKET_CODE,
        str({"permission": permissionDataLoaded["permission"]}),
    )

    db.session.add(send_packet)
    db.session.commit()

    print("sending to cleint: event -> " + Event.COMMAND_PERMISSION_CHECK_CODE.name)
    socketio.emit(
        Event.COMMAND_PERMISSION_CHECK_CODE.value,
        permissionDataLoaded,
        namespace=settings.ENDPOINT_IO_CORE,
        callback=callBackAckResponse,
    )
    ev.wait(timeout=5)

    if result != None:
        packet_data = json.loads(result)
        schema_packet = PacketDataSchema()
        schema_permission = PermissionSchema()
        try:
            result_packetData = schema_packet.load(
                remove_key_from_dict(packet_data, {"data"})
            )
            result_permissionData = schema_permission.load(packet_data.get("data"))
            packet = PacketData(**result_packetData)
            db.session.add(packet)
            db.session.commit()

        except Exception as err:
            print(err)

    return render_template(
        "pages/commands/permission_msg.html",
        timeout=True if result else False,
        has_permission=result_permissionData["status"],
    )


@login_required
def route_commands_record_audio():
    # test block event response callback from client
    ev = threading.Event()
    result = None
    records_audios = []

    recordData = request.get_json(force=True)
    if not recordData:
        raise VE(msg="There was an error in your request, please try again.", code=400)
    schema = AudioTimeRecordSchema()

    try:
        recordeDataLoad = schema.load(recordData)
    except ValidationError as err:
        print(err.messages)
        raise VE(msg=err.messages.get(list(err.messages)[0])[0], code=400)

    def callBackAckResponse(data):
        nonlocal result
        nonlocal ev

        result = data
        ev.set()

    if "records_audios" in session:
        records_audios = session["records_audios"]

    send_packet = build_packet_data(
        Event.GET_AUDIO_MIC_CODE,
        PacketType.SEND_PACKET_CODE,
        str({"seconds": recordeDataLoad["time_record"]}),
    )

    db.session.add(send_packet)
    db.session.commit()

    print("sending to cleint: event -> " + Event.GET_AUDIO_MIC_CODE.name)
    socketio.emit(
        Event.GET_AUDIO_MIC_CODE.value,
        {"seconds": recordeDataLoad["time_record"]},
        namespace=settings.ENDPOINT_IO_CORE,
        callback=callBackAckResponse,
    )
    ev.wait(timeout=recordeDataLoad["time_record"] + 5)

    if result != None:
        packet_data = json.loads(result)
        schema_packet = PacketDataSchema()
        schema_audio = AudioSchema()
        try:
            result_packetData = schema_packet.load(
                remove_key_from_dict(packet_data, {"data"})
            )
            result_audioData = schema_audio.load(packet_data.get("data"))
            audio = Audio(**result_audioData)
            records_audios.append(audio.serialize())
            print("schema Packet data dump: {}".format(result_packetData))
            packet = PacketData(**result_packetData)
            db.session.add(packet)
            db.session.commit()

        except Exception as err:
            print(err)
        # print("result from timeout: {}".format(json.loads(result)["data"] ))
    session["records_audios"] = records_audios
    return render_template("pages/commands/list_audios.html", audios=records_audios)
