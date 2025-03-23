import os

class Flag:
    name: str
    desc: str
    toggleText: str

    dataSectionOffset: int
    valueCount: int
    varType: bytes
    varFlags: int
    arrayDepth: int

    def __init__(self, name):
        self.name = name
        self.desc = ""
        self.toggleText = ""

    def getVariableType(self):
        match self.varType[0:1]:
            case b'\x21':
                return 'int'
            case b'\x22':
                return 'float'
            case b'\x25':
                return 'vec3d'
            case b'\x27':
                return 'key?3d?'
            case b'\x28':
                return 'obj'
            case b'\x29':
                return 'msg'
            case b'\x2b':
                return 'net?'
            case b'\x2c':
                return 'txt'
            case b'\x2e':
                return 'colour'

    def getArrayDepth(self):
        return int(self.arrayDepth / 0x4000)

    def getData(self, universFile, baseOffset):
        self.universFile = universFile
        self.dataSize = self.getDataSize()
        self.universFile.seek((baseOffset + self.dataSectionOffset), os.SEEK_SET)
        if self.valueCount == 1:
            dataBytes = self.getBytes(self.dataSize)
            return self.getFormattedData(dataBytes)
        else:
            return self.getArrayString(self.getArrayDepth())
            # arrayLength = int.from_bytes(self.getBytes(4), "little")
            # if arrayLength == self.valueCount:
            #     formatStr = "\"["
            #     for _ in range(arrayLength):
            #         dataBytes = self.getBytes(self.dataSize)
            #         formatStr = f"{formatStr} {self.getFormattedData(dataBytes)},"
            #     return f"{formatStr[:-1]} ]\""

    def getArrayString(self, depth, size = -1):
        if size == -1:
            arrayLength = int.from_bytes(self.getBytes(4), "little")
            if depth > 1:
                subArraySize = int.from_bytes(self.getBytes(4), "little")
        else:
            arrayLength = size
        formatStr = "["
        for _ in range(arrayLength):
            if depth > 1:
                formatStr = f"{formatStr} {self.getArrayString(depth - 1, subArraySize)},"
            else:
                dataBytes = self.getBytes(self.dataSize)
                formatStr = f"{formatStr} {self.getFormattedData(dataBytes)},"
        formatStr = f"{formatStr[:-1]} ]"
        if size == -1: return f"\"{formatStr}\""
        else: return formatStr

    def getBytes(self, size):
        return self.universFile.read(size)

    def getDataSize(self):
        match self.getVariableType():
            case "int" | "float" | "obj":
                return 4
            case "vec3d":
                return 12

    def getFormattedData(self, dataBytes):
        match self.getVariableType():
            case "int":
                return int.from_bytes(dataBytes, "little")
            case "float":
                return float.fromhex(dataBytes.hex())
            case "vec3d":
                return f"({float.fromhex(dataBytes[0:4].hex())}; {float.fromhex(dataBytes[4:8].hex())}; {float.fromhex(dataBytes[8:12].hex())})"
            case "obj":
                return dataBytes.hex()
