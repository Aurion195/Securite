import argparse
import png

def decryptMessage(new_pixels) :
    """
    Permit to decrypt the hidden message in picture

    Args:
        new_pixels ([array]): the pixels to decrypt
    """
    text = ""
    compteur = 0
    message = []
    messageDecrypter = ""
    
    #We find every LSB in pixel and add to message
    #When we have 8B we can add the bit in the array
    for byte in new_pixels :
        text += byte[-1]
        compteur += 1
        
        if(compteur == 8) :
            message.append(text)
            compteur = 0
            text = ""

    for char in message :
        tmp = chr(int(char, 2))
        
        #If the 8bit is not a printable we can break all the loop
        if(tmp.isprintable() is False) :
            break
        
        messageDecrypter += tmp

    return(messageDecrypter)

def readFunction() :
    """
    This function can read the image and find the hidden message in LSB
    
    Returns:
            [char]: the message decrypt in the picture
    """
    file = png.Reader(filename = "output.png")
    width, height, pixels, info = file.asRGBA8()
    new_pixels = [format(px, "08b") for row in pixels for px in row]
    
    return decryptMessage(new_pixels)

def convertTextToBinary(textToWrite) :
    """
    Permit to convert text to binary
    
    Args:
        textToWrite ([char]): the text to convert

    Returns:
        [char]: the binary text who has convert
    """
    
    res = ""
    for char in textToWrite :
        res += format(ord(char), "08b")

    return res

def encryptPicture(new_pixels, texteBin) :
    """
    Encrypt the picture with the message

    Args:
        new_pixels ([array]): array of the pixels
        texteBin ([char]): the message to replace in LSB
    """
    
    for i in range(0, len(texteBin)) :
        listPixel = list(new_pixels[i])
        listPixel[-1] = texteBin[i]
        pixel = "".join(listPixel)
        tmp = int(pixel, 2)
        new_pixels[i] = format(tmp, '08b')

    return new_pixels

def writeFunction(textToWrite) :
    """
    This function permit to write a hidden message in picture
    
    Args:
            textToWrite ([char]): message to write in hiden
    """
    
    texteBin = convertTextToBinary(textToWrite)
    #Open file with png
    file = png.Reader(filename = "Homer.png")
    width, height, pixels, info = file.asRGBA8()
    del info['palette']
    
    new_pixels = [format(px, "08b") for row in pixels for px in row]
    #In that case where the message to hidden is to long for the pixel image
    if(len(texteBin) > len(new_pixels)) :
        return("Error : le message est trop long pour l'image")
    
    new_pixels = encryptPicture(new_pixels, texteBin)
    
    #Create picture with the hidden message
    writer = png.Writer(width, height, **info)
    output_file = open("output.png", "wb")
    output = writer.array_scanlines([int(px, 2) for px in new_pixels])
    writer.write(output_file, output)
    
    return("The message has been encrypted")

def route(args) :
    """
    This function give the road to program and permit to execute him

    Args:
        args ([parser]): the argparse
    """
    
    text = ""
    if args.w :
        if args.t :
            print(writeFunction(args.t))
        elif args.f :
            filename = open(args.f)
            text = filename.read()
            print(writeFunction(text))
        else :
            text = input("text to write = \n")
            print(writeFunction(text))
    else :
        messageDecrypt = readFunction()
        print("Le message décrypter est : ", messageDecrypt)
def parser() :
    """
    This function permit to parse the line command and give the road to following
    as the program
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', help = 'write a message in picture', action = "store_true")
    parser.add_argument('-f', help = 'path of filename to find some text')
    parser.add_argument('-t', help = '"some text"')
    args = parser.parse_args()
    route(args)

parser()
