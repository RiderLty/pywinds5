import threading

from utils.ds5_events import *
from utils.mouse_keyboard_controller import *
from utils.pywinds5 import pywinds5


class hid_controller:
    def __init__(self) -> None:
        self.ds5 = pywinds5(
            index=0,
            onBTN=self.onBTN,
            onRT=self.onRT,
            onLT=self.onLT,
            onTouchPad_1=self.onTouchPad_1,
            )

        self.touchPoint_1_down = False
        self.touchPoint_1_last = (-1, -1)


        # threading.Thread(target=self.accView).start()
        threading.Thread(target=self.rsView).start()
        threading.Thread(target=self.lsWheel).start()
        

    def accView(self,):
        while True:
            x,y,z = self.ds5.getAccelerometer()
            x,y = int(-y / 100),int(-x / 200)
            if x == 0 and y == 0:
                pass
            else:
                mouse_move(x, y)
                sleep(1 / 250)
    
    def rsView(self,):
        while True:
            x, y = self.ds5.getRightStick()
            x = int(x / 9)
            y = int(-y / 9)
            if x == 0 and y == 0:
                pass
            else:
                mouse_move(x, y)
                sleep(1 / 250)


    def lsWheel(self,):
        while True:
            x,y = self.ds5.getLeftStick()
            wheel = int(y / 8) * 3
            mouse_wheel(wheel)
            sleep(1 / 50)
    
    
    def onRT(self,value):
        self.ds5.stateController.setLightBar_RGB(r = value * 200 / 255 + 55 )
        # self.ds5.stateController.setRightRumble(value / 32)

    def onLT(self,value):
        self.ds5.stateController.setLightBar_RGB(g = value * 200 / 255 + 55)
        # self.ds5.stateController.setLeftRumble(value / 32)
        


    def onBTN(self,code,down):
        if code == BTN_R2:
            mouse_press(MOUSE_BTN_LEFT) if down else mouse_release(MOUSE_BTN_LEFT)
        elif code == BTN_L2:
            mouse_press(MOUSE_BTN_RIGHT) if down else mouse_release(MOUSE_BTN_RIGHT)
        elif code == BTN_L1:
            if down:
                key_press(18)
                key_press(9)
                key_relese(9)
            else:
                key_relese(18)
        elif code == BTN_CIRCLE:
            if self.ds5.getBTN(BTN_L1):
                key_event(39, down)
        elif code == BTN_SQUARE:
            if self.ds5.getBTN(BTN_L1):
                key_event(37, down)
        elif code == BTN_DPAD_LEFT:
            key_event(37, down)
        elif code == BTN_DPAD_RIGHT:
            key_event(39, down)
        elif code == BTN_DPAD_UP:
            key_event(38, down)
        elif code == BTN_DPAD_DOWN:
            key_event(40, down)
            # self.ds5.stateController.setLightBar("#d9005188")
        elif code == TOUCH_POINT_1:
            self.touchPoint_1_down = down
            if down == False:
                self.touchPoint_1_last = (-1, -1)

    def onTouchPad_1(self, x, y):
        if self.touchPoint_1_down:
            if self.touchPoint_1_last == (-1, -1):
                self.touchPoint_1_last = (x, y)
            else:
                offset_x, offset_y = x - \
                    self.touchPoint_1_last[0], y-self.touchPoint_1_last[1]
                self.touchPoint_1_last = (x, y)
                # mouse_move(int(offset_x/4), int(offset_y / 4))
                mouse_wheel(int(offset_y))
        else:
            pass

    def run(self):
        return self.ds5.run()



hid_controller().run().join()




# def onLeft(x, y):
#     # print(f"LeftStick: {x}, {y}")
#     pass


# def onRight(x, y):
#     # print(f"RightStick: {x}, {y}")
#     pass


# def onLT(value):
#     # print(f"LT: {value}")
#     pass


# def onRT(value):
#     # print(f"RT: {value}")
#     pass

# def ononGyroscope(x, y, z):
#     # print(f"Gyro: {x}, {y}, {z}")
#     pass

# def onAccelerometer(x, y, z):
#     # print(f"Accelerometer: {x}, {y}, {z}")
#     pass

# def onTouchPad_1(x, y):
#     # print(f"TouchPad_1: {x}, {y}")
#     pass

# def onTouchPad_2(x, y):
#     # print(f"TouchPad_2: {x}, {y}")
#     pass

# def onBTN(code, downing):
#     # print(f"BTN: {NAME_MAP[code]}, {downing}")
#     pass

# def onUpdate():
#     # print("Update")
#     pass
# ds5 = pywinds5(
#     index=0,
#     onLeftStick=onLeft,
#     onRightStick=onRight,
#     onLT=onLT,
#     onRT=onRT,
#     onGyroscope=ononGyroscope,
#     onAccelerometer=onAccelerometer,
#     onTouchPad_1=onTouchPad_1,
#     onTouchPad_2=onTouchPad_2,
#     onBTN=onBTN,
#     onUpdate=onUpdate
#     )
               
# ds5.run()


# while True:
#     print(ds5.getBTN(BTN_MIC))
