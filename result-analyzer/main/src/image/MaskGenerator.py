import cv2
import numpy as np

from constant.Constant import Constant
from model.Range import Range
from util.ImageUtil import ImageUtil


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
    def createGoMask(img):
        return MaskGenerator.__createMaskForHsv(img, np.array([0, 1, 1]), np.array([30, 255, 255]), Range(150, 575, 450, 1400))

    @staticmethod
    def createGamesetMask(img):
        return MaskGenerator.__createMaskForHsv(img, np.array([50, 1, 1]), np.array([100, 255, 255]), Range(0, 1080, 0, 1920))

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

    @staticmethod
    def __createMaskForHsv(img, lower: np.array, upper: np.array, r: Range):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        inRange = cv2.inRange(hsv, lower, upper)
        image = ImageUtil.cutImage(inRange, r)
        image = cv2.medianBlur(image, 11)
        # 2回やらないとうまくノイズが消えないので一旦2回やる
        MaskGenerator.__deleteNoise(image, 18000)
        MaskGenerator.__deleteNoise(image, 18000)
        return image

    @staticmethod
    def __deleteNoise(img, areaSize):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            contour = contours[i]
            area = abs(cv2.contourArea(contour))
            if area >= areaSize:
                continue
            cv2.fillConvexPoly(img, contours[i], 0)
