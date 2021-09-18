from flask_restplus import Resource, reqparse
from nanobrok.models import PacketData
from nanobrok.ext.restapi import ns_events
from .resourceUtils import build_message_done
from .resourcesAuth import token_required_admin

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


def register_routes(app):
    ns_events.add_resource(EventsResource, "")
    print("ROUTERS Registed: EventController ")


class EventsResource(Resource):
    @ns_events.doc(responses={200: "Event listed successfully."})
    @ns_events.doc(responses={401: "User does not have permission to access"})
    @token_required_admin
    def get(self, current_user):

        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int, default=1)
        args = parser.parse_args()

        allPacketData = PacketData.query.order_by(PacketData.id.desc()).paginate(
            per_page=10, page=args["page"], error_out=False
        )
        packetDataPagination = {
            "items": PacketData.serialize_list(allPacketData.items),
            "next_num": allPacketData.next_num,
            "page": allPacketData.page,
            "pages": allPacketData.pages,
            "per_page": allPacketData.per_page,
            "prev_num": allPacketData.prev_num,
            "total": allPacketData.total,
            "has_next": allPacketData.has_next,
            "has_prev": allPacketData.has_prev,
        }

        return build_message_done(
            200, "User registered successfully.", packetDataPagination
        )
