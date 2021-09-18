from nanobrok.ext.database import db
from nanobrok.models import User, UserSchema
from sqlalchemy import text

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


def test_users_get_all(client, users):  # Arrange
    """Test get all candidatos"""
    # Act
    response = client.get("/api/v1/users")
    # Assert
    assert response.status_code == 400


def test_users_get_one(client, users):  # Arrange
    """Test get all data"""
    pass
