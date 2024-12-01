

def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def preproc(lines): 
    f, s = [], []
    for line in lines: 
        f.append(int(line.split()[0].strip()))
        s.append(int(line.split()[1].strip()))
    f.sort()
    s.sort()
    return f,s

def similarity_score(f, s): 
    # 01 - b)
    fd, sd = {},{}
    for x,y in zip(f,s): 
        try:
            fd[x] += 1
        except KeyError:
            fd[x] = 1
        try: 
            sd[y] += 1
        except KeyError: 
            sd[y] = 1
    sim_score = 0
    for kf,vf in zip(fd.keys(), fd.values()): 
        try: 
            vs = sd[kf]
        except:
            vs = 0
        print(kf, vf, vs)
        sim_score += kf * vf * vs
    print(sim_score)
    return sim_score

def pair_up(f,s): 
    # 01 - a)
    sum_ = sum([abs(x-y) for x, y in zip(f,s)])
    print(sum_)
    return sum_


if __name__ == '__main__':
    lines = read_data()
    f,s = preproc(lines)
    pair_up(f,s)
    similarity_score(f,s)