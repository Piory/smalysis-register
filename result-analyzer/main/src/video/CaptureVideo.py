#!/usr/bin/env python

import cv2
import numpy as np

from image.CharacterKnn import CharacterKnn


class CaptureVideo:
    def __init__(self, videoNo: int, characterKnn: CharacterKnn):
        self.videoNo = videoNo
        self.characterKnn = characterKnn

    def startCapture(self):
        cv2.VideoCapture(self.videoNo)


def rectangleOwnFighterName(img, imgCopy, knn) -> str:
    return rectangleFighterName(img, imgCopy, 0, 240, 262, 729, knn)


def rectangleOpponentFighterName(img, imgCopy, knn) -> str:
    return rectangleFighterName(img, imgCopy, 0, 240, 1052, 1519, knn)


def rectangleFighterName(img, imgCopy, xAxis, yAxis, height, width, knn) -> str:
    # i を1文字として判断させるため、縦方向に膨張
    kernel = np.zeros((5, 5), np.uint8)
    kernel[:, 2] = 1
    cutImg = cv2.dilate(img[xAxis: yAxis, height: width], kernel)
    return rectangleFindContours(cutImg, imgCopy, xAxis, yAxis, height, width, knn)


def rectangleFindContours(img, imgCopy, xAxis, yAxis, height, width, knn: CharacterKnn) -> str:
    # 輪郭取得
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    characterResults = []
    # 輪郭ごとに処理
    for i in range(0, len(contours)):
        contour = contours[i]

        x, y, w, h = cv2.boundingRect(contour)
        x = x + height
        # 1位になると光るエフェクトを除外
        # TODO PAC-MAN の - を除外したい
        if (w / h) > 2:
            cv2.rectangle(thresholdFrame, (x, y), (x + w, y + h), (0, 0, 0), -1)
            continue
        # 横長のものは2つの文字が1つの文字として判定されている可能性が高いので、収縮して再度輪郭を書く
        elif (w / h) > 1.2:
            erodeImg = cv2.erode(thresholdFrame[y: y + h, x: x + w], np.ones((3, 3), np.uint8))
            contours2, hierarchy2 = cv2.findContours(erodeImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for i2 in range(0, len(contours2)):
                contour2 = contours2[i2]
                x2, y2, w2, h2 = cv2.boundingRect(contour2)
                x2 = x2 + x
                y2 = y2 + y
                # cv2.rectangle(imgCopy, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 1)
                result = knn.findNearest(cv2.resize(thresholdFrame[y2: y2 + h2, x2: x2 + w2], dsize=(100, 100)), 1)
                characterResults.append((x2, y2 + h2, ord(result)))

                # if cv2.waitKey(1) & 0xFF == ord('s'):
                #     print('write img {0}'.format(time.time()))
                #     cv2.imwrite('../../resources/{0}_{1}_{2}_{3}_{4}_{5}.png'.format(xAxis, yAxis, height, width, i, i2), cv2.resize(thresholdFrame[y2: y2 + h2, x2: x2 + w2], dsize=(100, 100)))

            continue

        area = abs(cv2.contourArea(contour))
        # 小さすぎものは除外
        if area < 200:
            continue

        # 輪郭を描画
        # cv2.rectangle(imgCopy, (x, y), (x + w, y + h), (0, 255, 0), 1)
        result = knn.findNearest(cv2.resize(thresholdFrame[y: y + h, x: x + w], dsize=(100, 100)), 1)
        characterResults.append((x, y + h, ord(result)))

    return getFighterName(characterResults)

    # if cv2.waitKey(1) & 0xFF == ord('s'):
    #     print('write img {0}'.format(time.time()))
    #     cv2.imwrite('../../resources/{0}_{1}_{2}_{3}_{4}.png'.format(xAxis, yAxis, height, width, i), cv2.resize(thresholdFrame[y: y + h, x: x + w], dsize=(100, 100)))


def getFighterName(characterResults) -> str:
    characterResults = np.array(characterResults)
    characterResultCount = len(characterResults)
    # 文字が見つからなかった場合
    if characterResultCount == 0:
        return ''
    # ファイター名の一番先頭の文字取得
    firstCharacter = characterResults[characterResults[:, 0] == characterResults[:, 0].min()]
    # 1列目と2列目の文字列取得
    row1 = characterResults[characterResults[:, 1] <= firstCharacter[0, 1]]
    row2 = characterResults[characterResults[:, 1] > firstCharacter[0, 1]]
    # x 座標の昇順にソートしてその座標取得
    row1 = np.sort(row1[:, 0])
    row2 = np.sort(row2[:, 0])
    # x 座標に重複があった場合は何もしない（ファイター名で x 座標がかぶることがありえないため）
    if len(row1) != len(np.unique(row1)) or len(row2) != len(np.unique(row2)):
        return ''
    # ソートした座標順に文字列の格納された配列取得
    row1 = [characterResults[characterResults[:, 0] == row].ravel() for row in row1]
    row2 = [characterResults[characterResults[:, 0] == row].ravel() for row in row2]
    # 1列目と2列目を結合して、文字のみ取得
    sortedCharacterResults = np.vstack([np.array(row1), np.array(row2)]) if len(row2) != 0 else row1
    return ''.join([chr(int(c[2])) for c in sortedCharacterResults])


characterKnn = CharacterKnn('../../resources/concat')
captureVideo = cv2.VideoCapture(1)

while True:
    ref, frame = captureVideo.read()
    # 2色化
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    _, thresholdFrame = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)

    frameCopy = frame.copy()
    ownFighterName = rectangleOwnFighterName(thresholdFrame, frameCopy, characterKnn)
    if not ownFighterName == '':
        print('ownFighterName={0}'.format(ownFighterName))
    opponentFighterName = rectangleOpponentFighterName(thresholdFrame, frameCopy, characterKnn)
    if not opponentFighterName == '':
        print('opponentFighterName={0}'.format(opponentFighterName))

    cv2.imshow("SmalysisRegister", frameCopy)

    # qキーが押されたら途中終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captureVideo.release()
cv2.destroyAllWindows()
