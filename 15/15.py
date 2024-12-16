import numpy as np
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def splitlines(lines): 
    moved = {"<" : np.array([0,-1]), ">": np.array([0, 1]), "^" : np.array([-1, 0]), "v" : np.array([1, 0])}
    warehouse, moves, rawmoves = [], [], []
    start_moves = None
    for i, line in enumerate(lines): 
        if line == "\n":
            start_moves = i+1
            break
        warehouse.append([x for x in line.strip()])
    for line in lines[start_moves:]:
        for e in line.strip():
            moves.append(moved[e])
            rawmoves.append(e)
    return np.array(warehouse), np.array(moves), np.array(rawmoves)


class RobotMap: 
    def __init__(self, warehouse, moves, rawmoves):
        self.warehouse = warehouse
        self.moves = moves
        self.rawmoves = rawmoves
        rob_pos_x, rob_pos_y = np.where(warehouse == "@")
        self.robot_pos = np.array([rob_pos_x[0], rob_pos_y[0]])
        self.boxes = None

    def movevalid(self, cur_pos, move): 
        next_pos = tuple(cur_pos + move)
        if self.warehouse[next_pos] == "#": 
            return False
        if self.warehouse[next_pos] == "O":
            return self.movevalid(next_pos, move)
        if self.warehouse[next_pos] == ".":
            return True
        assert False
    def move(self, cur_pos, move, char_): 
        assert char_ in ["@", "O"]
        next_pos = tuple(cur_pos + move)
        if char_ == "@":
            self.warehouse[tuple(cur_pos)] = "."
        next_char_ = self.warehouse[next_pos]
        self.warehouse[next_pos] = char_
        if char_ == "@":
            self.robot_pos = cur_pos + move
        if next_char_ == ".": 
            return
        assert next_char_ == "O"
        self.move(next_pos, move, "O")
    def makemove(self, move): 
        if self.movevalid(self.robot_pos, move): 
            # print("valid move")
            # move
            self.move(self.robot_pos, move, "@")
        return
    def calcscore(self): 
        boxes_x, boxes_y = np.where(self.warehouse == "O")
        self.boxes = np.array([np.array([x,y]) for x,y in zip(boxes_x, boxes_y)])
        score = 0
        for box in self.boxes: 
            score += 100 * box[0] + box[1]
        print(f"a: {score}")
        return score
    def run(self): 
        for i, move in enumerate(moves): 
            self.makemove(move)
            # self.printwarehouse(self.rawmoves[i])
        # self.printwarehouse()
        return self.calcscore()
    
    def printwarehouse(self, move=""): 
        if move != "": 
            print(f"Move: {move}")
        for r in self.warehouse: 
            print("".join(r))

class RobotMap2: 
    def __init__(self, warehouse, moves, rawmoves):
        self.warehouse = self.setup_warehouse(warehouse)
        self.moves = moves
        self.rawmoves = rawmoves
        rob_pos_x, rob_pos_y = np.where(self.warehouse == "@")
        self.robot_pos = np.array([rob_pos_x[0], rob_pos_y[0]])
        self.boxes = None

    def setup_warehouse(self, warehouse): 
        new_warehouse = []
        for row in warehouse: 
            r_ = []
            for e in row: 
                if e == "#":
                    r_ += ["#","#"]
                elif e == "O":
                    r_ += ["[","]"]
                elif e == "@": 
                    r_ += ["@", "."]
                else: 
                    r_ += [".", "."]
            new_warehouse.append(r_)
        return np.array(new_warehouse)
    
    def movevalid(self, cur_pos, move): 
        next_pos = tuple(cur_pos + move)
        next_char = self.warehouse[next_pos]
        if next_char == "#": 
            return False
        if next_char in ["[", "]"]:
            # left right moves
            if move[0] == 0:
                next_pos = cur_pos + 2*move
                return self.movevalid(next_pos, move)
            else: # up down move
                aff_pos = cur_pos + move + np.array([0,1]) if next_char == "[" else cur_pos + move + np.array([0,-1])
                if self.movevalid(aff_pos, move):
                    return self.movevalid(next_pos, move)
                return False
        if next_char == ".":
            return True      
        assert False

    def move(self, cur_pos, move, char_): 
        assert char_ in ["@", "[", "]"]
        next_pos = tuple(cur_pos + move)
        if char_ == "@":
            self.warehouse[tuple(cur_pos)] = "."
        next_char_ = self.warehouse[next_pos]
        self.warehouse[next_pos] = char_
        if char_ == "@":
            self.robot_pos = cur_pos + move
        if next_char_ == ".": 
            return
        assert next_char_ in ["[", "]"]
        # left right
        if move[0] == 0: 
            self.move(next_pos, move, next_char_)
        else:
            aff_pos = cur_pos + move + np.array([0,1]) if next_char_ == "[" else cur_pos + move + np.array([0,-1])
            other_char = "[" if next_char_ == "]" else "]"
            self.warehouse[tuple(aff_pos)] = "."
            self.move(aff_pos, move, other_char)
            self.move(next_pos, move, next_char_)

    def makemove(self, move): 
        # self.printwarehouse()
        if self.movevalid(self.robot_pos, move): 
            self.move(self.robot_pos, move, "@")
        return
    
    def calcscore(self): 
        boxes_x, boxes_y = np.where(self.warehouse == "[")
        self.boxes = np.array([np.array([x,y]) for x,y in zip(boxes_x, boxes_y)])
        score = 0
        for box in self.boxes: 
            score += 100 * box[0] + box[1]
        print(f"b: {score}")
        return score
    
    def run(self): 
        for i, move in enumerate(moves): 
            self.makemove(move)
        return self.calcscore()
    
    def printwarehouse(self, move=""): 
        if move != "": 
            print(f"Move: {move}")
        for r in self.warehouse: 
            print("".join(r))
        

if __name__ == "__main__":
    lines = read_data()
    warehouse, moves, rawmoves = splitlines(lines)
    rm = RobotMap(warehouse.copy(), moves, rawmoves)
    rm.run()
    rm2 = RobotMap2(warehouse.copy(), moves, rawmoves)
    rm2.run()
