from flask import abort, render_template, request, flash, session, redirect, url_for
from nanobrok.models import Event, User, FilePacket
from wtforms import Form, StringField, validators
from nanobrok.ext.socketio import socketio
import threading, json, os
from dynaconf import settings
from nanobrok.ext.database import db
from nanobrok.blueprints.resources.resourceUtils import build_message_done
from nanobrok.blueprints.webui.utils import remove_key_from_dict
from ..utils import build_packet_data, checkUserIsAuthenticated
import os, base64
from nanobrok.exceptions import (
    ValidationError as VE,
)
from werkzeug.utils import secure_filename
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
def route_page_transfer():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    return render_template("pages/transfer/index.html", mobile_user=mobile_user)


def convert_bytes(num):
    for x in ["bytes", "KB", "MB"]:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


@login_required
def route_transfer_upload():
    ev = threading.Event()
    result = None

    def callBackAckResponse(data):
        nonlocal result
        nonlocal ev
        result = data
        ev.set()

    if request.method == "POST":

        file = request.files["file"]

        filePacket = {
            "content": base64.b64encode(file.read()).decode("ascii"),
            "content_type": file.content_type,
            "filename": secure_filename(file.filename),
        }
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        filePacket["size"] = convert_bytes(file_length)

        socketio.emit(
            Event.FILE_TRANSFER_CODE.value,
            filePacket,
            namespace=settings.ENDPOINT_IO_TRANSFER,
            callback=callBackAckResponse,
        )
        ev.wait(50 * 2)
        if result != None:
            return "uploaded"
    raise VE(
        msg="The device has either stopped responding or has been disconnected.",
        code=503,
    )
