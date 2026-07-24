class CursorDetector:

    def is_cursor_gesture(self, fingers):
        """
        Cursor Mode Gesture:
        Thumb + Index Finger
        [Thumb, Index, Middle, Ring, Pinky]
        [1,     1,     0,      0,    0]
        """
        if len(fingers) != 5:
            return False

        # Thumb Down
        # Index Up
        # Middle Up
        # Ring Down
        # Pinky Down

        return fingers == [1, 1, 0, 0, 0]