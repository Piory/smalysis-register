import glob
import os

import cv2
import numpy as np

from model.Range import Range


class ImageUtil:
    @staticmethod
    def concatTile(images):
        return cv2.vconcat([cv2.hconcat(image) for image in images])

    @staticmethod
    def loadPngImage(path: str, fileName: str):
        images = [cv2.imread(characterImage, cv2.IMREAD_GRAYSCALE) for characterImage in glob.glob(os.path.join(path, fileName))]
        return np.array(images)

    @staticmethod
    def binarization(image, fromVal: int, toVal: int):
        # 2色化
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, img = cv2.threshold(gray, fromVal, toVal, cv2.THRESH_BINARY)
        return img

    @staticmethod
    def cutImage(image, imageRange: Range):
        return image[imageRange.top:imageRange.bottom, imageRange.left:imageRange.right]
