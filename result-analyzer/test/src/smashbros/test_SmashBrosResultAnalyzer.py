import glob
import os
from typing import List
from unittest import TestCase

import cv2

from enums.Rank import Rank
from image.CharacterKnn import CharacterKnn
from smashbros.SmashBrosResultAnalyzer import SmashBrosResultAnalyzer
from util.FileUtil import FileUtil


class TestSmashBrosResultAnalyzer(TestCase):
    SMASH_BROS_RESULT_ANALYZER = SmashBrosResultAnalyzer(
        CharacterKnn('../../../main/resources/character/concat'),
        False,
        cv2.imread('../../../main/resources/mask/1on1/result_mask.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('../../../main/resources/mask/1on1/rank_mask.png', cv2.IMREAD_GRAYSCALE),
    )

    def test_analysisResult_1on1_no_contest(self) -> None:
        for resultImagePath in glob.glob(os.path.join('../../../test/resources/result/1on1/no-contest', '*.png')):
            self.__assertResultImage(resultImagePath, Rank.NO_CONTEST, Rank.NO_CONTEST)

    def test_analysisResult_1on1_1P_win(self) -> None:
        for resultImagePath in glob.glob(os.path.join('../../../test/resources/result/1on1/1P-win', '*.png')):
            self.__assertResultImage(resultImagePath, Rank.RANK_1ST, Rank.RANK_2ND)

    def test_analysisResult_1on1_2P_win(self) -> None:
        for resultImagePath in glob.glob(os.path.join('../../../test/resources/result/1on1/2P-win', '*.png')):
            self.__assertResultImage(resultImagePath, Rank.RANK_2ND, Rank.RANK_1ST)

    def __assertResultImage(self, resultImagePath: str, ownRank: Rank, opponentRank: Rank) -> None:
        with self.subTest(targetImageName=FileUtil.getFileName(resultImagePath)):
            resultImage = cv2.imread(resultImagePath)
            smashBrosResultInfo = self.SMASH_BROS_RESULT_ANALYZER.analysisResult(resultImage, resultImage.copy())
            fighterNames = self.__targetFighterName(resultImagePath)
            self.assertEqual(smashBrosResultInfo.ownFighterName, fighterNames[0])
            self.assertEqual(smashBrosResultInfo.ownRank, ownRank)
            self.assertEqual(smashBrosResultInfo.opponentFighterName, fighterNames[1])
            self.assertEqual(smashBrosResultInfo.opponentRank, opponentRank)

    @staticmethod
    def __targetFighterName(resultImagePath: str) -> List[str]:
        fileName = FileUtil.getFileNameExcludeExtension(resultImagePath)
        return fileName.split('_')
