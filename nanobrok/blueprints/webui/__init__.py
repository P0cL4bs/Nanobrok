from flask import Blueprint, render_template
import nanobrok.blueprints.webui.routes.network as nt
import nanobrok.blueprints.webui.routes.apps as apps
import nanobrok.blueprints.webui.routes.location as lt
import nanobrok.blueprints.webui.routes.index as main
import nanobrok.blueprints.webui.routes.about as ab
import nanobrok.blueprints.webui.routes.settings as settings
import nanobrok.blueprints.webui.routes.sync as sync
import nanobrok.blueprints.webui.routes.auth as auth
import nanobrok.blueprints.webui.routes.extensions as ext
import nanobrok.blueprints.webui.routes.events as evt
import nanobrok.blueprints.webui.routes.transfer as tf
import nanobrok.blueprints.webui.routes.commands as cm
import nanobrok.blueprints.webui.routes.netscan as nc
from flask_wtf.csrf import CSRFError

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


bp = Blueprint("webui", __name__, template_folder="templates")

bp.add_url_rule(
    "/",
    view_func=main.index,
    methods=["POST", "GET"],
)

bp.add_url_rule(
    "/dashboard/",
    view_func=main.index,
    methods=["POST", "GET"],
)

bp.add_url_rule(
    "/auth/",
    view_func=auth.route_login,
    methods=["GET"],
)

bp.add_url_rule(
    "/auth",
    view_func=auth.route_post_login,
    methods=["POST"],
)

bp.add_url_rule(
    "/logout",
    view_func=auth.logout,
    methods=["GET"],
)

bp.add_url_rule("/updateDashboard", view_func=main.updateDashboard, methods=["GET"])

bp.add_url_rule(
    "/sync",
    view_func=sync.sync_index,
    methods=["POST", "GET"],
)
bp.add_url_rule(
    "/update/sidebarHeader",
    view_func=main.route_header_sidebar,
    methods=["GET"],
)

bp.add_url_rule(
    "/network/",
    view_func=nt.route_network,
    methods=["POST", "GET"],
)
bp.add_url_rule(
    "/network_actions/<ipaddress>",
    view_func=nt.content_actions_network,
    methods=["GET"],
)
bp.add_url_rule("/network_views", view_func=nt.content_view_network, methods=["POST"])
bp.add_url_rule(
    "/network_actions_delete",
    view_func=nt.content_action_network_delete,
    methods=["POST"],
)
bp.add_url_rule(
    "/network_actions_delete_all",
    view_func=nt.content_action_network_delete_all,
    methods=["POST"],
)


bp.add_url_rule("/events/", view_func=evt.route_events, methods=["GET"])
bp.add_url_rule("/events/update", view_func=evt.route_update_events, methods=["GET"])
bp.add_url_rule(
    "/events/<int:page_num>", view_func=evt.route_pages_events, methods=["GET"]
)


bp.add_url_rule("/apps/", view_func=apps.route_pages_apps, methods=["GET", "POST"])
bp.add_url_rule("/apps/update", view_func=apps.route_pages_update_apps, methods=["GET"])

bp.add_url_rule("/location/", view_func=lt.route_pages_location, methods=["GET"])


bp.add_url_rule("/commands/", view_func=cm.route_page_commands, methods=["GET"])
bp.add_url_rule(
    "/commands/records/audio",
    view_func=cm.route_commands_record_audio,
    methods=["POST"],
)
bp.add_url_rule(
    "/commands/security/permission",
    view_func=cm.route_commands_permision,
    methods=["POST"],
)


bp.add_url_rule("/transfer/", view_func=tf.route_page_transfer, methods=["GET"])
bp.add_url_rule(
    "/transfer/upload", view_func=tf.route_transfer_upload, methods=["GET", "POST"]
)

bp.add_url_rule("/netscan/", view_func=nc.route_netscan, methods=["GET"])
bp.add_url_rule(
    "/netscan/action/startScanDevices",
    view_func=nc.route_action_startscan,
    methods=["GET"],
)
bp.add_url_rule(
    "/netscan/action/viewScanDevices",
    view_func=nc.route_action_view_netscan,
    methods=["POST"],
)

bp.add_url_rule(
    "/extensions/",
    view_func=ext.route_extensions,
    methods=["GET"],
)

bp.add_url_rule(
    "/extensions/action/getAllExtensions",
    view_func=ext.route_get_extensions,
    methods=["GET"],
)

bp.add_url_rule(
    "/settings/",
    view_func=settings.route_settings,
    methods=["GET", "POST"],
)

bp.add_url_rule(
    "/about/",
    view_func=ab.route_about,
    methods=["GET"],
)

bp.add_url_rule(
    "/privacy-policy/",
    view_func=ab.route_privacy,
    methods=["GET"],
)

bp.add_url_rule(
    "/team/",
    view_func=ab.route_team,
    methods=["GET"],
)


@bp.app_errorhandler(404)
def handle_404(err):
    return render_template("/errors/404.html", err=err), 404


@bp.app_errorhandler(500)
def handle_500(err):
    return render_template("/errors/500.html", err=err), 500


@bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template("/errors/csrf_error.html", reason=e.description), 400


def init_app(app):
    app.register_blueprint(bp)
