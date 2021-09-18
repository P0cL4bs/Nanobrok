import click
from nanobrok.ext.database import db
from nanobrok.ext.auth import create_user
from nanobrok.models import *
from nanobrok.models import User, UserSchema, UserAdm
from werkzeug.security import generate_password_hash
import uuid
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


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db_dev():
    """Populate db with sample data"""
    return None


def populate_db_prod():
    """Populate db with data for production"""
    return None


def populate_db():
    """Populate db with sample data"""
    user_data = {
        "username": "mh4x0f",
        "password": "mh4x0f",
    }

    user_data["password"] = generate_password_hash(
        user_data.get("password"), method="sha256"
    )
    new_user = UserAdm(**user_data, public_id=str(uuid.uuid4()))
    db.session.add(new_user)
    db.session.commit()

    return UserAdm.query.all()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db, populate_db_dev, populate_db_prod]:
        app.cli.add_command(app.cli.command()(command))

    # add a single command
    @app.cli.command()
    @click.option("--username", "-u")
    @click.option("--password", "-p")
    def add_user(username, password):
        """Adds a new user to the database"""
        return create_user(username, password)
