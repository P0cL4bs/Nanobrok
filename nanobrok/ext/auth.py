from werkzeug.security import check_password_hash, generate_password_hash
from nanobrok.ext.database import db
from nanobrok.models import User
from flask_login import LoginManager

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

login_manager = LoginManager()


def init_app(app):
    login_manager.session_protection = "strong"
    login_manager.login_view = "webui.route_login"
    login_manager.init_app(app)


def verify_login(user):
    """Valida o usuario e senha para efetuar o login"""
    username = user.get("username")
    password = user.get("password")
    if not username or not password:
        return False
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return False
    if check_password_hash(existing_user.password, password):
        return True
    return False


def create_user(username, password):
    """Registra um novo usuario caso nao esteja cadastrado"""
    if User.query.filter_by(username=username).first():
        raise RuntimeError(f"{username} ja esta cadastrado")
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user


# def init_app(app):
#     SimpleLogin(app, login_checker=verify_login)
