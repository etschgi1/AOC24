import numpy as np
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def getdiagonal(lines): 
    # 04 - part A)
    #left diagonal
    nr_diag = sum(lines.shape)-1
    linesF = np.fliplr(lines)
    left_dia = [lines.diagonal(offset=i) for i in range(-lines.shape[0]+1, lines.shape[1])]
    right_dia = [linesF.diagonal(offset=i) for i in range(-linesF.shape[0]+1, linesF.shape[1])]
    assert len(left_dia) == len(right_dia) == nr_diag
    # print(right_dia)
    left_dia = ["".join(x) for x in left_dia]
    right_dia = ["".join(x) for x in right_dia]
    return right_dia, left_dia

def xmascount(lines): 
    # 04 - part A)
    import re
    lines = np.array([[y for y in x.strip()] for x in lines])
    wT, wL= lines.shape
    linesT = lines.T
    Rdia, Ldia = getdiagonal(lines)
    lines = ["".join(lines[i,:]) for i in range(wT)]
    linesT = ["".join(linesT[i,:]) for i in range(wL)]

    pattern = re.compile("XMAS")
    patternback = re.compile("SAMX")
    total = 0
    for line in lines:
        total += len(pattern.findall(line) ) + len(patternback.findall(line))
    for line in linesT: 
        total += len(pattern.findall(line) ) + len(patternback.findall(line))
    for line in Rdia: 
        total += len(pattern.findall(line) ) + len(patternback.findall(line))
    for line in Ldia: 
        total += len(pattern.findall(line) ) + len(patternback.findall(line))
    print("a: " + str(total))

def match(local, kernel): 
    local, kernel = local.flatten(), kernel.flatten()
    if all([local[i] == kernel[i] for i in [0,2,4,6,8]]): 
        return 1
    return 0

def masfinder(lines):
    # 04 - part B)
    lines = np.array([[y for y in x.strip()] for x in lines])
    kernel = np.array([["M","","S"], ["","A",""],["M","","S"]])
    kernelT = kernel.T
    kernelF = np.fliplr(kernel)
    kernelFT = kernelF.T
    kernels = [kernel, kernelF, kernelT, kernelFT]
    # try to match kernels    
    total = 0
    for i in range(lines.shape[0]-2):
        for j in range(lines.shape[1]-2):
            local_ = lines[i:i+3,j:j+3].copy()
            total += sum([match(local_, kernel) for kernel in kernels])
    print("b: " + str(total))

if __name__ == "__main__":
    lines = read_data()
    xmascount(lines)
    masfinder(lines)