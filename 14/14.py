import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import functools

grid_dim = (103, 101) # (7,11)

def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def preprocrobots(lines): 
    robots = []
    for line in lines: 
        pos, vel = line.split(" ")[0][2:], line.split(" ")[1][2:]
        pos, vel = [int(x) for x in pos.split(",")], [int(x) for x in vel.split(",")]
        robots.append((tuple(pos), tuple(vel)))
    return robots

def robotstep(robot, n=1):
    # 14 a)
    global grid_dim
    pos, vel = robot
    new_pos = ((pos[0]+n*vel[0])%grid_dim[1], (pos[1]+n*vel[1])%grid_dim[0])
    return (new_pos, vel)

def getgrid(robots): 
    grid = np.zeros(grid_dim)
    for robot in robots: 
        pos, _ = robot
        pos = (pos[1], pos[0])
        grid[pos] += 1
    return grid

def printfield(robots, timesteps): 
    print(f"---{timesteps}---")
    grid = getgrid(robots)
    for i, e in enumerate(grid.flatten()):
        if i % grid_dim[1] == 0 and i != 0: 
            print()
        if e == 0: 
            print(".", end="")
        else:
            print(int(e), end="")
    print()
    

def simrobots(robots, timesteps):
    for t in range(timesteps):
        for i, robot in enumerate(robots): 
            robots[i] = robotstep(robot)
    
    # done with sim. 
    # printfield(robots, t)
    # split area
    grid = getgrid(robots)
    col_border, row_border = grid_dim[1]//2+1, grid_dim[0]//2+1
    print(row_border)
    print(col_border)
    q1 = grid[0:row_border-1, 0:col_border-1].sum()
    q2 = grid[row_border:, 0:col_border-1].sum()
    q3 = grid[0:row_border-1, col_border:].sum()
    q4 = grid[row_border:, col_border:].sum()
    res = q1 * q2 * q3 * q4
    print(f"a: {int(res)}")
    return res

@functools.cache
def getGrids(robots, Max_time): 
    grids = [getgrid(robots)]
    for timestep in range(Max_time): 
        new_robots = []
        for i, robot in enumerate(robots):
            new_robots.append(robotstep(robot))
        robots = tuple(new_robots)
        grids.append(getgrid(robots))
    return grids

def edge_score(grids):
    scores = [] 
    for i, grid in enumerate(grids):
        scores.append(1)
        for row in grid:
            c = 1
            for e in row: 
                if e > 0: 
                    scores[-1] *= c
                    c *= 2
                else: 
                    c = 1
    from math import log10
    scores = [log10(s) if s > 0 else 0 for s in scores]
    plt.scatter(range(len(scores)), scores)
    plt.savefig("scores.png")
    arg_max = np.argmax(scores)
    print(f"b: {arg_max}")
    return arg_max
                    
                


if __name__ == "__main__":
    lines = read_data()
    robots = preprocrobots(lines)
    simrobots(robots.copy(), 100)
    grids = getGrids(tuple(robots.copy()), 10000)
    edge_score(grids)

