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
    A = np.array([[machine["A"][0], machine["B"][0]],[machine["A"][1], machine["B"][1]]])
    b = np.array([machine["P"][0], machine["P"][1]])
    sol = np.linalg.solve(A,b)
    if all([abs(int(x) - x) < prec for x in sol]): 
        if sol[0]>100 or sol[1]>100: 
            print("too big heast")
        # print(machine)
        return sol
    return None
    # eq 1: A * X_A + B * X_B = X
    # eq 2: A * Y_A + B * Y_B = Y
    # min -> 3*A+B
    
def solvea(machines): 
    cost = 0
    winable= 0
    for machine in machines: 
        sol = solve(machine)
        if sol is not None:
            winable += 1
            
            cost += np.dot(sol, costs)
        break
    print(f"a: {cost}")
    print(f"a: winable {winable}")

    return cost

def preproc(lines): 
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