"""Deep: level stats, Fibonacci scaling, entanglement curve - no scipy"""
import numpy as np
PHI = (1+5**0.5)/2

def ham(L, lam, phi=0.0):
    H = np.zeros((L,L))
    for i in range(L-1):
        H[i,i+1]=H[i+1,i]=-1.0
    for i in range(L):
        H[i,i]=lam*np.cos(2*np.pi*PHI*i+phi)
    return H

def ipr(psi): return float(np.sum(np.abs(psi)**4))

def level_ratio(vals):
    d = np.diff(np.sort(vals))
    d = d[d>1e-12]
    r = [min(d[i],d[i+1])/max(d[i],d[i+1]) for i in range(len(d)-1)]
    return float(np.mean(r)) if r else 0.0

print("=== LEVEL RATIO <r> ===")
for lam in [0.5,2.0,2.5]:
    vals = np.linalg.eigvalsh(ham(21, lam))
    print(f"lam={lam} <r>={level_ratio(vals):.4f} {'POISSON ~0.386 localized' if level_ratio(vals)<0.45 else 'GOE ~0.53 extended'}")

print("\n=== FIBONACCI SCALING <IPR> ===")
for L in [13,21,34,55]:
    mean_iprs=[]
    for lam in [0.5,2.0,2.5]:
        vals,vecs = np.linalg.eigh(ham(L, lam))
        iprs=[ipr(vecs[:,i]) for i in range(L)]
        mean_iprs.append(np.mean(iprs))
    print(f"L={L} <IPR> lam0.5={mean_iprs[0]:.4f} lam2.0={mean_iprs[1]:.4f} lam2.5={mean_iprs[2]:.4f}")

print("\n=== ENTANGLEMENT vs CUT (lam=0.5) ===")
# quick entanglement from ground state
for L in [21]:
    H=ham(L,0.5)
    vals,vecs=np.linalg.eigh(H)
    psi0=vecs[:,0]
    for cut in [5,7,10,14]:
        # Schmidt from free fermion? approximate via participation
        rho = np.outer(psi0[:cut], psi0[:cut].conj())
        # trace out? simplified
        eig = np.linalg.eigvalsh(rho)
        eig=eig[eig>1e-12]
        S=-np.sum(eig*np.log(eig)) if len(eig) else 0
        print(f"L={L} cut={cut} S~{S:.4f}")
