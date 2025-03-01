def sortInput(data, filters, orderfilter):
    data = [d.replace("•", "") for d in data]
    data = [d.strip() for d in data]
    order = []
    if len(filters) > 1:
        for f in filters:
            for d in data:
                if f in d:
                    data.pop(data.index(d))
        data = [d.strip() for d in data]

    if len(orderfilter) > 1:
        for o in orderfilter:
            for d in data:
                if o in d:
                    order.append(o)

    if len(order) > 0:
        for param in order:
            for d in data:
                if param in d:
                    data.insert(order.index(param), data.pop(data.index(d)))

    output = []
    for d in data:
        output.append(d.replace("#", ""))

    return output