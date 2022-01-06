from flask import render_template, request, flash, redirect, url_for
from nanobrok.models import (
    User,
    WifiInfo,
    PacketData,
    PacketDataSchema,
    WifiInfoSchema,
    PacketType,
    Event,
)
from nanobrok.ext.socketio import socketio
import threading, json
from nanobrok.ext.database import db
from nanobrok.blueprints.resources.resourceUtils import build_message_done
from marshmallow import ValidationError
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
def content_actions_network(ipaddress):
    try:
        list_dateWifiInfo = WifiInfo.query.filter_by(ip_address=ipaddress).all()
        r_list_dateWifiInfo = [wifi.date for wifi in list_dateWifiInfo]
        return render_template(
            "pages/network/actions.html", list_dateWifiInfo=r_list_dateWifiInfo
        )
    except Exception:
        return build_message_done(400, "BADREQUEST", {})


@login_required
def content_view_network():
    try:
        content = request.get_json(silent=True)
        print("content: {}".format(content))
        last_wifiInfo = WifiInfo.query.filter_by(date=content["date"]).first()
        return render_template("pages/network/view.html", last_wifiInfo=last_wifiInfo)
    except Exception:
        return build_message_done(400, "BADREQUEST", {})


@login_required
def content_action_network_delete():
    content = request.get_json(silent=True)
    try:
        wifiInfo = WifiInfo.query.filter_by(date=content["date"]).first()
    except Exception:
        return build_message_done(400, "BADREQUEST", {})
    if wifiInfo != None:
        ipaddress = wifiInfo.ip_address
        WifiInfo.query.filter_by(date=content["date"]).delete()
        db.session.commit()
        return content_actions_network(ipaddress)
    return build_message_done(400, "BADREQUEST", {})


@login_required
def content_action_network_delete_all():
    content = request.get_json(silent=True)
    try:
        wifiInfo = WifiInfo.query.filter_by(ip_address=content["ip"]).first()
    except Exception:
        return build_message_done(400, "BADREQUEST", {})
    if wifiInfo != None:
        WifiInfo.query.filter_by(ip_address=content["ip"]).delete()
        db.session.commit()
        return content_actions_network(content["ip"])
    return build_message_done(400, "BADREQUEST", {})


@login_required
def route_network():
    if request.method == "POST":

        ev = threading.Event()
        packet_data = None

        def ack(data):
            nonlocal packet_data
            nonlocal ev

            packet_data = data
            ev.set()  # unblock HTTP route

        print("sending: event ")
        send_packet = build_packet_data(
            Event.GET_WIFI_INFO_CODE, PacketType.SEND_PACKET_CODE
        )

        db.session.add(send_packet)
        db.session.commit()

        print("Event target => " + Event[send_packet.event].name)
        print("data send: {}".format(send_packet.serialize()))
        socketio.emit(
            Event[send_packet.event].value,
            send_packet.serialize(),
            namespace=settings.ENDPOINT_IO_CORE,
            callback=ack,
        )

        ev.wait(timeout=5)
        print("result from timeout: {}".format(packet_data))
        schema = PacketDataSchema()
        schema_wifi = WifiInfoSchema()
        try:
            packet_without_data = json.loads(packet_data)
            packet_without_data.pop("data")
            schema_packetData = schema.load(packet_without_data)
            schema_wifiInfo = schema_wifi.load(json.loads(packet_data)["data"])
            print("schema Packet data dump: {}".format(schema_packetData))
            print("schema WifiInfo data dump: {}".format(schema_wifiInfo))
            packet = PacketData(**schema_packetData)
            wifiInfo = WifiInfo(**schema_wifiInfo)
            db.session.add(packet)
            db.session.add(wifiInfo)
            db.session.commit()
            flash("The command was successfully executed", "success")

        except Exception as err:
            print(err)
            flash("The device may not have received the command", "danger")
        # if not result:
        #     flash("The device may not have received the command","danger")
        # else:
        #     flash("The command was successfully executed","success")

    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    all_wifiInfo = WifiInfo.query.all()
    data = {}
    for wifi_info in all_wifiInfo:
        if not wifi_info.ip_address in data.keys():
            data[wifi_info.ip_address] = {"current": wifi_info, "wifiInfo": []}
            continue
        data[wifi_info.ip_address]["wifiInfo"].append(wifi_info)
        # result[wifi_info] = {"IP" : wifi_info.ip_address}
    last_wifiInfo = WifiInfo.query.order_by(WifiInfo.id.desc()).first()
    return render_template(
        "pages/network/index.html",
        mobile_user=mobile_user,
        dataWifiInfo=data,
        last_wifiInfo=last_wifiInfo,
    )
