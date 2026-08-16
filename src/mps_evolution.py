"""MPS-like time evolution via Trotter (no external deps)"""
import numpy as np
from tight_binding_hamiltonian import DIM, GOLDEN_RATIO

class SimpleMPS:
    def __init__(self, dim=DIM):
        self.dim=dim
        self.psi=np.ones(dim, dtype=complex)/np.sqrt(dim)
        self.t=GOLDEN_RATIO
    def trotter_step(self, dt):
        # First order Trotter for nearest neighbor hopping
        # Apply bond gates exp(-i t dt (|i><i+1|+h.c.))
        new_psi = self.psi.copy()
        for i in range(self.dim-1):
            # 2x2 block
            H2 = np.array([[0, self.t],[self.t,0]], dtype=complex)
            U2 = np.eye(2, dtype=complex) - 1j*H2*dt # linear approx, no scipy needed
            # orthonormalize approx
            v = np.array([self.psi[i], self.psi[i+1]], dtype=complex)
            v2 = U2 @ v
            new_psi[i] = v2[0]
            new_psi[i+1] = v2[1]
        self.psi = new_psi/np.linalg.norm(new_psi)
        return self.psi
    def run(self, steps=20, dt=0.1):
        purities=[]
        for s in range(steps):
            self.trotter_step(dt)
            rho=np.outer(self.psi, self.psi.conj())
            pur = float(np.real(np.trace(rho@rho)))
            purities.append(pur)
            if s%5==0:
                print(f"mps step {s} purity {pur:.6f}")
        return purities

if __name__ == "__main__":
    mps=SimpleMPS()
    mps.run(20,0.1)
