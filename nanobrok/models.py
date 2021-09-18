from nanobrok.ext.database import db
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import backref
from marshmallow import Schema, fields, validates, ValidationError, post_load
from enum import Enum
import datetime
import random, base64
import string, datetime
from flask_login import UserMixin
import re


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


def _get_date():
    return datetime.datetime.now()


class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


def _get_date():
    return datetime.datetime.now()


class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError("Invalid input type.")

        if value is None or value == b"":
            raise ValidationError("Invalid value")


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
    print("Random alphanumeric String is:", result_str)
    return result_str


def get_random_numeric_string(length):
    letters_and_digits = string.digits
    result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
    print("Random numeric String is:", result_str)
    return result_str


class Event(Enum):
    GET_WIFI_INFO_CODE = "e95bf8fc3c14e4ea"
    GET_USER_INFO_CODE = "e36d74f40130a52a"
    GET_SYSTEM_INFO_CODE = "0217815a4ac5379a"
    GET_USER_AND_WIFI_INFO_CODE = "ca0d9bf5223a67ba"
    GET_LOCAL_STORAGE_INFO_CODE = "45cae65c832faa02"
    GET_ALL_APPS_CODE = "fd36279506524242"
    GET_GEOLOCATION = "9e3f782e5b52e728"
    GET_AUDIO_MIC_CODE = "24a3378247b4b7a1"
    GET_DEVICEINFO_CODE = "e921f8fab42fdbb2"
    GET_EXTENIONS_CODE = "75c79c9cb1acacef"
    COMMAND_SECURITY_CODE = "87bbfc0f6f5c7876"
    COMMAND_MISC_TOAST_CODE = "ac69fe9a3314295d"
    COMMAND_PERMISSION_CHECK_CODE = "0a42c52b2b236828"
    COMMAND_SECURITY_ALARM_CODE = "eed4cdf10f13c4c5"
    PING_PONG_CODE = "24630175757b7f99"
    FILE_TRANSFER_CODE = "ea2e3b55b37ee7cb"
    NETWORK_SCAN_CODE = "1a2efdee835a65e3"
    CLIPBOARD_CODE = "da12a9858aec1751"


class PacketType(Enum):
    SEND_PACKET_CODE = 0
    RECEIVE_PACKET_CODE = 1


class SecCommandType(Enum):
    SET_LOCK_NOW = 0
    SET_MAX_INACTIVITY_TIME = 1
    SET_PASS_EXP_TIMEOUT = 2
    IS_DEVICE_ADMIN = 3
    WIPE_DATA_FACTORY = 4


class ExtensionType(Enum):
    LOCATION = 3
    PERMISSION = 2
    DEVICE_ADMIN = 1
    DEFAULT = 0


class Extensions(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(150))
    about = db.Column(db.String(150))
    status = db.Column(db.Boolean, default=False)
    requiredPermission = db.Column(db.Boolean, default=False)
    hasPermission = db.Column(db.Boolean, default=False)
    runningBackground = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.String(200))
    extensionType = db.Column(db.String(30))
    date = db.Column(db.DateTime, nullable=True, default=_get_date)

    def serialize(self):
        d = Serializer.serialize(self)
        if d["permissions"]:
            d["permissions"] = d["permissions"].split(",")
        return d


class ExtensionsSchema(Schema):
    title = fields.Str()
    subtitle = fields.Str()
    about = fields.Str()
    status = fields.Bool()
    requiredPermission = fields.Bool()
    hasPermission = fields.Bool()
    runningBackground = fields.Bool()
    permissions = fields.List(fields.Str())
    extensionType = fields.Int()
    date = db.Column(db.DateTime, nullable=True, default=_get_date)

    @post_load
    def validate_fields(self, item, many, **kwargs):
        item["extensionType"] = ExtensionType(item["extensionType"]).name
        item["permissions"] = ",".join(item["permissions"])
        return item


class Sessions(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True)
    data = db.Column(db.LargeBinary)
    expiry = db.Column(db.DateTime)

    def __init__(self, session_id, data, expiry):
        self.session_id = session_id
        self.data = data
        self.expiry = expiry

    def __repr__(self):
        return "<Session data %s>" % self.data


class DeviceScan(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15))
    deviceName = db.Column(db.String(100))
    online = db.Column(db.Boolean, default=False)
    hwAddress = db.Column(db.String(17))
    networkHw = db.Column(db.String(17))
    macVendor = db.Column(db.String(200))
    isScanningDevice = db.Column(db.Boolean, default=False)
    lastSeen = db.Column(db.DateTime, nullable=True)
    deviceType = db.Column(db.String(50))
    networkscan_id = db.Column(
        db.Integer, db.ForeignKey("network_scan.id", ondelete="CASCADE"), unique=False
    )


