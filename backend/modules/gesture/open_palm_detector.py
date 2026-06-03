class OpenPalmDetector:

    def is_open_palm(self, fingers):

        if len(fingers) < 5:
            return False

        return (
            fingers[1] == 1 and
            fingers[2] == 1 and
            fingers[3] == 1 and
            fingers[4] == 1
        )