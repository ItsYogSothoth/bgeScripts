import os
import sys

from univers.Flag import Flag

dataLength = 0
dataOffset = 0
filePath = ""

def splitToStringArray(data):
    strings = []
    string = ""
    prevByte = None
    for x in data:
        match x:
            case 0:
                if string != "":
                    strings.append(string)
                    string = ""
                    prevByte = None
            case 10:
                if prevByte == 13:
                    prevByte = None
                else :
                    string = string + chr(x)
            case 13:
                prevByte = x
            case _:
                string = string + chr(x)
    return strings

def parseFile(universFilePath):
    universFile = open(universFilePath, "rb")

    headerLength = int.from_bytes(universFile.read(4), "little")
    dataHeaderLength = int(headerLength / 12)
    dataArray = []
    for _ in range(dataHeaderLength):
        bufferOffset = universFile.read(4)
        valueCount = universFile.read(2)
        arrayDepth = universFile.read(2)
        variableType = universFile.read(2)
        variableFlags = universFile.read(2)

        dataArray.append({
            "bufferOffsetValue": int.from_bytes(bufferOffset, "little"),
            "valueCount": int.from_bytes(valueCount, "little"),
            "variableType": variableType,
            "variableFlags": int.from_bytes(variableFlags, "little"),
            "arrayDepth": int.from_bytes(arrayDepth, "little")
        })
    namesLength = int.from_bytes(universFile.read(4), "little")
    nameArray = splitToStringArray(universFile.read(namesLength))

    unknownsLength = int.from_bytes(universFile.read(4), "little")
    descsLength = int.from_bytes(universFile.read(4), "little")

    unknowns = []
    for _ in range (int(unknownsLength / 8)):
        unknowns.append(universFile.read(8))

    descArray = splitToStringArray(universFile.read(descsLength))

    global dataLength
    global dataOffset

    dataLength = int.from_bytes(universFile.read(4), "little")
    dataOffset = universFile.tell()

    flagArray = []
    descIndex = 0
    for i in range(len(nameArray)):
        flagArray.append(Flag(nameArray[i]))
        flagArray[i].dataSectionOffset = dataArray[i]["bufferOffsetValue"]
        flagArray[i].valueCount = dataArray[i]["valueCount"]
        flagArray[i].varType = dataArray[i]["variableType"]
        flagArray[i].varFlags = dataArray[i]["variableFlags"]
        flagArray[i].arrayDepth = dataArray[i]["arrayDepth"]

        if dataArray[i]["variableFlags"] & 0x2:
            if descIndex < len(descArray):
                flagArray[i].toggleText = descArray[descIndex]
            descIndex += 1
        if dataArray[i]["variableFlags"] & 0x8:
            if descIndex < len(descArray):
                flagArray[i].desc = descArray[descIndex]
            descIndex += 1

    universFile.close()
    return flagArray

def printFile(flagArray):
    universFile = open(filePath, "rb")
    print("index,name,dataSectionOffset,valueCount,variableType,variableFlags,arrayDepth,description,value")
    for i in range(len(flagArray)):
        print(f"{i},{flagArray[i].name},{flagArray[i].dataSectionOffset:04x},{flagArray[i].valueCount},{flagArray[i].getVariableType()},{flagArray[i].varFlags:04x},{flagArray[i].arrayDepth:04x},\"{flagArray[i].desc}\",{flagArray[i].getData(universFile, dataOffset)}")
    universFile.close()

def printUsage():
    print("Usage: " + os.path.basename(__file__) + " <univers file>")

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        printUsage()
    else:
        global filePath
        filePath = args[0]
        flagArray = parseFile(filePath)
        printFile(flagArray)

if __name__ == "__main__":
    main()
