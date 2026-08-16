# Tight-Binding Model with Golden-Ratio Hopping

## Hamiltonian
H = t Σ_{i} (|i><i+1| + |i+1><i|), t = φ = 1.618033988749895

## Modules (real science)
- `tight_binding_hamiltonian.py` — Hamiltonian, TightBindingState, U=exp(-iHt), purity Tr(ρ²), S_vN
- `evolution.py` — time evolution dt=0.15, depolarizing p=0.05, hash commitment chain
- `entanglement_spectrum.py` — reduced DM, Schmidt values λ, entanglement energies ξ=-log λ, S_A
- `correlation.py` — density n_i = |ψ_i|², C_ij = |ρ_ij|, saves correlations.json
- `mps_evolution.py` — Trotter decomposition, bond gates, no scipy required
- `structure_factor.py` — S(k) = (1/N) Σ e^{ik(i-j)} C_{ij}
- `jcs_rfc8785.py` — RFC8785 canonical JSON
- `hash_commitment.py` — SHA3-512

## Provenance
genesis_v1.tar.gz SHA512: 77caec2c4df2cf7d2cf2a6071eb0d8154a4ee4e9b890d9164d1f51acff369e1d6b391d0bd1179309aff02ab985e62b67a835e75fa9536222de1f3f77104d22ed
Latest dataset hash: see evolution.py output

## Run all
python3 src/evolution.py
python3 src/entanglement_spectrum.py
python3 src/correlation.py
python3 src/mps_evolution.py
python3 src/structure_factor.py
