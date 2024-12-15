import numpy as np
import matplotlib.pyplot as plt

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
        robots.append((pos, vel))
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
    

def neighbor(coords, xcord,ycord): 
    pos = [(xcord+x_, ycord+y_) for x_,y_ in zip([0,0,1,-1], [1,-1,0,0])]
    count = 0
    for p in pos: 
        if p in coords: 
            count+=1
    return count

def simrobots(robots, timesteps):
    # printfield(robots,0)
    if timesteps is None: 
        r2 = []
        robdis = []
        t_range = range(10000)
        for t_ in t_range:
            for i, robot in enumerate(robots): 
                robots[i] = robotstep(robot)
            robdist = 0
            x_coords = [x[0][0] for x in robots]
            y_coords = [x[0][1] for x in robots]
            coords = [(x,y) for x,y in zip(x_coords, y_coords)]
            for x1,y1 in zip(x_coords, y_coords): 
                robdist += neighbor(coords, x1,y1)
            # calc dist
            # m = (np.array(x_coords).mean(), np.array(y_coords).mean())
            # r2.append(sum([(x-m[0])**2 + (x-m[1])**2 for x,y in zip(x_coords, y_coords)]))
            robdis.append(robdist)

        plt.scatter(t_range, robdis)
        min_arg = np.argmin(np.array(robdis))
        print(min_arg)
        # plt.scatter(t_range, y_var)
        # plt.scatter(t_range, np.array(x_var)*np.array(y_var))
        plt.savefig("var.png")
        plt.close()
        return min_arg
        return

    if timesteps > 200: 
        # plot stuff
        for i,robot in enumerate(robots): 
            robots[i] = robotstep(robot, timesteps)
        grid = getgrid(robots)
        plt.imshow(grid)
        plt.savefig("heat.png")
        print("heatmap")
        return
    
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
    


if __name__ == "__main__":
    lines = read_data()
    robots = preprocrobots(lines)
    simrobots(robots.copy(), 100)
    argmin = simrobots(robots.copy(), None)
    simrobots(robots.copy(), argmin)