class NetworkScan(db.Model, Serializer):
    __tablename__ = "network_scan"
    id = db.Column(db.Integer, primary_key=True)
    baseIp = db.Column(db.String(15))
    mask = db.Column(db.Integer)
    interfaceName = db.Column(db.String(50))
    bssid = db.Column(db.String(17))
    ssid = db.Column(db.String(100))
    gateway = db.Column(db.String(17))
    rssi = db.Column(db.String(5))
    netmask = db.Column(db.String(17))
    date = db.Column(db.DateTime, nullable=True)
    devices = db.relationship(
        "DeviceScan", passive_deletes=True, backref="network_scan", uselist=True
    )


class NetworkScanSchema(Schema):
    mask = fields.Int()
    baseIp = fields.Str()
    interfaceName = fields.Str()
    bssid = fields.Str()
    ssid = fields.Str()
    gateway = fields.Str()
    rssi = fields.Str()
    netmask = fields.Str()
    date = fields.Float()

    @post_load
    def validate_fields(self, item, many, **kwargs):
        item["rssi"] = str(self.dbmToPercentage(int(item["rssi"])))
        item["date"] = datetime.datetime.fromtimestamp(item["date"] / 1000.0)
        return item

    def dbmToPercentage(self, rssi) -> int():
        # https://www.intuitibits.com/2016/03/23/dbm-to-percent-conversion/
        perfect_rssi = -20
        worst_rssi = -85

        signal_quality = (
            100 * (perfect_rssi - worst_rssi) * (perfect_rssi - worst_rssi)
            - (perfect_rssi - rssi)
            * (15 * (perfect_rssi - worst_rssi) + 62 * (perfect_rssi - rssi))
        ) / ((perfect_rssi - worst_rssi) * (perfect_rssi - worst_rssi))
        if signal_quality > 100:
            signal_quality = 100
        elif signal_quality < 1:
            signal_quality = 0
        return int(signal_quality)


class DeviceScanSchema(Schema):
    ip = fields.Str()
    deviceName = fields.Str()
    online = fields.Bool()
    hwAddress = fields.Str()
    networkHw = fields.Str()
    networkHw = fields.Str()
    macVendor = fields.Str()
    isScanningDevice = fields.Bool()
    lastSeen = fields.Float()
    deviceType = fields.Str()

    @post_load
    def validate_fields(self, item, many, **kwargs):
        item["lastSeen"] = datetime.datetime.fromtimestamp(item["lastSeen"] / 1000.0)
        return item


class NetworkWithDeviceSchema(Schema):
    devices = fields.List(fields.Nested(DeviceScanSchema))
    network = fields.Nested(NetworkScanSchema)


class DeviceInfo(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    upTime = db.Column(db.BigInteger)
    isRunningOnEmulator = db.Column(db.Boolean, default=False)
    hasSdCard = db.Column(db.Boolean, default=False)
    deviceRingerMode = db.Column(db.String(12))
    iPv4Address = db.Column(db.String(15))
    iPv6Address = db.Column(db.String(45))
    networkType = db.Column(db.String(20))
    totalRAM = db.Column(db.BigInteger)
    isDeviceCharging = db.Column(db.Boolean, default=False)
    batteryTechnology = db.Column(db.String(20))
    batteryVoltage = db.Column(db.Integer)
    batteryPercentage = db.Column(db.Integer)  # new
    isBatteryPresent = db.Column(db.Boolean, default=False)
    totalInternalMemory = db.Column(db.BigInteger)
    aInternalMemory = db.Column(db.BigInteger)
    buildVersionSDK = db.Column(db.Integer)  # new
    manufacturer = db.Column(db.String(200))  # new
    model = db.Column(db.String(100))  # new
    oSCodename = db.Column(db.String(100))  # new
    oSVersion = db.Column(db.String(100))  # new
    device = db.Column(db.String(100))  # new
    buildVersionRelease = db.Column(db.String(100))  # new
    isRoot = db.Column(db.Boolean, default=False)  # new
    isWifiEnabled = db.Column(db.Boolean, default=False)  # new
    isBluetoothEnabled = db.Column(db.Boolean, default=False)  # new
    isGpsEnabled = db.Column(db.Boolean, default=False)  # new
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False)


