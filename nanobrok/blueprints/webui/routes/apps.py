from flask import abort, render_template, request, flash, redirect, url_for
from nanobrok.models import (
    User,
    PacketData,
    Event,
    PacketType,
    PacketDataSchema,
    AppSchema,
    App,
)
from wtforms import Form, StringField, validators
from nanobrok.ext.socketio import socketio
from marshmallow import ValidationError
import threading, json
from dynaconf import settings
from nanobrok.ext.database import db
from ..utils import build_packet_data, checkUserIsAuthenticated
from nanobrok.blueprints.resources.resourceUtils import build_api_response
from flask_login import login_required
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
def route_pages_apps():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    packet_data = (
        PacketData.query.order_by(PacketData.id.desc())
        .filter_by(event=Event.GET_ALL_APPS_CODE.name)
        .filter_by(packet_type=PacketType.RECEIVE_PACKET_CODE)
        .first()
    )
    all_apps = App.query.all()
    dump_apps = App.serialize_list(all_apps)
    return render_template(
        "pages/apps/index.html",
        mobile_user=mobile_user,
        last_packet_data=packet_data,
        apps=dump_apps,
    )


@login_required
def route_pages_update_apps():
    ev = threading.Event()
    resp_packet_data = None

    def callbackResponse(data):
        nonlocal resp_packet_data
        nonlocal ev

        resp_packet_data = data
        ev.set()

    print("sending: event ")
    socketio.emit(
        Event.GET_ALL_APPS_CODE.value,
        {},
        namespace=settings.ENDPOINT_IO_CORE,
        callback=callbackResponse,
    )
    _packet_data = build_packet_data(
        Event.GET_ALL_APPS_CODE, PacketType.SEND_PACKET_CODE
    )
    db.session.add(_packet_data)
    db.session.commit()

    ev.wait(timeout=10)
    if resp_packet_data != None:
        packet_data = resp_packet_data
        schema_packet = PacketDataSchema()
        try:
            packet_without_data = json.loads(packet_data)
            packet_without_data.pop("data")
            schema_packetData = schema_packet.load(packet_without_data)
            db.session.query(App).delete()
            db.session.commit()
            for app in json.loads(packet_data)["data"]:
                schema_app = AppSchema()
                result_schema = schema_app.load(app)
                app_data = App(**result_schema)
                db.session.add(app_data)

            # print("schema Packet data dump: {}".format(schema_packetData))
            packet = PacketData(**schema_packetData)
            db.session.add(packet)
            db.session.commit()

        except Exception as err:
            print(err)
            return build_api_response(400, "bad request packetdata", "")

        last_packet_data = (
            PacketData.query.order_by(PacketData.id.desc())
            .filter_by(event=Event.GET_ALL_APPS_CODE.name)
            .filter_by(packet_type=PacketType.RECEIVE_PACKET_CODE)
            .first()
        )
        all_apps = App.serialize_list(App.query.all())
        return render_template(
            "pages/apps/content.html", last_packet_data=last_packet_data, apps=all_apps
        )

    return build_api_response(
        408,
        "The server did not receive a complete request from the client within the server’s allotted timeout period.",
        "",
    )
