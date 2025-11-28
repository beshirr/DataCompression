from Vector import Vector
import math


def PixelDifference(first, second) -> tuple[int, int, int]:
    return first[0] - second[0], first[1] - second[1], first[2] - second[2]


def AbsolutePixelDifference(first, second) -> tuple[int, int, int]:
    result = PixelDifference(first, second)
    return abs(result[0]), abs(result[1]), abs(result[2])


def SumTwoRGBPixels(first, second) -> tuple[int, int, int]:
    return first[0] + second[0], first[1] + second[1], first[2] + second[2]


def SumThreeColorChannelPixels(pixel: tuple[int, int, int]):
    return pixel[0] + pixel[1] + pixel[2]


def GetDistance(firstVector: Vector, secondVector: Vector, vectorWidth, vectorHeight) -> int:
    result: int = 0
    for row in range(vectorHeight):
        for col in range(vectorWidth):
            result += SumThreeColorChannelPixels(
                AbsolutePixelDifference(firstVector.GetPixel(row, col), secondVector.GetPixel(row, col)))
    return result


def GetAverage(vectorsList: list[Vector], vectorWidth, vectorHeight) -> Vector:
    result: Vector = Vector(vectorHeight, vectorWidth)
    numberOfVectors: int = len(vectorsList)

    for i in range(vectorHeight):
        for j in range(vectorWidth):
            for v_i in range(numberOfVectors):
                vctElm: Vector = vectorsList[v_i]
                sumResult = SumTwoRGBPixels(result.GetPixel(i, j), vctElm.GetPixel(i, j))
                result.SetPixel(i, j, sumResult)

    for i in range(vectorHeight):
        for j in range(vectorWidth):
            pixel = result.GetPixel(i, j)
            pixel = (pixel[0] // numberOfVectors, pixel[1] // numberOfVectors, pixel[2] // numberOfVectors)
            result.SetPixel(i, j, pixel)

    return result


def SplitVector(vector: Vector) -> tuple[Vector, Vector]:
    left: Vector = Vector(vector.vectorHeight, vector.vectorWidth)
    right: Vector = Vector(vector.vectorHeight, vector.vectorWidth)

    for i in range(vector.vectorHeight):
        for j in range(vector.vectorWidth):
            pixel = vector.GetPixel(i, j)
            leftPixel = (max(pixel[0] - 1, 0), max(pixel[1] - 1, 0), max(pixel[2] - 1, 0))
            rightPixel = (min(pixel[0] + 1, 255), min(pixel[1] + 1, 255), min(pixel[2] + 1, 255))
            left.SetPixel(i, j, leftPixel)
            right.SetPixel(i, j, rightPixel)

    return left, right


def NearDistanceComparison(pixelsList: list[list[Vector]], compareAgainst: list[Vector], clusterSize) -> list[list[Vector]]:
    result: list[list[Vector]] = [[] for _ in range(clusterSize)]

    # assign vectors
    for vectorList in pixelsList:
        for vector in vectorList:
            minIndex = 0
            minValue = GetDistance(vector, compareAgainst[0], vector.vectorWidth, vector.vectorHeight)
            for j in range(1, len(compareAgainst)):
                d = GetDistance(vector, compareAgainst[j], vector.vectorWidth, vector.vectorHeight)
                if d < minValue:
                    minValue = d
                    minIndex = j
            result[minIndex].append(vector)

    return result


def FlattenArray(TwoDVectorArray: list[[Vector]]) -> list[Vector]:
    flattened_list: list[Vector] = []
    for sublist in TwoDVectorArray:
        flattened_list.extend(sublist)
    return flattened_list


def GetCode(n: int, levels: int):
    return format(n, f'0{levels}b')
