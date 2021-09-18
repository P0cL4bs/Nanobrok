from nanobrok.models import Event, PacketType, PacketData, User
from flask import redirect, url_for

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


def remove_key_from_dict(d, keys):
    return {k: v for k, v in d.items() if k not in keys}


def checkUserIsAuthenticated(user_mobile: User):
    if user_mobile:
        if user_mobile.is_authenticated:
            return True
    return False


def build_packet_data(event: Event, packet_type: PacketType, command=""):
    return PacketData(command=command, event=event.name, packet_type=packet_type)
