from model.Range import Range


class __ConstMeta(type):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise TypeError(f'Can\'t rebind const ({name})')
        else:
            self.__setattr__(name, value)


class Constant(metaclass=__ConstMeta):
    CHARACTER_IMAGE_HEIGHT = 100
    CHARACTER_IMAGE_WIDTH = 100
    BINARIZATION_THRESH = 254
    BINARIZATION_MAX_VAL = 255
    OWN_FIGHTER_NAME_RANGE = Range(0, 240, 262, 729)
    OPPONENT_FIGHTER_NAME_RANGE = Range(0, 240, 1052, 1519)
    FIGHTER_NAME_CHARACTER_MIN_HEIGHT = 20
    KNN_K = 1
    GO_COMPARE_HIST_THRESHOLD = 0.95
    GAMESET_COMPARE_HIST_THRESHOLD = 0.95
