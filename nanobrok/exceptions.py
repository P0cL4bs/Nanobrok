from flask import jsonify
from werkzeug.exceptions import HTTPException

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


def exceptionUnprocessableEntity(message):
    response = jsonify({"code": 422, "message": message})
    response.status_code = 422
    return response


def exceptionBadRequest(message):
    response = jsonify({"code": 400, "message": message})
    response.status_code = 400
    return response


errors_messages = {
    "MessageUserNotFound": {
        "message": "The user not found",
        "status": 404,
    },
    "ResourceDoesNotExist": {
        "message": "A resource with that ID no longer exists.",
        "status": 410,
    },
}


class Error(HTTPException):
    """Base class for other exceptions"""

    def __init__(self, http_status_code=400, *args, **kwargs):
        # If the key `msg` is provided, provide the msg string
        # to Exception class in order to display
        # the msg while raising the exception
        self.http_status_code = http_status_code
        self.kwargs = kwargs
        msg = kwargs.get("msg", kwargs.get("message"))
        if msg:
            args = (msg,)
            super().__init__(args)
        self.args = list(args)
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])


class ValidationError(Error):
    """Should be raised in case of custom validations"""
