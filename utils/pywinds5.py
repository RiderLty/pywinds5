import threading
from copy import deepcopy
from typing import List

from utils.ds5_events import *
from utils.ds5w_h import *
from utils.interface import DS5W


class stateController:
    def __init__(self, ds5w: DS5W) -> None:
        self.ds5w = ds5w

    def setLightBar(self, colorStr):
        if colorStr.startswith('#'):
            colorStr = colorStr[1:]
            if len(colorStr) == 6:
                colorStr = colorStr + "FF"
            elif len(colorStr) != 8:
                raise Exception("colorStr error")
            value = int(colorStr, 16)
            a = value & 0xFF
            r = int(((value >> 24) & 0xFF) * a / 255)
            g = int(((value >> 16) & 0xFF) * a / 255)
            b = int(((value >> 8) & 0xFF) * a / 255)
            self.ds5w.outState.lightbar.r = r
            self.ds5w.outState.lightbar.g = g
            self.ds5w.outState.lightbar.b = b
        else:
            raise Exception('colorStr must start with #')

    def setLightBar_RGB(self, r=None, g=None, b=None):
        if r != None:
            assert 0 <= r <= 255
            self.ds5w.outState.lightbar.r = int(r)
        if g != None:
            assert 0 <= g <= 256
            self.ds5w.outState.lightbar.g = int(g)
        if b != None:
            assert 0 <= b <= 256
            self.ds5w.outState.lightbar.b = int(b)
        # print("self.ds5w.outState.lightbar",self.ds5w.outState.lightbar.r,self.ds5w.outState.lightbar.g,self.ds5w.outState.lightbar.b)
        self.ds5w.outState.disableLeds = False


    def setPlayerLEDs(self, bitmask=None, palyerLedFade=None, brightness=None):
        if bitmask != None:
            assert bitmask in [DS5W_OSTATE_PLAYER_LED_LEFT, DS5W_OSTATE_PLAYER_LED_MIDDLE_LEFT,
                               DS5W_OSTATE_PLAYER_LED_MIDDLE, DS5W_OSTATE_PLAYER_LED_MIDDLE_RIGHT, DS5W_OSTATE_PLAYER_LED_RIGHT]
            self.ds5w.outState.playerLeds.bitmask = bitmask
        if palyerLedFade != None:
            assert type(palyerLedFade) == bool
            self.ds5w.outState.playerLeds.playerLedFade = palyerLedFade
        if brightness != None:
            assert brightness in [LedBrightness.HIGH, LedBrightness.MEDIUM, LedBrightness.LOW]
            self.ds5w.outState.playerLeds.brightness = LedBrightness.HIGH

    def setLeftRumble(self, value):
        self.ds5w.outState.leftRumble = int(value)

    def setRightRumble(self, value):
        self.ds5w.outState.rightRumble = int(value)

    def makeTriggerEffect(self,triger,effect):
        # self.ds5w.outState.triggers.triggers[triger].effect = effect
        pass

    def setTriggerEffect(self,triger,effect):
        assert triger == LT or triger == RT
        trigger = None
        if triger == LT:
            trigger = self.ds5w.outState.leftTriggerEffect
        else:
            trigger = self.ds5w.outState.rightTriggerEffect

        trigger.effectType = effect.effectType
        trigger.effect = effect.effect
        triger.Continuous = effect.Continuous
        triger.Section = effect.Section
        triger.EffectEx = effect.EffectEx

