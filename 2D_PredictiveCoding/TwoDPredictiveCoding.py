from UniformQuantizerTable import UniformQuantizer
from PIL import Image
from utilities import PredictNext_Pixel, PixelDifference, GetMaxTupleFrom2DArray, GetMinTupleFrom2DArray, GetCode, TuplesTo2DGrid, PixelsToImage


# default pillow image access is [col,row]

class TwoDPredictiveCoding:
    def __init__(self, numberOfBits: int, imgPath: str):
        self.numberOfBits = numberOfBits
        self.img = Image.open(imgPath)
        self.originalImagePixels: Image.core.PixelAccess = self.img.load()
        self.imageWidth: int = self.img.width
        self.imageHeight: int = self.img.height
        self.firstRow: list[tuple[int, int, int]] = self._GetFirstRow()
        self.firstCol: list[tuple[int, int, int]] = self._GetFirstColumn()
        self.predictedPixels: list[list[tuple[int, int, int]]] = [[(0, 0, 0) for _ in range(self.imageWidth)] for _ in range(self.imageHeight)]
        self.errorsList: list[list[tuple[int, int, int]]] = self.ConstructErrors()

    def _GetFirstRow(self) -> list[tuple[int, int, int]]:
        result: list[tuple[int, int, int]] = []
        for i in range(self.imageWidth):
            pixel = self.originalImagePixels[i, 0]
            result.append(pixel[:3])  # take first 3 which are RGB
        return result

    def _GetFirstColumn(self) -> list[tuple[int, int, int]]:
        result: list[tuple[int, int, int]] = []
        for i in range(self.imageHeight):
            pixel = self.originalImagePixels[0, i]
            result.append(pixel[:3])  # take first 3 which are RGB
        return result

    def ConstructErrors(self) -> list[list[tuple[int, int, int]]]:
        errors: list[list[tuple[int, int, int]]] = [[(0, 0, 0) for _ in range(self.imageWidth - 1)] for _ in
                                                    range(self.imageHeight - 1)]

        for col in range(len(self.firstRow)):
            self.predictedPixels[0][col] = self.firstRow[col]

        for row in range(len(self.firstCol)):
            self.predictedPixels[row][0] = self.firstCol[row]

        for row in range(1, self.imageHeight):
            for col in range(1, self.imageWidth):
                A = self.predictedPixels[row][col - 1]
                B = self.predictedPixels[row - 1][col - 1]
                C = self.predictedPixels[row - 1][col]
                self.predictedPixels[row][col] = PredictNext_Pixel(A, B, C)

        for row in range(1, self.imageHeight):
            for col in range(1, self.imageWidth):
                P1: tuple[int, int, int] = self.originalImagePixels[col, row][:3]
                P2: tuple[int, int, int] = self.predictedPixels[row][col]
                errors[row - 1][col - 1] = PixelDifference(P1, P2)

        return errors

    # the content of the file is as following
    #  line number 1 => first row in the image
    #  line number 2 => first col in the image
    #  line number 3 => imageWidth,imageHeight
    #  line number 4 => first Q inverse Table
    #  line number 5 => second Q inverse Table
    #  line number 6 => third Q inverse Table
    #  line number 7 => data stream
    def Encode(self, filePath: str):
        rows = self.imageHeight - 1
        cols = self.imageWidth - 1
        MinValues: list[int] = GetMinTupleFrom2DArray(self.errorsList, rows, cols)
        MaxValues: list[int] = GetMaxTupleFrom2DArray(self.errorsList, rows, cols)

        firstQ: UniformQuantizer = UniformQuantizer(MaxValues[0], MinValues[0], self.numberOfBits)
        secondQ: UniformQuantizer = UniformQuantizer(MaxValues[1], MinValues[1], self.numberOfBits)
        thirdQ: UniformQuantizer = UniformQuantizer(MaxValues[2], MinValues[2], self.numberOfBits)

        predictedImage = PixelsToImage(self.predictedPixels)
        predictedImage.save("predictedImage.jpg")

        with open("errors.txt", "w") as errorsFile:
            errorsFile.write(TuplesTo2DGrid(self.errorsList))

        with open(filePath, "w") as file:
            file.write(str(self.firstRow) + "\n")
            file.write(str(self.firstCol) + "\n")
            file.write(str(self.imageWidth) + "," + str(self.imageHeight) + "\n")
            file.write(firstQ.GetQInverse() + "\n")
            file.write(secondQ.GetQInverse() + "\n")
            file.write(thirdQ.GetQInverse() + "\n")
            for row in self.errorsList:
                for pixel in row:
                    firstQCode = GetCode(firstQ.Q(pixel[0]), self.numberOfBits)
                    secondQCode = GetCode(secondQ.Q(pixel[1]), self.numberOfBits)
                    thirdQCode = GetCode(thirdQ.Q(pixel[2]), self.numberOfBits)
                    finalCode = firstQCode + secondQCode + thirdQCode
                    file.write(finalCode)

