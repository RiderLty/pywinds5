import os
import threading
from ctypes import *

from utils.ds5w_h import *

myLib = CDLL(os.path.join(os.path.dirname(__file__), "ds5w_x64.dll"))


class DS5W():
    def __init__(self, index, handeler=lambda: 0):  # 手柄编号 区分多个手柄连接的情况
        if myLib.testControllerInit(index) != 0:
            count = myLib.getConnectedControllerCount()
            raise Exception(
                f"connect to controller_{index} failed , total {count} controller found")
        Class_ctor_wrapper = myLib.CreateDS5WInstance
        Class_ctor_wrapper.restype = c_void_p
        self.instance = c_void_p(Class_ctor_wrapper(index))
        self.inState = DS5InputState()
        self.outState = DS5OutputState()
        self.handeler = handeler

    def run(self):
        HANDELERCFUNCTYPE = CFUNCTYPE(c_int,)
        handeler_func = HANDELERCFUNCTYPE(self.handeler)
        thread = threading.Thread(target=myLib.StartDS5WInstance, args=(
            self.instance, handeler_func, byref(self.inState), byref(self.outState)))
        thread.start()
        return thread

    def stop(self):
        myLib.StopDS5WInstance(self.instance)
