import unittest
from nanobrok.models import User, UserSchema
from pprint import pprint
from marshmallow import ValidationError
from nanobrok.ext.database import db
from nanobrok.blueprints.webui.utils import remove_key_from_dict

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


class TestUuser(unittest.TestCase):
    def setUp(self):
        pass

    def test_schema_to_user(self):
        user_data = {
            "name": "marcos",
            "username": "mh4x0f",
            "phone_number": "55-99999999999",
            "imei": "123456789012345",
            "imei2": "123456789012345",
            "mac_address": "10:09:09:04:06:03",
            "deviceInfo": {
                "aInternalMemory": 25820393472,
                "batteryPercentage": 75,
                "batteryTechnology": "Li-poly",
                "batteryVoltage": 3926,
                "buildVersionRelease": "10",
                "buildVersionSDK": 29,
                "device": "platina",
                "deviceRingerMode": "Normal",
                "hasSdCard": True,
                "iPv4Address": "10.0.0.93",
                "iPv6Address": "FE80::6BFF:52A7:DA15:1109",
                "isBatteryPresent": True,
                "isBluetoothEnabled": False,
                "isDeviceCharging": False,
                "isGpsEnabled": False,
                "isRoot": False,
                "isRunningOnEmulator": False,
                "isWifiEnabled": True,
                "manufacturer": "Xiaomi",
                "model": "MI 8 Lite",
                "networkType": "wireless",
                "oSCodename": "REL",
                "oSVersion": "10",
                "totalInternalMemory": 52567826432,
                "totalRAM": 3907751936,
                "upTime": 162539852880,
            },
        }
        schema = UserSchema()
        try:
            result = schema.load(user_data)
        except ValidationError as err:
            print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
            print(err.valid_data)  # => {"name": "John"}

        user = User(**remove_key_from_dict(result, "deviceInfo"))

        assert user.name == "marcos"
