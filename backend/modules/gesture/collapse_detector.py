import math


class CollapseDetector:

    def is_collapsed(
        self,
        landmarks
    ):

        if len(landmarks) < 21:
            return False

        palm_x = landmarks[0][1]
        palm_y = landmarks[0][2]

        tips = [
            4,
            8,
            12,
            16,
            20
        ]

        distances = []

        for tip in tips:

            tip_x = landmarks[tip][1]
            tip_y = landmarks[tip][2]

            distance = math.sqrt(
                (tip_x - palm_x) ** 2 +
                (tip_y - palm_y) ** 2
            )

            distances.append(
                distance
            )

        average_distance = (
            sum(distances)
            / len(distances)
        )

        return average_distance < 80