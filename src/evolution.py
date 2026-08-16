from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from tight_binding_hamiltonian import TightBindingState, GOLDEN_RATIO, DIM
from jcs_rfc8785 import canonicalize
from hash_commitment import hash_bytes
import json

state = TightBindingState(dim=DIM)
print(f"Tight-binding: sites={DIM}, t={GOLDEN_RATIO}")

records=[]
for step in range(10):
    state.unitary_evolution(dt=0.15)
    state.apply_decoherence_channel(pressure=0.05)
    r = {"step": step, "purity": state.purity(), "von_neumann_entropy": state.von_neumann_entropy()}
    r["sha3_512"] = hash_bytes(canonicalize(r))
    records.append(r)
    print(f"step {step}: Tr(rho^2)={r['purity']:.6f} S={r['von_neumann_entropy']:.6f}")

dataset = {"model": "tight_binding_golden_hopping", "hamiltonian": "H = t * sum_i (|i><i+1| + h.c.), t=phi", "sites": DIM, "hopping": GOLDEN_RATIO, "data": records}
print(f"hash {hash_bytes(canonicalize(dataset))[:32]}...")
Path("~/golden-ratio-tb/data/time_evolution.json").expanduser().write_text(json.dumps(dataset, indent=2))
