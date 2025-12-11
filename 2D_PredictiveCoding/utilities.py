from PIL import Image

def GetCode(n: int, levels: int):
    return format(n, f'0{levels}b')


# use it for the decompression
def ClampPixelToAllowedRanges(pixelValue: int) -> int:
    if pixelValue > 255:
        return 255
    elif pixelValue < 0:
        return 0
    return pixelValue


def PredictNext(A: int, B: int, C: int) -> int:
    if B >= max(A, C):
        return min(A, C)

    elif B <= min(A, C):
        return max(A, C)

    return A + C - B


def PredictNext_Pixel(p_A: tuple[int, int, int], p_B: tuple[int, int, int], p_C: tuple[int, int, int]) -> tuple[
    int, int, int]:
    result: list = [0, 0, 0]
    for i in range(3):
        result[i] = PredictNext(p_A[i], p_B[i], p_C[i])

    return result[0], result[1], result[2]


def PixelDifference(P1: tuple[int, int, int], P2: tuple[int, int, int]):
    return P1[0] - P2[0], P1[1] - P2[1], P1[2] - P2[2]


def GetMaxTupleFrom2DArray(values: list[list[tuple[int, int, int]]], ROWS: int, COLS: int) -> list[int]:
    result: list[int] = [values[0][0][0], values[0][0][1], values[0][0][2]]

    for row in range(ROWS):
        for col in range(COLS):
            result[0] = max(result[0], values[row][col][0])
            result[1] = max(result[1], values[row][col][1])
            result[2] = max(result[2], values[row][col][2])

    return result


def GetMinTupleFrom2DArray(values: list[list[tuple[int, int, int]]], ROWS: int, COLS: int) -> list[int]:
    result: list[int] = [values[0][0][0], values[0][0][1], values[0][0][2]]

    for row in range(ROWS):
        for col in range(COLS):
            result[0] = min(result[0], values[row][col][0])
            result[1] = min(result[1], values[row][col][1])
            result[2] = min(result[2], values[row][col][2])

    return result


def TuplesTo2DGrid(matrix):
    lines = []
    for row in matrix:
        line = " ".join(str(t) for t in row)
        lines.append(line)
    return "\n".join(lines)


def PixelsToImage(pixel_matrix):
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])

    img = Image.new("RGB", (width, height))
    flat_pixels = [pixel for row in pixel_matrix for pixel in row]
    img.putdata(flat_pixels)

    return img
