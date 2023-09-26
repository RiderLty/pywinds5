from ctypes import *

DS5W_ISTATE_BTX_SQUARE = 0x10
DS5W_ISTATE_BTX_CROSS = 0x20
DS5W_ISTATE_BTX_CIRCLE = 0x40
DS5W_ISTATE_BTX_TRIANGLE = 0x80
DS5W_ISTATE_DPAD_LEFT = 0x01
DS5W_ISTATE_DPAD_DOWN = 0x02
DS5W_ISTATE_DPAD_RIGHT = 0x04
DS5W_ISTATE_DPAD_UP = 0x08
DS5W_ISTATE_BTN_A_LEFT_BUMPER = 0x01
DS5W_ISTATE_BTN_A_RIGHT_BUMPER = 0x02
DS5W_ISTATE_BTN_A_LEFT_TRIGGER = 0x04
DS5W_ISTATE_BTN_A_RIGHT_TRIGGER = 0x08
DS5W_ISTATE_BTN_A_SELECT = 0x10
DS5W_ISTATE_BTN_A_MENU = 0x20
DS5W_ISTATE_BTN_A_LEFT_STICK = 0x40
DS5W_ISTATE_BTN_A_RIGHT_STICK = 0x80
DS5W_ISTATE_BTN_B_PLAYSTATION_LOGO = 0x01
DS5W_ISTATE_BTN_B_PAD_BUTTON = 0x02
DS5W_ISTATE_BTN_B_MIC_BUTTON = 0x04
DS5W_OSTATE_PLAYER_LED_LEFT = 0x01
DS5W_OSTATE_PLAYER_LED_MIDDLE_LEFT = 0x02
DS5W_OSTATE_PLAYER_LED_MIDDLE = 0x04
DS5W_OSTATE_PLAYER_LED_MIDDLE_RIGHT = 0x08
DS5W_OSTATE_PLAYER_LED_RIGHT = 0x10

class Touch(Structure):
    _fields_ = [
        ("x", c_uint),
        ("y", c_int),
        ("down", c_bool),
        ("id", c_ubyte)
    ]


class Battery(Structure):
    _fields_ = [
        ("charging", c_bool),
        ("fullyCharged", c_bool),
        ("level", c_ubyte),
    ]


class AnalogStick(Structure):
    _fields_ = [
        ("x", c_char),
        ("y", c_char),
    ]


class Vector3(Structure):
    _fields_ = [
        ("x", c_short),
        ("y", c_short),
        ("z", c_short),
    ]


class DS5InputState(Structure):
    _fields_ = [
        ("leftStick", AnalogStick),
        ("rightStick", AnalogStick),
        ("leftTrigger", c_ubyte),
        ("rightTrigger", c_ubyte),
        ("buttonsAndDpad", c_ubyte),
        ("buttonsA", c_ubyte),
        ("buttonsB", c_ubyte),
        ("accelerometer", Vector3),
        ("gyroscope", Vector3),
        ("touchPoint1", Touch),
        ("touchPoint2", Touch),
        ("battery", Battery),
        ("headPhoneConnected", c_bool),
        ("leftTriggerFeedback", c_ubyte),
        ("rightTriggerFeedback", c_ubyte),
    ]


class LedBrightness:
    LOW = 0x02
    MEDIUM = 0x01
    HIGH = 0x00


class MicLed:
    OFF = 0x00
    ON = 0x01
    PULSE = 0x02


class TriggerEffectType:
    NoResitance = 0x00
    ContinuousResitance = 0x01
    SectionResitance = 0x02
    EffectEx = 0x26
    Calibrate = 0xFC


class PlayerLeds(Structure):
    _fields_ = [
        ("bitmask", c_ubyte),
        ("playerLedFade", c_bool),
        ("brightness", c_ubyte),
    ]


class Color(Structure):
    _fields_ = [
        ("r", c_ubyte),
        ("g", c_ubyte),
        ("b", c_ubyte),
    ]


class Continuous(Structure):
    _fields_ = [
        ("startPosition", c_ubyte),
        ("force", c_ubyte),
        ("_pad", c_ubyte * 4),
    ]


class Section(Structure):
    _fields_ = [
        ("startPosition", c_ubyte),
        ("endPosition", c_ubyte),
        ("_pad", c_ubyte * 4),
    ]


class EffectEx(Structure):
    _fields_ = [
        ("startPosition", c_ubyte),
        ("keepEffect", c_bool),
        ("beginForce", c_ubyte),
        ("middleForce", c_ubyte),
        ("endForce", c_ubyte),
        ("frequency", c_ubyte),
    ]


class TriggerEffect_U(Union):
    _fields_ = [
        ("_u1_raw", c_ubyte * 16),
        ("Continuous", Continuous),
        ("Section", Section),
        ("EffectEx", EffectEx)
    ]

class TriggerEffect(Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("effectType", c_ubyte),
        ("effect", c_ubyte),
        ("u", TriggerEffect_U),
    ]


class DS5OutputState(Structure):
    _fields_ = [
        ("leftRumble", c_ubyte),
        ("rightRumble", c_ubyte),
        ("microphoneLed", c_byte),
        ("disableLeds", c_bool),
        ("playerLeds", PlayerLeds),
        ("lightbar", Color),
        ("leftTriggerEffect", TriggerEffect),
        ("rightTriggerEffect", TriggerEffect),
    ]
