import numpy as np
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

class Map():
    def __init__(self, map_, obstical=(None, None)):
        self.map = map_
        self.dim = self.map.shape
        self.visited = np.zeros_like(map_, dtype=int)
        self.guard_pos = (np.where(self.map == "^")[0][0], np.where(self.map == "^")[1][0])
        #print(f"Initial pos: {self.guard_pos} {self.map[self.guard_pos]}")
        self.visited[self.guard_pos] = 1
        self.heading = "upward"
        self.turns = {"upward": "right", "right": "downward", "downward": "left", "left": "upward"}
        self.guardfig = {"upward": "^", "right": ">", "left": "<", "downward": "↓"}
        if obstical != (None, None): 
            self.obstical = obstical
            self.map[self.obstical] = "#"
        self.pos_log = [self.guard_pos]

    def next_pos(self): 
        next_pos = None
        if self.heading == "upward": 
            next_pos = (self.guard_pos[0] - 1, self.guard_pos[1])
        elif self.heading == "downward":
            next_pos = (self.guard_pos[0] + 1, self.guard_pos[1])
        elif self.heading == "right": 
            next_pos = (self.guard_pos[0], self.guard_pos[1] + 1)
        elif self.heading == "left":
            next_pos = (self.guard_pos[0], self.guard_pos[1] - 1)

        #out of bounds
        if any([x < 0 for x in next_pos])  or next_pos[0] >= self.dim[0] or next_pos[1] >= self.dim[1]:
            return False
        #obstical
        if self.map[next_pos] == "#": # turn right
            self.heading = self.turns[self.heading]
            # self.print_Map()
            return self.next_pos() #no update - frist turn!
        # update pos
        self.pos_log.append(next_pos)
        self.guard_pos = next_pos
        self.visited[next_pos] = 1
        return True

    def check_for_loop(self): 
        # check if 2 cells repeat!
        if len(self.pos_log) < 2: # not possible in our case!
            if all([self.pos_log[0] == self.pos_log[i] for i in range(self.pos_log)]):
                return True
            return False
        if self.pos_log[-2] in self.pos_log[:-2]:
            positions = [i for i,val in enumerate(self.pos_log[:-2]) if val == self.pos_log[-2]]
            for pos in positions: 
                if self.pos_log[-1] == self.pos_log[pos+1]: 
                    return True
        return False

    def count_visited(self):
        return np.sum(self.visited)
    
    def print_Map(self):
        self.map[self.visited == 1] = "X"
        self.map[self.guard_pos] = self.guardfig[self.heading]
        print(self.map)

    def run(self, loopcheck=False):
        while self.next_pos(): 
            if loopcheck==True: 
                if self.check_for_loop(): 
                    return True
            continue
        if loopcheck: 
            return False
        return self.count_visited()


if __name__ == "__main__":
    lines = read_data()
    lines = np.array([list(line.strip()) for line in lines])
    a = Map(lines)
    import time
    start = time.time()
    print(f"a: {a.run()}")
    print(f"Took {time.time()-start} s")
    input("b takes about an hour because I did it badly :DDD (press any key to continue nevertheless)")
    start = time.time()
    loop = 0
    for i in range(lines.shape[0]):
        for j in range(lines.shape[1]):
            print(i,j)
            b = Map(lines.copy(), (i,j))
            if b.run(loopcheck=True): 
                print("loop")
                loop += 1
    print(f"b: {loop}")
    print(f"Took {time.time()-start} s")
