from VectorQuantization import VectorQuantization
import os


def compression_ratio(originalFile, compressedFiles):
    originalSize = os.path.getsize(originalFile)
    compressedSize = 0
    for file in compressedFiles:
        compressedSize += os.path.getsize(file)
    
    return originalSize / compressedSize


def encode():
    while True:
        imagePath = input("Enter image path: ")
        if os.path.exists(imagePath):
            break
        print("File not found. Please try again.")

    while True:
        try:
            codeBookSize = int(input("Enter code book size: "))
            if codeBookSize >= 2:
                break
            print("Code book size must be at least 2.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    vectorHeight = int(input("Enter vector height: "))
    vectorWidth = int(input("Enter vector width: "))
    VQ: VectorQuantization = VectorQuantization(imagePath, codeBookSize, vectorHeight, vectorWidth)
    VQ.Encode('EncodingStream.txt', 'CodeBook.txt')
    print(f"Compression Ratio: {compression_ratio(imagePath, ['EncodingStream.txt', 'CodeBook.txt'])}")


def decode():
    while True:
        codeBookFileName = input("Enter code book file name: ")
        if os.path.exists(codeBookFileName):
            break
        print("File not found. Please try again.")

    while True:
        bitsStreamFileName = input("Enter bits stream file name: ")
        if os.path.exists(bitsStreamFileName):
            break
        print("File not found. Please try again.")

    img = VectorQuantization.Decode(codeBookFileName, bitsStreamFileName)
    img.save('DecodedImage.jpg')


def main():
    while True:
        print("Vector Quantization Compression")
        print("1. Encode")
        print("2. Decode")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if (choice == "1"):
            encode()
        elif (choice == "2"):
            decode()
        elif (choice == "3"):
            break


if __name__ == "__main__":
    main()
