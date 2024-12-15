import numpy as np
costs = np.array([3,1])
prec = 1e-9
def read_data(chdir=True):
    if chdir:
        import os
        os.chdir(os.path.dirname(__file__))
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def solve(machine): 
    # 13 - a) 
    a_x, b_x, a_y, b_y = machine["A"][0], machine["B"][0], machine["A"][1], machine["B"][1]
    X, Y = machine["P"][0], machine["P"][1]
    b_sol = (a_y*X - a_x*Y)/(a_y*b_x - b_y*a_x)
    a_sol = (X - b_sol*b_x) / a_x
    if all([abs(int(x) - x) < prec for x in [a_sol, b_sol]]): 
        return (a_sol, b_sol)
    return None
    # eq 1: A * X_A + B * X_B = X
    # eq 2: A * Y_A + B * Y_B = Y
    
def solvea(machines): 
    # 13 - a) 
    cost = 0
    winable= 0
    for machine in machines: 
        sol = solve(machine)
        if sol is not None:
            winable += 1
            
            cost += np.dot(sol, costs)
        # break
    print(f"a: {cost}")
    print(f"a: winable {winable}")

    return cost

def preproc(lines, add_= None): 
    machines = []
    next_machine = {}
    for i, line in enumerate(lines):
        if i%4 == 0: 
            x,y = int(line.split("X+")[-1].split(",")[0]), int(line.split("Y+")[-1])
            next_machine["A"] = (x,y)
        elif i%4 == 1: 
            x,y = int(line.split("X+")[-1].split(",")[0]), int(line.split("Y+")[-1])
            next_machine["B"] = (x,y)
        elif i%4 == 2: 
            x, y = int(line.split("X=")[-1].split(",")[0]), int(line.split("Y=")[-1])
            if add_: 
                x,y = add_ + x, add_ + y
            next_machine["P"] = x,y
        else: 
            machines.append(next_machine)
            next_machine = {}
    machines.append(next_machine)
    print(f"using {len(machines) }")
    return machines

        
        

if __name__ == "__main__":
    lines = read_data()
    machines = preproc(lines)
    solvea(machines)
    machinesb = preproc(lines, add_ = 10000000000000)
    solvea(machinesb)