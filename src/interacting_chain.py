"""Real: Hubbard-like interacting chain, 2 particles exact diag"""
import numpy as np, itertools
PHI = (1+5**0.5)/2
L=6 # small for exact diag, 2 particles
t=PHI

def basis_2p(L):
    return list(itertools.combinations(range(L),2))

def hamiltonian_2p(L=L, t=t, U=1.0, V=0.0):
    basis = basis_2p(L)
    dim = len(basis)
    H = np.zeros((dim,dim), dtype=float)
    idx = {b:i for i,b in enumerate(basis)}
    for i,b in enumerate(basis):
        # on-site interaction if same site not allowed (fermions), use nearest neighbor V
        n1,n2 = b
        if abs(n1-n2)==1:
            H[i,i] += V
        # hopping
        for p in range(2):
            for d in [-1,1]:
                new_pos = b[p]+d
                if 0 <= new_pos < L and new_pos not in b:
                    new_b = tuple(sorted([new_pos, b[1-p]]))
                    j = idx.get(new_b)
                    if j is not None:
                        H[i,j] -= t
    return H, basis

if __name__ == "__main__":
    H, _ = hamiltonian_2p(L=6, t=PHI, V=1.0)
    vals = np.linalg.eigvalsh(H)
    print(f"2-particle L=6 t=phi V=1 spectrum: {vals.round(3).tolist()}")
    print(f"ground E={vals[0]:.4f} gap={vals[1]-vals[0]:.4f}")
