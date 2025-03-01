def addDots(data):
    firstItem = data.pop(0)
    outputArr = list(map(lambda str: "• " + str, data))
    outputArr.insert(0, firstItem)
    output = "\n".join(outputArr)
    return output