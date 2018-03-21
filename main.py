import sys
from PIL import Image

imagePath = sys.argv[1]
parseAmt = int(sys.argv[2])

class Slicer:
    def __init__(self, image):
        self.image = image
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.step = self.width / 10
        print self.step

    def getSlices(self):
        sliceList = []
        for s in range(0, self.width, self.step):
            box = (s, 0, s + self.step, self.height)
            region = self.image.crop(box)
            sliceList.append(region)
        return sliceList

    def slideSlices(self, sliceList):
        newIm = Image.new('RGB', (self.width / 2, self.height * 2))
        xOffset = 0
        yOffset = 0
        for i in range(0, len(sliceList)):
            cut = sliceList[i]
            newIm.paste(cut, (xOffset, yOffset))
            if i % 2 == 0:
                yOffset = self.height
            else:
                xOffset += self.step
                yOffset = 0
        return newIm

    def chop(self):
        return self.slideSlices(self.getSlices())

    def manyChop(self, its):
        chopped = self.__class__(self.image)
        for i in range(0, its):
            chopped = chopped.__class__(chopped.chop())
        return chopped.image

myImage = Image.open(imagePath)
sliced = Slicer(myImage)
if parseAmt < 10:
    sliced.manyChop(parseAmt).show()
else:
    print "ParseAmt must be less then 10"
