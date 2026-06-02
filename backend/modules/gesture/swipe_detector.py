class SwipeDetector:

    def __init__(self):

        self.previous_x = None
        self.previous_y = None

        self.cooldown = 0

    def detect_swipe(self, x, y):

        if self.previous_x is None:

            self.previous_x = x
            self.previous_y = y

            return None

        dx = x - self.previous_x
        dy = y - self.previous_y

        self.previous_x = x
        self.previous_y = y

        if self.cooldown > 0:

            self.cooldown -= 1
            return None

        THRESHOLD = 120

        if dx > THRESHOLD:

            self.cooldown = 20
            return "RIGHT"

        elif dx < -THRESHOLD:

            self.cooldown = 20
            return "LEFT"

        elif dy < -THRESHOLD:

            self.cooldown = 20
            return "UP"

        return None