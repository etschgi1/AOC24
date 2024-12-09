import itertools as it
import numpy as np
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def gendrive(line):

    ids = []
    id_ = 0
    true_index = 0
    next_free = [] 
    for i, n in enumerate(line): 
        if i % 2 == 0: #file
            ids += list(it.repeat(id_,int(n)))
            id_ += 1
        else: # empty 
            ids += list(it.repeat(".", int(n)))
            next_free += list(range(true_index, true_index+int(n)))
        true_index += int(n)
    return ids, next_free[::-1]

def reorderdrive(ids, next_free): 
    r_ids = ids.copy()[::-1]
    len_ = len(r_ids)
    for c, e in enumerate(r_ids): 
        if e == ".": 
            continue
        cur_ind = len_ - (c+1)
        insert_pos = next_free.pop()
        if insert_pos >= cur_ind: 
            res = np.array(ids.copy()[:cur_ind+1])
            break
        assert ids[insert_pos] == "."
        ids[insert_pos] = e
    indices = np.arange(len(res))
    print(res)
    print(f"a: {np.dot(indices, res)}")

def reorderwholefiles(ids): 
    blocks = []
    emptysizes = []
    new_ = True
    new_block = True
    last_symbol = None
    for c, e in enumerate(ids): 
        if e == ".":
            new_block = True
            if new_ == True: 
                new_ = False
                emptysizes.append((c,0)) 
            emptysizes[-1] = (emptysizes[-1][0],emptysizes[-1][1]+1)
        else: 
            new_ = True
            if new_block == True or last_symbol != e: 
                new_block = False
                blocks.append((c, 0))
            blocks[-1] = (blocks[-1][0],blocks[-1][1]+1)
            last_symbol = e
    # print(ids)
    len_ = len(ids)
    for block in blocks[::-1]: 
        # find place
        for c, free_space in enumerate(emptysizes): 
            if free_space[1] >= block[1] and free_space[0] < block[0]: 
                # move & remove stuff
                ids[free_space[0]: free_space[0]+free_space[1]] = [ids[block[0]] for _ in range(block[1])] + ["." for _ in range(free_space[1] - block[1])]
                assert len(ids) == len_
                if free_space[1] - block[1] > 0 : 
                    emptysizes[c] = (free_space[0]+block[1],free_space[1]-block[1])
                else: 
                    del emptysizes[c]
                ids[block[0]: block[0]+block[1]] = ["." for _ in range(block[1])]
                break
    indices = np.arange(len_)
    res = np.array([0 if x == "." else x for x in ids])
    print(indices)
    print(res)
    print(f"b: {np.dot(indices, res)}")



if __name__ == "__main__":
    lines = read_data()
    line = lines[0]
    ids, next_free = gendrive(line)
    reorderdrive(ids.copy(), next_free)
    reorderwholefiles(ids.copy())