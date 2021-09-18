from flask import render_template, request, redirect, url_for
from nanobrok.models import User
from flask_login import login_required
from wtforms import Form, StringField, validators, ValidationError
from dynaconf import settings
from nanobrok.blueprints.webui.utils import checkUserIsAuthenticated

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
    imei1_number = StringField("IMEI 1", [validators.Length(min=4, max=200)])
    imei2_number = StringField("IMEI 2", [validators.Length(min=4, max=25)])
    phone_number = StringField("Phone number", [validators.Length(min=4, max=25)])
    mac_address = StringField("Mac address", [validators.Length(min=4, max=25)])

    def validate_imei1_number(form, field):
        if len(field.data) > 50:
            raise ValidationError("Name must be less than 50 characters")


@login_required
def route_settings():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    form = Form(request.form)
    if request.method == "POST" and form.validate():
        pass

    return render_template("settings.html", mobile_user=mobile_user, form=form)
