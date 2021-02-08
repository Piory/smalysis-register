from typing import Optional

import cv2
import numpy as np

from constant.Constant import Constant
from enums.Rank import Rank
from image.CharacterKnn import CharacterKnn
from model.Range import Range
from model.SmashBrosResultInfo import SmashBrosResultInfo
from util.ImageUtil import ImageUtil


class SmashBrosResultAnalyzer:
    def __init__(self, characterKnn: CharacterKnn, isRectangle: bool, resultMaskFor1on1, rankMaskFor1on1):
        self.characterKnn = characterKnn
        self.isRectangle = isRectangle
        self.resultMaskFor1on1 = resultMaskFor1on1
        self.rankMaskFor1on1 = rankMaskFor1on1

    def analysisResult(self, resultImage, screenFrame) -> SmashBrosResultInfo:
        maskedResultImage = cv2.bitwise_and(resultImage, resultImage, mask=self.resultMaskFor1on1)
        binarizationImage = ImageUtil.binarization(maskedResultImage, Constant.BINARIZATION_THRESH, Constant.BINARIZATION_MAX_VAL)
        ownFighterName = self.__searchOwnFighterName(binarizationImage, screenFrame)
        opponentFighterName = self.__searchOpponentFighterName(binarizationImage, screenFrame)
        ownRank, opponentRank = self.__rank(maskedResultImage)
        return SmashBrosResultInfo(ownFighterName, ownRank, opponentFighterName, opponentRank)

    def __searchOwnFighterName(self, resultImage, screenFrame) -> Optional[str]:
        return self.__searchFighterName(resultImage, screenFrame, Constant.OWN_FIGHTER_NAME_RANGE)

    def __searchOpponentFighterName(self, resultImage, screenFrame) -> Optional[str]:
        return self.__searchFighterName(resultImage, screenFrame, Constant.OPPONENT_FIGHTER_NAME_RANGE)

    def __searchFighterName(self, resultImage, screenFrame, fighterNameRange: Range) -> Optional[str]:
        # i を1文字として判断させるため、縦方向に膨張
        kernel = np.zeros((5, 5), np.uint8)
        kernel[:, 2] = 1
        filteredFighterNameAreaImage = cv2.dilate(ImageUtil.cutImage(resultImage, fighterNameRange), kernel)

        # 輪郭取得
        contours, hierarchy = cv2.findContours(filteredFighterNameAreaImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        characterResults = []
        # 輪郭ごとに処理
        for i in range(len(contours)):
            contour = contours[i]

            x, y, w, h = cv2.boundingRect(contour)
            x = x + fighterNameRange.left
            # ファイター名の文字として検出された位置の高さが小さすぎる場合は除外
            if h <= Constant.FIGHTER_NAME_CHARACTER_MIN_HEIGHT:
                continue
            # 1位になると光るエフェクトを除外
            if (w / h) > 2:
                cv2.rectangle(resultImage, (x, y), (x + w, y + h), (0, 0, 0), -1)
                continue
            # 横長のものは2文字がまとめて検出されている可能性が高いので、収縮して再検出
            elif (w / h) > 1.2:
                erodeImg = cv2.erode(ImageUtil.cutImage(resultImage, Range.create(x, y, w, h)), np.ones((3, 3), np.uint8))
                contours2, hierarchy2 = cv2.findContours(erodeImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for i2 in range(len(contours2)):
                    contour2 = contours2[i2]
                    x2, y2, w2, h2 = cv2.boundingRect(contour2)
                    x2 = x2 + x
                    y2 = y2 + y
                    characterRange = Range.create(x2, y2, w2, h2)
                    if self.isRectangle:
                        cv2.rectangle(screenFrame, (characterRange.left, characterRange.top), (characterRange.right, characterRange.bottom), (0, 255, 0), 1)
                    character = self.__findNearestForCharacterKnn(resultImage, characterRange)
                    characterResults.append([x2, y2 + h2, ord(character)])
                continue

            # 小さすぎものは除外
            if self.__contourLessThan(contour, 200):
                continue

            characterRange = Range.create(x, y, w, h)
            if self.isRectangle:
                cv2.rectangle(screenFrame, (characterRange.left, characterRange.top), (characterRange.right, characterRange.bottom), (0, 255, 0), 1)
            character = self.__findNearestForCharacterKnn(resultImage, characterRange)
            characterResults.append([x, y + h, ord(character)])

        return self.__getFighterName(characterResults)

    def __rank(self, resultImage) -> tuple[Rank, Rank]:
        maskedRank = self.__binarization1stRank(resultImage)
        contours, hierarchy = cv2.findContours(self.rankMaskFor1on1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ranges = []
        for i in range(len(contours)):
            contour = contours[i]
            x, y, w, h = cv2.boundingRect(contour)
            ranges.append(Range.create(x, y, w, h))
        rankResult = []
        # 左順になるようにソート
        ranges.sort(key=lambda ran: ran.left)
        for r in ranges:
            img = ImageUtil.cutImage(maskedRank, r)
            # 全部黒色なら RANK_2ND に設定
            rankResult.append(Rank.RANK_2ND if img.max() == 0 else Rank.RANK_1ST)
        # どちらも黒色判定なら NO_CONTEST にする
        if rankResult.count(Rank.RANK_2ND) == 2:
            return Rank.NO_CONTEST, Rank.NO_CONTEST
        else:
            return rankResult[0], rankResult[1]

    def __binarization1stRank(self, result):
        rankAreaMasked = cv2.bitwise_and(result, result, mask=self.rankMaskFor1on1)
        lower = np.array([20, 165, 165])
        upper = np.array([60, 255, 255])
        rank1stMask = cv2.inRange(cv2.cvtColor(rankAreaMasked, cv2.COLOR_BGR2HSV), lower, upper)
        rank = cv2.bitwise_and(result, result, mask=rank1stMask)
        return ImageUtil.binarization(rank, 0, 254)

    def __findNearestForCharacterKnn(self, resultImage, characterRange: Range) -> str:
        resizedResultImage = cv2.resize(ImageUtil.cutImage(resultImage, characterRange), dsize=(Constant.CHARACTER_IMAGE_WIDTH, Constant.CHARACTER_IMAGE_HEIGHT))
        return self.characterKnn.findNearest(resizedResultImage, Constant.KNN_K)

    @staticmethod
    def __contourLessThan(contour, val) -> bool:
        area = abs(cv2.contourArea(contour))
        return area < val

    @staticmethod
    def __getFighterName(characterResults) -> Optional[str]:
        characterResults = np.array(characterResults)
        characterResultCount = len(characterResults)
        # 文字が見つからなかった場合
        if characterResultCount == 0:
            return None
        # ファイター名の一番先頭の文字x座標を取得
        firstCharacter = characterResults[characterResults[:, 0] == characterResults[:, 0].min()]
        # 1列目と2列目のファイター名取得
        fighterNameRow1 = SmashBrosResultAnalyzer.__sortFighterName(characterResults[characterResults[:, 1] <= firstCharacter[0, 1]])
        if fighterNameRow1 is None:
            return None
        fighterNameRow2 = SmashBrosResultAnalyzer.__sortFighterName(characterResults[characterResults[:, 1] > firstCharacter[0, 1]])
        return fighterNameRow1 + fighterNameRow2 if fighterNameRow2 is not None else fighterNameRow1

    @staticmethod
    def __sortFighterName(row) -> Optional[str]:
        # x座標に重複があった場合は何もしない（ファイター名でx座標がかぶることがありえないため）
        if len(row[:, 0]) != len(np.unique(row[:, 0])):
            return None
        # x座標の昇順にソート
        sortedRow = [row[i] for i in np.argsort(row[:, 0])]
        # 文字列を結合
        return ''.join([chr(int(c[2])) for c in sortedRow])