class DeviceInfoSchema(Schema):
    upTime = fields.Int()
    isRunningOnEmulator = fields.Bool()
    hasSdCard = fields.Bool()
    deviceRingerMode = fields.Str()
    iPv4Address = fields.Str()
    iPv6Address = fields.Str()
    networkType = fields.Str()
    totalRAM = fields.Int()
    isDeviceCharging = fields.Bool()
    batteryTechnology = fields.Str()
    batteryVoltage = fields.Int()
    batteryPercentage = fields.Int()
    isBatteryPresent = fields.Bool()
    totalInternalMemory = fields.Int()
    aInternalMemory = fields.Int()
    buildVersionSDK = fields.Int()
    manufacturer = fields.Str()
    model = fields.Str()
    oSCodename = fields.Str()
    oSVersion = fields.Str()
    device = fields.Str()
    buildVersionRelease = fields.Str()
    isRoot = fields.Bool()
    isWifiEnabled = fields.Bool()
    isBluetoothEnabled = fields.Bool()
    isGpsEnabled = fields.Bool()


class Location(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    address = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=True, default=_get_date)


class LocationSchema(Schema):
    latitude = fields.Float()
    longitude = fields.Float()
    address = fields.Str()


class UserAdm(UserMixin, db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(255), nullable=False, server_default="")
    public_id = db.Column(db.String(50), unique=True)

    def serialize(self):
        d = Serializer.serialize(self)
        # exclude feilds from Json
        del d["password"]
        return d


class PacketData(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(200))
    event = db.Column(db.String(200))
    packet_type = db.Column(db.Enum(PacketType))
    registred_at = db.Column(db.DateTime, nullable=True, default=_get_date)

    def serialize(self):
        d = Serializer.serialize(self)
        d["event"] = Event[d["event"]].value
        del d["id"]
        d["packet_type"] = PacketType(d["packet_type"]).value
        d["registred_at"] = round(datetime.datetime.timestamp(d["registred_at"]))
        return d


class PacketDataSchema(Schema):
    command = fields.Str(required=False)
    event = fields.Str(required=True)
    packet_type = fields.Int(required=True)
    data = fields.Str(required=False)
    registred_at = fields.Float(required=True)

    @post_load
    def validate_enums(self, item, many, **kwargs):
        item["event"] = Event(item["event"]).name
        item["packet_type"] = PacketType(item["packet_type"]).name
        item["registred_at"] = datetime.datetime.fromtimestamp(
            item["registred_at"] / 1000.0
        )
        if "data" in item:
            del item["data"]
        return item

    @validates("event")
    def validate_event(self, event_string):
        try:
            Event(event_string).name
        except ValueError:
            raise ValidationError("Event unknow")

    @validates("packet_type")
    def validate_packet_type(self, packet_type):
        try:
            PacketType(packet_type).name
        except ValueError:
            raise ValidationError("PacketType unknow")


# Entreprise Version
# class AppInfo(db.Model, Serializer):
#     id = db.Column(db.Integer, primary_key=True)
#     app_count = db.Column(db.Integer)
#     updated_at = db.Column(db.DateTime, nullable=True, default=_get_date)


class Audio(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)
    registred_at = db.Column(db.DateTime, nullable=True, default=_get_date)
    duration = db.Column(db.Integer)
    size = db.Column(db.String(50))

    def serialize(self):
        d = Serializer.serialize(self)
        d["data"] = base64.b64encode(getattr(self, "data")).decode("ascii")
        return d


class AudioSchema(Schema):
    data = fields.Str(required=False)
    registred_at = fields.Float(required=True)
    duration = fields.Int(required=True)
    size = fields.Str(required=False)

    @post_load
    def validate_fields(self, item, many, **kwargs):
        item["data"] = base64.b64decode(item["data"])
        item["registred_at"] = datetime.datetime.fromtimestamp(
            item["registred_at"] / 1000.0
        )
        return item


