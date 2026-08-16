"""Entanglement spectrum for bipartition of tight-binding chain"""
import numpy as np
from tight_binding_hamiltonian import TightBindingState, DIM, GOLDEN_RATIO

def reduced_density_matrix(psi, keep_sites):
    """Trace out complement, keep first keep_sites"""
    dim = len(psi)
    # For pure state |psi>, construct rho_A via SVD-like bipartition
    # Simple: reshape psi as matrix if we treat as product (approx for chain)
    # Here: proper reduced DM for cut after keep_sites via outer product trace
    psi = psi / np.linalg.norm(psi)
    # Use projector onto kept subspace
    rho = np.outer(psi, psi.conj())
    # Partition
    dA = keep_sites
    dB = dim - keep_sites
    # Trace over B
    rho_A = np.zeros((dA, dA), dtype=complex)
    for i in range(dA):
        for j in range(dA):
            # sum over B basis
            rho_A[i,j] = np.sum([rho[i + k*dA if False else i, j] if k==0 else 0 for k in range(1)]) # simplified
    # Better: use pure state Schmidt via SVD of reshaped psi for chain mapping
    # For 19 sites as 1D, we do naive cut in Hilbert space (not Fock) - entanglement of mode
    # Correct method: entanglement of site vs rest for single particle
    # For single particle state, rho_A diagonal = |psi_i|^2 for i in A, plus coherence
    rho_A = np.zeros((dA, dA), dtype=complex)
    prob_B = np.sum(np.abs(psi[dA:])**2)
    for i in range(dA):
        for j in range(dA):
            rho_A[i,j] = psi[i]*np.conj(psi[j])
    # Normalize conditional on A
    # Add prob_B as separate eigenvalue for B sector
    vals = np.linalg.eigvalsh(rho_A)
    vals = np.append(vals, prob_B)
    vals = vals[vals>1e-15]
    vals /= np.sum(vals)
    return vals

def entanglement_spectrum(psi, cut):
    vals = reduced_density_matrix(psi, cut)
    # Schmidt values lambda_i, entanglement energies xi_i = -log(lambda_i)
    lambdas = np.sqrt(vals)
    xi = -np.log(vals)
    entropy = -np.sum(vals*np.log(vals))
    return {"eigenvalues": vals.tolist(), "schmidt": lambdas.tolist(), "entanglement_energies": xi.tolist(), "entropy": float(entropy)}

if __name__ == "__main__":
    state = TightBindingState(DIM)
    state.unitary_evolution(0.5)
    for cut in [5,9,14]:
        spec = entanglement_spectrum(state.psi, cut)
        print(f"cut={cut} S={spec['entropy']:.4f} eigenvalues={spec['eigenvalues'][:3]}...")
