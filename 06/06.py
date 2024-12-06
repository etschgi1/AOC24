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
        print(f"Initial pos: {self.guard_pos} {self.map[self.guard_pos]}")
        self.visited[self.guard_pos] = 1
        self.heading = "upward"
        self.turns = {"upward": "right", "right": "downward", "downward": "left", "left": "upward"}
        self.guardfig = {"upward": "^", "right": ">", "left": "<", "downward": "↓"}
        self.obstical = obstical
        self.pos_log = [self.guard_pos]
        self.inLoop = False

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

    def check_for_loop(self, last = 2): 
        # check if 2 cells repeat!
        if len(self.pos_log) < 2: # not possible in our case!
            if all([self.pos_log[0] == self.pos_log[i] for i in range(self.pos_log)]):
                return True
            return False
        if self.pos_log[-last:] in self.pos_log[:-last]:
            return True
        return False

    def count_visited(self):
        return np.sum(self.visited)
    
    def print_Map(self):
        self.map[self.visited == 1] = "X"
        self.map[self.guard_pos] = self.guardfig[self.heading]
        print(self.map)

    def run(self):
        while self.next_pos(): 
            continue
        return self.count_visited()

    def runobsticalsearch(self): 
        loop_counter = 0
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                self.obstical = (i,j)
                if self.map[self.obstical] == "#": # no loop here is already an obstical
                    continue
                else: 
                    self.map[self.obstical] = "#"
                while self.next_pos():
                    if self.check_for_loop():
                        loop_counter += 1
                        break
        return loop_counter



if __name__ == "__main__":
    lines = read_data()
    lines = np.array([list(line.strip()) for line in lines])
    a = Map(lines)
    b = Map(lines)
    import time
    start = time.time()
    print(f"a: {a.run()}")
    print(f"Took {time.time()-start} s")
    start = time.time()
    print(f"b: {b.runobsticalsearch()}")
    print(f"Took {time.time()-start} s")
