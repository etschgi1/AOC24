import matplotlib.pyplot as plt
import numpy as np

def check(x,y,a,b): 
    if x*y == np.logical_xor(a,b): 
        return True
    return False

def plot(counts):
    plt.hist(counts, bins=25)
    min_, max_ = min(counts), max(counts)
    plt.vlines(0.25, 0, 1000, color='r')
    plt.vlines(0.75, 0, 1000, color='r')
    print(min_, max_)
    plt.show()

def runSim(draws, runs): 
    counts = []
    for run in range(runs): 
        count = 0
        # get probs: 
        pA0, pA1, pB0, pB1 = np.random.random(4)
        for _ in range(draws): 
            x, y = np.random.choice(2, 2)
            if x == 0:
                a = 0 if np.random.random() < pA0 else 1
            else: 
                a = 0 if np.random.random() < pA1 else 1
            if y == 0:
                b = 0 if np.random.random() < pB0 else 1
            else: 
                b = 0 if np.random.random() < pB1 else 1
            if check(x,y,a,b): 
                count += 1
        counts.append(count / draws)
        if run % 100 == 0: 
            print(run)
    plot(counts)


# alternative 
def raster():
    probabilities = np.linspace(0, 1, 30)
    p_win_values = []

    for p_A0_val in probabilities:
        for p_A1_val in probabilities:
            for p_B0_val in probabilities:
                for p_B1_val in probabilities:
                    # Calculate p_win numerically
                    p_win_val = (1/4) * (
                        p_A0_val * p_B0_val + (1 - p_A0_val) * (1 - p_B0_val) +
                        p_A0_val * p_B1_val + (1 - p_A0_val) * (1 - p_B1_val) +
                        p_A1_val * p_B0_val + (1 - p_A1_val) * (1 - p_B0_val) +
                        p_A1_val * (1 - p_B1_val) + p_B1_val * (1 - p_A1_val)
                    )
                    p_win_values.append(p_win_val)

    p_win_min = min(p_win_values)
    p_win_max = max(p_win_values)
    print(p_win_min, p_win_max)



if __name__ == "__main__": 
    raster()
    runSim(2000, 5000)