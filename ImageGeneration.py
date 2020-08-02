import sys
import os
import shutil
from PIL import Image

# we don't want any fancy organization. Just an input dir of images 
# then an output dir with the originals, M and S versions. 

inputDirName = "images"
outputDirName = "output"

largeSizePercentage: float = 1
mediumSizePercentage: float = .50
smallSizePercentage: float = .10

def clearOutputDir(outDir: str):
    if os.path.exists(outDir):
        shutil.rmtree(outDir)
    if os.path.exists(outDir):
        print("removing outdir failed")
        exit(1)

def chdir_to_script():
    dirname: str = os.path.dirname(os.path.abspath(__file__))
    cwd: str = os.getcwd()
    if cwd != dirname:
        print(f"dirname: {dirname} and cwd: {cwd}")
        os.chdir(os.path.dirname(__file__))
    print("script dir")


def checkImagesForErrors(resPaths):
    if len(resPaths) == 0:
        print("no images found")
        exit(1)
    for thisPath in resPaths:
        found: bool = False 
        validImageSet: set = set()
        validImageSet.add(".png")
        validImageSet.add(".jpg")
        for extension in validImageSet:
            if extension in str.lower(thisPath):
                found = True
        if not found:
            print("image is lacking a valid extension")

def walk_input_dir(inputDir: str) -> list:
    if not os.path.exists(inputDir):
        print(f"./{inputDir} does not exist")
        exit(1)
    listOfFiles = os.listdir(inputDir)
    resPaths: list = list()
    for filename in listOfFiles:
        fullpath = os.path.realpath(os.path.join(inputDir, filename))
        if os.path.isdir(fullpath):
            print("no subdirs in input folder!")
            exit(1)
        resPaths.append(fullpath)
    checkImagesForErrors(resPaths)
    return resPaths 

def create_output_dir(outDir: str) -> str:
    os.mkdir(outDir)
    return os.path.realpath(outDir)


def create_image_of_size(image: object, sizePercentage: float, outdir: str, file_extension: str, filename: str):
        width: int = image.width
        height: int = image.height

        resize = width*sizePercentage, height*sizePercentage

        sizeTag: str = ""
        if sizePercentage == largeSizePercentage:
            if sizePercentage == 1:
                sizeTag = ""
            else:
                sizeTag = "-l"
        if sizePercentage ==  mediumSizePercentage:
            sizeTag = "-m"
        if sizePercentage == smallSizePercentage:
            sizeTag = "-s"

        image.thumbnail(resize)
        outPath = os.path.realpath(outdir)
        outFilePath = os.path.join(outPath, f"{os.path.basename(filename)}{sizeTag}{file_extension}")
        image.save(outFilePath)

def process_images(outdir: str, inputFiles: list):
    """we need to  resize twice and copy original"""
    originalTag: str = 'l'
    medTag: str = 'm'
    smTag: str = 's'

    for filepath in inputFiles:
        filename, file_extension = os.path.splitext(filepath)
        if not filename or not filepath:
            print("file is maleformed")
        
        image = Image.open(filepath)
        create_image_of_size(image, largeSizePercentage, outdir, file_extension, filename)
        image = Image.open(filepath)
        create_image_of_size(image, mediumSizePercentage, outdir, file_extension, filename)
        image = Image.open(filepath)
        create_image_of_size(image, smallSizePercentage, outdir, file_extension, filename)
        

def main():
    chdir_to_script()
    inputDir: str = f"./{inputDirName}"
    outDir: str = f"./{outputDirName}"
    clearOutputDir(outDir)
    inputFiles: list = walk_input_dir(inputDir)
    create_output_dir(outDir)
    process_images(outDir, inputFiles)


main()
