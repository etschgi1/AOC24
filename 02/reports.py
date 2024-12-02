import numpy as np

def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def preproc(lines, no_rem=False): 
    orig_len = len(lines)
    lines = [[int(x) for x in y.split()] for y in lines]
    if no_rem: 
        return lines
    # remove non increasing / decreasing
    mod_lines = []
    for line in lines: 
        if all([line[x] > line[x-1] for x in range(1, len(line))]) or all([line[x] < line[x-1] for x in range(1, len(line))]):
            mod_lines.append(line)
    return mod_lines, orig_len

def count_safe(lines):
    # 02 - a)
    safe_lines_count = 0
    diff = lambda x,y: True if abs(x-y) >= 1 and abs(x-y) <= 3 else False
    for line in lines: 
        if all([diff(line[x], line[x-1]) for x in range(1, len(line))]): 
            safe_lines_count +=1
    return safe_lines_count

def dampener(lines):
    # 02 - b) 
    diff = lambda x,y: True if abs(x-y) >= 1 and abs(x-y) <= 3 else False
    def checkLine(line):
        if all([line[x] > line[x-1] for x in range(1, len(line))]) or all([line[x] < line[x-1] for x in range(1, len(line))]):
            if all([diff(line[x], line[x-1]) for x in range(1, len(line))]):
                return True
        return False
    save_count = 0
    for line in lines: 
        if checkLine(line): 
                save_count += 1
                continue
        for unsafe_index in range(len(line)):
            to_check = line[0:unsafe_index] + line[unsafe_index+1:]
            if checkLine(to_check): 
                save_count += 1
                break
    return save_count

if __name__ == '__main__':
    lines_raw = read_data()
    lines, len_orig = preproc(lines_raw)
    count_ = count_safe(lines)
    print("a: " + str(count_))
    count_ = dampener(preproc(lines_raw, True))
    print("b: " + str(count_))