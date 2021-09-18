from flask import render_template, url_for, redirect
from nanobrok.models import Location, User
from flask_login import login_required
from nanobrok.blueprints.webui.utils import checkUserIsAuthenticated


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


@login_required
def route_pages_location():
    mobile_user = User.query.one_or_none()
    if not checkUserIsAuthenticated(mobile_user):
        return redirect(url_for("webui.sync_index"))
    location_data = Location.query.order_by(Location.id.desc()).first()
    locations = Location.query.order_by(Location.id.desc()).all()
    return render_template(
        "pages/location/index.html",
        mobile_user=mobile_user,
        last_location=location_data,
        locations=locations,
    )
