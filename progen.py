# Name:         Ethan Wagner
# Assignment:   Generate BMP files that are unique
# Term:         Start: 2 November 2021
#               End: v1.0 5 November 2021

# import queue
# from typing import List, Tuple
import os
from struct import pack
import random
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import Figlet

class Bitmap():
  def __init__(self, width, height):
    self._bfType = 19778 # Bitmap signature
    self._bfReserved1 = 0
    self._bfReserved2 = 0
    self._bfOffBits = 54
    self._bcPlanes = 1
    self._bcSize = 40
    self._bcBitCount = 24
    self._bcWidth = width
    self._bcHeight = height
    self._bfSize = self._bfOffBits+self._bcWidth*self._bcBitCount*self._bcHeight
    self._bcCompression = 0
    self.bcFinalSize = 12288
    self._XpPM = 0
    self._YpPM = 0
    self._bcTotalColors = 0
    self._bcImpColors = 0
    self._redC = 16711680
    self._greenC = 65280
    self._blueC = 255
    self._alphaC = 4278190080
    self._Win = 1468624416
    self._CSE = 0
    self._redG = 0
    self._greenG = 0
    self._blueG = 0
    self.clear()


  def clear(self):
    self._graphics = [(0,0,0)]*self._bcWidth*self._bcHeight


  def setPixel(self, x, y, color):
    if isinstance(color, tuple):
      if x<0 or y<0 or x>self._bcWidth-1 or y>self._bcHeight-1:
        raise ValueError('Coords out of range')
      if len(color) != 3:
        raise ValueError('Color must be a tuple of 3 elems')
      self._graphics[y*self._bcWidth+x] = (color[2], color[1], color[0])
    else:
      raise ValueError('Color must be a tuple of 3 elems')


  def write(self, file):
    with open(file, 'wb') as f:
      f.write(pack('<HLHHL', 
                   self._bfType, 
                   self._bfSize, 
                   self._bfReserved1, 
                   self._bfReserved2, 
                   self._bfOffBits)) # Writing BITMAPFILEHEADER
      f.write(pack('<LLLHHLLLLLL', 
                   self._bcSize, 
                   self._bcWidth, 
                   self._bcHeight, 
                   self._bcPlanes, 
                   self._bcBitCount,
                   self._bcCompression,
                   self.bcFinalSize,
                   self._XpPM,
                   self._YpPM,
                   self._bcTotalColors,
                   self._bcImpColors
                   )) # Writing DIBHEADER

      for px in self._graphics:
        f.write(pack('<BBB', int.from_bytes(px[0], 'little'), int.from_bytes(px[1], 'little'), int.from_bytes(px[2], 'little')))
    #   for i in range((4 - ((self._bcWidth*4) % 4)) % 4):
    #     f.write(pack('B', 0))

def attr_set(b: Bitmap, dir: str, attr: str, side: int, ign: list) -> None:
    '''
       Method takes in descriptive information from the main driving code in 
       order to create a layer over our generated image. It will then write
       the pixel array to the bmp file.
    '''
    attr_path = os.path.join(dir, attr)
    onlyfiles = [f for f in os.listdir(attr_path) if os.path.isfile(os.path.join(attr_path, f))]
    
    #selection process
    file_slctd_path = os.path.join(attr_path, onlyfiles[0])
    file_slctd = open(file_slctd_path, "rb")
    file_slctd.seek(b._bfOffBits)

    #layer those pixels
    for j in range(0, side):
        for i in range(0, side):
            b_val = file_slctd.read(1)
            g_val = file_slctd.read(1)
            r_val = file_slctd.read(1)
            # print(b_val)
            # print(g_val) 
            # print(r_val)
            # print("\n")
            if [b_val, g_val, r_val] != [(ign[0]).to_bytes(1, byteorder='big'), (ign[1]).to_bytes(1, byteorder='big') ,(ign[2]).to_bytes(1, byteorder='big')]:
                b.setPixel(i, j, (r_val, g_val, b_val))

def rand_attr_set(b: Bitmap, dir: str, attr: str, side: int, ign: list, table: list) -> None:
    '''
       Method takes in descriptive information from the main driving code in 
       order to create a layer over our generated image. It will then write
       the pixel array to the bmp file. THIS ONE USES A RANDOM NUMBER GENERATOR
       FOR UNIQUE LAYERS. 
    '''
    attr_path = os.path.join(dir, attr)
    onlyfiles = [f for f in os.listdir(attr_path) if os.path.isfile(os.path.join(attr_path, f))]
    
    #selection process
    file_slctd_path = os.path.join(attr_path, onlyfiles[0])
    file_slctd = open(file_slctd_path, "rb")
    file_slctd.seek(b._bfOffBits)

    #generate a random color
    color_tbu = table[random.randint(0, len(table)-1)]
    
    #layer those pixels
    for j in range(0, side):
        for i in range(0, side):
            b_val = file_slctd.read(1)
            g_val = file_slctd.read(1)
            r_val = file_slctd.read(1)
            # print(b_val)
            # print(g_val) 
            # print(r_val)
            # print("\n")
            if [b_val, g_val, r_val] != [(ign[0]).to_bytes(1, byteorder='big'), (ign[1]).to_bytes(1, byteorder='big') , (ign[2]).to_bytes(1, byteorder='big')]:
                if [b_val, g_val, r_val] != [(0).to_bytes(1, byteorder='big'), (0).to_bytes(1, byteorder='big') , (0).to_bytes(1, byteorder='big')]: #if not black
                    b.setPixel(i, j, (color_tbu[0], color_tbu[1], color_tbu[2]))
                else:
                    b.setPixel(i, j, (r_val, g_val, b_val))


