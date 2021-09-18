import dynaconf
from flask import render_template, url_for, redirect
from nanobrok.models import (
    Event,
    User,
    PacketData,
    PacketDataSchema,
    PacketType,
    Extensions,
    ExtensionsSchema,
)
from nanobrok.ext.socketio import socketio
import threading, json
from nanobrok.ext.database import db
from nanobrok.blueprints.webui.utils import remove_key_from_dict
from ..utils import build_packet_data, checkUserIsAuthenticated
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
def route_extensions():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    extensions = Extensions.serialize_list(Extensions.query.all())
    return render_template(
        "pages/extensions/index.html",
        mobile_user=mobile_user,
        extensions=extensions,
    )


@login_required
def route_get_extensions():

    ev = threading.Event()
    result = None

    def callBackAckResponse(data):
        nonlocal result
        nonlocal ev

        result = data
        ev.set()

    send_packet = build_packet_data(
        Event.GET_EXTENIONS_CODE,
        PacketType.SEND_PACKET_CODE,
        "",
    )

    db.session.add(send_packet)
    db.session.commit()

    print("sending to cleint: event -> " + Event.GET_EXTENIONS_CODE.name)
    socketio.emit(
        Event.GET_EXTENIONS_CODE.value,
        {},
        namespace=settings.ENDPOINT_IO_CORE,
        callback=callBackAckResponse,
    )
    ev.wait(timeout=5)

    if result != None:
        packet_data = json.loads(result)
        schema_packet = PacketDataSchema()
        try:
            result_packetData = schema_packet.load(
                remove_key_from_dict(packet_data, {"data"})
            )
            db.session.query(Extensions).delete()
            db.session.commit()
            for ext in packet_data["data"]:
                schema_extensions = ExtensionsSchema()
                result_extensions = schema_extensions.load(ext)
                packet = Extensions(**result_extensions)
                db.session.add(packet)

            packet = PacketData(**result_packetData)
            db.session.add(packet)
            db.session.commit()

        except Exception as err:
            print(err)
    extensions = Extensions.serialize_list(Extensions.query.all())
    return render_template(
        "pages/extensions/content.html",
        extensions=extensions,
    )
