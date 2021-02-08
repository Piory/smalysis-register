class Range:
    def __init__(self, top: int, bottom: int, left: int, right: int):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    @staticmethod
    def create(x: int, y: int, w: int, h: int):
        return Range(y, y + h, x, x + w)
