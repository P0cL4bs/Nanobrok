import unittest, json
from nanobrok.models import (
    Location,
    LocationSchema,
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


class TestLocationSchema(unittest.TestCase):
    def setUp(self):
        pass

    def test_packet_data_with_location(self):
        app_data_packet = '{"command": "", "event": "9e3f782e5b52e728", "registred_at" : 1508484583259, "packet_type": 1, "data": {"latitude": 36.115278, "longitude": -115.075514}}'
        app_data_packet = json.loads(app_data_packet)

        schema_packet_data = PacketDataSchema()
        schema_location = LocationSchema()
        try:
            result_packet_data = schema_packet_data.load(
                remove_key_from_dict(app_data_packet, {"data"})
            )
            result_location = schema_location.load(app_data_packet.get("data"))
        except ValidationError as err:
            print(err.messages)
            print(err.valid_data)

        obj_packet_data = PacketData(**result_packet_data)
        obj_location = Location(**result_location)

        self.assertEqual(obj_packet_data.event, Event.GET_GEOLOCATION.name)
        self.assertEqual(obj_location.latitude, 36.115278)
        self.assertEqual(obj_location.longitude, -115.075514)


if __name__ == "__main__":
    unittest.main()
