from VectorQuantization import VectorQuantization

VQ: VectorQuantization = VectorQuantization('RandomImage.jpg', 4, 2, 2)

VQ.Encode('EncodingStream.txt', 'CodeBook.txt')



img = VectorQuantization.Decode('CodeBook.txt','EncodingStream.txt')
img.save('DecodedImage.jpg')


