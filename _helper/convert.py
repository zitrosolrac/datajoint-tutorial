from glob import glob
from os.path import splitext
import numpy as np
from scipy.io import savemat

files = glob('*.npy')

for f in files:
    base = splitext(f)[0]
    data = np.load(f)
    d = dict(data=data)
    savemat(base, d)
    print('Saved {}.mat!'.format(base))