class App(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    icon = db.Column(db.String)
    package_name = db.Column(db.String(200))
    version_name = db.Column(db.String(200))
    installed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    sourceDir = db.Column(db.String(300))
    dataDir = db.Column(db.String(300))

    def serialize(self):
        d = Serializer.serialize(self)
        return d


class AppSchema(Schema):
    name = fields.Str(required=True)
    icon = fields.Str(required=True)
    package_name = fields.Str(required=True)
    version_name = fields.Str(required=True)
    installed_at = fields.Int(required=True)
    updated_at = fields.Int(required=True)
    sourceDir = fields.Str(required=True)
    dataDir = fields.Str(required=True)

    @post_load
    def validate_fields(self, item, many, **kwargs):
        try:
            item["installed_at"] = datetime.datetime.fromtimestamp(
                item["installed_at"] / 1000.0
            )
        except Exception:
            item["installed_at"] = None
        try:
            item["updated_at"] = datetime.datetime.fromtimestamp(
                item["updated_at"] / 1000.0
            )
        except Exception:
            item["updated_at"] = None
        return item


class WifiInfo(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    bssid = db.Column(db.String(17))
    ssid = db.Column(db.String(100))
    frequency = db.Column(db.String(20))
    ip_address = db.Column(db.String(15))
    link_spped = db.Column(db.String(20))
    mac_address = db.Column(db.String(17))
    rssi = db.Column(db.String(20))
    dns1 = db.Column(db.String(15))
    dns2 = db.Column(db.String(15))
    gateway = db.Column(db.String(15))
    netmask = db.Column(db.String(15))
    serverAddress = db.Column(db.String(15))
    leaseDuration = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=True, default=_get_date)


class WifiInfoSchema(Schema):
    bssid = fields.Str(required=True)
    ssid = fields.Str(required=True)
    frequency = fields.Str(required=True)
    ip_address = fields.Str(required=False)
    link_spped = fields.Str(required=False)
    mac_address = fields.Str(required=True)
    rssi = fields.Str(required=False)
    dns1 = fields.Str(required=True)
    dns2 = fields.Str(required=True)
    gateway = fields.Str(required=True)
    netmask = fields.Str(required=True)
    serverAddress = fields.Str(required=True)
    leaseDuration = fields.Int(required=True)

    @post_load
    def validate_fields(self, item, many, **kwargs):
        item["rssi"] = str(self.dbmToPercentage(int(item["rssi"])))
        return item

    def dbmToPercentage(self, rssi) -> int():
        # https://www.intuitibits.com/2016/03/23/dbm-to-percent-conversion/
        perfect_rssi = -20
        worst_rssi = -85

        signal_quality = (
            100 * (perfect_rssi - worst_rssi) * (perfect_rssi - worst_rssi)
            - (perfect_rssi - rssi)
            * (15 * (perfect_rssi - worst_rssi) + 62 * (perfect_rssi - rssi))
        ) / ((perfect_rssi - worst_rssi) * (perfect_rssi - worst_rssi))
        if signal_quality > 100:
            signal_quality = 100
        elif signal_quality < 1:
            signal_quality = 0
        return int(signal_quality)


class User(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(200))
    password = db.Column(db.String(255), nullable=False, server_default="")
    imei = db.Column(db.String(15))
    imei2 = db.Column(db.String(15))
    public_id = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.String(100))
    mac_address = db.Column(db.String(100))
    is_connected = db.Column(db.Boolean, default=False)
    lest_seen = db.Column(db.DateTime, nullable=False, default=_get_date)
    deviceInfo = db.relationship(
        "DeviceInfo", backref=backref("user", cascade="delete"), uselist=False
    )
    lest_sync = db.Column(db.DateTime, nullable=True, default=_get_date)
    is_authenticated = db.Column(db.Boolean, default=False)

    def serialize(self):
        d = Serializer.serialize(self)
        # exclude feilds from Json
        del d["password"]
        del d["deviceInfo"]
        return d


class UserSchema(Schema):
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    imei = fields.Str(required=True)
    imei2 = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    mac_address = fields.Str(required=True)
    is_connected = fields.Bool(required=False)
    deviceInfo = fields.Nested(DeviceInfoSchema)

    @validates("imei")
    def validate_imei(self, imei):
        if len(imei) > 15:
            raise ValidationError("Error: invalid IMEI number")

    @validates("imei2")
    def validate_imei2(self, imei2):
        if len(imei2) > 15:
            raise ValidationError("Error: invalid IMEI number")

    @validates("mac_address")
    def validate_imei(self, mac):
        if not re.match(
            "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()
        ):
            raise ValidationError("Error: invalid MAC address")


class UserSchemaSocketIO(Schema):
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    public_id = fields.Str(required=False)
    imei = fields.Str(required=False)
    imei2 = fields.Str(required=False)
    phone_number = fields.Str(required=True)
    mac_address = fields.Str(required=True)
    is_connected = fields.Bool(required=False)
    deviceInfo = fields.Nested(DeviceInfoSchema)


class MessageToastSchema(Schema):
    message = fields.Str(required=True)


class ClipboardSchema(Schema):
    action = fields.Str(required=True)
    content = fields.Str(required=True)


class PermissionSchema(Schema):
    status = fields.Bool(required=True)


class AlarmSchema(Schema):
    status = fields.Bool(required=True)


class FilePacket(Schema):
    filename = fields.Str(required=True)
    content_type = fields.Str(required=True)
    content = BytesField(required=True)


class TimeLookSchema(Schema):
    timeMs = fields.Int(required=True)

    @validates("timeMs")
    def validate_timeMs(self, timeMs):
        if timeMs >= 60:
            raise ValidationError("Error: invalid value for timeMs")


class PermissionCheckShema(Schema):
    permission = fields.Str(required=True)


class AudioTimeRecordSchema(Schema):
    time_record = fields.Int(required=True)

    @validates("time_record")
    def validate_timeRecord(self, time_record):
        if time_record >= 50:
            raise ValidationError("Invalid value for time_record")
