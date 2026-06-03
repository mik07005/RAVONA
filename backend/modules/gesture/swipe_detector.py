class SwipeDetector:

    def __init__(self):

        self.start_x = None
        self.start_y = None

    def arm(self, x, y):

        self.start_x = x
        self.start_y = y

    def detect_swipe(self, current_x, current_y):

        if self.start_x is None:
            return None

        dx = current_x - self.start_x

        THRESHOLD = 150

        # Final Navigation Mapping

        if dx > THRESHOLD:

            self.start_x = None

            return "NEXT_WINDOW"

        elif dx < -THRESHOLD:

            self.start_x = None

            return "PREVIOUS_WINDOW"

        return None