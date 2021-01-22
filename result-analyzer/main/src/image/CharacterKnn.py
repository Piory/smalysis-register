import glob
import os

import cv2
import numpy as np

from util.FileUtil import FileUtil


class CharacterKnn:
    def __init__(self, characterImageDirectoryPath: str):
        characterCellImages = [self.__CharacterCellImage(FileUtil.getFileNameExcludeExtension(path), cv2.imread(path, cv2.IMREAD_GRAYSCALE)) for path in glob.glob(os.path.join(characterImageDirectoryPath, '*.png'))]

        samples = np.empty((0, 100 * 100))
        labels = []
        for characterCellImage in characterCellImages:
            for i in range(characterCellImage.characterImageCount):
                cell = characterCellImage.cells[i]
                sample = cell.reshape((1, -1))
                samples = np.append(samples, sample, 0)
                labels.append(ord(characterCellImage.targetCharacter))
            print('Loaded character image is {0}'.format(characterCellImage.targetCharacter))

        labels = np.array(labels)
        labels = labels.reshape((labels.size, 1))

        knn = cv2.ml.KNearest_create()
        knn.train(np.array(samples, np.float32), cv2.ml.ROW_SAMPLE, np.array(labels, np.float32))
        self.knn = knn

    def findNearest(self, characterImage, k: int) -> str:
        sample = characterImage.reshape((1, -1))
        s = np.array(sample, np.float32)
        retval, result, neigh_resp, dists = self.knn.findNearest(s, k)
        return chr(int(retval))

    class __CharacterCellImage:
        def __init__(self, targetCharacter: str, tileImage):
            self.targetCharacter = self.__getLabel(targetCharacter)
            cells = self.__getCells(tileImage)
            characterImageCount = self.__countCharacterImage(cells)
            self.cells = np.array([cells[i] for i in range(characterImageCount)])
            self.characterImageCount = characterImageCount

        @staticmethod
        def __getLabel(s: str) -> str:
            return str.lower(s[0]) if s[-1] == '2' else s[0]

        @staticmethod
        def __getCells(tileImage):
            height, width = tileImage.shape[:2]
            tile = np.array([np.hsplit(row, int(width / 100)) for row in np.vsplit(tileImage, int(height / 100))])
            return tile.reshape((-1, 100, 100))

        @staticmethod
        def __countCharacterImage(cells) -> int:
            # 文字が書かれている画像をカウント
            return len([i for i in range(len(cells)) if not cells[i].max() == 0])
