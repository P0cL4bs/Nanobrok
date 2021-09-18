from flask import abort, render_template, request, flash, url_for, redirect, session
from nanobrok.models import *
from sqlalchemy import or_
from werkzeug.security import check_password_hash
from nanobrok.ext.auth import login_manager
from nanobrok.blueprints.resources.resourcesAuth import generateTokenJwt
from flask_login import login_user, logout_user, login_required
from ..utils import checkUserIsAuthenticated

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
def route_about():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    return render_template("about.html", mobile_user=mobile_user)


@login_required
def route_privacy():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    return render_template("privacy_policy.html", mobile_user=mobile_user)


@login_required
def route_team():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    return render_template("team.html", mobile_user=mobile_user)
