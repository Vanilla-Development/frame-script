# Here is the PyMidnight source code is it messy yes is it poorly optimized yes Have fun :P
# Have fun (:
# From U
# Thanks for all the support <3

import threading
import time
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
import numpy as np
import win32api
from ctypes import windll, Structure, wintypes
import ctypes
from numpy import array, float32, linalg
import dearpygui.dearpygui as dpg
from requests import get
from pymem import Pymem
from pymem.process import list_processes
from psutil import pid_exists
import json
import math
from PyQt5.QtGui import QColor, QBrush, QPainter
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
import random
from OpenGL.GL import *
import platform
import requests
import re
import win32con
def check_windows_version():
    if platform.system() != "Windows":
        return "Not Windows"
    release = platform.release()
    if release == "10":
        build = int(platform.version().split(".")[2])
        if build >= 22000:
            return "Windows 11"
        else:
            return "Windows 10"
    elif release == "11":
        return "Windows 11"
    else:
        return f"Windows {release}"
v = check_windows_version()
swidth = win32api.GetSystemMetrics(0)
sheight = win32api.GetSystemMetrics(1)
os.system("title Midnight - Login")
theme = "Pink"
def get_default_config_path2():
    home_dir = os.path.expanduser('~')
    return os.path.join(home_dir, ".pymidnightconfig", "login.json")
def get_configs_directory2():
    filepath = get_default_config_path2()
    config_dir = os.path.dirname(filepath)
    os.makedirs(config_dir, exist_ok=True)
    return config_dir
def is_logged_in():
    filepath = get_default_config_path2()
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
            return config.get('logged_in', False)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Warning: Could not read or parse login config. Assuming not logged in. Error: {e}")
        return False
def set_logged_in(status: bool):
    get_configs_directory2()
    filepath = get_default_config_path2()
    config_data = {"logged_in": status}
    try:
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        print(f"Error: Could not write login configuration to file. {e}")
os.system("cls")
PID = -1
baseAddr = None
pm = Pymem()
fovfill = False
fovglow = False
aimbot_enabled = False
aimbot_keybind = 'Right Mouse'
shape = "circle"
Humanization_enabled = False
waiting_for_keybind = False
injected = False
aimbot_smoothness_enabled = False
aimbot_smoothness_value = 1
aimbot_ignoreteam = False
aimbot_ignoredead = False
aimbot_hitpart = "Head"
aimbot_type = "Mouse"
aimbot_prediction_enabled = False
aimbot_prediction_x = 0.0
speed_enabled = False
aimbot_prediction_y = 0.0
triggerbot_keybind = 'Delete'
aimbot_fov = 160 * 2
opamount = 255
fovtoggle = False
speed = 20.0
keybind_bg_color = [35, 35, 45]
keybind_line_color = [180, 100, 255]
keybind_text_color = [220, 220, 230]
fovoutline = False
fovglowamount = 10
lockedplr = 0
dataModel = 0
wsAddr = 0
camAddr = 0
fly_keybind = 81
speed_keybind = 45
oldfov = 0
camCFrameRotAddr = 0
plrsAddr = 0
lpAddr = 0
matrixAddr = 0
camPosAddr = 0
target = 0
nameOffset = 0
childrenOffset = 0
joystick = None
VK_CODES = {
    'Left Mouse': 0x01, 'Right Mouse': 0x02, 'Middle Mouse': 0x04, 'X1 Mouse': 0x05, 'X2 Mouse': 0x06,
    'Backspace': 0x08, 'Tab': 0x09, 'Enter': 0x0D, 'Shift': 0x10, 'Ctrl': 0x11, 'Alt': 0x12, 'Pause': 0x13, 'Caps Lock': 0x14, 'Esc': 0x1B, 'Space': 0x20,
    'Page Up': 0x21, 'Page Down': 0x22, 'End': 0x23, 'Home': 0x24, 'Left Arrow': 0x25, 'Up Arrow': 0x26, 'Right Arrow': 0x27, 'Down Arrow': 0x28, 'Select': 0x29, 'Print': 0x2A, 'Execute': 0x2B, 'Print Screen': 0x2C, 'Insert': 0x2D, 'Delete': 0x2E, 'Help': 0x2F,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45, 'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A, 'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F, 'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54, 'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59, 'Z': 0x5A,
    'Left Win': 0x5B, 'Right Win': 0x5C, 'Apps': 0x5D,
    'Numpad 0': 0x60, 'Numpad 1': 0x61, 'Numpad 2': 0x62, 'Numpad 3': 0x63, 'Numpad 4': 0x64, 'Numpad 5': 0x65, 'Numpad 6': 0x66, 'Numpad 7': 0x67, 'Numpad 8': 0x68, 'Numpad 9': 0x69, 'Multiply': 0x6A, 'Add': 0x6B, 'Separator': 0x6C, 'Subtract': 0x6D, 'Decimal': 0x6E, 'Divide': 0x6F,
    'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73, 'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B, 'F13': 0x7C, 'F14': 0x7D, 'F15': 0x7E, 'F16': 0x7F, 'F17': 0x80, 'F18': 0x81, 'F19': 0x82, 'F20': 0x83, 'F21': 0x84, 'F22': 0x85, 'F23': 0x86, 'F24': 0x87,
    'Num Lock': 0x90, 'Scroll Lock': 0x91,
    'Left Shift': 0xA0, 'Right Shift': 0xA1, 'Left Ctrl': 0xA2, 'Right Ctrl': 0xA3, 'Left Alt': 0xA4, 'Right Alt': 0xA5,
    'Browser Back': 0xA6, 'Browser Forward': 0xA7, 'Browser Refresh': 0xA8, 'Browser Stop': 0xA9, 'Browser Search': 0xAA, 'Browser Favorites': 0xAB, 'Browser Home': 0xAC,
    'Volume Mute': 0xAD, 'Volume Down': 0xAE, 'Volume Up': 0xAF, 'Next Track': 0xB0, 'Previous Track': 0xB1, 'Stop Media': 0xB2, 'Play/Pause': 0xB3, 'Mail': 0xB4, 'Media Select': 0xB5, 'Launch App 1': 0xB6, 'Launch App 2': 0xB7,
    'Semicolon': 0xBA, 'Equals': 0xBB, 'Comma': 0xBC, 'Minus': 0xBD, 'Period': 0xBE, 'Slash': 0xBF, 'Grave': 0xC0, 'Left Bracket': 0xDB, 'Backslash': 0xDC, 'Right Bracket': 0xDD, 'Apostrophe': 0xDE,
}
def update_offsets_from_url(cpp_url, json_template_text):
    try:
        response = requests.get(cpp_url)
        response.raise_for_status()
        cpp_offsets_text = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching offsets from URL: {e}")
        return None
    parsed_cpp_offsets = {}
    current_namespace = None
    for line in cpp_offsets_text.splitlines():
        line = line.strip()
        namespace_match = re.match(r'namespace (\w+)', line)
        if namespace_match:
            current_namespace = namespace_match.group(1)
            continue
        offset_match = re.match(r'inline constexpr uintptr_t (\w+) = (0x[\da-fA-F]+);', line)
        if offset_match and current_namespace:
            offset_name = offset_match.group(1)
            offset_value = offset_match.group(2)
            parsed_cpp_offsets[f"{current_namespace}::{offset_name}"] = offset_value
        version_match = re.match(r'inline std::string ClientVersion = "([^"]+)";', line)
      
        if version_match:
            parsed_cpp_offsets["ClientVersion"] = version_match.group(1)
    json_data = json.loads(json_template_text)
    key_mapping = {
        "Adornee": "Misc::Adornee", "Anchored": "PrimitiveFlags::Anchored", "AnimationId": "Misc::AnimationId",
        "AttributeToNext": "Instance::AttributeToNext", "AttributeToValue": "Instance::AttributeToValue",
        "Camera": "Workspace::CurrentCamera", "CameraMaxZoomDistance": "Player::MaxZoomDistance",
        "CameraMinZoomDistance": "Player::MinZoomDistance", "CameraMode": "Player::CameraMode",
        "CameraPos": "Camera::Position", "CameraRotation": "Camera::Rotation", "CameraSubject": "Camera::CameraSubject",
        "CameraType": "Camera::CameraType", "CanCollide": "PrimitiveFlags::CanCollide", "CanTouch": "PrimitiveFlags::CanTouch",
        "Children": "Instance::ChildrenStart", "ChildrenEnd": "Instance::ChildrenEnd", "ClassDescriptor": "Instance::ClassDescriptor",
        "ClassDescriptorToClassName": "Instance::ClassName", "ClickDetectorMaxActivationDistance": "ClickDetector::MaxActivationDistance",
        "ClockTime": "Lighting::ClockTime", "CreatorId": "DataModel::CreatorId", "DataModelPrimitiveCount": "DataModel::PrimitiveCount",
        "DecalTexture": "Textures::Decal_Texture", "Dimensions": "VisualEngine::Dimensions", "DisplayName": "Player::DisplayName",
        "FOV": "Camera::FieldOfView", "FakeDataModelPointer": "FakeDataModel::Pointer", "FakeDataModelToDataModel": "FakeDataModel::RealDataModel",
        "FogColor": "Lighting::FogColor", "FogEnd": "Lighting::FogEnd", "FogStart": "Lighting::FogStart",
        "FrameRotation": "GuiObject::Rotation", "FrameSizeX": "GuiObject::Size", "GameId": "DataModel::GameId",
        "GameLoaded": "DataModel::GameLoaded", "Gravity": "Workspace::ReadOnlyGravity", "Health": "Humanoid::Health",
        "HipHeight": "Humanoid::HipHeight", "HumanoidState": "Humanoid::HumanoidState", "HumanoidStateId": "Humanoid::HumanoidStateID",
        "InputObject": "MouseService::InputObject", "InstanceAttributePointer1": "Instance::AttributeContainer",
        "InstanceAttributePointer2": "Instance::AttributeList", "JobEnd": "TaskScheduler::JobEnd", "JobId": "DataModel::JobId",
        "JobStart": "TaskScheduler::JobStart", "Job_Name": "TaskScheduler::JobName", "JumpPower": "Humanoid::JumpPower",
        "LocalPlayer": "Player::LocalPlayer", "LocalScriptByteCode": "LocalScript::ByteCode", "LocalScriptBytecodePointer": "ByteCode::Pointer",
        "LocalScriptHash": "LocalScript::Hash", "MaxHealth": "Humanoid::MaxHealth", "MaxSlopeAngle": "Humanoid::MaxSlopeAngle",
        "MeshPartTexture": "MeshPart::Texture", "ModelInstance": "Player::ModelInstance", "ModuleScriptByteCode": "ModuleScript::ByteCode",
        "ModuleScriptBytecodePointer": "ByteCode::Pointer", "ModuleScriptHash": "ModuleScript::Hash", "MoonTextureId": "Sky::MoonTextureId",
        "MousePosition": "MouseService::MousePosition", "MouseSensitivity": "MouseService::SensitivityPointer",
        "Name": "Instance::Name", "NameSize": "Misc::StringLength", "OutdoorAmbient": "Lighting::OutdoorAmbient",
        "Parent": "Instance::Parent", "PartSize": "BasePart::Size", "Ping": "StatsItem::Value", "PlaceId": "DataModel::PlaceId",
        "PlayerMouse": "Player::Mouse", "Position": "BasePart::Position", "Primitive": "BasePart::Primitive",
        "PrimitivesPointer1": "Workspace::PrimitivesPointer1", "PrimitivesPointer2": "Workspace::PrimitivesPointer2",
        "ProximityPromptActionText": "ProximityPrompt::ActionText", "ProximityPromptEnabled": "ProximityPrompt::Enabled",
        "ProximityPromptGamepadKeyCode": "ProximityPrompt::GamepadKeyCode", "ProximityPromptHoldDuraction": "ProximityPrompt::HoldDuration",
        "ProximityPromptMaxActivationDistance": "ProximityPrompt::MaxActivationDistance", "ProximityPromptMaxObjectText": "ProximityPrompt::ObjectText",
        "RenderJobToFakeDataModel": "TaskScheduler::RenderJobToFakeDataModel", "RenderJobToRenderView": "TaskScheduler::RenderJobToRenderView",
        "RigType": "Humanoid::RigType", "Rotation": "BasePart::Rotation", "ScriptContext": "DataModel::ScriptContext",
        "SkyboxBk": "Sky::SkyboxBk", "SkyboxDn": "Sky::SkyboxDn", "SkyboxFt": "Sky::SkyboxFt", "SkyboxLf": "Sky::SkyboxLf",
        "SkyboxRt": "Sky::SkyboxRt", "SkyboxUp": "Sky::SkyboxUp", "StarCount": "Sky::StarCount", "StringLength": "Misc::StringLength",
        "SunTextureId": "Sky::SunTextureId", "TaskSchedulerMaxFPS": "TaskScheduler::MaxFPS", "TaskSchedulerPointer": "TaskScheduler::Pointer",
        "Team": "Player::Team", "TeamColor": "Team::BrickColor", "TextLabelText": "GuiObject::Text", "TextLabelVisible": "GuiObject::Visible",
        "Transparency": "BasePart::Transparency", "UserId": "Player::UserId", "Value": "Misc::Value", "Velocity": "BasePart::AssemblyLinearVelocity",
        "VisualEngine": "RenderView::VisualEngine", "VisualEnginePointer": "VisualEngine::Pointer", "VisualEngineToDataModel1": "VisualEngine::ToDataModel1",
        "VisualEngineToDataModel2": "VisualEngine::ToDataModel2", "WalkSpeed": "Humanoid::Walkspeed", "WalkSpeedCheck": "Humanoid::WalkspeedCheck",
        "Workspace": "DataModel::Workspace", "viewmatrix": "VisualEngine::ViewMatrix",
    }
    if "ClientVersion" in parsed_cpp_offsets:
        json_data["RobloxVersion"] = f"Roblox Version: {parsed_cpp_offsets['ClientVersion']}"
        print(parsed_cpp_offsets['ClientVersion'])
    for json_key, cpp_key in key_mapping.items():
        if cpp_key in parsed_cpp_offsets:
            json_data[json_key] = parsed_cpp_offsets[cpp_key]
    return json.dumps(json_data, indent=2)
