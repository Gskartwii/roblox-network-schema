def readStdString(addr):
    strLen = Dword(addr + 0x10)
    if strLen == 0xFFFFFFFF:
        raise Exception("Failed to read len at address" + str(addr))
    if strLen < 0x10:
        return GetString(addr, strLen, 0)
    return GetString(Dword(addr), strLen, 0)

with open("instances.txt", "w") as thisFile:
    insAddr = LocByName("SchemaStart")
    insEnd = LocByName("SchemaEnd")
    propAddr = LocByName("PropertySchemaStart")
    propEnd = LocByName("PropertySchemaEnd")
    thisFile.write(str((insEnd-insAddr) / 0x3C) + "\n")
    for addr in range(insAddr, insEnd, 0x3C):
        classID = Word(addr)
        firstPropertyIndex = Word(addr+2)
        lastPropertyIndex = Word(addr+4)
        infoStart = Dword(addr+8)
        if infoStart == 0:
            className = "ERR_UNKNOWN"
        else:
            className = readStdString(Dword(infoStart+4))
        thisFile.write(str(className) + "\n")
        thisFile.write("\t" + str(lastPropertyIndex - firstPropertyIndex) + "\n")
        for thisPropAddr in range(propAddr+firstPropertyIndex * 0x10, propAddr+lastPropertyIndex * 0x10, 0x10):
            propertyID = Word(thisPropAddr)
            propertyType = Word(thisPropAddr + 4)
            propInfoStart = Dword(thisPropAddr+0xC)
            if propInfoStart == 0:
                propertyName = "ERR_UNKNOWN"
                propertyTypeName = "ERR_UNKNOWN"
            else:
                propertyName = readStdString(Dword(propInfoStart+4))
                typeInfoStart = Dword(propInfoStart + 0x28)
                propertyTypeName = readStdString(Dword(typeInfoStart+4))
            thisFile.write("\t" + str(propertyType) + " '" + propertyName + "' " + propertyTypeName + "\n")
    print("Done")

with open("properties.txt", "w") as thisFile:
    insAddr = LocByName("SchemaStart")
    insEnd = LocByName("SchemaEnd")
    propAddr = LocByName("PropertySchemaStart")
    propEnd = LocByName("PropertySchemaEnd")
    thisFile.write(str((propEnd-propAddr) / 0x10) + "\n")
    totalDumped = 0
    for addr in range(insAddr, insEnd, 0x3C):
        classID = Word(addr)
        firstPropertyIndex = Word(addr+2)
        lastPropertyIndex = Word(addr+4)
        infoStart = Dword(addr+8)
        if infoStart == 0:
            className = "ERR_UNKNOWN"
        else:
            className = readStdString(Dword(infoStart+4))
        for thisPropAddr in range(propAddr+firstPropertyIndex * 0x10, propAddr+lastPropertyIndex * 0x10, 0x10):
            propertyID = Word(thisPropAddr)
            totalDumped += 1
            propertyType = Word(thisPropAddr + 4)
            propInfoStart = Dword(thisPropAddr+0xC)
            if propInfoStart == 0:
                propertyName = "ERR_UNKNOWN"
                propertyTypeName = "ERR_UNKNOWN"
            else:
                propertyName = readStdString(Dword(propInfoStart+4))
                typeInfoStart = Dword(propInfoStart + 0x28)
                propertyTypeName = readStdString(Dword(typeInfoStart+4))
            thisFile.write(str(propertyType) + " '" + propertyName + "' " + propertyTypeName + " " + str(classID) + "\n")
    thisFile.write("28 'Parent' Object 0\n")
    print("Done" + str(totalDumped))

with open("events.txt", "w") as thisFile:
    eventAddr = LocByName("EventSchemaStart")
    eventEnd = LocByName("EventSchemaEnd")
    thisFile.write(str((eventEnd-eventAddr) / 0x14) + "\n")
    for addr in range(eventAddr, eventEnd, 0x14):
        eventID = Dword(addr)
        argTypeStart = Dword(addr+4)
        infoStart = Dword(addr+0x10)
        if infoStart == 0:
            thisFile.write("\tERR_UNKNOWN\n0\n")
        else:
            eventName = readStdString(Dword(infoStart+4))
            argListStart = Dword(Dword(infoStart + 0x28))
            argCount = Dword(infoStart + 0x2C)
            thisFile.write(eventName + "\n")
            thisFile.write("\t" + str(argCount) + "\n")
            currentArg = argListStart
            for argIndex in range(0, argCount):
                argTypeString = readStdString(Dword(Dword(currentArg + 0xC) + 4))
                argName = readStdString(Dword(currentArg + 8))
                argTypeInfo = Word(argTypeStart + argIndex * 8)
                thisFile.write("\t" + argName + " " + str(argTypeInfo) + " " + argTypeString + "\n")
                currentArg = Dword(currentArg)

print("Done")
