import numpy as np
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def solvea(lines): 
    a = np.array([[int(y) for y in x.strip()] for x in lines])
    trailhead_pos = np.where(a == 0)
    

if __name__ == "__main__":
    lines = read_data()
    solvea(lines)
