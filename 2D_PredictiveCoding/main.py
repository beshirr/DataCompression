from TwoDPredictiveCoding import TwoDPredictiveCoding
import os


def encode():
    while True:
        imagePath = input("Enter image path: ")
        if os.path.exists(imagePath):
            break
        print("File not found. Please try again.")

    while True:
        try:
            numberOfBits = int(input("Enter number of bits (default is 2): "))
            if numberOfBits > 0:
                break
            print("Number of bits must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    outputFile = "EncodedStream.txt"
    predictiveCoding = TwoDPredictiveCoding(numberOfBits, imagePath)
    predictiveCoding.Encode(outputFile)


def decode():
    while True:
        filePath = input("Enter decompressed metadata file path: ")
        if os.path.exists(filePath):
            break
        print("File not found. Please try again.")
    TwoDPredictiveCoding.Decode(filePath)


def main():
    while True:
        print("2D Predictive Coding Compression")
        print("1. Encode")
        print("2. Decode")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            encode()
        elif choice == "2":
            decode()
        if choice == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()