"""Two-point correlation C(i,j)=<c_i^dag c_j> and density"""
import numpy as np
from tight_binding_hamiltonian import TightBindingState, DIM

def correlations(psi):
    psi = psi/np.linalg.norm(psi)
    rho = np.outer(psi, psi.conj())
    density = np.real(np.diag(rho))
    corr = np.abs(rho)
    return density, corr

if __name__ == "__main__":
    import json
    from pathlib import Path
    state = TightBindingState(DIM)
    state.unitary_evolution(0.8)
    density, corr = correlations(state.psi)
    print(f"density: {density.round(3).tolist()}")
    print(f"C(0,1)={corr[0,1]:.4f} C(0,9)={corr[0,9]:.4f}")
    # save heatmap data
    out = Path.home() / "golden-ratio-tb/data/correlations.json"
    out.write_text(json.dumps({"density": density.tolist(), "correlation_matrix": corr.tolist()}, indent=2))
    print(f"saved {out}")
