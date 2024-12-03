

def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def mult(lines): 
    # part a
    import re
    pattern = re.compile(r"mul\([0-9]+,[0-9]+\)")
    hits = pattern.findall(lines)
    prods = [int(x.split(",")[0][4:]) * int(x.split(",")[1][:-1]) for x in hits]
    sum_ = sum(prods)
    print("a: " + str(sum_))
    return sum_

def multdo(lines): 
    # part b
    import re
    pattern_mul = r"mul\([0-9]+,[0-9]+\)"
    pattern_do = r"do\(\)"
    pattern_dont = r"don't\(\)"
    pattern = re.compile("|".join([pattern_mul, pattern_do, pattern_dont]))
    hits = pattern.findall(lines)
    count = True
    res = 0
    for hit in hits: 
        if hit == "don't()":
            count = False
            continue
        elif hit == "do()":
            count = True
            continue
        if count == True: 
            res += int(hit.split(",")[0][4:]) * int(hit.split(",")[1][:-1])
    print("b: " + str(res))
    return res


if __name__ == '__main__':
    lines = read_data()
    lines = "".join(lines) # preprocs
    mult(lines)
    multdo(lines)