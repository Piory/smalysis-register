import cv2
import numpy as np

from constant.Constant import Constant


class MaskGenerator:
    BLACK_IMG = np.zeros((1080, 1920))
    WHITE = (255, 255, 255)

    @staticmethod
    def createResultMask():
        mask = MaskGenerator.BLACK_IMG.copy()
        MaskGenerator.__createResultMask(mask, Constant.OWN_FIGHTER_NAME_RANGE.left)
        MaskGenerator.__createResultMask(mask, Constant.OPPONENT_FIGHTER_NAME_RANGE.left)
        return mask

    @staticmethod
    def createWinLoseMask():
        mask = MaskGenerator.BLACK_IMG.copy()
        MaskGenerator.__createWinLoseMask(mask, 667)
        MaskGenerator.__createWinLoseMask(mask, 1458)
        return mask

    @staticmethod
    def __createResultMask(img, start):
        wight = 606
        end = start + wight
        bottom = 1016
        leftTop = 68
        rightTop = 10
        resultZone = np.array([[start, leftTop], [end, rightTop], [end, bottom], [start, bottom]], np.int32)
        cv2.fillPoly(img, [resultZone], MaskGenerator.WHITE)

    @staticmethod
    def __createWinLoseMask(img, start):
        height = 200
        cv2.rectangle(img, (start, 0), (start + height, height), (255, 255, 255), -1)
