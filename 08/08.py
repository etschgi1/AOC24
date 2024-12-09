import itertools as it
import numpy as np
from more_itertools import distinct_combinations as idp
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

class Vec: 
    def __init__(self, r,c):
        self.c = c
        self.r = r
    def __add__(self, other): 
        return Vec(self.r+other.r, self.c+other.c)
    def __sub__(self, other): 
        return Vec(self.r-other.r, self.c-other.c)
    def __mul__(self, m): 
        return Vec(m*self.r, m*self.c)
    def __rmul__(self, m): 
        return self.__mul__(m)
    def __repr__(self):
        return f"({self.r}, {self.c})"

def gen_coords(lines): 
    a = np.array([[y for y in x.strip()] for x in lines])
    antennas = {}
    for r in range(a.shape[0]): 
        for c in range(a.shape[1]):
            e = a[r,c]
            if e != ".":
                try: 
                    antennas[str(e)] += [Vec(r,c)]
                except KeyError: 
                    antennas[str(e)] = [Vec(r,c)]
    return a, antennas, a.shape

def inbounds(vec, shape): 
    if vec.r >= 0 and vec.c >= 0: 
        if vec.r < shape[0] and vec.c < shape[1]:
            return True
    return False

def getpoints(start, vec, shape): 
    points = [start]
    i = 0
    for op in ["+","-"]:
        while True:
            if op == "+":
                i += 1
            else: 
                i -= 1 
            next_point = start + i*vec
            if inbounds(next_point, shape):
                points.append(next_point)
            else:
                break
    return points

def solveantinodes(a, coords, shape, solveA=True): 
    # 08 - a) 
    antinode_count = 0
    for key in coords.keys(): # one key after another
        combinations = idp(coords[key],2)
        for comb in combinations: 
            vec = comb[0]-comb[1]
            p0, p1 = comb[0] + vec, comb[1] - vec
            if solveA: 
                points_to_check = [p0,p1]
            else: 
                points_to_check = getpoints(comb[0], vec, shape)
            for p in points_to_check: 
                if inbounds(p, shape) and a[p.r, p.c] != "#": 
                    antinode_count+=1
                    a[p.r, p.c] = "#"
        #     break
        # break
    print(a)
    print(f"a: {antinode_count}")

if __name__ == "__main__":
    lines = read_data()
    a, coords, shape = gen_coords(lines)
    solveantinodes(a.copy(), coords, shape)
    solveantinodes(a.copy(), coords, shape, solveA=False)
