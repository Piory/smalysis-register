from threading import Lock

import cv2

from constant.Constant import Constant
from enums.SmashBrosStatus import SmashBrosStatus
from image.MaskGenerator import MaskGenerator
from smashbros.Singleton import Singleton



class SmashBrosManager(Singleton, object):
    __instance = None
    __lock = Lock()

    def __init__(self, smashBrosStatus: SmashBrosStatus, goMask):
        self.smashBrosStatus = smashBrosStatus
        self.goMaskHist = cv2.calcHist([goMask], [0], None, [256], [0, 256])

    @classmethod
    def getInstance(cls, smashBrosStatus: SmashBrosStatus, goMask):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls._instance = cls.__internalNew(smashBrosStatus, goMask)
        return cls._instance

    @classmethod
    def __internalNew(cls, status: SmashBrosStatus, goMask):
        return super().__new__(cls, status, goMask)

    @property
    def status(self) -> SmashBrosStatus:
        return self.smashBrosStatus

    def analysisSmashBrosStatus(self, img):
        if self.smashBrosStatus is SmashBrosStatus.START:
            pass
        elif self.smashBrosStatus is SmashBrosStatus.RESULT:
            pass
        elif self.smashBrosStatus is SmashBrosStatus.END or self.smashBrosStatus is None:
            if self.__checkGo(img):
                self.smashBrosStatus = SmashBrosStatus.START
        pass

    def __checkGo(self, img) -> bool:
        hist = cv2.calcHist([MaskGenerator.createGoMask(img)], [0], None, [256], [0, 256])
        compareHist = cv2.compareHist(self.goMaskHist, hist, cv2.HISTCMP_CORREL)
        return compareHist > Constant.GO_COMPARE_HIST_THRESHOLD
