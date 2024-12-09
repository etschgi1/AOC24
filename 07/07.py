import itertools as it
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def concat(res, input_): 
    # 07 -b return all possible concat sequences!
    out = []
    len_in = len(input_)
    drop_whitespace = it.product(range(2), repeat=len_in-1)
    for drop_id in drop_whitespace: 
        line = f"{res}: {input_[0]}"
        for i, d in enumerate(drop_id):
            if d == 0: 
                line +=  f" {input_[i+1]}"
            else: 
                line += f"{input_[i+1]}"
        out.append(line)
    return out


def solveable(line, solveB = False): 
    res = int(line.split(":")[0])
    input_ = [int(x) for x in "".join(line.split(":")[1]).split(" ")[1:]]
    ops = ["".join(op) for op in it.product(["+","*"], repeat=len(input_)-1)]

    if len(input_) == 1:
        if input_[0] == res: 
            return True
        return False

    for comb in ops: 
        cur_res = input_[0]
        for i,c in enumerate(comb): 
            if c== "*":
                cur_res *= input_[i+1]
            else: 
                cur_res += input_[i+1]
        if cur_res == res: 
            return True
    if solveB == True: 
        # if res == 7290:
        #     print("...")
        # b)
        ops = ["".join(op) for op in it.product(["+","*", "|"], repeat=len(input_)-1)]
        for comb in ops: 
            cur_res = input_[0]
            for i,c in enumerate(comb): 
                if c== "*":
                    cur_res *= input_[i+1]
                elif c == "+":
                    cur_res += input_[i+1]
                else: 
                    cur_res = int(str(cur_res)+str(input_[i+1]))
            if cur_res == res: 
                return True
    return False

def solve(lines, solveB= False): 
    # 07 - a
    total = 0
    for line in lines: 
        if (solveable(line, solveB=solveB)): 
            total += int(line.split(":")[0])
    if solveB: 
        print(f"b: {total}")
    else:
        print(f"a: {total}")
    return total

if __name__ == "__main__":
    lines = [x.strip() for x in read_data()]
    solve(lines)
    solve(lines,solveB=True)

