# Useful classes and/or functions for simple algorithms/data structures

# FUNCTIONS #
def array_2d(row, col):
    arr = []
    for y in range(col):
        cells = []
        for x in range(row):
            cells.append([])
        arr.append(cells)
    return arr