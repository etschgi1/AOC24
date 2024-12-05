import numpy as np
from collections import deque
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def splitinput(lines):
    ordering, pages = {}, []
    page_start = 0
    for i, line in enumerate(lines):
        if line == "\n":
            page_start = i+1
            break
        v,k = line.strip().split("|")
        try:
            ordering[int(k)] += [int(v)]
        except KeyError:
            ordering[int(k)] = [int(v)]
    for line in lines[page_start:]:
        pages.append([int(x) for x in line.strip().split(",")])

    return ordering, pages

def find(sequence, e): 
    for i,s in enumerate(sequence): 
        if s==e:
            return i
    return np.inf

def check_sequence(ordering, sequence): 
        # print(f"Check {sequence}")
        for i, e in enumerate(sequence): 
            if e in ordering.keys(): # we have rules
                for before in ordering[e]: 
                    if before in sequence and find(sequence, before) > i: 
                        # print(f"{before} shouldn't be in front of {e}")
                        # doesn't work
                        return False
        return True

def printer(ordering, pages):
    # 05 - a)
    middle_sum = 0
    wrongpages = []
    for page in pages: 
        if check_sequence(ordering, page): 
            middle_sum += page[len(page)//2]
        else: 
            wrongpages.append(page)
    print(f"a: {middle_sum}")
    return middle_sum, wrongpages

def reorder(ordering, page): 
    # 05 - b)
    org_len = len(page)
    change = False
    res = deque()
    # for i, e in enumerate(page): 
    i = 0
    while len(page) != 0: 
        e = page[i]
        try: 
            before = ordering[e]
        except KeyError:
            page.remove(e)
            res.append(e)
            continue
        for b in before: 
            if b in page and find(page, b) > i: 
                res.append(b)
                # remove from page!
                change = True
                page.remove(b)
        page.remove(e)
        res.append(e)
        if change: 
            break
    res = list(list(res) + page)
    assert len(res) == org_len
    if check_sequence(ordering, res): 
        return res
    return reorder(ordering, res)

def order(ordering, wrongpages):
    # 05 - b)
    correct_ordering = []
    mid_sum = 0
    for page in wrongpages: 
        reordered = reorder(ordering, page)
        assert check_sequence(ordering, reordered) == True
        correct_ordering.append(reordered)
        mid_sum += reordered[len(reordered)//2]
    print(f"b: {mid_sum}")
    return mid_sum

if __name__ == "__main__":
    lines = read_data()
    ordering, pages = splitinput(lines)
    _, wrongpages = printer(ordering, pages)
    order(ordering, wrongpages)