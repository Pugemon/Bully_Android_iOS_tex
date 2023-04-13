from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Bully: Anniversary Edition [Android|iOS]", ".tex")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    #noesis.logPopup()
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data)
    if bs.readBytes(4) != b'\x07\x00\x00\x00': return 0
    return 1
    
def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    bs.seek(0x4, NOESEEK_ABS)
    numTex = bs.readUInt() - 1
    bs.readInt()
    infoOffset = bs.readUInt()
    for i in range(numTex):
        imgFmt = bs.readUInt()
        offset = bs.readUInt()
    infoSize = bs.readUInt()
    info = noeStrFromBytes(bs.readBytes(infoSize))
    for i in range(numTex):
        imgFmt = bs.readUInt()
        imgWidth = bs.readUInt()
        imgHeight = bs.readUInt()
        bs.readInt()
        if "compressondisk=true" in info:
            compSize = bs.readUInt() - 4
            decompSize = bs.readUInt() 
            data = bs.readBytes(compSize)
            data = rapi.decompInflate(data, decompSize)
        else:
            datasize = bs.readUInt()
            data = bs.readBytes(datasize)      
        #RGBA8888
        if imgFmt == 0x0:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8 b8 a8")
            texFmt = noesis.NOESISTEX_RGBA32
        #RGB888
        elif imgFmt == 0x1:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b8 g8 r8")
            texFmt = noesis.NOESISTEX_RGBA32
        #RGB565
        elif imgFmt == 0x3:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "b5 g6 r5")
            texFmt = noesis.NOESISTEX_RGBA32
        #RGBA4444
        elif imgFmt == 0x4:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a4 b4 g4 r4")
            texFmt = noesis.NOESISTEX_RGBA32
        #DXT1
        elif imgFmt == 0x5:
            texFmt = noesis.NOESISTEX_DXT1
        #DXT5
        elif imgFmt == 0x7:
            texFmt = noesis.NOESISTEX_DXT5
        #A8
        elif imgFmt == 0x8:
            data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8")
            texFmt = noesis.NOESISTEX_RGBA32
        #PVRTC2 4bpp ???
        elif imgFmt == 0x9:
            data = rapi.imageDecodePVRTC(data, imgWidth, imgHeight, 4, noesis.PVRTC_DECODE_PVRTC2_ROTATE_BLOCK_PAL)
            texFmt = noesis.NOESISTEX_RGBA32
        texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, data, texFmt))
    return 1