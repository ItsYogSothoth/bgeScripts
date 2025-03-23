import lzo
import os
import sys

def processBank(bankFile):
    bankFilename = os.path.basename(bankFile.name)[:-4]
    decompSize = int.from_bytes(bankFile.read(4), "little")
    compSize = int.from_bytes(bankFile.read(4), "little")
    print(bankFilename + "\nCompressed size: " + str(compSize) + "\nDecompressed size: " + str(decompSize))
    compressedBytes = bankFile.read(compSize)
    decompressBytes = lzo.decompress(compressedBytes, False, decompSize)
    outFile = open(bankFilename + "-decomp.bin" , "wb")
    outFile.write(decompressBytes)
    outFile.close()

def printUsage():
    print("Usage: " + os.path.basename(__file__) + " <soundbank file>")

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        printUsage()
    else:
        compressedBankFile = open(args[0], "rb")
        processBank(compressedBankFile)
        compressedBankFile.close()

if __name__ == "__main__":
    main()