class pywinds5():
    def __init__(self,
                 index=0,
                 onBTN=lambda name, down: None,
                 onLeftStick=lambda x, y: None,
                 onRightStick=lambda x, y: None,
                 onRT=lambda value: None,
                 onLT=lambda value: None,
                 onGyroscope=lambda x, y, z: None,
                 onTouchPad_1=lambda x, y: None,
                 onTouchPad_2=lambda x, y: None,
                 onAccelerometer=lambda x, y, z: None,
                 onUpdate=lambda: None,
                 ) -> None:
        try:
            self.onBTN = onBTN
            self.onLeftStick = onLeftStick
            self.onRightStick = onRightStick
            self.onRT = onRT
            self.onLT = onLT
            self.onGyroscope = onGyroscope
            self.onTouchPad_1 = onTouchPad_1
            self.onTouchPad_2 = onTouchPad_2
            self.onAccelerometer = onAccelerometer
            self.onUpdate = onUpdate

            self.ds5Controller = DS5W(index, self.handeler)

            self.lastState = DS5InputState()
            self.currentState = self.ds5Controller.inState

            self.stateController = stateController(self.ds5Controller)

        except Exception as e:
            raise e

    def getBTN(self, code) -> int:  # DOWN UP
        if code in BUTTONSANDDPAD_MAP:
            index = BUTTONSANDDPAD_MAP.index(code)
            return self.currentState.buttonsAndDpad >> index & 0x1 == 1
        elif code in BUTTONSA_MAP:
            index = BUTTONSA_MAP.index(code)
            return self.currentState.buttonsA >> index & 0x1 == 1
        elif code in BUTTONSB_MAP:
            index = BUTTONSB_MAP.index(code)
            return self.currentState.buttonsB >> index & 0x1 == 1
        elif code == TOUCH_POINT_1:
            return self.currentState.touchPoint1.down
        elif code == TOUCH_POINT_2:
            return self.currentState.touchPoint2.down
        return False

    def getLeftStick(self) -> List[int]:  # x y
        x = int.from_bytes(
            self.ds5Controller.inState.leftStick.x, byteorder='big', signed=True)
        y = int.from_bytes(
            self.ds5Controller.inState.leftStick.y, byteorder='big', signed=True)
        return x, y

    def getRightStick(self) -> List[int]:
        x = int.from_bytes(
            self.ds5Controller.inState.rightStick.x, byteorder='big', signed=True)
        y = int.from_bytes(
            self.ds5Controller.inState.rightStick.y, byteorder='big', signed=True)
        return x, y

    def getRT(self) -> int:
        return self.ds5Controller.inState.rightTrigger

    def getLT(self) -> int:
        return self.ds5Controller.inState.leftTrigger

    def getGyroscope(self) -> List[int]:  # x y z
        return self.currentState.gyroscope.x, self.currentState.gyroscope.y, self.currentState.gyroscope.z

    def getTouchPoint_1(self) -> List[int]:  # x y
        return self.currentState.touchPoint1.x, self.currentState.touchPoint1.y

    def getTouchPoint_2(self) -> List[int]:
        return self.currentState.touchPoint2.x, self.currentState.touchPoint2.y

    def getAccelerometer(self) -> List[int]:  # x y z
        return self.currentState.accelerometer.x, self.currentState.accelerometer.y, self.currentState.accelerometer.z

    def handeler(self) -> int:
        if self.currentState.leftStick.x != self.lastState.leftStick.x or self.currentState.leftStick.y != self.lastState.leftStick.y:
            self.onLeftStick(int.from_bytes(self.currentState.leftStick.x, byteorder='big', signed=True), int.from_bytes(
                self.currentState.leftStick.y, byteorder='big', signed=True))

        if self.currentState.rightStick.x != self.lastState.rightStick.x or self.currentState.rightStick.y != self.lastState.rightStick.y:
            self.onRightStick(int.from_bytes(self.currentState.rightStick.x, byteorder='big', signed=True), int.from_bytes(
                self.currentState.rightStick.y, byteorder='big', signed=True))

        if self.currentState.leftTrigger != self.lastState.leftTrigger:
            self.onLT(self.currentState.leftTrigger)

        if self.currentState.rightTrigger != self.lastState.rightTrigger:
            self.onRT(self.currentState.rightTrigger)

        if self.currentState.gyroscope.x != self.lastState.gyroscope.x or self.currentState.gyroscope.y != self.lastState.gyroscope.y or self.currentState.gyroscope.z != self.lastState.gyroscope.z:
            self.onGyroscope(self.currentState.gyroscope.x,
                             self.currentState.gyroscope.y, self.currentState.gyroscope.z)

        if self.currentState.accelerometer.x != self.lastState.accelerometer.x or self.currentState.accelerometer.y != self.lastState.accelerometer.y or self.currentState.accelerometer.z != self.lastState.accelerometer.z:
            self.onAccelerometer(self.currentState.accelerometer.x,
                                 self.currentState.accelerometer.y, self.currentState.accelerometer.z)

        if self.currentState.touchPoint1.down != self.lastState.touchPoint1.down:
            self.onBTN(TOUCH_POINT_1, self.currentState.touchPoint1.down)
        if self.currentState.touchPoint1.x != self.lastState.touchPoint1.x or self.currentState.touchPoint1.y != self.lastState.touchPoint1.y:
            self.onTouchPad_1(self.currentState.touchPoint1.x,
                              self.currentState.touchPoint1.y)

        if self.currentState.touchPoint2.down != self.lastState.touchPoint2.down:
            self.onBTN(TOUCH_POINT_2, self.currentState.touchPoint2.down)
        if self.currentState.touchPoint2.x != self.lastState.touchPoint2.x or self.currentState.touchPoint2.y != self.lastState.touchPoint2.y:
            self.onTouchPad_2(self.currentState.touchPoint2.x,
                              self.currentState.touchPoint2.y)

        if self.currentState.buttonsAndDpad != self.lastState.buttonsAndDpad:
            for i in range(8):
                current = self.currentState.buttonsAndDpad >> i
                last = self.lastState.buttonsAndDpad >> i
                if current & 0x1 != last & 0x1:
                    self.onBTN(BUTTONSANDDPAD_MAP[i], current == 1)
        if self.currentState.buttonsA != self.lastState.buttonsA:
            for i in range(8):
                current = self.currentState.buttonsA >> i
                last = self.lastState.buttonsA >> i
                if current & 0x1 != last & 0x1:
                    self.onBTN(BUTTONSA_MAP[i], current == 1)

        if self.currentState.buttonsB != self.lastState.buttonsB:
            for i in range(3):
                current = self.currentState.buttonsB >> i
                last = self.lastState.buttonsB >> i
                if current & 0x1 != last & 0x1:
                    self.onBTN(BUTTONSB_MAP[i], current == 1)
        self.onUpdate()  # ON UPDATE 可以拿到当前与last两个状态
        self.lastState = deepcopy(self.currentState)
        return 0

    def mainLoop(self):
        self.ds5Controller.run()

    def run(self):
        thread = threading.Thread(target=self.mainLoop)
        thread.start()
        return thread
