import numpy as np
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def findroute(startpos, map_, endpos): 
    start_val = map_[startpos[0], startpos[1]]
    neighbors = [(x+startpos[0], y+startpos[1]) for x,y in zip([-1,0,0,1], [0,-1,1,0])]
    trails_total = 0
    for neighbor in neighbors: 
        try: 
            if neighbor[0] < 0 or neighbor[1] < 0: 
                continue
            n_val = map_[neighbor[0], neighbor[1]]
            assert neighbor[0] >= 0 
            assert neighbor[1] >= 0 
        except IndexError: 
            continue
        if start_val == 8 and n_val == 9: 
            trails_total+=1
            endpos.add((int(neighbor[0]), int(neighbor[1])))
        if (1+start_val) == n_val: 
            endpos, add_ = findroute(neighbor, map_, endpos)
            trails_total+= add_
    return endpos, trails_total


def solvea(lines): 
    a = np.array([[int(y) for y in x.strip()] for x in lines])
    trailhead_pos = np.where(a == 0)
    trailhead_pos = np.c_[trailhead_pos[0], trailhead_pos[1]]
    sum_ = 0
    sum_total = 0
    for pos in trailhead_pos:
        # print(pos)
        add_, total = findroute(pos, a, set())
        # print(add_, len(add_))
        sum_ += len(add_)
        sum_total += total
    print(f"a: {sum_}")
    print(f"b: {sum_total}")
    return sum_, sum_total

if __name__ == "__main__":
    lines = read_data()
    solvea(lines)
