#!/usr/bin/env python
import os

import cv2
import numpy as np

from util.ImageUtil import ImageUtil


class CharacterImageGenerator:
    def __init__(self, characterImagePath: str):
        self.images = None
        self.characterImagePath = characterImagePath
        self.loadImages()

    def concatCharacterTile(self, horizontalImageCount: int, outputImagePath: str) -> None:
        rowCount = np.ceil(len(self.images) / horizontalImageCount).astype(int)
        characterTile = np.zeros((rowCount * horizontalImageCount, 100, 100))
        for i in range(len(self.images)):
            characterTile[i] = self.images[i]
        cv2.imwrite(outputImagePath, ImageUtil.concatTile(np.vsplit(characterTile, rowCount)))

    def loadImages(self):
        self.images = ImageUtil.loadPngImage(self.characterImagePath, '*.png')


for dirName in os.listdir('../../resources'):
    if dirName.startswith('.'):
        continue
    if dirName == 'concat' or dirName == 'Q':
        continue
    print(dirName)
    characterImageGenerator = CharacterImageGenerator('../../resources/{0}/'.format(dirName))
    characterImageGenerator.concatCharacterTile(10, '../../resources/concat/{0}.png'.format(dirName))