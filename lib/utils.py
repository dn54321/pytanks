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
    msk = array_2d(dims[0], dims[1])
    for i in range(dims[0]):
        for j in range(dims[1]):
            msk[i][j] = arr[i][j] is key
    return msk
    
def matrix_transpose(arr, dims):
    h,w = dims
    arr_t = array_2d(w, h)
    for i in range(w):
        for j in range(h):
            arr_t[i][j] = arr[j][i]
    return arr_t
    
    
        
        
    