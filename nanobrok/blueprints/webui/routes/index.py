from flask import abort, render_template, request, flash, redirect, url_for
from nanobrok.models import *
from wtforms import Form, StringField, validators
from nanobrok.ext.socketio import socketio
from marshmallow import ValidationError
import threading, json
from dynaconf import settings
from nanobrok.ext.database import db
from ..utils import build_packet_data, checkUserIsAuthenticated
from nanobrok.blueprints.resources.resourceUtils import build_api_response
from nanobrok.blueprints.webui.utils import remove_key_from_dict
from flask_login import login_required, current_user
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


class Form(Form):
    username = StringField("Udsa", [validators.Length(min=4, max=25)])


@login_required
def route_header_sidebar():

    ev = threading.Event()
    result_ping = None
    isOnline = False

    def ping_response(data):
        nonlocal result_ping, isOnline
        nonlocal ev
        result_ping = data
        isOnline = True
        ev.set()

    socketio.emit(
        Event.PING_PONG_CODE.value,
        namespace=settings.ENDPOINT_IO_CORE,
        callback=ping_response,
    )
    ev.wait(timeout=5)
    mobile_user = User.query.one_or_none()
    if mobile_user:
        mobile_user.is_connected = isOnline
        db.session.commit()

    return render_template("/default/header_sidebar.html", mobile_user=mobile_user)


@login_required
def index():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))

    wifiInfo_last = WifiInfo.query.order_by(WifiInfo.id.desc()).first()
    locations = Location.query.order_by(Location.id.desc()).paginate(
        per_page=3, error_out=False
    )
    allPacketData = PacketData.query.order_by(PacketData.id.desc()).paginate(
        per_page=3, error_out=False
    )

    return render_template(
        "index.html",
        mobile_user=mobile_user,
        wifiInfo=wifiInfo_last,
        allPacketData=allPacketData,
        locations=locations,
    )


@login_required
def updateDashboard():

    ev = threading.Event()
    recv_data = None

    def callbackResponseCommand(data):
        nonlocal recv_data
        nonlocal ev
        recv_data = data
        print("result: {}".format(recv_data))
        ev.set()  # unblock HTTP route

    packet_data = build_packet_data(
        Event.GET_USER_AND_WIFI_INFO_CODE, PacketType.SEND_PACKET_CODE
    )
    db.session.add(packet_data)
    db.session.commit()
    print("sending: event packetdata")
    print("Event target => " + Event[packet_data.event].name)
    print("data send: {}".format(packet_data.serialize()))

    socketio.emit(
        Event[packet_data.event].value,
        packet_data.serialize(),
        namespace=settings.ENDPOINT_IO_CORE,
        callback=callbackResponseCommand,
    )
    ev.wait(timeout=5.0)
    print("result from timeout: {}".format(recv_data))

    if recv_data:
        schema_packet = PacketDataSchema()
        schema_user = UserSchemaSocketIO()
        schema_wifi = WifiInfoSchema()
        try:
            packet_without_data = json.loads(recv_data)
            packet_without_data.pop("data")
            result_packetData = schema_packet.load(packet_without_data)
            result_user = schema_user.load(json.loads(recv_data)["data"]["user"])
            result_wifiInfo = schema_wifi.load(
                json.loads(recv_data)["data"]["wifiInfo"]
            )
        except ValidationError as err:
            print(err)
            return build_api_response(
                400,
                "The server was unable to process the request sent by the client due to invalid syntax.",
                {},
            )

        # #emit('my response', data)
        mobile_user = User.query.one_or_none()
        if mobile_user:
            User.query.filter_by(public_id=mobile_user.public_id).update(
                remove_key_from_dict(result_user, {"deviceInfo"})
            )
            DeviceInfo.query.filter_by(id=mobile_user.deviceInfo.id).update(
                result_user.get("deviceInfo")
            )
        wifiInfo = WifiInfo(**result_wifiInfo)
        packetdata = PacketData(**result_packetData)
        db.session.add(wifiInfo)
        db.session.add(packetdata)
        db.session.commit()
    locations = Location.query.order_by(Location.id.desc()).paginate(
        per_page=3, error_out=False
    )
    allPacketData = PacketData.query.order_by(PacketData.id.desc()).paginate(
        per_page=3, error_out=False
    )

    mobile_user = User.query.one_or_none()
    wifiInfo_last = WifiInfo.query.order_by(WifiInfo.id.desc()).first()
    return render_template(
        "pages/home/content.html",
        mobile_user=mobile_user,
        wifiInfo=wifiInfo_last,
        locations=locations,
        allPacketData=allPacketData,
    )
