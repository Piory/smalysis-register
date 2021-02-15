from threading import Lock


class Singleton:
    __instance = None
    __lock = Lock()

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def getInstance(cls, input):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls._instance = cls.__internalNew(input)
        return cls._instance

    @classmethod
    def __internalNew(cls, input):
        return super().__new__(cls, input)