offsets_url = "https://imtheo.lol/Offsets/Offsets.hpp"
json_template = """
    {
      "RobloxVersion": "Roblox Version: version-4aeb17bd13994560", "ByfronVersion": "Byfron Version: ???", "Adornee": "0xD0",
      "Anchored": "0x26A", "AnchoredMask": "0x4", "AnimationId": "0xD0", "AttributeToNext": "0x58", "AttributeToValue": "0x18",
      "AutoJumpEnabled": "0x1DB", "BeamBrightness": "0x190", "BeamColor": "0x120", "BeamLightEmission": "0x19C", "BeamLightInfuence": "0x1A0",
      "CFrame": "0x90", "Camera": "0x410", "CameraMaxZoomDistance": "0x2F0", "CameraMinZoomDistance": "0x2F4", "CameraMode": "0x2F8",
      "CameraPos": "0x11C", "CameraRotation": "0xF8", "CameraSubject": "0xE8", "CameraType": "0x158", "CanCollide": "0x26A", "CanCollideMask": "0x8",
      "CanTouch": "0x26A", "CanTouchMask": "0x10", "CharacterAppearanceId": "0x298", "Children": "0x60", "ChildrenEnd": "0x8",
      "ClassDescriptor": "0x18", "ClassDescriptorToClassName": "0x8", "ClickDetectorMaxActivationDistance": "0x100", "ClockTime": "0x1B8",
      "CreatorId": "0x188", "DataModelDeleterPointer": "0x73A7090", "DataModelPrimitiveCount": "0x480", "DataModelToRenderView1": "0x1D0",
      "DataModelToRenderView2": "0x8", "DataModelToRenderView3": "0x28", "DecalTexture": "0x198", "Deleter": "0x10", "DeleterBack": "0x18",
      "Dimensions": "0x720", "DisplayName": "0x130", "EvaluateStateMachine": "0x1DD", "FOV": "0x160", "FakeDataModelPointer": "0x73A7088",
      "FakeDataModelToDataModel": "0x1C0", "FogColor": "0xFC", "FogEnd": "0x134", "FogStart": "0x138", "ForceNewAFKDuration": "0x1F8",
      "FramePositionOffsetX": "0x4DC", "FramePositionOffsetY": "0x4E4", "FramePositionX": "0x4D8", "FramePositionY": "0x4E0", "FrameRotation": "0x188",
      "FrameSizeOffsetX": "0x500", "FrameSizeOffsetY": "0x504", "FrameSizeX": "0x4F8", "FrameSizeY": "0x4FC", "GameId": "0x190", "GameLoaded": "0x678",
      "Gravity": "0x958", "Health": "0x194", "HealthDisplayDistance": "0x318", "HipHeight": "0x1A0", "HumanoidDisplayName": "0xD0",
      "HumanoidState": "0x858", "HumanoidStateId": "0x20", "InputObject": "0x100", "InsetMaxX": "0x100", "InsetMaxY": "0x104", "InsetMinX": "0xF8",
      "InsetMinY": "0xFC", "InstanceAttributePointer1": "0x40", "InstanceAttributePointer2": "0x18", "InstanceCapabilities": "0xD08",
      "JobEnd": "0x1D8", "JobId": "0x138", "JobStart": "0x1D0", "Job_Name": "0x18", "JobsPointer": "0x778C2C0", "JumpPower": "0x1B0",
      "LocalPlayer": "0x130", "LocalScriptByteCode": "0x1A8", "LocalScriptBytecodePointer": "0x10", "LocalScriptHash": "0x1B8", "MaterialType": "0x0",
      "MaxHealth": "0x1B4", "MaxSlopeAngle": "0x1B8", "MeshPartColor3": "0x194", "MeshPartTexture": "0x310", "ModelInstance": "0x360",
      "ModuleScriptByteCode": "0x150", "ModuleScriptBytecodePointer": "0x10", "ModuleScriptHash": "0x168", "MoonTextureId": "0xD8",
      "MousePosition": "0xEC", "MouseSensitivity": "0x7389F74", "MoveDirection": "0x158", "Name": "0x80", "NameDisplayDistance": "0x324",
      "NameSize": "0x10", "OnDemandInstance": "0x38", "OutdoorAmbient": "0x108", "Parent": "0x50", "PartSize": "0xFC", "Ping": "0xC8",
      "PlaceId": "0x198", "PlayerConfigurerPointer": "0x7382528", "PlayerMouse": "0xCC8", "Position": "0xB4", "Primitive": "0x150",
      "PrimitiveValidateValue": "0x3919F80", "PrimitivesPointer1": "0x428", "PrimitivesPointer2": "0xDF0", "ProximityPromptActionText": "0xD0",
      "ProximityPromptEnabled": "0x156", "ProximityPromptGamepadKeyCode": "0x13C", "ProximityPromptHoldDuraction": "0x140",
      "ProximityPromptMaxActivationDistance": "0x148", "ProximityPromptMaxObjectText": "0xF0", "RenderJobToDataModel": "0x1B0",
      "RenderJobToFakeDataModel": "0x38", "RenderJobToRenderView": "0x218", "RequireBypass": "0x870", "RigType": "0x1C8",
      "Rotation": "0x98", "RunContext": "0x148", "ScriptContext": "0x3D0", "Sit": "0x1DC", "SkyboxBk": "0x100", "SkyboxDn": "0x128",
      "SkyboxFt": "0x150", "SkyboxLf": "0x178", "SkyboxRt": "0x1A0", "SkyboxUp": "0x1C8", "SoundId": "0xE0", "StarCount": "0x220",
      "StringLength": "0x10", "SunTextureId": "0x1F0", "TagList": "0x0", "TaskSchedulerMaxFPS": "0x1B0", "TaskSchedulerPointer": "0x778C0E8",
      "Team": "0x270", "TeamColor": "0xD0", "TextLabelText": "0xA98", "TextLabelVisible": "0x571", "Tool_Grip_Position": "0x454",
      "Transparency": "0xF0", "UserId": "0x2A8", "Value": "0xD0", "Velocity": "0xC0", "ViewportSize": "0x2E8", "VisualEngine": "0x10",
      "VisualEnginePointer": "0x7109240", "VisualEngineToDataModel1": "0x700", "VisualEngineToDataModel2": "0x1C0", "WalkSpeed": "0x1D4",
      "WalkSpeedCheck": "0x3A0", "Workspace": "0x178", "WorkspaceToWorld": "0x428", "viewmatrix": "0x4B0"
    }
    """
updated_json_string = update_offsets_from_url(offsets_url, json_template)
offsets = json.loads(updated_json_string)
def initialize_controller():
    global joystick
    pygame.init()
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
def is_key_pressed(key_identifier):
    global joystick
    try:
        if isinstance(key_identifier, str):
            if key_identifier.startswith("Controller Button"):
                if not joystick: return False
                pygame.event.pump()
                button_index = int(key_identifier.split(" ")[-1])
                return joystick.get_button(button_index)
            elif key_identifier == "Left Trigger":
                if not joystick: return False
                pygame.event.pump()
                return joystick.get_axis(4) > 0.5
            elif key_identifier == "Right Trigger":
                if not joystick: return False
                pygame.event.pump()
                return joystick.get_axis(5) > 0.5
            else:
                vk_code = VK_CODES.get(key_identifier)
                if vk_code:
                    return (windll.user32.GetAsyncKeyState(vk_code) & 0x8000) != 0
        else:
            return (windll.user32.GetAsyncKeyState(key_identifier) & 0x8000) != 0
    except (ValueError, IndexError, pygame.error):
        return False
    return False
def get_key_name(key_identifier):
    if isinstance(key_identifier, str):
        return key_identifier
    for name, code in VK_CODES.items():
        if code == key_identifier:
            return name
    return f"Key {key_identifier}"
def DRP(address):
    if isinstance(address, str):
        address = int(address, 16)
    return int.from_bytes(pm.read_bytes(address, 8), "little")
def simple_get_processes():
    return [{"Name": i.szExeFile.decode(), "ProcessId": i.th32ProcessID} for i in list_processes()]
def yield_for_program(program_name, printInfo=True):
    try:
        global PID, baseAddr, pm
        for proc in simple_get_processes():
            if proc["Name"] == program_name:
                pm.open_process_from_id(proc["ProcessId"])
                PID = proc["ProcessId"]
                windll.kernel32.OpenProcess(0x1038, False, PID)
                for module in pm.list_modules():
                    if module.name == "RobloxPlayerBeta.exe":
                        baseAddr = module.lpBaseOfDll
                        break
        return False
    except:
        print("Roblox not open bro :c")
def is_process_dead():
    return not pid_exists(PID)
def get_base_addr():
    return baseAddr
def ReadRobloxString(expected_address):
    string_count = pm.read_int(expected_address + 0x10)
    if string_count > 15:
        ptr = DRP(expected_address)
        return pm.read_string(ptr, string_count)
    return pm.read_string(expected_address, string_count)
def GetClassName(instance):
    ptr = pm.read_longlong(instance + 0x18)
    ptr = pm.read_longlong(ptr + 0x8)
    fl = pm.read_longlong(ptr + 0x18)
    if fl == 0x1F:
        ptr = pm.read_longlong(ptr)
    return ReadRobloxString(ptr)
def GetName(instance):
    return ReadRobloxString(DRP(instance + nameOffset))
def GetChildren(instance):
    if not instance:
        return []
    children = []
    start = DRP(instance + childrenOffset)
    if start == 0:
        return []
    end = DRP(start + 8)
    current = DRP(start)
    for _ in range(1000):
        if current == end:
            break
        children.append(pm.read_longlong(current))
        current += 0x10
    return children
def GetAllChildren3(instance):
    if not instance:
        return {}
    children_start = DRP(instance + childrenOffset)
    if not children_start:
        return {}
    children_end = DRP(children_start + 8)
    current_address = DRP(children_start)
    while current_address != children_end:
           try:
            child_instance = pm.read_longlong(current_address)
            current_address += 0x10
            if not child_instance:
                continue
            namec = GetClassName(child_instance)
            if namec == "Players":
                return child_instance
           except:
                continue
    return {}
def FindFirstChild(instance, child_name):
    if not instance:
        return 0
    start = DRP(instance + childrenOffset)
    if start == 0:
        return 0
    end = DRP(start + 8)
    current = DRP(start)
    for _ in range(1000):
        if current == end:
            break
        child = pm.read_longlong(current)
        try:
            if GetName(child) == child_name:
                return child
        except:
            pass
        current += 0x10
    return 0
def FindFirstChildOfClass(instance, class_name):
    if not instance:
        return 0
    start = DRP(instance + childrenOffset)
    if start == 0:
        return 0
    end = DRP(start + 8)
    current = DRP(start)
    for _ in range(1000):
        if current == end:
            break
        child = pm.read_longlong(current)
        try:
            if GetClassName(child) == class_name:
                return child
        except:
            pass
        current += 0x10
    return 0
def find_window_by_title(title):
    return windll.user32.FindWindowW(None, title)
def fast_normalize(vx, vy, vz):
    mag = math.sqrt(vx * vx + vy * vy + vz * vz)
    if mag == 0:
        return 0.0, 0.0, 0.0
    inv = 1.0 / mag
    return vx * inv, vy * inv, vz * inv
def cframe_look_at(fx, fy, fz, tx, ty, tz):
    lx, ly, lz = fast_normalize(tx - fx, ty - fy, tz - fz)
    if abs(ly) > 0.999:
        ux, uy, uz = 0.0, 0.0, -1.0
    else:
        ux, uy, uz = 0.0, 1.0, 0.0
    rx = uy * lz - uz * ly
    ry = uz * lx - ux * lz
    rz = ux * ly - uy * lx
    rx, ry, rz = fast_normalize(rx, ry, rz)
    ux = ly * rz - lz * ry
    uy = lz * rx - lx * rz
    uz = lx * ry - ly * rx
    return lx, ly, lz, ux, uy, uz, rx, ry, rz
def world_to_screen_with_matrix(world_pos, matrix, screen_width, screen_height):
    wx, wy, wz = world_pos
    cx = wx * matrix[0][0] + wy * matrix[0][1] + wz * matrix[0][2] + matrix[0][3]
    cy = wx * matrix[1][0] + wy * matrix[1][1] + wz * matrix[1][2] + matrix[1][3]
    cz = wx * matrix[2][0] + wy * matrix[2][1] + wz * matrix[2][2] + matrix[2][3]
    cw = wx * matrix[3][0] + wy * matrix[3][1] + wz * matrix[3][2] + matrix[3][3]
    if cw == 0:
        return None
    inv_w = 1.0 / cw
    ndc_x = cx * inv_w
    ndc_y = cy * inv_w
    ndc_z = cz * inv_w
    if ndc_z < 0 or ndc_z > 1:
        return None
    x = (ndc_x + 1.0) * 0.5 * screen_width
    y = (1.0 - ndc_y) * 0.5 * screen_height
    return int(x), int(y)
def init():
    global dataModel, wsAddr, camAddr, camCFrameRotAddr, plrsAddr, lpAddr, matrixAddr, camPosAddr, injected, oldfov
    try:
        fakeDatamodel = pm.read_longlong(baseAddr + int(offsets['FakeDataModelPointer'], 16))
        dataModel = pm.read_longlong(fakeDatamodel + int(offsets['FakeDataModelToDataModel'], 16))
        wsAddr = pm.read_longlong(dataModel + int(offsets['Workspace'], 16))
        camAddr = pm.read_longlong(wsAddr + int(offsets['Camera'], 16))
        camCFrameRotAddr = camAddr + int(offsets['CameraRotation'], 16)
        camPosAddr = camAddr + int(offsets['CameraPos'], 16)
        visualEngine = pm.read_longlong(baseAddr + int(offsets['VisualEnginePointer'], 16))
        matrixAddr = visualEngine + int(offsets['viewmatrix'], 16)
        game_tree = GetAllChildren3(dataModel)
        plrsAddr = game_tree
        lpAddr = pm.read_longlong(plrsAddr + int(offsets['LocalPlayer'], 16))
        oldfov = pm.read_float(camAddr + int(offsets["FOV"], 16))
    except:
        print('Error Getting DataModel: Outdated offsets or unsupported game')
        time.sleep(999999)
        return
    if not injected:
        injected = True
    show_main_features()
