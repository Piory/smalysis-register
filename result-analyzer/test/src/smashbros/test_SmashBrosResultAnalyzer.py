import glob
import os
from typing import List
from unittest import TestCase

import cv2

from image.CharacterKnn import CharacterKnn
from smashbros.SmashBrosResultAnalyzer import SmashBrosResultAnalyzer
from util.FileUtil import FileUtil


class TestSmashBrosResultAnalyzer(TestCase):
    SMASH_BROS_RESULT_ANALYZER = SmashBrosResultAnalyzer(CharacterKnn('../../../main/resources/concat'))

    def test_analysisResult(self) -> None:
        for noContestResultImagePath in glob.glob(os.path.join('../../../test/resources/result/no-contest', '*.png')):
            with self.subTest(targetImageName=FileUtil.getFileName(noContestResultImagePath)):
                resultImage = cv2.imread(noContestResultImagePath)
                smashBrosResultInfo = self.SMASH_BROS_RESULT_ANALYZER.analysisResult(resultImage)
                fighterNames = self.__targetFighterName(noContestResultImagePath)
                self.assertEqual(smashBrosResultInfo.ownFighterName, fighterNames[0])
                self.assertEqual(smashBrosResultInfo.opponentFighterName, fighterNames[1])

    @staticmethod
    def __targetFighterName(resultImagePath: str) -> List[str]:
        fileName = FileUtil.getFileNameExcludeExtension(resultImagePath)
        return fileName.split('_')
