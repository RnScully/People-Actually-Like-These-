import random
import numpy as np

samples = np.random.randint(low=1, high=395000000, size=20000)
with open('samples.txt', 'a') as the_file:
    for i in samples:
        the_file.write(str(i)+'\n')
