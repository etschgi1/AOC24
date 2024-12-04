import numpy as np

# Define the matrices for the gates
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])

X = np.array([
    [0, 1],
    [1, 0]
])

I = np.eye(2)

# Tensor products for the gates
I_tensor_X = np.kron(I, X)  # (I ⊗ X)
X_tensor_I = np.kron(X, I)  # (X ⊗ I)

# Circuit 1: CNOT * (I ⊗ X)
CIRCUIT_1 = CNOT @ I_tensor_X

# Circuit 2: (I ⊗ X) * (X ⊗ I) * CNOT
CIRCUIT_2 = CNOT @ X_tensor_I @ I_tensor_X 

# Print the results for both circuits
print(CIRCUIT_1)
print(CIRCUIT_2)
