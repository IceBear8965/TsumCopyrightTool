"""
Copyright (C) 2025 IceBear8965

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.
"""


def sortInput(data, filters, orderfilter):
    data = [d.replace("•", "") for d in data]
    data = [d.strip() for d in data]
    order = []
    if len(filters) > 0:
        for f in filters:
            for d in data:
                if f in d:
                    data.pop(data.index(d))
        data = [d.strip() for d in data]

    if len(orderfilter) > 0:
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
