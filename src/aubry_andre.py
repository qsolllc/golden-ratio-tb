"""Real: Aubry-André model with quasiperiodic potential V_n = λ cos(2π φ n)"""
import numpy as np

PHI = (1+5**0.5)/2
DIM = 19

def hamiltonian_aubry_andre(t=1.0, lam=2.0, phi=0.0):
    H = np.zeros((DIM,DIM), dtype=float)
    for i in range(DIM-1):
        H[i,i+1] = H[i+1,i] = -t
    for i in range(DIM):
        H[i,i] = lam * np.cos(2*np.pi*PHI*i + phi)
    return H

def ipr(psi):
    """Inverse participation ratio - localization diagnostic"""
    psi = psi/np.linalg.norm(psi)
    return float(np.sum(np.abs(psi)**4))

def spectrum(t=1.0, lam=2.0):
    H = hamiltonian_aubry_andre(t, lam)
    vals, vecs = np.linalg.eigh(H)
    iprs = [ipr(vecs[:,i]) for i in range(DIM)]
    return vals, iprs

if __name__ == "__main__":
    for lam in [0.5, 1.5, 2.0, 2.5]:
        vals, iprs = spectrum(lam=lam)
        print(f"lambda={lam} <IPR>={np.mean(iprs):.4f} gap_min={np.min(np.diff(np.sort(vals))):.4f}")
        # lam=2 is critical point for Aubry-André
