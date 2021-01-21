import glob
import os

import cv2
import numpy as np


class ImageUtil:
    @staticmethod
    def concatTile(images):
        return cv2.vconcat([cv2.hconcat(image) for image in images])

    @staticmethod
    def loadPngImage(path: str, fileName: str):
        images = [cv2.imread(characterImage, cv2.IMREAD_GRAYSCALE) for characterImage in glob.glob(os.path.join(path, fileName))]
        return np.array(images)
