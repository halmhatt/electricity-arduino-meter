
class BaseMath:
    """A base class implementing math functions."""

    @staticmethod
    def average(values):
        """Returns the average"""
        return sum(values) / len(values)

    @classmethod
    def similar(cls, values, persentage=0.2) -> float:
        """Returns True if the values are similar in percent."""
        average = cls.average(values)

        for value in values:
            diff = value - average
            if diff / average > persentage:
                return False
        return True