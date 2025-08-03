


class PikaUserInput:
    def __init__(self, xDirection=0, yDirection=0, powerHit=0):
        self.xDirection = xDirection  # 0: no horizontal-direction input, -1: left-direction input, 1: right-direction input
        self.yDirection = yDirection  # 0: no vertical-direction input, -1: up-direction input, 1: down-direction input
        self.powerHit = powerHit    # 0: auto-repeated or no power hit input, 1: not auto-repeated power hit input