from PIL import Image
from Vector import Vector
from collections import deque
from utilities import GetAverage, SplitVector, GetDistance, GetCode, FlattenArray, NearDistanceComparison
import math


class VectorQuantization:
    def __init__(self, imagePath: str, CodeBookSize: int, vectorHeight: int, vectorWidth: int):
        self.CodeBookSize = CodeBookSize
        self.vectorHeight = vectorHeight
        self.vectorWidth = vectorWidth
        img = Image.open(imagePath)
        self.imageHeight = img.height + self._GetHeightPaddingValue(img.height)
        self.imageWidth = img.width + self._GetWidthPaddingValue(img.width)
        pixelsList = img.load()
        paddedPixelsList: list[[tuple[int, int, int]]] = [[(0, 0, 0) for _ in range(self.imageWidth)] for _ in
                                                          range(self.imageHeight)]
        for row in range(img.height):
            for col in range(img.width):
                paddedPixelsList[row][col] = pixelsList[col, row]

        self.vectorsArray = self._InitializeVectorsArray(paddedPixelsList)
        self.numberOfLevels = math.ceil(math.log2(CodeBookSize))
        self.numberOfDiscards: int = int(math.pow(2, self.numberOfLevels) - CodeBookSize)
        self.defaultAssosiationValue = 3

    def _GetHeightPaddingValue(self, originalImageHeight) -> int:
        return (self.vectorHeight - (originalImageHeight % self.vectorHeight)) % self.vectorHeight

    def _GetWidthPaddingValue(self, originalImageWidth) -> int:
        return (self.vectorWidth - (originalImageWidth % self.vectorWidth)) % self.vectorWidth

    def _InitializeVectorsArray(self, pixelsList: list[[tuple[int, int, int]]]) -> list[[Vector]]:
        result: list[[Vector]] = []
        for row in range(0, self.imageHeight, self.vectorHeight):
            subResult: list[Vector] = []
            for col in range(0, self.imageWidth, self.vectorWidth):
                vct: Vector = Vector(self.vectorHeight, self.vectorWidth)

                for v_row in range(self.vectorHeight):
                    for v_col in range(self.vectorWidth):
                        vct.SetPixel(v_row, v_col, pixelsList[v_row + row][v_col + col])

                subResult.append(vct)
            result.append(subResult)

        return result

    # returns the assosiation list after reaching required level
    # more assosiation should be done later
    def LBG(self) -> list[Vector]:
        currentLevel = 0

        initialAvg = GetAverage(FlattenArray(self.vectorsArray), self.vectorWidth, self.vectorHeight)
        Q: deque = deque()
        Q.append(initialAvg)

        while currentLevel < self.numberOfLevels:
            queueSize = len(Q)
            splittingArray: list[Vector] = []

            for _ in range(queueSize):
                vct = Q.pop()
                a, b = SplitVector(vct)
                splittingArray.append(a)
                splittingArray.append(b)

            # create empty clusters
            result = NearDistanceComparison(self.vectorsArray, splittingArray, len(splittingArray))
            for cluster in result:
                Q.append(GetAverage(cluster, self.vectorWidth, self.vectorHeight))

            currentLevel += 1

        return list(Q)

    def FinalizeLBG(self, assosiatedList: list[Vector]) -> list[Vector]:
        if self.numberOfDiscards:
            assosiatedList = assosiatedList[:-self.numberOfDiscards]
        finalCookBookResult = assosiatedList
        for _ in range(self.defaultAssosiationValue):
            finalAssosiation: list[list[Vector]] = NearDistanceComparison(self.vectorsArray, finalCookBookResult,
                                                                          self.CodeBookSize)
            finalCookBookResult = [
                GetAverage(cluster, self.vectorWidth, self.vectorHeight)
                for cluster in finalAssosiation
            ]

        return finalCookBookResult

    def WriteLabels(self, codeBook: list[Vector]):
        for vectors in self.vectorsArray:
            for vector in vectors:
                minIndex = 0
                minValue = GetDistance(vector, codeBook[0], vector.vectorWidth, vector.vectorHeight)
                for j in range(1, len(codeBook)):
                    d = GetDistance(vector, codeBook[j], vector.vectorWidth, vector.vectorHeight)
                    if d < minValue:
                        minValue = d
                        minIndex = j

                vector.SetLabel(codeBook[minIndex].GetLabel())

    ## Important Note
    ## the first number writen in the codebook file
    ## is the codeBookSize
    ## Second is the vectorWidth
    ## third is vectorHeight
    ## fourth is ImageWidth
    ## fifth is ImageHeight
    def Encode(self, fileName, codeBookFileName):
        leveledList = self.LBG()
        codeBook: list[Vector] = self.FinalizeLBG(leveledList)
        for i in range(len(codeBook)):
            code = GetCode(i, self.numberOfLevels)
            codeBook[i].SetLabel(code)

        self.WriteLabels(codeBook)
        with open(codeBookFileName, 'w') as codeBookFile:
            codeBookFile.write(str(self.CodeBookSize) + "\n")
            codeBookFile.write(str(self.vectorWidth) + "\n")
            codeBookFile.write(str(self.vectorHeight) + "\n")
            codeBookFile.write(str(self.imageWidth) + "\n")
            codeBookFile.write(str(self.imageHeight) + "\n")
            for vectorCode in codeBook:
                codeBookFile.write(vectorCode.GetVectorStringRepresented() + "\n")

        with open(fileName, 'w') as encodingFile:
            for vectors in self.vectorsArray:
                for vector in vectors:
                    encodingFile.write(vector.GetLabel())

    @staticmethod
    def Decode(codeBookFile, bitsStreamFile) -> Image:
        with open(codeBookFile, 'r') as f:
            codeBookSize = int(f.readline().strip())
            vectorWidth = int(f.readline().strip())
            vectorHeight = int(f.readline().strip())
            imageWidth = int(f.readline().strip())
            imageHeight = int(f.readline().strip())

            pixelsList: list[list[tuple[int, int, int]]] = []
            for line in f:
                if not line.strip():
                    continue

                row = []
                for t in line.split():
                    values = tuple(map(int, t.strip("()").split(",")))
                    row.append((values[0], values[1], values[2]))
                pixelsList.append(row)

            codeBookVectors: list[Vector] = []
            for i in range(codeBookSize):
                vct = Vector(vectorHeight, vectorWidth)
                for r in range(vectorHeight):
                    for c in range(vectorWidth):
                        vct.SetPixel(r, c, pixelsList[(i * vectorHeight) + r][c])
                codeBookVectors.append(vct)

        numberOfLevels = math.ceil(math.log2(codeBookSize))
        mapResult: dict[str, Vector] = {}

        for i in range(len(codeBookVectors)):
            code = GetCode(i, numberOfLevels)
            codeBookVectors[i].SetLabel(code)
            mapResult[code] = codeBookVectors[i]

        vectorsArray: list[Vector] = []

        with open(bitsStreamFile, 'r') as stream:
            while True:
                code = stream.read(numberOfLevels)
                if not code:
                    break
                vectorsArray.append(mapResult[code])

        img = Image.new("RGB", (imageWidth, imageHeight), (0, 0, 0))

        pixelsList: list[[tuple[int, int, int]]] = [[(0, 0, 0) for _ in range(imageWidth)] for _ in range(imageHeight)]

        imgPixels = img.load()
        idx = 0
        for row in range(0, imageHeight, vectorHeight):
            for col in range(0, imageWidth, vectorWidth):
                vct = vectorsArray[idx]
                idx += 1
                for v_row in range(vectorHeight):
                    for v_col in range(vectorWidth):
                        imgPixels[col + v_col, row + v_row] = vct.GetPixel(v_row, v_col)

        return img
