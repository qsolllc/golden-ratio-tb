import numpy as np
try:
    from scipy.linalg import expm
except:
    expm = None

GOLDEN_RATIO = (1 + 5**0.5)/2
DIM = 19

class TightBindingState:
    def __init__(self, dim=DIM):
        self.dim = dim
        self.psi = np.ones(dim, dtype=complex) / np.sqrt(dim)
    def unitary_evolution(self, dt=0.1):
        H = np.zeros((self.dim, self.dim), dtype=complex)
        for i in range(self.dim-1):
            H[i,i+1] = GOLDEN_RATIO
            H[i+1,i] = GOLDEN_RATIO
        U = expm(-1j*H*dt) if expm is not None else np.eye(self.dim)-1j*H*dt
        self.psi = U @ self.psi
        self.psi /= np.linalg.norm(self.psi)
        return self
    def apply_decoherence_channel(self, pressure=0.05):
        rho = np.outer(self.psi, self.psi.conj())
        rho = (1-pressure)*rho + pressure*np.eye(self.dim)/self.dim
        vals, vecs = np.linalg.eigh(rho)
        self.psi = vecs[:,-1]
        self.psi /= np.linalg.norm(self.psi)
        return self
    def purity(self):
        rho = np.outer(self.psi, self.psi.conj())
        return float(np.real(np.trace(rho@rho)))
    def von_neumann_entropy(self):
        rho = np.outer(self.psi, self.psi.conj())
        vals = np.linalg.eigvalsh(rho)
        vals = vals[vals>1e-12]
        return float(-np.sum(vals*np.log(vals)))
