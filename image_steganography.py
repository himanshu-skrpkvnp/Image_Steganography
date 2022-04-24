"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw  # pillow module used
import textwrap

# to decode


def decode_image(file_location="images/encoded_image.png"):

    encoded_image = Image.open(file_location)   # opens image file
    # storing the list of red pixels
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]              # width of encoded img
    y_size = encoded_image.size[1]              # height of encoded img

    # creates a new RGB img of same dimension as encoded img
    decoded_image = Image.new("RGB", encoded_image.size)
    # stores pixel map, curr(0,0,0)
    pixels = decoded_image.load()

    # looping through every pixel (i,j) < (width,height)
    for i in range(x_size):
        for j in range(y_size):
            # checks if binary of red_channel pixel of encoded img ends with '0'
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)      # storing white
            else:
                pixels[i, j] = (0, 0, 0)            # stores black
    decoded_image.save("images/decoded_image.png")  # saves the decoded image

# to write your msg for encryption


def write_text(text_to_write, image_size):

    image_text = Image.new("RGB", image_size)
    # sets the default font to pass in text parameter below
    font = ImageFont.load_default().font
    # creating image_text draw object to write on it
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)  # text written
        offset += 10
    return image_text

# encode your secret msg


def encode_image(text_to_encode, template_image="images/isdf.jpg"):

    template_image = Image.open(template_image)  # opens image
    red_template = template_image.split()[0]     # takes list of red px
    green_template = template_image.split()[1]   # list of green px
    blue_template = template_image.split()[2]    # list of blue px

    x_size = template_image.size[0]              # width of img
    y_size = template_image.size[1]              # height of img

    # text draw
    image_text = write_text(text_to_encode, template_image.size)
    # converts image_text to grayscale (to define pixels on just one parameter because is rgb format we have 3 parameters )
    bw_encode = image_text.convert('1')

    # encode text into image
    encoded_image = Image.new("RGB", (x_size, y_size))
    pixels = encoded_image.load()  # stores pixel map, curr(0,0,0)

    for i in range(x_size):
        for j in range(y_size):
            # gets pixel from red pixel list as (x,y)
            red_template_pix = bin(red_template.getpixel((i, j)))
            # bin converts pix to binary string
            tencode_pix = bin(bw_encode.getpixel((i, j)))
            # changing red pixel by +1 (not visible to naked eyes)
            if tencode_pix[-1] == '1':
                red_template_pix = red_template_pix[:-1] + '1'
            else:
                red_template_pix = red_template_pix[:-1] + '0'
            # putting (changed red pixel, original green pixel, original blue pixel) in encoded img
            pixels[i, j] = (int(red_template_pix, 2), green_template.getpixel(
                (i, j)), blue_template.getpixel((i, j)))

    encoded_image.save("images/encoded_image.png")


# main
if __name__ == '__main__':
    encode_image("h3ll0_w0rld")  # encoding img function call
    decode_image()               # decode img function call
