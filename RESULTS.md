# Results — Golden-Ratio Tight-Binding

## 1. Aubry-André localization (19 sites, t=1)
V_n = λ cos(2π φ n), φ=golden ratio

| λ | <IPR> | min gap | phase |
|---|---|---|---|
| 0.5 | 0.0934 | 0.0708 | extended |
| 1.5 | 0.1835 | 0.0477 | extended |
| 2.0 | 0.3156 | 0.0243 | critical |
| 2.5 | 0.5155 | 0.0030 | localized |

IPR = Σ|ψ|⁴. At λ=2, IPR doubles — metal-insulator transition. Textbook Aubry-André.

## 2. Interacting 2-particle chain L=6, t=φ=1.618, V=1
Ground state E0 = -4.8299
Gap Δ = 1.3826
Full spectrum 15 levels: -4.83 to 5.089

Shows interaction lifts degeneracy, opens gap.

## 3. Time evolution (19 sites, t=φ)
Purity Tr(ρ²)=1.0, S_vN~0 preserved over 10 steps dt=0.15
Hash chain sha3-512:2bffb...

## 4. Entanglement bipartition
Cut 5: S_A=0.5610 λ=[0.248,0.751]
Cut 9: S_A=0.6916
Cut 14: S_A=0.5610
Symmetric — correct for pure state.

## 5. Correlations
Density n_i ≈ 0.057 interior, 0.02 edges
C(0,1)=0.0333, C(0,9)=0.0333 — long-range coherence

## 6. Structure factor
S(k=0)=0.980 S(k=π)=0.000 — uniform mode dominates

## 7. Provenance
Archive: 77caec2c4df2cf7d2cf2a6071eb0d8154a4ee4e9b890d9164d1f51acff369e1d6b391d0bd1179309aff02ab985e62b67a835e75fa9536222de1f3f77104d22ed
Dataset hash: sha3-512:2bffb073...

## How to cite
Tight-binding chain with golden-ratio hopping, Aubry-André potential V_n=λ cos(2π φ n), IPR localization, 2-particle exact diag, hash-chained data.

## Deep analysis (Aug 16, Termux)

### Level spacing ratio <r>
- lam=0.5: 0.7242 GOE-like extended
- lam=2.0: 0.3529 Poisson critical/localized
- lam=2.5: 0.4221 Poisson localized

### Fibonacci finite-size scaling <IPR>
| L | lam0.5 | lam2.0 | lam2.5 |
| 13 | 0.1248 | 0.3406 | 0.5283 |
| 21 | 0.0804 | 0.2675 | 0.4703 |
| 34 | 0.0508 | 0.2234 | 0.4498 |
| 55 | 0.0323 | 0.1746 | 0.4418 |
Extended ~1/L collapse, localized ~const

### Chain provenance
- STITCH-0000 genesis_hash aa94d42b...
- POCATELLO 46/45 stitches E0=0.15, final anchor 42e34f88

## L=89 + Entanglement (Aug 16)
### Scaling to L=89
- L=55 lam0.5 0.03232 -> L=89 0.02038 extended 1/L
- L=55 lam2.5 0.44176 -> L=89 0.43331 localized const

### Entanglement spectrum L=21 lam0.5 ground state Nf=10
- cut7 S=0.8053 top eigenvalue 0.613
- cut10 S=0.7680 top eigenvalue 0.556
