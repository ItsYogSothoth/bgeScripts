class WaveFile:
    byteHeader: bytes
    byteContent: bytes
    filename: str
    hasData: bool

    def __init__(self, filename, hasData):
        self.filename = filename
        self.hasData = hasData

    def getDataSize(self):
        return int.from_bytes(self.byteHeader[-4:], "little")