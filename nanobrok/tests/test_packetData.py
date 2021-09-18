import unittest
from nanobrok.models import PacketData, PacketDataSchema, Event, PacketType
from pprint import pprint
from marshmallow import ValidationError
from nanobrok.ext.database import db

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


class TestPacketDataSchema(unittest.TestCase):
    def setUp(self):
        pass

    def test_packet_data_schema(self):
        packet_data = {
            "command": "Sansung S21 Pro",
            "event": "0217815a4ac5379a",
            "registred_at": 1508484583259,
            "data": "",
            "packet_type": 0,
        }
        schema = PacketDataSchema()
        try:
            result = schema.load(packet_data)
        except ValidationError as err:
            print(err.messages)
            print(err.valid_data)

        packet = PacketData(**result)

        self.assertEqual(packet.packet_type, PacketType.SEND_PACKET_CODE.name)
        self.assertEqual(packet.event, Event.GET_SYSTEM_INFO_CODE.name)


if __name__ == "__main__":
    unittest.main()
