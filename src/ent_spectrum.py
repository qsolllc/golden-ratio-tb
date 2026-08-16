"""Entanglement spectrum + L=89 scaling"""
import numpy as np
PHI=(1+5**0.5)/2

def ham(L, lam):
    H=np.zeros((L,L))
    for i in range(L-1):
        H[i,i+1]=H[i+1,i]=-1.0
    for i in range(L):
        H[i,i]=lam*np.cos(2*np.pi*PHI*i)
    return H

def ipr(psi): return float(np.sum(np.abs(psi)**4))

print("=== L=89 SCALING ===")
for L in [55,89]:
    for lam in [0.5,2.0,2.5]:
        w,v=np.linalg.eigh(ham(L,lam))
        print(f"L={L} lam={lam} <IPR>={np.mean([ipr(v[:,i]) for i in range(L)]):.5f}")

print("\n=== ENTANGLEMENT SPECTRUM lam=0.5 L=21 ===")
# free fermion entanglement from correlation matrix
L=21
H=ham(L,0.5)
vals,vecs=np.linalg.eigh(H)
# ground state: fill lower half
Nf=L//2
C=vecs[:,:Nf] @ vecs[:,:Nf].T
for cut in [7,10]:
    Csub=C[:cut,:cut]
    ev=np.linalg.eigvalsh(Csub)
    ev=np.clip(ev,1e-12,1-1e-12)
    ent=np.sort(-ev*np.log(ev)-(1-ev)*np.log(1-ev))[-5:] # top 5
    print(f"cut={cut} S={float(np.sum(-ev*np.log(ev)-(1-ev)*np.log(1-ev))):.4f} spectrum top5={ent}")
