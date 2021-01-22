import os


class FileUtil:
    @staticmethod
    def getFileName(path) -> str:
        return os.path.basename(path)

    @staticmethod
    def getFileNameExcludeExtension(path) -> str:
        return os.path.splitext(os.path.basename(path))[0]
