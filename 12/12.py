import numpy as np

region_dict = {}
region_counter = {}
area_dim = None

dir_dict = {0: (0, 1), 2: (0, -1), 1: (1, 0), 3: (-1, 0)}


class Region():
    def __init__(self, Name):
        self.name = Name
        self.letter = Name.split("_")[0]
        self.coords = []
        self.edge_nodes = []
    
    def add_field(self, a, coord): 
        # print(f"add {a[coord]} {coord} to {self.name}")
        self.coords.append(coord)
        a[coord] = " "
    
    def number_common_neighbors(self, coord):
        same_group = 0
        for x,y in zip([0,0,1,-1], [1,-1,0,0]):
            if (coord[0]+x, coord[1]+y) in self.coords:
                same_group += 1
        return same_group
    
    def calcRScore(self): 
        area = len(self.coords)
        circum = 0
        for coord in self.coords: 
            circum += 4-self.number_common_neighbors(coord)
        assert circum > 0
        assert area > 0
        return area*circum
    
    def getedgeNeighbors(self, node): 
        out = []
        for x,y in zip([0,1,0,-1], [1,0,-1,0]): #rdlu
            neighbor = (node[0]+x,node[1]+y)
            if neighbor in self.edge_nodes: 
                out.append(neighbor)
            else:
                out.append(None)
        return out
    
    def move(self, start_node): 
        # move until i have to turn!
        neighbors_ = self.getedgeNeighbors(start_node)#rdlu
        # get dir
        dir_ = None
        for i, n in enumerate(neighbors_): 
            if n is not None: 
                dir_ = dir_dict[i]
                break
        assert dir_ is not None
        # walk until stuck! 
        while True: 
            next_ = (start_node[0]+dir_[0], start_node[1]+dir_[1])
            if next_ in self.edge_nodes: 
                start_node = next_
            else: 
                break # turn!
        return start_node


        


    def calcScoreB(self): 
        area = len(self.coords)
        #build edge nodes
        for coord in self.coords:
            com_neigh = self.number_common_neighbors(coord)
            if com_neigh != 4:
                assert coord not in self.edge_nodes
                self.edge_nodes.append(coord)
        # start somewhere
        edge_counter = 0
        next_node = self.edge_nodes[0]
        self.edge_nodes.remove(next_node) # remove first!
        while len(self.edge_nodes): 
            next_node = self.move(next_node)
            edge_counter += 1
        return edge_counter

    def __repr__(self):
        return f"{len(self.coords)} {self.coords}"

    
def neighbor_indices(grid, tup): 
    global area_dim
    i,j = tup
    out = []
    for x,y in zip([0,0,1,-1], [1,-1,0,0]):
        if i+x>=0 and y+j>=0 and i+x < area_dim[0] and j+y < area_dim[1]:
            n = (i+x, j+y)
            if grid is not None and grid[n] == " ":
                continue
            out.append(n)
    return out

def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def buildarea(grid, start): 
    global area_dim
    start_key = grid[start]
    # init key!
    if start_key == " ": 
        print("EMPTY REGION")
        assert False
        return
    try: 
        key_ = f"{start_key}_{region_counter[start_key]}"
        region_counter[start_key] += 1
    except KeyError: 
        key_ = f"{start_key}_{0}"
        region_counter[start_key] = 1
    cur_reg = Region(key_)
    region_dict[key_] = cur_reg
    cur_reg.add_field(grid, start)

    neighbor_stack = neighbor_indices(grid, start)
    while len(neighbor_stack): 
        next_neighbor = neighbor_stack.pop()
        next_val = grid[next_neighbor]
        # print(f"{cur_reg.name} {next_neighbor} {next_val}")
        if next_val == " ": 
            # print("Go on")
            continue
        if next_val != start_key and next_val not in region_counter.keys(): # counting on this region not started!
            buildarea(grid, next_neighbor)
        elif next_val == start_key: #this belongs to our area 
            cur_reg.add_field(grid, next_neighbor)
            neighbor_stack += neighbor_indices(grid, next_neighbor)

        # printa(grid)


def calcfence():
    total_fence = 0
    for region in region_dict.values(): 
        total_fence += region.calcRScore()
    print(f"a) total_fence: {total_fence}")
    return total_fence    

def calcfenceb():
    total_fence = 0
    for region in region_dict.values():
        total_fence += region.calcScoreB()
    print(f"b) {total_fence}")
    return total_fence

def printa(a):
    global area_dim
    for i in range(area_dim[0]):
        for j in range(area_dim[1]):
            print(a[i,j],end="")
        print()

def buildregions(lines): 
    global area_dim
    a_orig = np.array([[x for x in line.strip()] for line in lines])
    a = a_orig.copy()
    # start at 0,0
    area_dim = a.shape
    while True:
        start = tuple(np.array(np.where(a != " ")).T[0])
        buildarea(a, start)
        if np.all(a == " "):
            break
    # calcfence()
    calcfenceb()
    # print(region_dict)

if __name__ == "__main__":
    lines = read_data()
    buildregions(lines)
