import json
from datetime import datetime
from typing import Any

import cv2

from enums.Rank import Rank
from enums.SmashBrosStatus import SmashBrosStatus
from image.CharacterKnn import CharacterKnn
from image.MaskGenerator import MaskGenerator
from smashbros.SmashBrosManager import SmashBrosManager
from smashbros.SmashBrosResultAnalyzer import SmashBrosResultAnalyzer


def mainVideoCapture():
    resultMask = cv2.imread('../resources/mask/1on1/result_mask.png', cv2.IMREAD_GRAYSCALE)
    rankMask = cv2.imread('../resources/mask/1on1/rank_mask.png', cv2.IMREAD_GRAYSCALE)
    smashBrosAnalyzer = SmashBrosResultAnalyzer(CharacterKnn('../resources/character/concat'), False, resultMask, rankMask)
    captureVideo = cv2.VideoCapture(1)
    smashBrosManager = SmashBrosManager.getInstance(SmashBrosStatus.NONE, cv2.imread('../resources/mask/go/mask.png'))

    while True:
        ref, frame = captureVideo.read()
        if frame is None:
            print('frame is None')
            continue

        # frameCopy = frame.copy()
        # result = smashBrosAnalyzer.analysisResult(frame, frameCopy)
        # isFighterNameNotNone = result.ownFighterName is not None and result.opponentFighterName is not None
        # if isFighterNameNotNone and len(result.ownFighterName) > 2 and len(result.opponentFighterName) > 2:
        smashBrosManager.analysisSmashBrosStatus(frame)
        cv2.imshow("SmalysisRegister", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            print('write img')
            cv2.imwrite(f'./go_{datetime.now().microsecond}.png', frame)

            # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    captureVideo.release()
    cv2.destroyAllWindows()


class EnumJSONEncoder(json.JSONEncoder):
    ENUMS = {
        'Rank': Rank,
    }

    def default(self, o: Any) -> Any:
        if type(o) in self.ENUMS.values():
            return {'__enum__': str(o)}
        return json.JSONEncoder.default(o)


def main():
    gameset = cv2.imread('../../test/resources/gameset/gameset_4.png', cv2.IMREAD_COLOR)
    cv2.imwrite('./go.png', MaskGenerator.createGamesetMask(gameset))


main()
