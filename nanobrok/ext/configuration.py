from importlib import import_module
from flask import request, abort
from dynaconf import FlaskDynaconf, settings

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


def load_extensions(app):
    print("\nRegisters: Extensions\n")
    for extension in app.config.EXTENSIONS:
        module_name, factory = extension.split(":")
        print(f"ext: {module_name}")
        ext = import_module(module_name)
        getattr(ext, factory)(app)

    print("\nRegisters: Routers\n")
    for route in app.config.ROUTERS:
        module_name, factory = route.split(":")
        ext = import_module(module_name)
        getattr(ext, factory)(app)
        
    print("\n[*] Nanobrok is running")


def setHeaderResponse(app):
    @app.after_request
    def apply_caching(response):
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response

    # block http connection rule
    if app.config.BLOCK_HTTP_CONNECTION:
        
        @app.before_request
        def before_request():
            if not request.is_secure:
                return abort(403)


def init_app(app, **config):
    FlaskDynaconf(app, **config)
    setHeaderResponse(app)
