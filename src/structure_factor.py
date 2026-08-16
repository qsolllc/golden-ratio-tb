"""Structure factor S(k) = (1/N) sum_{ij} e^{ik(i-j)} C_{ij}"""
import numpy as np
from tight_binding_hamiltonian import TightBindingState, DIM

def structure_factor(corr_matrix):
    N = corr_matrix.shape[0]
    ks = np.linspace(0, 2*np.pi, 100)
    Sk = []
    for k in ks:
        s = 0j
        for i in range(N):
            for j in range(N):
                s += np.exp(1j*k*(i-j))*corr_matrix[i,j]
        Sk.append(float(np.real(s)/N))
    return ks.tolist(), Sk

if __name__ == "__main__":
    state = TightBindingState(DIM)
    state.unitary_evolution(1.0)
    rho = np.outer(state.psi, state.psi.conj())
    ks, Sk = structure_factor(np.abs(rho))
    print(f"S(k=0)={Sk[0]:.3f} S(k=pi)={Sk[50]:.3f}")
