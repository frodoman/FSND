def listToString(stringlist): 
    if len(stringlist) == 0:
        return ""

    result = ""
    for oneString in stringlist: 
        result += (oneString + ",")

    return result