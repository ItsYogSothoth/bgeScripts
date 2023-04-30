import os
import sys
from waveFile.WaveFile import WaveFile

def processBank(bankFile):
    bankFilename = os.path.basename(bankFile.name)[:-4]
    fileCount = int.from_bytes(bankFile.read(4), "little")
    print("Number of files: " + str(fileCount))
    files = []
    for _ in range(fileCount):
        resKey = bankFile.read(4).hex()
        inContainer = int.from_bytes(bankFile.read(4), "little")
        files.append(WaveFile(resKey, inContainer == 0))

    for x in range(len(files)):
        files[x].byteHeader = bankFile.read(46)

    for x in range(len(files)):
        if files[x].hasData:
            files[x].byteContent = bankFile.read(files[x].getDataSize())

    outputDir = "output/" + bankFilename
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    for x in range(len(files)):
        if files[x].hasData:
            print("Writing file " + files[x].filename)
            outFile = open(outputDir + "/" + files[x].filename + ".wav", "wb")
            outFile.write(files[x].byteHeader + files[x].byteContent)
            outFile.close()
        else:
            print("File " + files[x].filename + " has no content data - skipping.")

def printUsage():
    print("Usage: " + os.path.basename(__file__) + " <soundbank file>")

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        printUsage()
    else:
        bankFile = open(args[0], "rb")
        processBank(bankFile)
        bankFile.close()

main()