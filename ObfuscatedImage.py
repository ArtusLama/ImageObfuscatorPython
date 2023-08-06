import math
import time
from math import sqrt

from PIL import Image
import random
import numpy as np


class ObfuscatedImage:

    def __init__(self, pixels: np.ndarray):
        self.pixels = pixels
        self.out = []
        self.pattern = []

    @staticmethod
    def fromImagePath(path):
        image = Image.open(path)
        pixels = np.asarray(image)
        return ObfuscatedImage(pixels)

    @staticmethod
    def keyFromPattern(pattern):

        return pattern

    @staticmethod
    def patternFromKey(key):
        return key

    def getListFromImage(self, img):
        image = img.copy()
        out = []
        for row in image:
            out.append(row[...].tolist())
        return out

    def getImageArrayFromList(self, imgList, out):
        i = 0
        for row in out:
            row[...] = imgList[i]
            i += 1

        return out



    def obfuscate(self):
        img: np.ndarray = self.pixels.copy()

        image, pattern = self.shuffle(img)

        self.out = image.copy()
        self.pattern = pattern
        Image.fromarray(image).save("out.jpg")

    def rotateList(self, inList):
        return list(zip(*inList[::-1]))

    def rotateListBack(self, inList):
        return list(zip(*inList))[::-1]

    def shuffle(self, npArray):
        pixelList = self.getListFromImage(npArray)

        out = []
        pattern = [[], []]

        def randomizeList(savePattern, inList):
            tmpList = inList.copy()
            for r in tmpList:
                rowIndex = random.randint(1, len(tmpList) - 1)
                row = tmpList[0]
                tmpList.insert(rowIndex, row)
                tmpList.pop(0)

                pattern[savePattern].append(rowIndex)
            return tmpList

        out = randomizeList(0, pixelList.copy())
        out = self.rotateList(out)
        out = randomizeList(1, out)
        out = self.rotateListBack(out)



        image = self.getImageArrayFromList(out, npArray)
        return image, pattern


    def decode(self, pattern):
        pixelList = self.getListFromImage(self.out)

        def decodeRows(patternType, inList):
            tmpList = inList
            pattern[patternType].reverse()
            for rowIndex in pattern[patternType]:
                row = tmpList[rowIndex - 1]
                tmpList.insert(0, row)
                tmpList.pop(rowIndex)

            return tmpList

        out = decodeRows(0, pixelList.copy())
        out = self.rotateList(out)
        out = decodeRows(1, out)
        out = self.rotateListBack(out)

        out = self.getImageArrayFromList(out, self.out)
        Image.fromarray(out).save("out2.jpg")
