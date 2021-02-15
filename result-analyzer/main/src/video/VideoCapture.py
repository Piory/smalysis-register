#!/usr/bin/env python

import cv2

from image.CharacterKnn import CharacterKnn


class VideoCapture:
    def __init__(self, videoNo: int, characterKnn: CharacterKnn):
        self.videoCapture = cv2.VideoCapture(videoNo)
        self.characterKnn = characterKnn

    def startCapture(self):
        while True:
            ref, frame = self.videoCapture.read()
            # 2色化
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            _, thresholdFrame = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)

