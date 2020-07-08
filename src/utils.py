import numpy as np


#  Taken from:
#  https://stackoverflow.com/questions/36960320/convert-a-2d-matrix-to-a-3d-one-hot-matrix-numpy
def onehot_board(a):
    ncols = a.max()+1
    out = np.zeros( (a.size,ncols), dtype=np.uint8)
    out[np.arange(a.size),a.ravel()] = 1
    out.shape = a.shape + (ncols,)

    # move board dims to second and third axis
    out = np.moveaxis(out, 1, 2)
    out = np.moveaxis(out, 0, 1)

    # ignore plane that encodes empty fields
    out = out[1:]

    return out
