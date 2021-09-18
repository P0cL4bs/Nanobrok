from flask import abort, render_template, request, flash, url_for, redirect, session
from nanobrok.models import *
from sqlalchemy import or_
from werkzeug.security import check_password_hash
from nanobrok.ext.auth import login_manager
from nanobrok.blueprints.resources.resourcesAuth import generateTokenJwt
from flask_login import login_user, logout_user, login_required
import datetime
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


@login_manager.user_loader
def load_user(user_id):
    try:
        return UserAdm.query.get(user_id)
    except:
        return None


def route_login():
    logout_user()
    return render_template("login.html")


@login_required
def logout():
    logout_user()
    return redirect(url_for("webui.index"))


def route_post_login():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    if not session.get("attempt"):
        session["attempt"] = settings.FALIED_LOGIN_ATTEMPTS
        session["attempt_date"] = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.FALIED_TIME_WAIT_MINUTES
        )

    if session["attempt"] == 1:
        attempt_date = session.get("attempt_date")
        current_date = datetime.datetime.utcnow()
        if current_date < attempt_date:
            flash(
                f"Your has been blocked after too many failed login attempts. wait for {settings.FALIED_TIME_WAIT_MINUTES} minutes and try again"
            )
            return redirect(url_for("webui.route_login"))
        else:
            session["attempt"] = settings.FALIED_LOGIN_ATTEMPTS
            session["attempt_date"] = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=settings.FALIED_TIME_WAIT_MINUTES
            )

    attempt = session.get("attempt")
    attempt -= 1
    session["attempt"] = attempt

    user = UserAdm.query.filter(
        or_(UserAdm.username.like(email), UserAdm.email.like(email))
    ).first()
    # check if the user actually exists
    if not user or not check_password_hash(user.password, password):
        logout_user()
        flash(
            f"Please check your login details and try again, you have more {attempt} failed login attempts."
        )
        return redirect(
            url_for("webui.route_login")
        )  # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    session["token"] = generateTokenJwt(user)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for("webui.index"))
