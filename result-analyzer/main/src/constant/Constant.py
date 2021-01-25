# クラス定義そのものに対してのsetter制御用メタクラス
class __ConstMeta(type):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise TypeError(f'Can\'t rebind const ({name})')
        else:
            self.__setattr__(name, value)


class Constant(metaclass=__ConstMeta):
    CHARACTER_IMAGE_HEIGHT = 100
    CHARACTER_IMAGE_WIDTH = 100
