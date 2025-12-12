import math


class UniformQuantizer:
    # in our case the max would be max value of errors, min value of errors
    def __init__(self, Max: int, Min: int, numberOfBits: int):
        self.bitsNumber: int = numberOfBits
        self.Min = Min
        self.Max = Max

        self.FullScale = Max - Min + 1
        self.Q_Step = math.ceil(self.FullScale / (2 ** numberOfBits))
        self.steps: int = math.ceil(self.FullScale / self.Q_Step)
        self.rangeQMap: dict[tuple[int, int], int] = self._Construct_Q()

        # makes a Ranges tuple that maps to Q values

    def _Construct_Q(self) -> dict[tuple[int, int], int]:
        lower: int = self.Min
        upper: int = lower + self.Q_Step - 1
        result: dict[tuple[int, int], int] = {}

        for i in range(self.steps):
            result[(lower, upper)] = i

            lower = upper + 1
            upper = lower + self.Q_Step - 1

            if lower > self.Max:
                break

        return result

    def Q(self, value: int) -> int:
        for k, v in self.rangeQMap.items():
            if k[0] <= value <= k[1]:
                return v
        raise Exception(f"value:{value} does not fall in a range")

    def Q_Inverse(self, Q: int) -> int:
        for k, v in self.rangeQMap.items():
            if Q == v:
                return math.ceil((k[0] + k[1]) / 2)
        raise Exception(f"Q:{Q} value is not in the map")

    def GetQInverse(self) -> str:
        values: list[int] = [self.Q_Inverse(step) for step in range(self.steps)]
        result: str = ""
        for i in range(len(values) - 1):
            result += str(values[i]) + ","

        result += str(values[len(values) - 1])
        return result

    def GetMax(self) -> int:
        return self.Max

    def GetMin(self) -> int:
        return self.Min
