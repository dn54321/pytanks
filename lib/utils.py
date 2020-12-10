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

def msk_2d(arr, key, dims):
    msk = arr.copy()
    for i in dims[0]:
        for j in dims[1]:
            msk[i][j] = arr[i][j] is key
    return msk
    

    
        
        
    