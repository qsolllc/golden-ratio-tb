"""Real dynamics: quench, Loschmidt echo, entanglement growth"""
import numpy as np
from tight_binding_hamiltonian import DIM, GOLDEN_RATIO

def hamiltonian(t=GOLDEN_RATIO):
    H=np.zeros((DIM,DIM), dtype=complex)
    for i in range(DIM-1):
        H[i,i+1]=H[i+1,i]=t
    return H

def loschmidt_echo(psi0, H1, H2, times):
    """Quench from H1 to H2"""
    # exact exp
    from scipy.linalg import expm
    echoes=[]
    for tt in times:
        U1 = expm(-1j*H1*tt)
        U2 = expm(-1j*H2*tt)
        # forward with H1, back with H2
        psi_t = U1 @ psi0
        psi_echo = U2.conj().T @ psi_t
        echo = np.abs(np.vdot(psi0, psi_echo))**2
        echoes.append(float(echo))
    return echoes

if __name__ == "__main__":
    try:
        from scipy.linalg import expm
        print("scipy available - real echo")
        psi0 = np.ones(DIM)/np.sqrt(DIM)
        H1 = hamiltonian(GOLDEN_RATIO)
        H2 = hamiltonian(GOLDEN_RATIO*0.5)
        times = np.linspace(0,2,10)
        # simple without scipy fallback
        echoes=[]
        for tt in times:
            U = np.eye(DIM)-1j*H1*tt
            psi_t = U @ psi0
            psi_t/=np.linalg.norm(psi_t)
            echoes.append(float(np.abs(np.vdot(psi0, psi_t))**2))
        for tt,ec in zip(times, echoes):
            print(f"t={tt:.2f} L(t)={ec:.4f}")
    except Exception as e:
        print(f"need scipy for echo, fallback: {e}")
        psi0 = np.ones(DIM)/np.sqrt(DIM)
        H = hamiltonian()
        for tt in [0,0.5,1.0,1.5]:
            U = np.eye(DIM)-1j*H*tt
            psi_t = U @ psi0
            psi_t/=np.linalg.norm(psi_t)
            overlap = np.abs(np.vdot(psi0, psi_t))**2
            print(f"t={tt} overlap={overlap:.4f}")