def mk_pixl_array(pixl_val: str) -> list:
    '''
       Method takes in the line of a .txt file which should be made by the user in the imgs directory.
       The method will take in type str and make a list of 3 formatted bytes in order blue, green, red.
    '''
    val_list = pixl_val.split(" ")
    for i in range(len(val_list)):
        val_list[i] = (int(val_list[i].rstrip('\n'))).to_bytes(1, "big")

    return val_list


def main() -> None:
    '''
       Driving code that will need the number of images to be generated, and a transparency 
       value from the user. Directories will have to be set up specifically as the code needs
       to access specific directory names in order to generate the color tables as well as a 
       specific place to put the generated images.
    '''
    #Print title
    f = Figlet(font='isometric2')
    cprint("\n\n\n\n-----------------------------------------------", "yellow")
    cprint(f.renderText("PRO"), "yellow")
    cprint(f.renderText("GEN"), "yellow")
    cprint("-----------------------------------------------\n", "yellow")

    #Ask how many images to generate
    side = int(input("\nWhat is the length of your image? (Has to be a multiple of 4): "))
    taskCount = int(input("How many unique images do you want to generate?: "))
    print("\nEnter the transparent value in decimal (BGR): \n")
    forb_b = int(input("B: "))
    forb_g = int(input("G: "))
    forb_r = int(input("R: "))
    forb_bga = [forb_b, forb_g, forb_r]

    
    #Receive batch number
    cwd = os.getcwd()
    imgDir = os.path.join(cwd, "imgs")
    try:
        batchPath = os.path.join(imgDir, "BatchNum.txt")
        batchFile = open(batchPath, "r+")
        batchNum = int(batchFile.read())
        batchFile.seek(0)
        newNum = batchNum + 1
        batchFile.write(str(newNum))
        batchFile.truncate()
        batchFile.close()
    except FileNotFoundError:
        print("*ERROR* : File Structure Incorrectly Made By User\n")
        exit(0)

    dirName = "batch"
    dirName = dirName + str(batchNum)
    dirpath = os.path.join(imgDir, dirName)
    os.makedirs(dirpath)

    #generate color table
    print("Generating Color Table..... ")
    colorTable_path = os.path.join(imgDir, "colorIndex_std.txt")
    colorTable_file = open(colorTable_path, "r")
    colorTable = []
    for color in colorTable_file:
        colorTable.append(mk_pixl_array(color))
    colorTable_file.close()
    print("complete!\n")

    #generate skin table
    print("Generating Skin Table..... ")
    skinTable_path = os.path.join(imgDir, "skinIndex_std.txt")
    skinTable_file = open(skinTable_path, "r")
    skinTable = []
    for tone in skinTable_file:
        skinTable.append(mk_pixl_array(tone))
    skinTable_file.close()
    print("complete!\n")

    # print(str(colorTable) + "\n\n")
    # print(str(skinTable))
    # exit(0)

    for edition in range(taskCount):
        #Create file
        bmpPath = os.path.join(imgDir, "bmps")
        fileName = "edition_"
        fileName = fileName + str(edition) + ".bmp"
        filepath = os.path.join(dirpath, fileName)
        
        genEdition = Bitmap(side, side)

    #write pxl data:
    # 1) Choose background
        rand_attr_set(genEdition, bmpPath, "background", side, forb_bga, colorTable)

    # 2) Choose figure
        attr_set(genEdition, bmpPath, "figures", side, forb_bga)

    # 3) Choose skin
        rand_attr_set(genEdition, bmpPath, "skin", side, forb_bga, skinTable)

    # 4) Choose brain
        attr_set(genEdition, bmpPath, "brain", side, forb_bga)

    # 5) Choose mouth
        attr_set(genEdition, bmpPath, "mouth", side, forb_bga)

    # 6) Choose eyes
        rand_attr_set(genEdition, bmpPath, "eyes", side, forb_bga, colorTable)

    # 7) Choose foot apparel
        rand_attr_set(genEdition, bmpPath, "feetApparel", side, forb_bga, colorTable)

    # 8) Choose bottom apparel
        rand_attr_set(genEdition, bmpPath, "bottomApparel", side, forb_bga, colorTable)

    # 9) Choose accessory
        rand_attr_set(genEdition, bmpPath, "accessory", side, forb_bga, colorTable)

    # 10) Choose top apparel
        rand_attr_set(genEdition, bmpPath, "topApparel", side, forb_bga, colorTable)

    # 11) Choose brain damnage logo
        rand_attr_set(genEdition, bmpPath, "bd", side, forb_bga, colorTable)

    # 12) Choose brain for logo
        attr_set(genEdition, bmpPath, "brainLogo", side, forb_bga)
        
    # Write to the file
        genEdition.write(filepath) 

    print("\n\nFinished generating.... " + str(taskCount) + " images!\n")

if __name__ == "__main__":
    main()
