import glob
import os
from unittest import TestCase

import cv2

from image.CharacterKnn import CharacterKnn
from util.FileUtil import FileUtil


class TestCharacterKnn(TestCase):
    def test_findNearest(self) -> None:
        characterKnn = self.__createCharacterKnn()
        for dirName in os.listdir('../../../main/resources'):
            if dirName.startswith('.'):
                continue
            if dirName == 'concat' or dirName == 'Q':
                continue
            # TODO K 1以降はVとtの教師データが1枚しかないのでできない
            k = 1
            targetCharacter = self.__targetCharacter(dirName)
            for characterImagePath in glob.glob(os.path.join('../../../main/resources', dirName, '*.png')):
                with self.subTest(targetCharacter=targetCharacter, targetImageName=FileUtil.getFileName(characterImagePath), k=k):
                    result = characterKnn.findNearest(cv2.imread(characterImagePath, cv2.IMREAD_GRAYSCALE), k)
                    self.assertEqual(result, targetCharacter)

    @staticmethod
    def __createCharacterKnn() -> CharacterKnn:
        return CharacterKnn('../../../main/resources/concat')

    @staticmethod
    def __targetCharacter(dirName) -> str:
        return str.lower(dirName[0]) if dirName[-1] == '2' else dirName[0]
