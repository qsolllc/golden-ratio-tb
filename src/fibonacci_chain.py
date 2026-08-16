"""Clean rename of vortex_core.py — topological Fibonacci chain"""
import numpy as np
PHI = (1+5**0.5)/2
GOLDEN_ANGLE = np.pi*(3-5**0.5)
FIB_RUNGS = np.array([-8,-5,-3,-2,-1,0,1,2,3,5,8])
DIM=19

class GoldenChainState:
    def __init__(self, dim=DIM):
        self.dim=dim
        self.psi=np.ones(dim,dtype=complex)/np.sqrt(dim)
    def hamiltonian(self):
        H=np.zeros((self.dim,self.dim),dtype=complex)
        for i in range(self.dim-1):
            H[i,i+1]=H[i+1,i]=PHI
        return H
    def purity(self):
        rho=np.outer(self.psi,self.psi.conj())
        return float(np.real(np.trace(rho@rho)))
