import functools


def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def blink(stones): 
    # part a - bruteforce
    out = []
    for stone in stones: 
        len_ = len(str(stone))
        if stone == 0: #rule 1
            out.append(1)
        elif len_ % 2 == 0: 
            out.append(int(str(stone)[:len_//2]))
            out.append(int(str(stone)[len_//2:]))
        else: 
            out.append(stone*2024)
    return out

@functools.cache
def handle(stone): 
    # part b 
    if stone == 0: 
        return 1
    len_ = len(str(stone))
    if len_ % 2 == 0: 
        return (int(str(stone)[:len_//2]), int(str(stone)[len_//2:]))
    return stone*2024

@functools.cache
def cleverblink(stone, n): 
    # part b 
    count_ = 1
    while n>0: 
        n-=1
        res = handle(stone)
        if type(res) == tuple: #we grow!!!
            count_ += cleverblink(res[1], n)
            stone = res[0]
        else:
            stone = res
    return count_


def blinkabit(stones, n=25): 
    if n==25:
        for i in range(n): 
            stones = blink(stones)
        print(f"a: {len(stones)}")
        return
    sum_ = 0
    for stone in stones:
        sum_ += cleverblink(stone, n)
    if n==25:
        print(f"a: {sum_}")
        return
    print(f"b: {sum_}")

if __name__ == "__main__":
    lines = read_data()[0]
    stones = [int(x) for x in lines.split(" ")]
    blinkabit(stones)
    blinkabit(stones, 75)