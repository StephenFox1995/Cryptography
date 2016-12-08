from PIL import Image
import bitstring
# generator for each bit in a message
def messageBitsGenerator(messageBits):
    i = 0
    while i < len(messageBits):
      yield messageBits[i]
      i += 1 

# Hide a message in the least significant bits of each pixel of an image
def hide(image, message):
  (width, height) = image.size # Get width and height of image.

  binMessage = ''.join(format(ord(x), 'b') for x in message)
  bitsGenerator = messageBitsGenerator(binMessage) # Generator for each bit in message
  for x in range(0, width):
    for y in range(0, height):
      pixel = image.getpixel((x, y))

      if (image.mode is not 'P'): # Only support L mode as it is enough for grayscale
        print("This function does not support %s pixel models" % image.mode)
        return
      
      binPixel = bin(pixel)
      try:
        messageBit = bitsGenerator.next() # Get the current bit for the message
        binPixel = binPixel[:-1] + messageBit # Set the message bit as the LSB for the current pixel
        pixel = bitstring.Bits(binPixel).uint
        image.putpixel((x, y), pixel) # Put pixel back into image at same coordinates.
      except StopIteration: 
        return # No more message bits to hide in image

image = Image.open("baboon.bmp")
message = "Hello World!" * 100
hide(image, message)
image.save("hiddenMessage.bmp")