def keybind_listener():
    global waiting_for_keybind, aimbot_keybind, triggerbot_keybind, joystick,fly_keybind,speed_keybind
    while True:
        time.sleep(0.001)
        if waiting_for_keybind:
            time.sleep(0.3)
            for vk_code in range(1, 256):
                windll.user32.GetAsyncKeyState(vk_code)
            if joystick:
                pygame.event.clear()
            key_found = False
            while waiting_for_keybind and not key_found:
                for name, code in VK_CODES.items():
                    if windll.user32.GetAsyncKeyState(code) & 0x8000:
                        if code == 27:
                            waiting_for_keybind = False
                            break
                        try:
                            if "..." in dpg.get_item_label("keybind_button"):
                                aimbot_keybind = name
                                dpg.configure_item("keybind_button", label=name)
                            elif "..." in dpg.get_item_label("triggerbot_keybind_button"):
                                triggerbot_keybind = name
                                dpg.configure_item("triggerbot_keybind_button", label=name)
                            elif "..." in dpg.get_item_label("fly_keybind_button"):
                                fly_keybind = name
                                dpg.configure_item("fly_keybind_button", label=name)
                            elif "..." in dpg.get_item_label("speed_keybind_button"):
                                speed_keybind = name
                                dpg.configure_item("speed_keybind_button", label=name)
                        except Exception:
                            pass
                        waiting_for_keybind = False
                        key_found = True
                        break
                if key_found: continue
                if joystick:
                    pygame.event.pump()
                    for i in range(joystick.get_numbuttons()):
                        if joystick.get_button(i):
                            button_name = f"Controller Button {i}"
                            try:
                                if "..." in dpg.get_item_label("keybind_button"):
                                    aimbot_keybind = button_name
                                    dpg.configure_item("keybind_button", label=button_name)
                                elif "..." in dpg.get_item_label("triggerbot_keybind_button"):
                                    triggerbot_keybind = button_name
                                    dpg.configure_item("triggerbot_keybind_button", label=button_name)
                                elif "..." in dpg.get_item_label("fly_keybind_button"):
                                    fly_keybind = button_name
                                    dpg.configure_item("fly_keybind_button", label=button_name)
                                elif "..." in dpg.get_item_label("speed_keybind_button"):
                                    speed_keybind = button_name
                                    dpg.configure_item("speed_keybind_button", label=button_name)
                            except Exception:
                                pass
                            waiting_for_keybind = False
                            key_found = True
                            break
                    if key_found: continue
                    if joystick.get_axis(4) > 0.5:
                        trigger_name = "Left Trigger"
                        try:
                            if "..." in dpg.get_item_label("keybind_button"):
                                aimbot_keybind = trigger_name
                                dpg.configure_item("keybind_button", label=trigger_name)
                            elif "..." in dpg.get_item_label("triggerbot_keybind_button"):
                                triggerbot_keybind = trigger_name
                                dpg.configure_item("triggerbot_keybind_button", label=trigger_name)
                            elif "..." in dpg.get_item_label("fly_keybind_button"):
                                fly_keybind = trigger_name
                                dpg.configure_item("fly_keybind_button", label=trigger_name)
                            elif "..." in dpg.get_item_label("speed_keybind_button"):
                                speed_keybind = trigger_name
                                dpg.configure_item("speed_keybind_button", label=trigger_name)
                        except Exception:
                            pass
                        waiting_for_keybind = False
                        key_found = True
                    if not key_found and joystick.get_axis(5) > 0.5:
                        trigger_name = "Right Trigger"
                        try:
                            if "..." in dpg.get_item_label("keybind_button"):
                                aimbot_keybind = trigger_name
                                dpg.configure_item("keybind_button", label=trigger_name)
                            elif "..." in dpg.get_item_label("triggerbot_keybind_button"):
                                triggerbot_keybind = trigger_name
                                dpg.configure_item("triggerbot_keybind_button", label=trigger_name)
                            elif "..." in dpg.get_item_label("fly_keybind_button"):
                                fly_keybind = trigger_name
                                dpg.configure_item("fly_keybind_button", label=trigger_name)
                            elif "..." in dpg.get_item_label("speed_keybind_button"):
                                speed_keybind = trigger_name
                                dpg.configure_item("speed_keybind_button", label=trigger_name)
                        except Exception:
                            pass
                        waiting_for_keybind = False
                        key_found = True
                time.sleep(0.01)
            if not key_found:
                 try:
                    dpg.configure_item("keybind_button", label=get_key_name(aimbot_keybind))
                    dpg.configure_item("triggerbot_keybind_button", label=get_key_name(triggerbot_keybind))
                    dpg.configure_item("fly_keybind_button", label=get_key_name(fly_keybind))
                    dpg.configure_item("speed_keybind_button", label=get_key_name(speed_keybind))
                 except:
                    pass
        else:
            time.sleep(0.1)
