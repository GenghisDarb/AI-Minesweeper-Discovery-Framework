class BetaConfidence:
    def __init__(self):
        self.alpha = 0.0
        self.beta = 0.0

    def update(self, revealed_is_false: bool):
        if revealed_is_false:
            self.alpha += 0.5
        else:
            self.beta += 0.5