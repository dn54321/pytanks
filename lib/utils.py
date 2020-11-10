# Useful classes and/or functions for simple algorithms/data structures

# FUNCTIONS #
def array_2d(index_1, index_2, default=None):
    arr = []
    for y in range(index_1):
        cells = []
        for x in range(index_2):
            if default is None: cells.append([])
            else: cells.append(default)
        arr.append(cells)
    return arr