threading.Thread(target=keybind_listener, daemon=True).start()
newtrg = 0
isvis = False
Enemy = 0
fly_enabled = False
fly_mode = "Hold"
fly_toggled = False
fly_speed = 20.0
fly_thread = None
fly_active = False
speed_mode = "Hold"
speed_toggled = False
speed_thread = None
class FlyThread(threading.Thread):
    def __init__(self, pm, base, offsets):
        super().__init__(daemon=True)
        self.pm = pm
        self.base = base
        self.offsets = offsets
        self.running = True
        self.datamodel = 0
        self.playersS = 0
        self.zero_bytes = array([0.0, 0.0, 0.0], dtype=float32).tobytes()
    def run(self):
        while self.running:
            self.datamodel = dataModel
            global fly_enabled, fly_keybind, fly_mode, fly_toggled, fly_speed, fly_active
            time.sleep(0.0000001)
            if not fly_enabled:
                time.sleep(0.1)
                continue
            key_pressed = is_key_pressed(fly_keybind)
            if fly_mode == "Toggle":
                if key_pressed and not fly_active:
                    fly_toggled = not fly_toggled
                    fly_active = True
                elif not key_pressed:
                    fly_active = False
                should_fly = fly_toggled
            else:
                should_fly = key_pressed
            if not should_fly:
                time.sleep(0.00001)
                continue
            try:
                lp = self.pm.read_longlong(plrsAddr + int(self.offsets['LocalPlayer'], 16))
                ch = lp and self.pm.read_longlong(lp + int(self.offsets['ModelInstance'], 16))
                hr = ch and self.find_first_child(ch, "HumanoidRootPart")
                pr = hr and self.pm.read_longlong(hr + int(self.offsets['Primitive'], 16))
                ws = self.pm.read_longlong(self.datamodel + int(self.offsets['Workspace'], 16))
                ca = ws and self.pm.read_longlong(ws + int(self.offsets['Camera'], 16))
                if not all((lp, ch, hr, pr, ws, ca)):
                    time.sleep(0.00001)
                    continue
                cam_rot_addr = ca + int(self.offsets['CameraRotation'], 16)
                cam_matrix = []
                for i in range(9):
                    addr = cam_rot_addr + (i % 3) * 4 + (i // 3) * 12
                    cam_matrix.append(self.pm.read_float(addr))
                look = array([-cam_matrix[2], -cam_matrix[5], -cam_matrix[8]], dtype=float32)
                right = array([cam_matrix[0], cam_matrix[3], cam_matrix[6]], dtype=float32)
                mv = array([0.0, 0.0, 0.0], dtype=float32)
                if windll.user32.GetAsyncKeyState(87) & 0x8000:
                    mv += look
                if windll.user32.GetAsyncKeyState(83) & 0x8000:
                    mv -= look
                if windll.user32.GetAsyncKeyState(65) & 0x8000:
                    mv -= right
                if windll.user32.GetAsyncKeyState(68) & 0x8000:
                    mv += right
                if windll.user32.GetAsyncKeyState(32) & 0x8000:
                    mv[1] += 1.0
                norm = linalg.norm(mv)
                if norm > 0:
                    mv = mv / norm * fly_speed * 2
                vel_addr = pr + int(self.offsets['Velocity'], 16)
                self.pm.write_float(vel_addr, float(mv[0]))
                self.pm.write_float(vel_addr + 4, float(mv[1]))
                self.pm.write_float(vel_addr + 8, float(mv[2]))
            except Exception:
                pass
    def stop(self):
        self.running = False
    def get_children(self, inst):
        children = []
        try:
            start = self.pm.read_longlong(inst + childrenOffset)
            if start == 0:
                return []
            end = self.pm.read_longlong(start + 8)
            current = self.pm.read_longlong(start)
            for _ in range(1000):
                if current == end:
                    break
                children.append(self.pm.read_longlong(current))
                current += 0x10
        except:
            pass
        return children
    def get_class_name(self, inst):
        try:
            ptr = self.pm.read_longlong(inst + 0x18)
            ptr = self.pm.read_longlong(ptr + 0x8)
            fl = self.pm.read_longlong(ptr + 0x18)
            if fl == 0x1F:
                ptr = self.pm.read_longlong(ptr)
            return ReadRobloxString(ptr)
        except:
            return ""
    def find_first_child(self, parent, target):
        for c in self.get_children(parent):
            try:
                if GetName(c) == target:
                    return c
            except:
                pass
        return
class SpeedThread(threading.Thread):
    def __init__(self, pm, base, offsets):
        super().__init__(daemon=True)
        self.pm = pm
        self.base = base
        self.offsets = offsets
        self.running = True
        self.datamodel = 0
        self.playersS = 0
        self.zero_bytes = array([0.0, 0.0, 0.0], dtype=float32).tobytes()
    def run(self):
        while self.running:
            self.datamodel = dataModel
            global speed_enabled, speed_keybind, speed_mode, speed_toggled, speed, fly_active
            time.sleep(0.0000001)
            if not speed_enabled:
                time.sleep(0.1)
                continue
            key_pressed = is_key_pressed(speed_keybind)
            speed_fly = key_pressed
            if not speed_fly:
                time.sleep(0.00001)
                continue
            try:
                lp = self.pm.read_longlong(plrsAddr + int(self.offsets['LocalPlayer'], 16))
                ch = lp and self.pm.read_longlong(lp + int(self.offsets['ModelInstance'], 16))
                hr = ch and self.find_first_child(ch, "HumanoidRootPart")
                pr = hr and self.pm.read_longlong(hr + int(self.offsets['Primitive'], 16))
                ws = self.pm.read_longlong(self.datamodel + int(self.offsets['Workspace'], 16))
                ca = ws and self.pm.read_longlong(ws + int(self.offsets['Camera'], 16))
                if not all((lp, ch, hr, pr, ws, ca)):
                    time.sleep(0.00001)
                    continue
                cam_rot_addr = ca + int(self.offsets['CameraRotation'], 16)
                cam_matrix = []
                for i in range(9):
                    addr = cam_rot_addr + (i % 3) * 4 + (i // 3) * 12
                    cam_matrix.append(self.pm.read_float(addr))
                look = array([-cam_matrix[2], -cam_matrix[5], -cam_matrix[8]], dtype=float32)
                right = array([cam_matrix[0], cam_matrix[3], cam_matrix[6]], dtype=float32)
                mv = array([0.0, 0.0, 0.0], dtype=float32)
                if windll.user32.GetAsyncKeyState(87) & 0x8000:
                    mv += look
                if windll.user32.GetAsyncKeyState(83) & 0x8000:
                    mv -= look
                if windll.user32.GetAsyncKeyState(65) & 0x8000:
                    mv -= right
                if windll.user32.GetAsyncKeyState(68) & 0x8000:
                    mv += right
                if windll.user32.GetAsyncKeyState(32) & 0x8000:
                    mv[1] += 1.0
                norm = linalg.norm(mv)
                if norm > 0:
                    mv = mv / norm * speed * 2
                vel_addr = pr + int(self.offsets['Velocity'], 16)
                self.pm.write_float(vel_addr, float(mv[0]))
                self.pm.write_float(vel_addr + 8, float(mv[2]))
            except Exception:
                pass
    def stop(self):
        self.running = False
    def get_children(self, inst):
        children = []
        try:
            start = self.pm.read_longlong(inst + childrenOffset)
            if start == 0:
                return []
            end = self.pm.read_longlong(start + 8)
            current = self.pm.read_longlong(start)
            for _ in range(1000):
                if current == end:
                    break
                children.append(self.pm.read_longlong(current))
                current += 0x10
        except:
            pass
        return children
    def get_class_name(self, inst):
        try:
            ptr = self.pm.read_longlong(inst + 0x18)
            ptr = self.pm.read_longlong(ptr + 0x8)
            fl = self.pm.read_longlong(ptr + 0x18)
            if fl == 0x1F:
                ptr = self.pm.read_longlong(ptr)
            return ReadRobloxString(ptr)
        except:
            return ""
    def find_first_child(self, parent, target):
        for c in self.get_children(parent):
            try:
                if GetName(c) == target:
                    return c
            except:
                pass
        return 0
def aimbotLoop():
    global target, lockedplr, aimbot_fov, newtrg, aimbot_type, swidth, sheight, Enemy, isvis
    newtrg = 0
    last_scan = 0

    while True:
        try:
     
            if aimbot_type != "Memory" or not aimbot_enabled:
                time.sleep(1)
                continue

            should_aim = is_key_pressed(aimbot_keybind)

       
            if not should_aim and time.time() - last_scan > 0.0001:
                last_scan = time.time()
                mymodel = pm.read_longlong(lpAddr + int(offsets["ModelInstance"], 16))
                mypart = FindFirstChild(mymodel, "HumanoidRootPart")
                if not mypart:
                    continue

                primitive1 = pm.read_longlong(mypart + int(offsets['Primitive'], 16))
                targetPos1 = primitive1 + int(offsets['Position'], 16)
                my_pos = np.array([
                    pm.read_float(targetPos1),
                    pm.read_float(targetPos1 + 4),
                    pm.read_float(targetPos1 + 8)
                ], dtype=np.float32)

                if matrixAddr > 0:
                    matrix_flat = [pm.read_float(matrixAddr + i * 4) for i in range(16)]
                    view_proj_matrix = np.reshape(np.array(matrix_flat, dtype=np.float32), (4, 4))
                    widthCenter, heightCenter = swidth / 2, sheight / 2
                    minDistance = float('inf')

                    for v in GetChildren(plrsAddr):
                        if v == lpAddr:
                            continue
                        char = pm.read_longlong(v + int(offsets['ModelInstance'], 16))
                        hitpart = FindFirstChild(char, aimbot_hitpart)
                        hum = FindFirstChildOfClass(char, 'Humanoid')
                        if not (hitpart and hum):
                            continue

                        health = pm.read_float(hum + int(offsets['Health'], 16))
                        if aimbot_ignoredead and health <= 0:
                            continue

                        primitive = pm.read_longlong(hitpart + int(offsets['Primitive'], 16))
                        targetPos = primitive + int(offsets['Position'], 16)
                        obj_pos = np.array([
                            pm.read_float(targetPos),
                            pm.read_float(targetPos + 4),
                            pm.read_float(targetPos + 8)
                        ], dtype=np.float32)

                        if np.linalg.norm(my_pos - obj_pos) >= 1000:
                            continue

                        screen_coords = world_to_screen_with_matrix(obj_pos, view_proj_matrix, swidth, sheight)
                        if screen_coords and screen_coords != (-1, -1):
                            distance = math.sqrt((widthCenter - screen_coords[0]) ** 2 + (heightCenter - screen_coords[1]) ** 2)
                            if distance <= aimbot_fov and distance < minDistance:
                                minDistance = distance
                                target = targetPos
                                Enemy = v
                                lockedplr = v
                                newtrg = hum

          
            if should_aim and target > 0 and matrixAddr > 0:
                
                health = pm.read_float(newtrg + int(offsets['Health'], 16))
                if health <= 0:
                    newtrg = target = lockedplr = Enemy = 0
                    continue

                cam_pos = [
                    pm.read_float(camPosAddr),
                    pm.read_float(camPosAddr + 4),
                    pm.read_float(camPosAddr + 8)
                ]
                head_pos = [
                    pm.read_float(target),
                    pm.read_float(target + 4),
                    pm.read_float(target + 8)
                ]

                lx, ly, lz, ux, uy, uz, rx, ry, rz = cframe_look_at(
                    cam_pos[0], cam_pos[1], cam_pos[2],
                    head_pos[0], head_pos[1], head_pos[2]
                )

                pm.write_float(camCFrameRotAddr + 0,  -rx)
                pm.write_float(camCFrameRotAddr + 4,   ux)
                pm.write_float(camCFrameRotAddr + 8,  -lx)
                pm.write_float(camCFrameRotAddr + 12, -ry)
                pm.write_float(camCFrameRotAddr + 16,  uy)
                pm.write_float(camCFrameRotAddr + 20, -ly)
                pm.write_float(camCFrameRotAddr + 24, -rz)
                pm.write_float(camCFrameRotAddr + 28,  uz)
                pm.write_float(camCFrameRotAddr + 32, -lz)

 
            if not should_aim and target == 0:
                target = lockedplr = newtrg = Enemy = 0

        except:
            continue


scnpos = 0
aimbot_sens = 1
def aimbotLoop2d():
    global aimbot_sens, target, lockedplr, aimbot_fov, newtrg, scnpos, aimbot_smoothness_value, aimbot_smoothness_enabled, aimbot_type, Enemy, isvis, Humanization_enabled, aimbot_enabled, matrixAddr, pm, offsets, aimbot_prediction_enabled, aimbot_prediction_x, aimbot_prediction_y, aimbot_keybind, lpAddr, aimbot_ignoreteam, aimbot_ignoredead, aimbot_hitpart, plrsAddr
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD), ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.c_ulonglong)]
    class INPUT_union(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    class INPUT(ctypes.Structure):
        _fields_ = [("type", wintypes.DWORD), ("union", INPUT_union)]
    SendInput = ctypes.windll.user32.SendInput
    SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
    SendInput.restype = wintypes.UINT
    def send_rel_mouse_move(dx, dy, no_coalesce=True):
        if dx == 0 and dy == 0: return 
        flags = MOUSEEVENTF_MOVE | (MOUSEEVENTF_MOVE_NOCOALESCE if no_coalesce else 0)
        mi = MOUSEINPUT(int(dx), int(dy), 0, int(flags), 0, 0)
        inp = INPUT(0, INPUT_union(mi=mi))
        SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
    easings = {'linear': lambda t: t, 'ease_in': lambda t: t * t, 'ease_out': lambda t: t * (2 - t), 'ease_in_out': lambda t: 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t, 'curve': lambda t: t ** 3}
    easing_func = easings['linear']
    def smooth_move_by(dx, dy, smoothing=None, easing=easing_func):
        if dx == 0 and dy == 0: return
        smoothing = int(max(1, min(200, smoothing if smoothing is not None else aimbot_smoothness_value)))
        duration = max(0.0001, smoothing / 2500.0)
        steps = max(2, smoothing)
        last_x, last_y = 0.0, 0.0
        start = time.perf_counter()
        for i in range(1, steps + 1):
            t = i / steps
            e = easing(t)
            cur_x, cur_y = dx * e, dy * e
            step_x, step_y = int(round(cur_x - last_x)), int(round(cur_y - last_y))
            if step_x != 0 or step_y != 0:
                send_rel_mouse_move(step_x, step_y)
            last_x += step_x
            last_y += step_y
            sleep_for = (start + duration * t) - time.perf_counter()
            if sleep_for > 0:
                time.sleep(sleep_for)
    newtrg = scnpos = 0
    while True:
        try:
            time.sleep(0.0007)
            if aimbot_type != "Mouse" or not aimbot_enabled:
                time.sleep(1)
                continue
            should_aim = is_key_pressed(aimbot_keybind)
            if should_aim and target > 0 and matrixAddr > 0:
                hp = pm.read_float(newtrg + int(offsets['Health'], 16))
                if hp <= 0:
                    Enemy = scnpos = target = lockedplr = newtrg = 0
                    continue
                matrix_flat = [pm.read_float(matrixAddr + i * 4) for i in range(16)]
                view_proj_matrix = np.reshape(array(matrix_flat, dtype=float32), (4, 4))
                to_pos = array([pm.read_float(target), pm.read_float(target + 4), pm.read_float(target + 8)], dtype=float32)
                if aimbot_prediction_enabled:
                    try:
                        velocity_offset = target - int(offsets['Position'], 16) + int(offsets['Velocity'], 16)
                        velocity = [pm.read_float(velocity_offset + i * 4) for i in range(3)]
                        to_pos += np.array([velocity[0] * aimbot_prediction_x, velocity[1] * aimbot_prediction_y, 0])
                    except Exception:
                        pass
                screen_coords = world_to_screen_with_matrix(to_pos, view_proj_matrix, swidth, sheight)
                if screen_coords and screen_coords != (-1, -1):
                    current_mouse_x, current_mouse_y = win32api.GetCursorPos()
                    dx, dy = screen_coords[0] - current_mouse_x, screen_coords[1] - current_mouse_y
                    
                    
                    move_x = dx * aimbot_sens
                    move_y = dy * aimbot_sens

             
                

                    if aimbot_smoothness_enabled:
                        smooth_move_by(int(move_x), int(move_y))
                    else:
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(move_x), int(move_y), 0, 0)

            else:
                target = lockedplr = newtrg = scnpos = Enemy = 0
                if not find_window_by_title("Roblox") or matrixAddr <= 0:
                    time.sleep(0.1)
                    continue
                matrix_flat = [pm.read_float(matrixAddr + i * 4) for i in range(16)]
                view_proj_matrix = np.reshape(array(matrix_flat, dtype=float32), (4, 4))
                widthCenter, heightCenter = swidth / 2, sheight / 2
                minDistance = float('inf')
                for v in GetChildren(plrsAddr):
                    try:
                        if v == lpAddr:
                            continue
                        char = pm.read_longlong(v + int(offsets['ModelInstance'], 16))
                        hum = FindFirstChildOfClass(char, 'Humanoid')
                        if not hum or (aimbot_ignoredead and pm.read_float(hum + int(offsets['Health'], 16)) <= 0):
                            continue
                        targetPos = None
                        selected_part = None
                        if Humanization_enabled:
                            possible_parts = []
                            for part_name in ["HumanoidRootPart", "Head"]:
                                part_inst = FindFirstChild(char, part_name)
                                if part_inst:
                                    primitive = pm.read_longlong(part_inst + int(offsets['Primitive'], 16))
                                    possible_parts.append((primitive + int(offsets['Position'], 16), part_inst))
                            if possible_parts:
                                min_screen_dist = float('inf')
                                for pos, part_inst in possible_parts:
                                    part_pos = array([pm.read_float(pos), pm.read_float(pos + 4), pm.read_float(pos + 8)], dtype=float32)
                                    screen_coords = world_to_screen_with_matrix(part_pos, view_proj_matrix, swidth, sheight)
                                    if screen_coords and screen_coords != (-1, -1):
                                        dist = math.sqrt((widthCenter - screen_coords[0]) ** 2 + (heightCenter - screen_coords[1]) ** 2)
                                        if dist < min_screen_dist:
                                            min_screen_dist = dist
                                            targetPos, selected_part = pos, part_inst
                        else:
                            selected_part = FindFirstChild(char, aimbot_hitpart)
                            if selected_part:
                                primitive = pm.read_longlong(selected_part + int(offsets['Primitive'], 16))
                                targetPos = primitive + int(offsets['Position'], 16)
                        if not selected_part or not targetPos:
                            continue
                        mymodel = pm.read_longlong(lpAddr + int(offsets["ModelInstance"], 16))
                        mypart = FindFirstChild(mymodel, "HumanoidRootPart")
                        primitive1 = pm.read_longlong(mypart + int(offsets['Primitive'], 16))
                        targetPos1 = primitive1 + int(offsets['Position'], 16)
                        my_pos = array([pm.read_float(targetPos1 + i * 4) for i in range(3)], dtype=float32)
                        obj_pos = array([pm.read_float(targetPos + i * 4) for i in range(3)], dtype=float32)
                        if linalg.norm(my_pos - obj_pos) >= 1000:
                            continue
                        predicted_pos = obj_pos
                        if aimbot_prediction_enabled:
                            primitive = pm.read_longlong(selected_part + int(offsets['Primitive'], 16))
                            velocity_offset = primitive + int(offsets['Velocity'], 16)
                            velocity = [pm.read_float(velocity_offset + i * 4) for i in range(3)]
                            predicted_pos += np.array([velocity[0] * aimbot_prediction_x, velocity[1] * aimbot_prediction_y, 0])
                        screen_coords = world_to_screen_with_matrix(predicted_pos, view_proj_matrix, swidth, sheight)
                        if not screen_coords or screen_coords == (-1, -1):
                            continue
                        mouse_x, mouse_y = win32api.GetCursorPos()
                        screen_distance = math.sqrt((mouse_x - screen_coords[0]) ** 2 + (mouse_y - screen_coords[1]) ** 2)
                        if screen_distance <= aimbot_fov and screen_distance < minDistance:
                            minDistance = screen_distance
                            target, scnpos, lockedplr, newtrg, Enemy = targetPos, screen_coords, v, hum, v
                    except Exception:
                        continue
        except Exception:
            target = lockedplr = newtrg = scnpos = Enemy = 0
            continue
def aimbot_callback(sender, app_data):
    global aimbot_enabled
    if not injected: return
    aimbot_enabled = app_data
def fovfill_callback(sender, app_data):
    global fovfill
    fovfill = app_data
def fovglow_callback(sender, app_data):
    global fovglow
    fovglow = app_data
def esp_fov_callback(sender, app_data):
    global fovtoggle
    fovtoggle = app_data
def fly_callback(sender, app_data):
    global fly_enabled
    fly_enabled = app_data
def fovoutline_callback(sender, app_data):
    global fovoutline
    fovoutline = app_data
def aimbot_ignoreteam_callback(sender, app_data):
    global aimbot_ignoreteam
    aimbot_ignoreteam = app_data
def aimbot_humer_callback(sender, app_data):
    global Humanization_enabled
    Humanization_enabled = app_data
def aimbot_ignoredead_callback(sender, app_data):
    global aimbot_ignoredead
    aimbot_ignoredead = app_data
def aimbot_smoothness_callback(sender, app_data):
    global aimbot_smoothness_enabled
    aimbot_smoothness_enabled = app_data
def op_callback(sender, app_data):
    global opamount
    opamount = int(app_data)
def fly_speed_callback(sender, app_data):
    global fly_speed
    fly_speed = float(app_data)
def speed_enabled_callback(sender, app_data):
    global speed_enabled
    speed_enabled = app_data
def speed_value_callback(sender, app_data):
    global speed
    speed = float(app_data)
def smoothness_value_callback(sender, app_data):
    global aimbot_smoothness_value
    aimbot_smoothness_value = app_data
def sens_value_callback(sender, app_data):
    global aimbot_sens
    aimbot_sens = app_data
def fovglowamount_callback(sender, app_data):
    global fovglowamount
    fovglowamount = app_data
def keybind_callback():
    global waiting_for_keybind
    if not waiting_for_keybind:
        waiting_for_keybind = True
        dpg.configure_item("keybind_button", label="...")
def inject_callback():
    init()
def show_main_features():
    dpg.show_item("aimbot_hitpart_combo")
    dpg.show_item("aimbot_prediction_checkbox")
def aimbot_hitpart_callback(sender, app_data):
    global aimbot_hitpart
    aimbot_hitpart = app_data
def change_shape(sender, app_data):
    global shape
    shape = app_data
def aimbot_mouse_callback(sender, app_data):
    global aimbot_type
    aimbot_type = app_data
def aimbot_prediction_checkbox(sender, app_data):
    global aimbot_prediction_enabled
    aimbot_prediction_enabled = app_data
def prediction_x_callback(sender, app_data):
    global aimbot_prediction_x
    aimbot_prediction_x = app_data
def setfov_callback(sender, app_data):
    global aimbot_fov
    aimbot_fov = app_data * 2
def prediction_y_callback(sender, app_data):
    global aimbot_prediction_y
    aimbot_prediction_y = app_data
def triggerbot_keybind_callback():
    global waiting_for_keybind
    if not waiting_for_keybind:
        waiting_for_keybind = True
        dpg.configure_item("triggerbot_keybind_button", label="...")
def fly_keybind_callback():
    global waiting_for_keybind
    if not waiting_for_keybind:
        waiting_for_keybind = True
        dpg.configure_item("fly_keybind_button", label="...")
def speed_keybind_callback():
    global waiting_for_keybind
    if not waiting_for_keybind:
        waiting_for_keybind = True
        dpg.configure_item("speed_keybind_button", label="...")
def get_configs_directory():
    home_dir = os.path.expanduser('~')
    config_dir = os.path.join(home_dir, ".pymidnightconfig")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir
def get_config_files():
    config_dir = get_configs_directory()
    if not os.path.exists(config_dir):
        return []
    files = [f.replace('.json', '') for f in os.listdir(config_dir) if f.endswith('.json') and f != 'login.json']
    return files
