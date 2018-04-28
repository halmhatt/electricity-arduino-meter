
class OverlapFilter:

    @staticmethod
    def filter(steps: list) -> list:
        new_list = []

        for step in steps:
            overlap = False
            for _step in new_list:
                if _step.first.utc_datetime < step.first.utc_datetime < _step.last.utc_datetime:
                    # Overlap
                    overlap = True

            if not overlap:
                new_list.append(step)
        return new_list