from flask import render_template, request, flash, url_for, redirect
from nanobrok.models import (
    User,
    PacketData,
    PacketDataSchema,
    PacketType,
    Event,
    NetworkWithDeviceSchema,
    NetworkScan,
    DeviceScan,
)
from nanobrok.ext.socketio import socketio
import threading, json
from nanobrok.ext.database import db
from nanobrok.blueprints.resources.resourceUtils import build_message_done
from marshmallow import ValidationError
from ..utils import build_packet_data, checkUserIsAuthenticated
from nanobrok.blueprints.webui.utils import remove_key_from_dict
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
def route_action_startscan():
    # test block event response callback from client
    ev = threading.Event()
    result = None

    def ack(data):
        nonlocal result
        nonlocal ev

        result = data
        ev.set()

    send_packet = build_packet_data(
        Event.NETWORK_SCAN_CODE, PacketType.SEND_PACKET_CODE
    )

    db.session.add(send_packet)
    db.session.commit()

    print("sending: event ")
    socketio.emit(
        Event.NETWORK_SCAN_CODE.value, namespace=settings.ENDPOINT_IO_CORE, callback=ack
    )
    ev.wait()
    if result != None:
        packet_data = json.loads(result)
        schema_packet = PacketDataSchema()
        schema_networkwithDevice = NetworkWithDeviceSchema()
        try:
            schema_packetData = schema_packet.load(
                remove_key_from_dict(packet_data, {"data"})
            )
            result_network = schema_networkwithDevice.load(packet_data.get("data"))
            print(result_network.get("network"))
            print(result_network.get("devices"))
            networkScan = NetworkScan(**result_network.get("network"))
            db.session.add(networkScan)
            db.session.commit()

            for device in result_network.get("devices"):
                db.session.add(DeviceScan(**device, networkscan_id=networkScan.id))
            packet = PacketData(**schema_packetData)
            db.session.add(packet)
            db.session.commit()

            return render_template(
                "pages/netscan/result.html",
                current_network=networkScan,
                devices=networkScan.devices,
            )
        except Exception as err:
            print(err)
            return build_message_done(400, "BADREQUEST", {})
    return render_template(
        "pages/netscan/result.html", current_network=None, devices=[]
    )


@login_required
def route_action_view_netscan():
    content = request.get_json(force=True)
    try:
        networkScan = NetworkScan.query.filter_by(date=content["date"]).first()
    except Exception:
        return build_message_done(400, "BADREQUEST", {})
    if networkScan != None:
        return render_template(
            "pages/netscan/result.html",
            current_network=networkScan,
            devices=networkScan.devices,
        )
    return render_template(
        "pages/netscan/result.html", current_network=None, devices=[]
    )


@login_required
def route_netscan():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    networks = NetworkScan.query.order_by(NetworkScan.id.desc()).all()
    return render_template(
        "pages/netscan/index.html",
        mobile_user=mobile_user,
        current_network=None,
        devices=[],
        networks=networks,
    )