def refresh_config_list():
    configs = get_config_files()
    dpg.configure_item("config_dropdown", items=configs)
def create_config_callback():
    new_name = dpg.get_value("new_config_name_input")
    if not new_name or not new_name.strip():
        return
    safe_name = "".join(c for c in new_name if c.isalnum() or c in (' ', '_', '-')).rstrip()
    if not safe_name:
        return
    filepath = os.path.join(get_configs_directory(), f"{safe_name}.json")
    if os.path.exists(filepath):
        return
    if save_config_to_file(filepath):
        refresh_config_list()
        dpg.set_value("config_dropdown", safe_name)
        dpg.set_value("new_config_name_input", "")
def load_selected_config():
    global keybind_bg_color, keybind_line_color, keybind_text_color, theme
    config_name = dpg.get_value("config_dropdown")
    if not config_name:
        return
    filepath = os.path.join(get_configs_directory(), f"{config_name}.json")
    load_config_from_file(filepath)
    if theme == "Pink":
        apply_purpleish_pink_theme()
        keybind_bg_color = [35, 35, 45]
        keybind_line_color = [180, 100, 255]
        keybind_text_color = [220, 220, 230]
    elif theme == "White":
        apply_white_and_grey_theme()
        keybind_bg_color = [220, 220, 220]
        keybind_line_color = [140, 140, 140]
        keybind_text_color = [20, 20, 20]
    elif theme == "Black":
        apply_black_and_white_theme()
        keybind_bg_color = [30, 30, 30]
        keybind_line_color = [80, 80, 80]
        keybind_text_color = [240, 240, 240]
    elif theme == "Blue":
        apply_blueish_cyan_theme()
        keybind_bg_color = [35, 45, 55]
        keybind_line_color = [100, 150, 200]
        keybind_text_color = [220, 230, 240]
def save_selected_config():
    config_name = dpg.get_value("config_dropdown")
    if not config_name:
        print("No config selected to save to.")
        return
    filepath = os.path.join(get_configs_directory(), f"{config_name}.json")
    save_config_to_file(filepath)
def open_config_folder():
    os.startfile(get_configs_directory())
def save_config_to_file(filepath):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        config = {
            "aimbot": {
                "type": aimbot_type, "enabled": aimbot_enabled, "keybind": aimbot_keybind, "fov": aimbot_fov,
                "hitpart": aimbot_hitpart, "ignore_team": aimbot_ignoreteam, "ignore_dead": aimbot_ignoredead,
                "smoothness_enabled": aimbot_smoothness_enabled, "smoothness_value": aimbot_smoothness_value,
                "prediction_enabled": aimbot_prediction_enabled, "prediction_x": aimbot_prediction_x,
                "prediction_y": aimbot_prediction_y, "hum": Humanization_enabled, "flyk": fly_keybind,
                "flye": fly_enabled, "flya": fly_speed,"sens": aimbot_sens,
            },
            "esp": {
                "fovfill": fovfill, "fovglow": fovglow, "fov": fovtoggle, "fc": fovColor,
                "shape": shape, "fovout": fovoutline, "opa": opamount, "fovgl": fovglowamount,
                "show_box": global_show_box, "show_skeleton": global_show_skeleton,
                "show_name": global_show_name, "show_health": global_show_health,
                "show_distance": global_show_distance, "box_color": global_box_color,
                "dis_color": global_dis_color, "name_color": global_name_color,
                "health_color": global_health_color, "head_color": global_head_color,
                "skelly_color": global_skelly_color, "dead": global_aimbot_ignoredead,
                "team": global_IgnoreTeam, "fps": overlay_fps, "keybind": global_show_keybinds
            },
            "menuu": {
                "key": triggerbot_keybind, "them": theme
            }
        }
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        return False
def load_config_from_file(filepath):
    global aimbot_enabled, aimbot_keybind, aimbot_fov, aimbot_hitpart, aimbot_ignoreteam, aimbot_ignoredead
    global aimbot_smoothness_enabled, aimbot_smoothness_value, aimbot_prediction_enabled, aimbot_prediction_x, aimbot_prediction_y
    global triggerbot_keybind, fovtoggle, fovfill, fovglow, fovColor, shape, Humanization_enabled
    global fovglowamount, opamount, fovoutline, theme, aimbot_type, fly_speed, fly_enabled, fly_keybind
    global global_show_box, global_show_skeleton, global_show_name, global_show_health, global_show_distance
    global global_box_color, global_dis_color, global_name_color, global_health_color, global_head_color, global_skelly_color,global_aimbot_ignoredead,global_IgnoreTeam,aimbot_sens,overlay_fps,global_show_keybinds
    try:
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'r') as f:
            config = json.load(f)
        if "aimbot" in config:
            aimbot_config = config["aimbot"]
            aimbot_type = aimbot_config.get("type", "Mouse")
            aimbot_sens = aimbot_config.get("sens",1.0)
            aimbot_enabled = aimbot_config.get("enabled", False)
            aimbot_keybind = aimbot_config.get("keybind", 'Right Mouse')
            fly_speed = aimbot_config.get("flya", 50)
            fly_enabled = aimbot_config.get("flye", False)
            fly_keybind = aimbot_config.get("flyk", "Q")
            aimbot_fov = aimbot_config.get("fov", 50)
            aimbot_hitpart = aimbot_config.get("hitpart", "Head")
            aimbot_ignoreteam = aimbot_config.get("ignore_team", False)
            aimbot_ignoredead = aimbot_config.get("ignore_dead", False)
            aimbot_smoothness_enabled = aimbot_config.get("smoothness_enabled", False)
            aimbot_smoothness_value = aimbot_config.get("smoothness_value", 1)
            aimbot_prediction_enabled = aimbot_config.get("prediction_enabled", False)
            aimbot_prediction_x = aimbot_config.get("prediction_x", 0)
            aimbot_prediction_y = aimbot_config.get("prediction_y", 0)
            Humanization_enabled = aimbot_config.get("hum", False)
        if "esp" in config:
            esp_config = config["esp"]
            fovtoggle = esp_config.get("fov", False)
            fovfill = esp_config.get("fovfill", False)
            fovglow = esp_config.get("fovglow", False)
            fovColor = esp_config.get("fc", [255, 255, 255, 255])
            shape = esp_config.get("shape", "circle")
            fovglowamount = esp_config.get("fovgl", 10)
            opamount = esp_config.get("opa", 255)
            fovoutline = esp_config.get("fovout", False)
            global_show_box = esp_config.get("show_box", False)
            global_show_skeleton = esp_config.get("show_skeleton", False)
            global_show_name = esp_config.get("show_name", False)
            global_show_health = esp_config.get("show_health", False)
            global_show_distance = esp_config.get("show_distance", False)
            global_box_color = esp_config.get("box_color", [255, 0, 0, 255])
            global_dis_color = esp_config.get("dis_color", [0, 255, 0, 255])
            global_name_color = esp_config.get("name_color", [0, 0, 255, 255])
            global_health_color = esp_config.get("health_color", [255, 255, 0, 255])
            global_head_color = esp_config.get("head_color", [255, 0, 255, 255])
            global_skelly_color = esp_config.get("skelly_color", [0, 255, 255, 255])
            global_aimbot_ignoredead = esp_config.get("dead",False)
            global_IgnoreTeam =  esp_config.get("team",False)
            overlay_fps = esp_config.get("fps",240)
            global_show_keybinds = esp_config.get("keybind",False)
        if "menuu" in config:
            menu_config = config["menuu"]
            triggerbot_keybind = menu_config.get("key", 'Delete')
            theme = menu_config.get("them", "Pink")
        update_gui_from_config()
        return True
    except Exception as e:
        print(f"Error loading config from {filepath}: {e}")
        return False
def update_gui_from_config():
    dpg.set_value("esp_ignoredead_checkbox",global_aimbot_ignoredead)
    dpg.set_value("esp_ignoreteam_checkbox",global_IgnoreTeam)
    dpg.set_value("aimbot_checkbox", aimbot_enabled)
    dpg.set_value("keybindlist", global_show_keybinds)
    dpg.set_value("sens_slider", aimbot_sens)
    dpg.set_value("overlay_fps_slider", overlay_fps)
    dpg.configure_item("keybind_button", label=f"{get_key_name(aimbot_keybind)}")
    dpg.set_value("aimbot_hitpart_combo", aimbot_hitpart)
    dpg.set_value("move_fly", fly_enabled)
    dpg.set_value("move_speed", fly_speed)
    dpg.set_value("aimbotfov_slider", aimbot_fov / 2)
    dpg.set_value("aimbot_ignoreteam_checkbox", aimbot_ignoreteam)
    dpg.set_value("aimbot_ignoredead_checkbox", aimbot_ignoredead)
    dpg.set_value("aimbot_smoothness_checkbox", aimbot_smoothness_enabled)
    dpg.set_value("smoothness_slider", aimbot_smoothness_value)
    dpg.set_value("aimbot_prediction_checkbox", aimbot_prediction_enabled)
    dpg.set_value("prediction_x_slider", aimbot_prediction_x)
    dpg.set_value("prediction_y_slider", aimbot_prediction_y)
    dpg.set_value("aimbot_option", aimbot_type)
    dpg.set_value("aimbot_hum_checkbox", Humanization_enabled)
    dpg.set_value("op_buffer", opamount)
    dpg.set_value("glow_buffer", fovglowamount)
    dpg.set_value("esp_outline", fovoutline)
    dpg.set_value("themer", theme)
    dpg.set_value("esp_fov", fovtoggle)
    dpg.set_value("esp_fovfill", fovfill)
    dpg.set_value("esp_fovglow", fovglow)
    dpg.set_value("fover_option", shape)
    dpg.set_value("fc", fovColor)
    dpg.configure_item("fly_keybind_button", label=f"{get_key_name(fly_keybind)}")
    dpg.configure_item("triggerbot_keybind_button", label=f"{get_key_name(triggerbot_keybind)}")
    dpg.set_value("esp_box_toggle", global_show_box)
    dpg.set_value("esp_skeleton_toggle", global_show_skeleton)
    dpg.set_value("esp_name_toggle", global_show_name)
    dpg.set_value("esp_health_toggle", global_show_health)
    dpg.set_value("esp_distance_toggle", global_show_distance)
    dpg.set_value("box_color_picker", global_box_color)
    dpg.set_value("dis_color_picker", global_dis_color)
    dpg.set_value("name_color_picker", global_name_color)
    dpg.set_value("health_color_picker", global_health_color)
    dpg.set_value("head_color_picker", global_head_color)
    dpg.set_value("skelly_color_picker", global_skelly_color)
esp_instance = None
esp_app = None
fovColor = [255, 255, 255, 255]
def update_fov_color(sender, app_data, user_data):
    if all(isinstance(c, float) and 0 <= c <= 1 for c in app_data):
        fovColor[:] = [int(c * 255) for c in app_data]
    else:
        fovColor[:] = list(app_data)
def background_process_monitor():
    global baseAddr
    try:
        while True:
            if is_process_dead():
                while not yield_for_program("RobloxPlayerBeta.exe"):
                    time.sleep(0.5)
                baseAddr = get_base_addr()
            time.sleep(0.1)
    except:
        print("Roblox isn't currently running.")
