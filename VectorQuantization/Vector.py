# colors are RGB mode (R,G,B) as a tuple
# i wanted to work with Grayscale, but conversion from grayscale to rgb does not return the colors back

class Vector:
    def __init__(self, vectorHeight, vectorWidth):
        self.vectorHeight = vectorHeight
        self.vectorWidth = vectorWidth
        self.vector: list[[tuple[int, int, int]]] = [[(0, 0, 0) for _ in range(vectorWidth)] for _ in
                                                           range(vectorHeight)]
        self.Label = ""

    def GetPixel(self, row, col) -> tuple[int, int, int]:
        if not self._isValid(row, col):
            raise Exception(f'Invalid row value:{row} and col value:{col}')

        return self.vector[row][col]

    def GetLabel(self):
        return self.Label

    def SetLabel(self, label: str):
        self.Label = label

    def SetPixel(self, row, col, value: tuple[int, int, int]) -> None:
        if not self._isValid(row, col):
            raise Exception(f'Invalid row value:{row} and col value:{col}')

        self.vector[row][col] = value

    def _isValid(self, row, col) -> bool:
        return 0 <= row < self.vectorHeight and 0 <= col < self.vectorWidth

    def GetVectorStringRepresented(self):
        S: str = ""
        for row in self.vector:
            subS: str = ""
            for col in row:
                subS += f'({col[0]},{col[1]},{col[2]})' + " "
            S += subS + "\n"

        return S
