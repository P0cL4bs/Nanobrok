import unittest, json
from nanobrok.models import (
    DeviceInfo,
    DeviceInfoSchema,
    PacketType,
    PacketDataSchema,
    PacketData,
    Event,
)
from pprint import pprint
from marshmallow import ValidationError
from nanobrok.ext.database import db
from datetime import datetime
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


class TestDeviceInfoSchema(unittest.TestCase):
    def setUp(self):
        pass

    def test_only_deviceInfo(self):
        app_device_packet = '{"upTime":  182428741, \
        "isRunningOnEmulator": false, "hasSdCard" : false, \
        "batteryVoltage": 3963, "isBatteryPresent" : false, \
        "totalInternalMemory" : 35678318016, \
        "aInternalMemory": 34719318016, \
        "totalRAM" : 3907751936, "isDeviceCharging": false, "batteryTechnology": "Litio", \
         "deviceRingerMode": "Normal", "iPv4Address": "10.0.0.106", \
          "iPv6Address": "FE80::201F:281B:9E88:7ED6", "networkType" : "WIFI/WIFIMAX"}'
        app_device_packet = json.loads(app_device_packet)

        schema_device = DeviceInfoSchema()
        try:
            result_deviceInfo = schema_device.load(app_device_packet)
        except ValidationError as err:
            print(err.messages)
            print(err.valid_data)

        obj_deviceInfo = DeviceInfo(**result_deviceInfo)

        self.assertEqual(obj_deviceInfo.upTime, 182428741)
        self.assertEqual(obj_deviceInfo.totalRAM, 3907751936)

    def test_packet_data_with_deviceInfo(self):
        app_device_packet = '{"command": "", "event": "e921f8fab42fdbb2", \
         "registred_at" : 1508484583259, "packet_type": 1, "data": '
        app_device_packet += '{"upTime":  182428741, \
        "isRunningOnEmulator": false, "hasSdCard" : false, \
        "batteryVoltage": 3963, "isBatteryPresent" : false, \
         "totalInternalMemory" : 35678318016, \
        "aInternalMemory": 34719318016, \
        "totalRAM" : 3907751936, "isDeviceCharging": false, "batteryTechnology": "Litio", \
         "deviceRingerMode": "Normal", "iPv4Address": "10.0.0.106", \
          "iPv6Address": "FE80::201F:281B:9E88:7ED6", "networkType" : "WIFI/WIFIMAX"}}'
        app_device_packet = json.loads(app_device_packet)

        schema_packet_data = PacketDataSchema()
        schema_deficeInfo = DeviceInfoSchema()
        try:
            result_packet_data = schema_packet_data.load(
                remove_key_from_dict(app_device_packet, {"data"})
            )
            result_deviceInfo = schema_deficeInfo.load(app_device_packet.get("data"))
        except ValidationError as err:
            print(err.messages)
            print(err.valid_data)

        obj_packet_data = PacketData(**result_packet_data)
        obj_deviceInfo = DeviceInfo(**result_deviceInfo)

        self.assertEqual(obj_packet_data.event, Event.GET_DEVICEINFO_CODE.name)
        self.assertEqual(obj_deviceInfo.upTime, 182428741)
        self.assertEqual(obj_deviceInfo.totalRAM, 3907751936)


if __name__ == "__main__":
    unittest.main()