threading.Thread(target=background_process_monitor, daemon=True).start()
def apply_purpleish_pink_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 25, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (25, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (25, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 60, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (30, 30, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (30, 30, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (35, 30, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (60, 50, 75, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 60, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (80, 70, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (90, 80, 110, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 70, 100, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (180, 100, 255, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 120, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (25, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (60, 50, 75, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (70, 60, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (120, 80, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (30, 30, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (80, 70, 100, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (90, 80, 110, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (100, 90, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (120, 80, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (150, 100, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (80, 80, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (120, 100, 140, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (40, 35, 50, 180))
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 0)
    dpg.bind_theme(global_theme)
def apply_white_and_grey_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 240, 240, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (230, 230, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (20, 20, 20, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 200, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (220, 220, 220, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (210, 210, 210, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (220, 220, 220, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (220, 220, 220, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (200, 200, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (200, 200, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (180, 180, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (190, 190, 190, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (170, 170, 170, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (180, 180, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (160, 160, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (230, 230, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (200, 200, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (180, 180, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (80, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (230, 230, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (180, 180, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (160, 160, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (140, 140, 140, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (120, 120, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (100, 100, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (150, 150, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (180, 180, 180, 150))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (20, 20, 20, 180))
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 0)
    dpg.bind_theme(global_theme)
def apply_black_and_white_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (10, 10, 10, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (20, 20, 20, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (15, 15, 15, 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (25, 25, 25, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 240, 240, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (80, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (40, 40, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (20, 20, 20, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (20, 20, 20, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (50, 50, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 70, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (60, 60, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (80, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 60, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 100, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (50, 50, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (70, 70, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (230, 230, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (30, 30, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (80, 80, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (100, 100, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (120, 120, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (150, 150, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (180, 180, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (100, 100, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (70, 70, 70, 150))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (20, 20, 20, 180))
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 0)
    dpg.bind_theme(global_theme)
def apply_blueish_cyan_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 30, 35, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (25, 30, 35, 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (30, 35, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 230, 240, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 70, 80, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 45, 55, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (40, 50, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (30, 40, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (30, 40, 50, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (50, 60, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 70, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (60, 80, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (70, 90, 110, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (80, 100, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 100, 130, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (100, 150, 200, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (120, 170, 220, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (30, 35, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (50, 70, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (60, 80, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (100, 180, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (30, 35, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (70, 100, 130, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (80, 110, 140, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (90, 120, 150, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (100, 180, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (120, 200, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (80, 90, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (80, 120, 160, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (20, 25, 30, 180))
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 0)
    dpg.bind_theme(global_theme)
def theme_callback(sender, app_data):
    global theme, keybind_bg_color, keybind_line_color, keybind_text_color
    if app_data == "Pink":
        apply_purpleish_pink_theme()
        theme = "Pink"
        keybind_bg_color = [35, 35, 45]
        keybind_line_color = [180, 100, 255]
        keybind_text_color = [220, 220, 230]
    elif app_data == "White":
        apply_white_and_grey_theme()
        theme = "White"
        keybind_bg_color = [220, 220, 220]
        keybind_line_color = [140, 140, 140]
        keybind_text_color = [20, 20, 20]
    elif app_data == "Black":
        apply_black_and_white_theme()
        theme = "Black"
        keybind_bg_color = [30, 30, 30]
        keybind_line_color = [80, 80, 80]
        keybind_text_color = [240, 240, 240]
    elif app_data == "Blue":
        apply_blueish_cyan_theme()
        theme = "Blue"
        keybind_bg_color = [35, 45, 55]
        keybind_line_color = [100, 150, 200]
        keybind_text_color = [220, 230, 240]
PLAYER_PART_CACHE = {}
childrenOffset = int(offsets['Children'], 16)
nameOffset = int(offsets['Name'], 16)
teamOffset = int(offsets['Team'], 16)
modelInstanceOffset = int(offsets['ModelInstance'], 16)
primitiveOffset = int(offsets['Primitive'], 16)
positionOffset = int(offsets['Position'], 16)
healthOffset = int(offsets['Health'], 16)
maxhealthOffset = int(offsets['MaxHealth'], 16)
global_IgnoreTeam = False
global_aimbot_ignoredead = False
def GetTargetPositions(pm):
    global PLAYER_PART_CACHE, global_wnd_height, global_wnd_width
    positions = []
    if not all([matrixAddr, lpAddr, plrsAddr]):
        return []
    width, height = global_wnd_width, global_wnd_height
    matrix_bytes = pm.read_bytes(matrixAddr, 16 * 4)
    view_proj_matrix = np.reshape(np.frombuffer(matrix_bytes, dtype=np.float32), (4, 4))
    lpTeam = pm.read_longlong(lpAddr + teamOffset)
    children = GetChildren(plrsAddr)
    if not children:
        return []
    lp_char_addr = pm.read_longlong(lpAddr + modelInstanceOffset)
    myPrim = 0
    if lp_char_addr:
        lp_head = FindFirstChild(lp_char_addr, "Head")
        if lp_head:
            myPrim = pm.read_longlong(lp_head + primitiveOffset)
    myHeadPos = np.frombuffer(pm.read_bytes(myPrim + positionOffset, 12), dtype=np.float32) if myPrim else np.array([0,0,0], dtype=np.float32)
    for v in children:
        try:
            if v == lpAddr:
                continue
            char = pm.read_longlong(v + modelInstanceOffset)
            if not char: continue
            team = pm.read_longlong(v + teamOffset)
            if global_IgnoreTeam and team == lpTeam and team > 0: continue
            hum = FindFirstChildOfClass(char, "Humanoid")
            if not hum: continue
            health = pm.read_float(hum + healthOffset)
            maxhealth = pm.read_float(hum + maxhealthOffset)
            if global_aimbot_ignoredead and health <= 0: continue
            if maxhealth <= 0: maxhealth = 100
            health = max(0.0, min(float(maxhealth), float(health)))
            cache_entry = PLAYER_PART_CACHE.get(v)
            if cache_entry and cache_entry.get('char_addr') == char:
                part_primitive_addresses = cache_entry['parts']
            else:
                is_r6 = not FindFirstChild(char, "RightFoot")
                part_map_names = {
                    "Head": "Head", "HumanoidRootPart": "HumanoidRootPart",
                    "RightArmEnd": "Right Arm" if is_r6 else "RightLowerArm",
                    "LeftArmEnd": "Left Arm" if is_r6 else "LeftLowerArm",
                    "RightLeg": "Right Leg" if is_r6 else "RightFoot",
                    "LeftLeg": "Left Leg" if is_r6 else "LeftFoot"
                }
                part_primitive_addresses = {}
                for logical_name, part_name in part_map_names.items():
                    part_obj = FindFirstChild(char, part_name)
                    prim_addr = pm.read_longlong(part_obj + primitiveOffset) if part_obj else 0
                    part_primitive_addresses[logical_name] = prim_addr
                PLAYER_PART_CACHE[v] = {'char_addr': char, 'parts': part_primitive_addresses}
            enemy_prim = part_primitive_addresses.get("Head")
            if not enemy_prim: continue
            enemy_head_pos = np.frombuffer(pm.read_bytes(enemy_prim + positionOffset, 12), dtype=np.float32)
            if not np.all(np.isfinite(enemy_head_pos)) or not np.all(np.isfinite(myHeadPos)):
                continue
            distance = int(np.linalg.norm(enemy_head_pos - myHeadPos))
            if distance >= 1000:
                continue
            if hide_distance and distance >= distancetohide: continue
            UserName = GetName(char) or "Unknown"
            skeleton_screens = {}
            left_x, top_y = float('inf'), float('inf')
            right_x, bottom_y = float('-inf'), float('-inf')
            for logical_name, prim_addr in part_primitive_addresses.items():
                if prim_addr == 0:
                    skeleton_screens[logical_name] = None
                    continue
                pos = np.frombuffer(pm.read_bytes(prim_addr + positionOffset, 12), dtype=np.float32)
                screen = world_to_screen_with_matrix(pos, view_proj_matrix, width, height)
                skeleton_screens[logical_name] = screen
                if screen and screen != (-1, -1):
                    x, y = screen
                    left_x, top_y = min(left_x, x), min(top_y, y)
                    right_x, bottom_y = max(right_x, x), max(bottom_y, y)
            box = [0, 0, 0, 0]
            if left_x != float('inf'):
                padding = 5
                box = [int(left_x - padding), int(top_y - padding),
                       int(right_x - left_x + 2 * padding), int(bottom_y - top_y + 2 * padding)]
            positions.append({
                "box": box, "name": UserName, "health": health,
                "maxhealth": maxhealth, "distance": distance, "skeleton": skeleton_screens
            })
        except Exception:
            continue
    return positions
def clear_cache_periodically():
    global PLAYER_PART_CACHE
    while True:
        time.sleep(2)
        PLAYER_PART_CACHE.clear()
WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20
WS_EX_TOPMOST = 0x00000008
WS_POPUP = 0x80000000
SW_SHOW = 5
WM_DESTROY = 0x0002
WM_CLOSE = 0x0010
AC_SRC_OVER = 0x00
AC_SRC_ALPHA = 0x01
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32
user32.DefWindowProcW.restype = ctypes.c_longlong
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.PostQuitMessage.argtypes = [ctypes.c_int]
class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG), ("top", wintypes.LONG), ("right", wintypes.LONG), ("bottom", wintypes.LONG)]
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG), ("biHeight", wintypes.LONG), ("biPlanes", wintypes.WORD),
                ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD), ("biSizeImage", wintypes.DWORD),
                ("biXPelsPerMeter", wintypes.LONG), ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)]
class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3)]
class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [("BlendOp", ctypes.c_byte), ("BlendFlags", ctypes.c_byte), ("SourceConstantAlpha", ctypes.c_byte), ("AlphaFormat", ctypes.c_byte)]
class SIZE(ctypes.Structure):
    _fields_ = [("cx", ctypes.c_int), ("cy", ctypes.c_int)]
WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
class WNDCLASSW(ctypes.Structure):
    _fields_ = [("style", wintypes.UINT), ("lpfnWndProc", WNDPROC), ("cbClsExtra", ctypes.c_int), ("cbWndExtra", ctypes.c_int),
                ("hInstance", wintypes.HINSTANCE), ("hIcon", wintypes.HANDLE), ("hCursor", wintypes.HANDLE),
                ("hbrBackground", wintypes.HBRUSH), ("lpszMenuName", wintypes.LPCWSTR), ("lpszClassName", wintypes.LPCWSTR)]
user32.CreateWindowExW.restype = wintypes.HWND
user32.CreateWindowExW.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID]
user32.RegisterClassW.restype = wintypes.ATOM
user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]
user32.UpdateLayeredWindow.restype = wintypes.BOOL
user32.UpdateLayeredWindow.argtypes = [wintypes.HWND, wintypes.HDC, ctypes.POINTER(wintypes.POINT), ctypes.POINTER(SIZE), wintypes.HDC, ctypes.POINTER(wintypes.POINT), wintypes.COLORREF, ctypes.POINTER(BLENDFUNCTION), wintypes.DWORD]
def wnd_proc(hwnd, msg, wparam, lparam):
    if msg == WM_CLOSE or msg == WM_DESTROY:
        global_running_event.clear()
        user32.PostQuitMessage(0)
        return 0
    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
def setup_renderer():
    screen_dc = user32.GetDC(None)
    mem_dc = gdi32.CreateCompatibleDC(screen_dc)
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = global_wnd_width
    bmi.bmiHeader.biHeight = -global_wnd_height
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = 0
    bitmap = gdi32.CreateDIBSection(screen_dc, ctypes.byref(bmi), 0, ctypes.byref(ctypes.c_void_p()), None, 0)
    gdi32.SelectObject(mem_dc, bitmap)
    user32.ReleaseDC(None, screen_dc)
    return mem_dc, bitmap
global_hwnd = None
global_wnd_width = user32.GetSystemMetrics(0)
global_wnd_height = user32.GetSystemMetrics(1)
global_boxes = []
global_running_event = threading.Event()
global_running_event.set()
thread_lock = threading.Lock()
global_show_distance = False
global_show_box = False
global_show_name = False
global_show_health = False
global_show_skeleton = False
global_corner_box = False
global_show_head = False
global_box_color = [255, 255,255, 255]
global_dis_color = [255, 255,255, 255]
global_name_color = [255, 255, 255, 255]
global_health_color = [255, 255, 255, 255]
global_head_color = [255,255,255,255]
global_skelly_color = [255,255,255,255]
global_text_size = 16
global_dis_size = 16
global_head_size = 4
global_corner_value = 0.25
dynamic_health_color = True
hide_distance = False
distancetohide = 1000
overlay_fps = 244
def RGB(r, g, b):
    return r | (g << 8) | (b << 16)
def draw_shape(mem_dc, shape_type, x, y, r, pen, brush):
    old_pen = gdi32.SelectObject(mem_dc, pen)
    old_brush = gdi32.SelectObject(mem_dc, brush)
    if shape_type == "circle":
        gdi32.Ellipse(mem_dc, x - r, y - r, x + r, y + r)
    else:
        sides = 0
        if shape_type == "polygon": sides = 16
        elif shape_type == "triangle": sides = 3
        elif shape_type == "square": sides = 4
        elif shape_type == "star": sides = 10
        else:
             gdi32.Ellipse(mem_dc, x - r, y - r, x + r, y + r)
        if sides > 0:
            POINT_ARRAY = (wintypes.POINT * sides)()
            for i in range(sides):
                angle = i * (2 * math.pi / sides) - (math.pi / 2)
                current_radius = r if shape_type != "star" or i % 2 == 0 else r / 2
                px = int(x + current_radius * math.cos(angle))
                py = int(y + current_radius * math.sin(angle))
                POINT_ARRAY[i] = wintypes.POINT(px, py)
            gdi32.Polygon(mem_dc, POINT_ARRAY, sides)
    gdi32.SelectObject(mem_dc, old_pen)
    gdi32.SelectObject(mem_dc, old_brush)
global_show_keybinds = False
keybind_list_pos = [20, sheight // 2 - 100]
KEYBIND_LIST_WIDTH = 180
KEYBIND_LIST_HEIGHT = 110
def overlay_loop():
    global pm
    mem_dc, bitmap = None, None
    transparent_brush = gdi32.CreateSolidBrush(0x000000)
    null_brush = gdi32.GetStockObject(5)
    null_pen = gdi32.GetStockObject(8)
    dark_brush = gdi32.CreateSolidBrush(0x202020)
    name_font = gdi32.CreateFontW(global_text_size, 0,0,0,400,0,0,0,0,0,0,0,0, "Tahoma")
    dist_font = gdi32.CreateFontW(global_dis_size, 0,0,0,400,0,0,0,0,0,0,0,0, "Tahoma")
    keybind_title_font = gdi32.CreateFontW(17, 0, 0, 0, 400, 0, 0, 0, 0, 0, 0, 0, 0, "Verdana")
    keybind_entry_font = gdi32.CreateFontW(16, 0, 0, 0, 400, 0, 0, 0, 0, 0, 0, 0, 0, "Verdana")
    try:
        mem_dc, bitmap = setup_renderer()
        blend_func = BLENDFUNCTION(AC_SRC_OVER, 0, 255, AC_SRC_ALPHA)
        while global_running_event.is_set():
            try:
                frame_start_time = time.perf_counter()
                positions = GetTargetPositions(pm)
                with thread_lock:
                    global_boxes[:] = positions
                rect = RECT(0, 0, global_wnd_width, global_wnd_height)
                user32.FillRect(mem_dc, ctypes.byref(rect), transparent_brush)
                if global_show_keybinds:
                    kx, ky = keybind_list_pos[0], keybind_list_pos[1]
                    width, height = KEYBIND_LIST_WIDTH, KEYBIND_LIST_HEIGHT
                    padding = 10
                    r_bg, g_bg, b_bg = keybind_bg_color
                    bg_brush = gdi32.CreateSolidBrush(RGB(r_bg, g_bg, b_bg))
                    bg_rect = RECT(kx, ky, kx + width, ky + height)
                    user32.FillRect(mem_dc, ctypes.byref(bg_rect), bg_brush)
                    gdi32.DeleteObject(bg_brush)
                    r_ln, g_ln, b_ln = keybind_line_color
                    line_pen = gdi32.CreatePen(0, 1, RGB(r_ln, g_ln, b_ln))
                    old_pen = gdi32.SelectObject(mem_dc, line_pen)
                    gdi32.MoveToEx(mem_dc, kx + padding, ky + padding, None)
                    gdi32.LineTo(mem_dc, kx + width - padding, ky + padding)
                    gdi32.SelectObject(mem_dc, old_pen)
                    gdi32.DeleteObject(line_pen)
                    r_txt, g_txt, b_txt = keybind_text_color
                    gdi32.SetTextColor(mem_dc, RGB(r_txt, g_txt, b_txt))
                    gdi32.SetBkMode(mem_dc, 1)
                    gdi32.SelectObject(mem_dc, keybind_title_font)
                    title_text = "keybinds"
                    ts = wintypes.SIZE()
                    gdi32.GetTextExtentPoint32W(mem_dc, title_text, len(title_text), ctypes.byref(ts))
                    gdi32.TextOutW(mem_dc, kx + (width - ts.cx) // 2, ky + padding + 8, title_text, len(title_text))
                    gdi32.SelectObject(mem_dc, keybind_entry_font)
                    current_y = ky + padding + 35
                    keybind_entries = [("Fly", f"[{get_key_name(fly_keybind)}]"), ("Aimbot", f"[{get_key_name(aimbot_keybind)}]"), ("Menu", f"[{get_key_name(triggerbot_keybind)}]")]
                    for name, status in keybind_entries:
                        gdi32.TextOutW(mem_dc, kx + padding, current_y, name, len(name))
                        gdi32.GetTextExtentPoint32W(mem_dc, status, len(status), ctypes.byref(ts))
                        gdi32.TextOutW(mem_dc, kx + width - ts.cx - padding, current_y, status, len(status))
                        current_y += 20
                if fovtoggle:
                    current_mouse_x, current_mouse_y = win32api.GetCursorPos()
                    radius = int(aimbot_fov / 2)
                    r, g, b, a = fovColor
                    if fovglow:
                        for i in range(int(fovglowamount / 2), 0, -1):
                            glow_opacity = 0.3 * (1 - (i / (fovglowamount / 2)))
                            glow_r, glow_g, glow_b = int(r * glow_opacity), int(g * glow_opacity), int(b * glow_opacity)
                            glow_color = RGB(glow_r, glow_g, glow_b)
                            glow_brush = gdi32.CreateSolidBrush(glow_color)
                            glow_pen = gdi32.CreatePen(0, 1, glow_color)
                            draw_shape(mem_dc, shape, current_mouse_x, current_mouse_y, radius + i, glow_pen, glow_brush)
                            gdi32.DeleteObject(glow_pen)
                            gdi32.DeleteObject(glow_brush)
                    if fovfill:
                        fill_color = RGB(int(r * 0.2), int(g * 0.2), int(b*0.2))
                        fill_brush = gdi32.CreateSolidBrush(fill_color)
                        draw_shape(mem_dc, shape, current_mouse_x, current_mouse_y, radius, null_pen, fill_brush)
                        gdi32.DeleteObject(fill_brush)
                    if fovoutline:
                        outline_color = RGB(r, g, b)
                        outline_pen = gdi32.CreatePen(0, 1, outline_color)
                        draw_shape(mem_dc, shape, current_mouse_x, current_mouse_y, radius, outline_pen, null_brush)
                        gdi32.DeleteObject(outline_pen)
                for entry in global_boxes:
                    try:
                        x, y, w, h = entry["box"]
                        if w <= 0 or h <= 0: continue
                        if global_show_skeleton and "skeleton" in entry:
                            sk = entry["skeleton"]
                            r_sk, g_sk, b_sk, _ = global_skelly_color
                            pen = gdi32.CreatePen(0, 1, RGB(r_sk, g_sk, b_sk))
                            old_pen = gdi32.SelectObject(mem_dc, pen)
                            def draw_line(p1_key, p2_key):
                                p1 = sk.get(p1_key)
                                p2 = sk.get(p2_key)
                                if p1 and p2 and p1 != (-1, -1) and p2 != (-1, -1):
                                    gdi32.MoveToEx(mem_dc, int(p1[0]), int(p1[1]), None)
                                    gdi32.LineTo(mem_dc, int(p2[0]), int(p2[1]))
                            draw_line("Head", "HumanoidRootPart")
                            draw_line("HumanoidRootPart", "RightArmEnd")
                            draw_line("HumanoidRootPart", "LeftArmEnd")
                            draw_line("HumanoidRootPart", "RightLeg")
                            draw_line("HumanoidRootPart", "LeftLeg")
                            gdi32.SelectObject(mem_dc, old_pen)
                            gdi32.DeleteObject(pen)
                        if global_show_box:
                            r_box, g_box, b_box, _ = global_box_color
                            pen = gdi32.CreatePen(0, 1, RGB(r_box, g_box, b_box))
                            old_pen = gdi32.SelectObject(mem_dc, pen)
                            gdi32.SelectObject(mem_dc, null_brush)
                            if global_corner_box:
                                corner_len = int(min(w, h) * global_corner_value)
                                gdi32.MoveToEx(mem_dc, x, y + corner_len, None); gdi32.LineTo(mem_dc, x, y); gdi32.LineTo(mem_dc, x + corner_len, y)
                                gdi32.MoveToEx(mem_dc, x + w - corner_len, y, None); gdi32.LineTo(mem_dc, x + w, y); gdi32.LineTo(mem_dc, x + w, y + corner_len)
                                gdi32.MoveToEx(mem_dc, x + w, y + h - corner_len, None); gdi32.LineTo(mem_dc, x + w, y + h); gdi32.LineTo(mem_dc, x + w - corner_len, y + h)
                                gdi32.MoveToEx(mem_dc, x + corner_len, y + h, None); gdi32.LineTo(mem_dc, x, y + h); gdi32.LineTo(mem_dc, x, y + h - corner_len)
                            else:
                                gdi32.Rectangle(mem_dc, x, y, x + w, y + h)
                            gdi32.SelectObject(mem_dc, old_pen)
                            gdi32.DeleteObject(pen)
                        if global_show_health:
                            health, maxhealth = entry["health"], entry["maxhealth"]
                            bar_w = 1
                            fill_h = int((health / maxhealth) * h)
                            if dynamic_health_color:
                                green = int((health / maxhealth) * 255)
                                color = RGB(255 - green, green, 0)
                            else:
                                r_h, g_h, b_h, _ = global_health_color
                                color = RGB(r_h, g_h, b_h)
                            bg_rect = RECT(x - bar_w - 2, y, x - 2, y + h)
                            user32.FillRect(mem_dc, ctypes.byref(bg_rect), dark_brush)
                            if fill_h > 0:
                                fg_rect = RECT(x - bar_w - 2, y + (h - fill_h), x - 2, y + h)
                                health_brush = gdi32.CreateSolidBrush(color)
                                user32.FillRect(mem_dc, ctypes.byref(fg_rect), health_brush)
                                gdi32.DeleteObject(health_brush)
                        gdi32.SetBkMode(mem_dc, 1)
                        if global_show_name:
                            r_n, g_n, b_n, _ = global_name_color
                            gdi32.SetTextColor(mem_dc, RGB(r_n, g_n, b_n))
                            gdi32.SelectObject(mem_dc, name_font)
                            name = entry["name"]
                            ts = wintypes.SIZE()
                            gdi32.GetTextExtentPoint32W(mem_dc, name, len(name), ctypes.byref(ts))
                            gdi32.TextOutW(mem_dc, x + (w - ts.cx) // 2, y - ts.cy - 2, name, len(name))
                        if global_show_distance:
                            r_d, g_d, b_d, _ = global_dis_color
                            gdi32.SetTextColor(mem_dc, RGB(r_d, g_d, b_d))
                            gdi32.SelectObject(mem_dc, dist_font)
                            dist_text = f"[{int(entry['distance'])}m]"
                            ts = wintypes.SIZE()
                            gdi32.GetTextExtentPoint32W(mem_dc, dist_text, len(dist_text), ctypes.byref(ts))
                            gdi32.TextOutW(mem_dc, x + (w - ts.cx) // 2, y + h + 2, dist_text, len(dist_text))
                    except Exception:
                        continue
                user32.UpdateLayeredWindow(global_hwnd, None, None, ctypes.byref(SIZE(global_wnd_width, global_wnd_height)), mem_dc, ctypes.byref(wintypes.POINT(0, 0)), 0, ctypes.byref(blend_func), 2)
                elapsed_time = time.perf_counter() - frame_start_time
                sleep_duration = (1.0 / overlay_fps if overlay_fps > 0 else 0) - elapsed_time
                if sleep_duration > 0:
                    time.sleep(sleep_duration)
            except Exception:
                time.sleep(0.01)
    finally:
        if bitmap: gdi32.DeleteObject(bitmap)
        if mem_dc: gdi32.DeleteDC(mem_dc)
        if transparent_brush: gdi32.DeleteObject(transparent_brush)
        if dark_brush: gdi32.DeleteObject(dark_brush)
        if name_font: gdi32.DeleteObject(name_font)
        if dist_font: gdi32.DeleteObject(dist_font)
        if keybind_title_font: gdi32.DeleteObject(keybind_title_font)
        if keybind_entry_font: gdi32.DeleteObject(keybind_entry_font)
HWND_TOPMOST = -1
SWP_NOACTIVATE = 0x0010
def start():
    global pm
    wc = WNDCLASSW()
    wc.lpszClassName = ctypes.c_wchar_p("OverlayWindow")
    wc.lpfnWndProc = WNDPROC(wnd_proc)
    wc.hInstance = wintypes.HINSTANCE(kernel32.GetModuleHandleW(None))
    wc.hCursor = user32.LoadCursorW(None, wintypes.LPCWSTR(32512))
    wc.hIcon = None
    wc.style = 0
    atom = user32.RegisterClassW(ctypes.byref(wc))
    if not atom:
        raise RuntimeError("RegisterClassW failed")
    global global_hwnd
    global_hwnd = user32.CreateWindowExW(WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST |  0x00000080, wc.lpszClassName, ctypes.c_wchar_p("EOverlay"), WS_POPUP, 0, 0, global_wnd_width, global_wnd_height, None, None, wc.hInstance, None)
    if not global_hwnd:
        raise RuntimeError("CreateWindowExW failed")
    user32.ShowWindow(global_hwnd, SW_SHOW)
    user32.SetWindowPos(global_hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)

    threading.Thread(target=overlay_loop, daemon=True).start()
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
def toggle_distance(sender, app_data, user_data):
    global global_show_distance
    global_show_distance = app_data
def toggle_box(sender, app_data, user_data):
    global global_show_box
    global_show_box = app_data
def toggle_name(sender, app_data, user_data):
    global global_show_name
    global_show_name = app_data
def toggle_health(sender, app_data, user_data):
    global global_show_health
    global_show_health = app_data
def toggle_skeleton(sender, app_data, user_data):
    global global_show_skeleton
    global_show_skeleton = app_data
def color_callback(sender, app_data, user_data):
    color_variable_name = user_data
    new_color = [int(c * 255) for c in app_data]
    if color_variable_name == "global_box_color": global global_box_color; global_box_color = new_color
    elif color_variable_name == "global_dis_color": global global_dis_color; global_dis_color = new_color
    elif color_variable_name == "global_name_color": global global_name_color; global_name_color = new_color
    elif color_variable_name == "global_health_color": global global_health_color; global_health_color = new_color
    elif color_variable_name == "global_head_color": global global_head_color; global_head_color = new_color
    elif color_variable_name == "global_skelly_color": global global_skelly_color; global_skelly_color = new_color
def esp_ignoredead_callback(sender, app_data):
    global global_aimbot_ignoredead
    global_aimbot_ignoredead = app_data
def esp_ignoreteam_callback(sender, app_data):
    global global_IgnoreTeam
    global_IgnoreTeam = app_data
def esp_keybind(sender, app_data):
    global global_show_keybinds
    global_show_keybinds = app_data
def update_overlay_fps(sender, app_data):
    global overlay_fps
    overlay_fps = app_data
galaxy_window = None
class BackgroundController(QObject):
    visibility_changed = pyqtSignal(bool)
class GalaxyBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setFixedSize(screen_geometry.width(), screen_geometry.height())
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        hwnd = int(self.winId())
        extended_style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, extended_style | 0x20)
        self.stars = []
        self.particles = []
        self.num_stars = 300
        self.num_particles = 20
        self.init_stars()
        self.init_particles()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)
        self.show()
        hwnd = windll.user32.FindWindowW(None, "Crono External")
        if hwnd:
                windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
        hwnd = windll.user32.FindWindowW(None, "Crono External")
        if hwnd:
                windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
    def init_stars(self):
        self.stars = []
        for _ in range(self.num_stars):
            self.stars.append({'x': random.uniform(0, self.width()), 'y': random.uniform(0, self.height()), 'size': random.uniform(1, 3), 'opacity': random.uniform(0.1, 0.8), 'speed': random.uniform(0.1, 0.5)})
    def init_particles(self):
        self.particles = []
        colors = [QColor("#6a0dad"), QColor("#2a52be"), QColor("#8e44ad")]
        for _ in range(self.num_particles):
            self.particles.append({'x': random.uniform(0, self.width()), 'y': random.uniform(0, self.height()), 'size': random.uniform(50, 200), 'color': random.choice(colors), 'opacity': random.uniform(0.01, 0.05), 'speed': random.uniform(0.2, 0.6)})
    def update_animation(self):
        for star in self.stars:
            star['x'] -= star['speed']
            if star['x'] < 0:
                star['x'] = self.width()
                star['y'] = random.uniform(0, self.height())
        for particle in self.particles:
            particle['x'] -= particle['speed']
            if particle['x'] < 0:
                particle['x'] = self.width()
                particle['y'] = random.uniform(0, self.height())
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 0, 200)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        for particle in self.particles:
            color = particle['color']
            color.setAlphaF(particle['opacity'])
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(particle['x']), int(particle['y']), int(particle['size']), int(particle['size']))
        for star in self.stars:
            color = QColor(255, 255, 255)
            color.setAlphaF(star['opacity'])
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(star['x']), int(star['y']), int(star['size']), int(star['size']))
controller = None
def run_galaxy_background():
    global galaxy_window, controller
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    controller = BackgroundController()
    galaxy_window = GalaxyBackground()
    controller.visibility_changed.connect(galaxy_window.setVisible)
    app.exec_()
known_config_files = []
def checkconfigidk():
    global known_config_files
    while True:
        current_configs = get_config_files()
        if set(current_configs) != set(known_config_files):
                known_config_files = current_configs
                if dpg.does_item_exist("config_dropdown"):
                     dpg.configure_item("config_dropdown", items=known_config_files)
        time.sleep(2)
if __name__ == "__main__":
    if v == "Windows 10":
     threading.Thread(target=run_galaxy_background, daemon=True).start()
    initialize_controller()
    dpg.create_context()
    with dpg.window(label="crono external", no_title_bar=True, no_resize=True, tag="Primary Window", width=715, height=590):
        with dpg.child_window(label="Main Tabs", width=718, height=590, border=True, no_scrollbar=True):
            with dpg.tab_bar():
                with dpg.tab(label="Aim"):
                    with dpg.group(horizontal=True):
                        with dpg.child_window(label="Aimbot", width=340, height=270, border=True):
                            dpg.add_text("Main Settings")
                            dpg.add_separator()
                            with dpg.group(horizontal=True):
                                dpg.add_checkbox(label="Aimbot", default_value=aimbot_enabled, callback=aimbot_callback, tag="aimbot_checkbox")
                                dpg.add_button(label=f"Key: {get_key_name(aimbot_keybind)}", tag="keybind_button", callback=keybind_callback)
                            dpg.add_slider_float(label="Fov", default_value=aimbot_fov / 2, min_value=1.0, max_value=360.0, format="%.0f", callback=setfov_callback, tag="aimbotfov_slider")
                            dpg.add_combo(["Memory", "Mouse"], default_value="Mouse", tag="aimbot_option", width=120, callback=aimbot_mouse_callback)
                            dpg.add_combo(["Head", "HumanoidRootPart"], default_value="Head", tag="aimbot_hitpart_combo", width=120, callback=aimbot_hitpart_callback)
                        with dpg.child_window(label="Humanization", width=340, height=270, border=True):
                            dpg.add_text("Extra Settings")
                            dpg.add_separator()
                            dpg.add_checkbox(label="Team Check", default_value=aimbot_ignoreteam, callback=aimbot_ignoreteam_callback, tag="aimbot_ignoreteam_checkbox",show=False)
                            dpg.add_checkbox(label="Dead Check", default_value=aimbot_ignoredead, callback=aimbot_ignoredead_callback, tag="aimbot_ignoredead_checkbox")
                    with dpg.group(horizontal=True):
                        with dpg.child_window(label="Place Holder 1", width=340, height=270, border=True):
                            dpg.add_text("Mouse Settings")
                            dpg.add_separator()
                            dpg.add_checkbox(label="Humanization", default_value=Humanization_enabled, callback=aimbot_humer_callback, tag="aimbot_hum_checkbox")
                            dpg.add_checkbox(label="Smoothness", default_value=aimbot_smoothness_enabled, callback=aimbot_smoothness_callback, tag="aimbot_smoothness_checkbox")
                            dpg.add_slider_float(label="Smooth Amount", default_value=aimbot_smoothness_value, min_value=1, max_value=100, format="%.0f", callback=smoothness_value_callback, tag="smoothness_slider")
                            dpg.add_slider_float(label="Sensitivity", default_value=aimbot_sens, min_value=0.1, max_value=2, format="%.1f", callback=sens_value_callback, tag="sens_slider")
                            dpg.add_checkbox(label="Smart Aim", default_value=aimbot_prediction_enabled, callback=aimbot_prediction_checkbox, tag="aimbot_prediction_checkbox")
                            dpg.add_slider_float(label="Manual X", default_value=aimbot_prediction_x, min_value=0.0, max_value=1.0, format="%.2f", callback=prediction_x_callback, tag="prediction_x_slider")
                            dpg.add_slider_float(label="Manual Y", default_value=aimbot_prediction_y, min_value=0.0, max_value=1.0, format="%.2f", callback=prediction_y_callback, tag="prediction_y_slider")
                with dpg.tab(label="Visual"):
                    with dpg.group(horizontal=True):
                        with dpg.child_window(label="Fov Visuals", width=340, height=270, border=True):
                            dpg.add_text("Fov Settings")
                            dpg.add_separator()
                            dpg.add_checkbox(label="Fov", default_value=fovtoggle, callback=esp_fov_callback, tag="esp_fov")
                            dpg.add_checkbox(label="Fill", default_value=fovfill, callback=fovfill_callback, tag="esp_fovfill")
                            dpg.add_checkbox(label="Glow", default_value=fovglow, callback=fovglow_callback, tag="esp_fovglow")
                            dpg.add_checkbox(label="Outline", default_value=fovoutline, callback=fovoutline_callback, tag="esp_outline")
                            dpg.add_slider_float(label="Glow Amount", default_value=fovglowamount, min_value=10.0, max_value=100.0, format="%.1f", callback=fovglowamount_callback, tag="glow_buffer")
                            dpg.add_slider_float(label="Opacity", default_value=opamount, min_value=1.0, max_value=255.0, format="%.0f", callback=op_callback, tag="op_buffer",show=False)
                            dpg.add_combo(["circle", "polygon", "triangle", "square", "star"], default_value=shape, tag="fover_option", width=120, callback=change_shape)
                            dpg.add_color_edit(label="Fov Color", default_value=fovColor, callback=update_fov_color, no_inputs=True, tag="fc")
                        with dpg.child_window(label="Esp Visuals", width=340, height=270, border=True):
                            dpg.add_text("Esp Settings")
                            dpg.add_separator()
                            dpg.add_checkbox(label="Show Box", default_value=global_show_box, callback=toggle_box, tag="esp_box_toggle")
                            dpg.add_checkbox(label="Show Skeleton", default_value=global_show_skeleton, callback=toggle_skeleton, tag="esp_skeleton_toggle")
                            dpg.add_checkbox(label="Show Name", default_value=global_show_name, callback=toggle_name, tag="esp_name_toggle")
                            dpg.add_checkbox(label="Show Health", default_value=global_show_health, callback=toggle_health, tag="esp_health_toggle")
                            dpg.add_checkbox(label="Show Distance", default_value=global_show_distance, callback=toggle_distance, tag="esp_distance_toggle")
                            dpg.add_color_edit(label="Box Color", default_value=global_box_color, callback=color_callback, no_inputs=True, tag="box_color_picker", user_data="global_box_color")
                            dpg.add_color_edit(label="Skeleton Color", default_value=global_skelly_color, callback=color_callback, no_inputs=True, tag="skelly_color_picker", user_data="global_skelly_color")
                            dpg.add_color_edit(label="Name Color", default_value=global_name_color, callback=color_callback, no_inputs=True, tag="name_color_picker", user_data="global_name_color")
                            dpg.add_color_edit(label="Distance Color", default_value=global_dis_color, callback=color_callback, no_inputs=True, tag="dis_color_picker", user_data="global_dis_color")
                            dpg.add_color_edit(label="Health Color", default_value=global_health_color, callback=color_callback, no_inputs=True, tag="health_color_picker", user_data="global_health_color",show=False)
                            dpg.add_color_edit(label="Head Color", default_value=global_head_color, callback=color_callback, no_inputs=True, tag="head_color_picker", user_data="global_head_color",show=False)
                    with dpg.group(horizontal=True):
                        with dpg.child_window(label="Esp Settings", width=340, height=270, border=True):
                                 dpg.add_text("Esp Checks")
                                 dpg.add_separator()
                                 dpg.add_checkbox(label="Dead Check", default_value=global_aimbot_ignoredead, callback=esp_ignoredead_callback, tag="esp_ignoredead_checkbox")
                                 dpg.add_checkbox(label="Team Check", default_value=global_IgnoreTeam, callback=esp_ignoreteam_callback, tag="esp_ignoreteam_checkbox",show=False)
                        with dpg.child_window(label="Esp Overlay", width=340, height=270, border=True):
                                 dpg.add_text("Overlay")
                                 dpg.add_separator()
                                 dpg.add_checkbox(label="Keybind List", default_value=global_show_keybinds, callback=esp_keybind, tag="keybindlist")
                                 dpg.add_slider_int(label="Overlay FPS", default_value=overlay_fps, min_value=1, max_value=244, callback=update_overlay_fps, tag="overlay_fps_slider")
                with dpg.tab(label="Extra"):
                    with dpg.group(horizontal=True):
                        with dpg.child_window(label="Fly Movement", width=340, height=270, border=True):
                            dpg.add_text("Fly Settings")
                            dpg.add_separator()
                            dpg.add_checkbox(label="Fly", default_value=fly_enabled, callback=fly_callback, tag="move_fly")
                            dpg.add_slider_float(label="Fly Speed", default_value=fly_speed, min_value=1.0, max_value=100.0, format="%.0f", callback=fly_speed_callback, tag="move_speed")
                            dpg.add_button(label=f"{get_key_name(fly_keybind)} ", tag="fly_keybind_button", callback=fly_keybind_callback, user_data=None)
                with dpg.tab(label="Config"):
                    with dpg.child_window(label="Config Management", border=True):
                        dpg.add_text("Load Config")
                        dpg.add_combo(label="Select Config", tag="config_dropdown", items=get_config_files())
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Load Config", callback=load_selected_config)
                            dpg.add_button(label="Save Config", callback=save_selected_config)
                        dpg.add_separator()
                        dpg.add_text("Create Config")
                        dpg.add_input_text(label="Name", tag="new_config_name_input")
                        dpg.add_button(label="Create & Save", callback=create_config_callback)
                        dpg.add_separator()
                        dpg.add_button(label="Open Config Folder", callback=open_config_folder)
                with dpg.tab(label="Menu"):
                    with dpg.group(horizontal=True):
                        with dpg.child_window(label="Keybinds", width=340, height=270, border=True):
                            dpg.add_text("Menu Settings")
                            dpg.add_separator()
                            dpg.add_button(label=f"Toggle UI Key: {get_key_name(triggerbot_keybind)} ", tag="triggerbot_keybind_button", callback=triggerbot_keybind_callback, user_data=None)
                            dpg.add_combo(items=["Pink", "White", "Black", "Blue"], label="Theme", default_value=theme, callback=theme_callback, tag="themer")
                            dpg.add_button(label=f"Attach Again plz", tag="retach", callback=init, user_data=None)
    drag_pos = None
    def mouse_drag_callback(sender, app_data):
        global drag_pos
        if drag_pos:
            new_pos = dpg.get_viewport_pos()
            delta = [app_data[1], app_data[2]]
            dpg.set_viewport_pos([new_pos[0] + delta[0], new_pos[1] + delta[1]])
    def mouse_down_callback(sender, app_data):
        global drag_pos
        if app_data[0] == 0 and dpg.is_item_hovered("Primary Window"):
            drag_pos = True
    def mouse_up_callback(sender, app_data):
        global drag_pos
        drag_pos = None
    os.system("cls")
    os.system("title Midnight - Home")
    inject_callback()
    time.sleep(1)
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 20, 25, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (25, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (25, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (25, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 230, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 60, 70, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (30, 30, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (30, 30, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (35, 30, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (60, 50, 75, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (70, 60, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (80, 70, 100, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (90, 80, 110, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 70, 100, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (180, 100, 255, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 120, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (25, 25, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (60, 50, 75, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (70, 60, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (120, 80, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (30, 30, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (80, 70, 100, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (90, 80, 110, 220))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (100, 90, 120, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (120, 80, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (150, 100, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (80, 80, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (120, 100, 140, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (40, 35, 50, 180))
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 0)
    dpg.bind_theme(global_theme)
    refresh_config_list()
    config_list = get_config_files()
    if config_list:
        first_config = config_list[0]
        dpg.set_value("config_dropdown", first_config)
        load_selected_config()
    else:
        dpg.set_value("new_config_name_input", "default")
        create_config_callback()
    if theme == "Pink":
        apply_purpleish_pink_theme()
        keybind_bg_color = [35, 35, 45]
        keybind_line_color = [180, 100, 255]
        keybind_text_color = [220, 220, 230]
    elif theme == "White":
        apply_white_and_grey_theme()
        keybind_bg_color = [220, 220, 220]
        keybind_line_color = [140, 140, 140]
        keybind_text_color = [20, 20, 20]
    elif theme == "Black":
        apply_black_and_white_theme()
        keybind_bg_color = [30, 30, 30]
        keybind_line_color = [80, 80, 80]
        keybind_text_color = [240, 240, 240]
    elif theme == "Blue":
        apply_blueish_cyan_theme()
        keybind_bg_color = [35, 45, 55]
        keybind_line_color = [100, 150, 200]
        keybind_text_color = [220, 230, 240]
    ui_visible = True
    last_toggle_time = 0
    toggle_debounce_delay = 0.2
    def toggle_ui_visibility():
        global ui_visible, last_toggle_time
        current_time = time.time()
        if current_time - last_toggle_time < toggle_debounce_delay:
            return
        last_toggle_time = current_time
        ui_visible = not ui_visible
        if controller:
            controller.visibility_changed.emit(ui_visible)
        time.sleep(0.05)
        if ui_visible:
            dpg.set_viewport_always_top(True)
            hwnd = windll.user32.FindWindowW(None, "Crono External")
            if hwnd:
                windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
        else:
            dpg.set_viewport_always_top(False)
            hwnd = windll.user32.FindWindowW(None, "Roblox")
            if hwnd:
                windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
            hwnd = windll.user32.FindWindowW(None, "Crono External")
            if hwnd:
                windll.user32.SetWindowPos(hwnd, 1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
    def del_key_listener():
        while True:
            if ui_visible:
                hwnd = windll.user32.FindWindowW(None, "Crono External")
                if hwnd:
                    windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
            else:
                dpg.set_viewport_always_top(False)
                hwnd = windll.user32.FindWindowW(None, "Crono External")
                if hwnd:
                    windll.user32.SetWindowPos(hwnd, 1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0040)
            if is_key_pressed(triggerbot_keybind):
                toggle_ui_visibility()
            time.sleep(0.1)
    dpg.create_viewport(title="Crono External", decorated=False, resizable=True, width=735, height=610, always_on_top=True)
    with dpg.handler_registry():
        dpg.add_mouse_down_handler(callback=mouse_down_callback)
        dpg.add_mouse_drag_handler(callback=mouse_drag_callback)
        dpg.add_mouse_release_handler(callback=mouse_up_callback)
    dpg.set_viewport_pos([410, 150])
    dpg.setup_dearpygui()
    dpg.set_primary_window("Primary Window", True)
    threading.Thread(target=del_key_listener, daemon=True).start()
    threading.Thread(target=aimbotLoop2d, daemon=True).start()
    threading.Thread(target=aimbotLoop, daemon=True).start()
    threading.Thread(target=clear_cache_periodically, daemon=True).start()
    threading.Thread(target=start,daemon=True).start()
    threading.Thread(target=checkconfigidk,daemon=True).start()
    dpg.set_viewport_always_top(True)
    fly_thread = FlyThread(pm, baseAddr, offsets)
    fly_thread.start()
    dpg.show_viewport()
    hwnd = windll.user32.FindWindowW(None, "Crono External")
    if hwnd:
        GWL_EXSTYLE = -20
        WS_EX_TOOLWINDOW = 0x00000080
        SWP_FRAMECHANGED = 0x0020
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_NOZORDER = 0x0004
        ex_style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        new_ex_style = ex_style | WS_EX_TOOLWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_ex_style)
        windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
    dpg.start_dearpygui()
    dpg.destroy_context()