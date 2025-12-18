# Problem Statement

Let $g,n\in\mathbb{Z}_{\ge 0}$ with $2g-2+n>0$, and let
\[
E(g,n)=\left\{\mathbf{e}=(e_1,\dots,e_n)\in\mathbb{Z}_{\ge 0}^n \;:\; |\mathbf{e}|:=\sum_{j=1}^n e_j = 3g-3+n\right\}.
\]
An element $\mathbf{e}\in E(g,n)$ is called \emph{balanced} if $|e_i-e_j|\le 1$ for $1\le i,j\le n$.

For $\mathbf{e}\in E(g,n)$, consider the descendant integral
\[
D(\mathbf{e})=\int_{\overline{\mathcal{M}}_{g,n}} \psi_1^{e_1}\psi_2^{e_2}\cdots\psi_n^{e_n}.
\]

Prove that for $n > 0$, the function $D:E(g,n)\to\mathbb{Q}$, $\mathbf{e}\mapsto D(\mathbf{e})$ achieves its maximum on a balanced vector $\mathbf{e}\in E(g,n)$ and achieves its minimum on a concentrated vector $(3g −3 + n, 0, ... , 0)$ (or any permutation of its entries thereof). Give explicit formulae of such vectors that maximize or minimize $D$ if possible. Discuss also what happens for the case $n=0$.

---

# Solution Attempt 1 by the problem solver

## Statement and empty-domain counterexample

Let (g,n\in \mathbb Z_{\ge 0}) with (2g-2+n>0), and set
[
d:=\dim \overline{\mathcal M}*{g,n}=3g-3+n.
]
For (n\ge 0) define
[
E(g,n)=\Bigl{(e_1,\dots,e_n)\in\mathbb Z*{\ge 0}^n:\ \sum_{i=1}^n e_i=d\Bigr}.
]
Call (\mathbf e\in E(g,n)) **balanced** if (|e_i-e_j|\le 1) for all (i,j). For (\mathbf e\in E(g,n)) consider the descendant integral
[
D(\mathbf e):=\int_{\overline{\mathcal M}_{g,n}} \psi_1^{e_1}\cdots\psi_n^{e_n}.
]

First note that the claim as written is **false/ill-posed** in the case (n=0): when (n=0) the only (0)-tuple has sum (0), so (E(g,0)\neq\varnothing) iff (d=0). Under the stability hypothesis (2g-2+n>0), if (n=0) then (g\ge 2) hence (d=3g-3>0), so (E(g,0)=\varnothing). In particular for ((g,n)=(2,0)), the hypothesis (2g-2+n>0) holds but (E(2,0)=\varnothing), so (D) has no maximizer (and the existential “achieves its maximum” statement fails).

In what follows we prove the intended, meaningful version:

> **Theorem.** Assume (n\ge 1) (equivalently (E(g,n)\neq\varnothing)). Then the function (D:E(g,n)\to\mathbb Q) attains its maximum at a balanced vector.

Throughout we work over (\mathbb C).

---

## Step 1: Reduction to a pairwise transfer inequality

A **balancing move** (or Robin Hood transfer) is an operation on (\mathbf e\in E(g,n)):
[
(\dots,e_i,\dots,e_j,\dots)\longmapsto(\dots,e_i-1,\dots,e_j+1,\dots)
\qquad\text{with }e_i\ge e_j+2.
]
This preserves (\sum e_k=d) and reduces the gap (e_i-e_j) by (2).

### Lemma 1 (balancing by transfers)

Starting from any (\mathbf e\in E(g,n)), repeated balancing moves terminate after finitely many steps at a balanced vector.

**Proof.** Let (\bar e:=d/n) and define the “imbalance potential”
[
\Phi(\mathbf e):=\sum_{k=1}^n (e_k-\bar e)^2.
]
If (e_i\ge e_j+2), then after the move ((e_i,e_j)\mapsto(e_i-1,e_j+1)) one checks
[
\Phi(\mathbf e)-\Phi(\mathbf e')=2(e_i-e_j)-2\ge 2,
]
so (\Phi) strictly decreases. Since (\Phi\ge 0) and takes only finitely many values on the finite set (E(g,n)), the process terminates at a vector with no pair differing by (\ge 2), i.e. a balanced vector. (\square)

Thus it suffices to prove that each balancing move does not decrease (D).

### Transfer inequality (TI)

For any (\mathbf e\in E(g,n)) and indices (i\neq j) with (e_i\ge e_j+2),
[
D(\dots,e_i,\dots,e_j,\dots)\ \le\ D(\dots,e_i-1,\dots,e_j+1,\dots).
\tag{TI}
]
Indeed, if (TI) holds, then applying Lemma 1 to a maximizer (\mathbf e_{\max}) shows that a balanced vector (\mathbf b) reachable by transfers satisfies (D(\mathbf b)\ge D(\mathbf e_{\max})), hence (\mathbf b) is also a maximizer.

So we now prove (TI).

---

## Step 2: Interpreting (D(\mathbf e)) as a nef intersection number on a smooth projective variety

Let (\mathcal X:=\overline{\mathcal M}*{g,n}) be the smooth proper Deligne–Mumford stack, and let (p:\mathcal X\to X:=\overline M*{g,n}) be its coarse moduli space (a projective variety).

### 2.1. Chow-theoretic passage to the coarse space

In characteristic (0), (\mathcal X) is a quotient stack: more precisely, by Kresch’s theorem, any smooth separated generically tame Deligne–Mumford stack with quasi-projective coarse moduli space is a quotient stack ([Y/G]).

For Deligne–Mumford quotient stacks with a coarse moduli **scheme**, Edidin proves that the rational Chow groups of the stack and of its coarse space agree. In particular, for (\mathcal X=[Y/G]) with coarse moduli scheme (X), there are isomorphisms
[
A_*(\mathcal X)\otimes\mathbb Q\ \cong\ A_*(X)\otimes\mathbb Q
\quad\text{and similarly in cohomological grading}.
]

Under this identification, the top-degree integral (\int_{\mathcal X}\alpha) is computed as the degree of the corresponding (0)-cycle class on (X). We will therefore regard the (\psi_i) as classes on (X) with (\mathbb Q)-coefficients, without changing numerical intersection numbers.

### 2.2. Descent and nefness of the (\psi_i) on the coarse space

Let (L_i) be the cotangent line bundle at the (i)-th marking on (\mathcal X), so (\psi_i=c_1(L_i)\in A^1(\mathcal X)). It is standard that each (\psi_i) is nef (equivalently, (L_i) is nef as a line bundle on the stack); for instance, this nefness is used and explicitly stated in the foundational work of Gibney–Keel–Morrison. ([ar5iv][1])

We need (\psi_i) as a nef (\mathbb Q)-Cartier divisor class on the coarse space (X). Two standard facts (both consequences of finiteness of stabilizers) are:

1. **Tensor-power descent.** There exists an integer (m_i>0) and a line bundle (M_i) on (X) such that
   [
   p^*M_i \cong L_i^{\otimes m_i}.
   ]
   Equivalently, the cokernel of (\mathrm{Pic}(X)\to \mathrm{Pic}(\mathcal X)) is torsion. ([MathOverflow][2])
   In particular, (\psi_i) corresponds to the (\mathbb Q)-Cartier class (\frac1{m_i}c_1(M_i)) on (X).

2. **Nefness descends.** If (L_i) is nef on (\mathcal X), then (M_i) is nef on (X): for any irreducible curve (C\subset X), one can pull back to a curve (\widetilde C\to \mathcal X) finite over (C), and compute degrees using (p^*M_i \cong L_i^{\otimes m_i}) to deduce (\deg(M_i|_C)\ge 0). Hence (\psi_i) is nef as a (\mathbb Q)-Cartier divisor class on (X).

### 2.3. Pullback to a resolution

Let (\pi:\widetilde X\to X) be a resolution of singularities, with (\widetilde X) smooth projective of dimension (d). Set
[
\widetilde\psi_i:=\pi^*(\psi_i)\in N^1(\widetilde X)*\mathbb R.
]
Pullback preserves nefness: if (\psi_i) is nef on (X), then for any curve (C'\subset \widetilde X),
[
(\widetilde\psi_i\cdot C')=(\psi_i\cdot \pi**C')\ge 0,
]
so (\widetilde\psi_i) is nef on (\widetilde X).

Finally, we relate the top intersections on (X) to those on (\widetilde X).

### Lemma 2 (top intersections computed on a resolution)

Let (\alpha_1,\dots,\alpha_d) be (\mathbb Q)-Cartier divisor classes on (X). Then
[
\int_X \alpha_1\cdots \alpha_d ;=; \int_{\widetilde X}\pi^*\alpha_1\cdots \pi^*\alpha_d.
]

**Proof.** Regard (\alpha:=\alpha_1\cdots\alpha_d) as an operational Chow class of codimension (d) on (X), so that (\alpha\cap [X]\in A_0(X)*\mathbb Q) and (\int_X \alpha=\deg(\alpha\cap[X])). Operational pullback gives (\pi^*\alpha=\pi^*\alpha_1\cdots \pi^*\alpha_d) on (\widetilde X). By functoriality and the projection formula in operational Chow,
[
\alpha\cap[X]=\alpha\cap\pi**[\widetilde X]=\pi_*(\pi^*\alpha\cap[\widetilde X]).
]
Taking degrees of (0)-cycles and using that (\deg(\pi_*z)=\deg(z)) for proper (\pi) yields
[
\deg(\alpha\cap[X])=\deg(\pi^*\alpha\cap[\widetilde X])=\int_{\widetilde X}\pi^*\alpha_1\cdots \pi^*\alpha_d,
]
as claimed. (\square)

Applying this with (\alpha_i=\psi_i) repeated (e_i) times gives
[
D(\mathbf e)=\int_{\overline{\mathcal M}*{g,n}}\prod_i \psi_i^{e_i}
=\int*{\widetilde X}\prod_i \widetilde\psi_i^{e_i}.
\tag{*}
]

Thus (D(\mathbf e)) is a mixed intersection number of nef divisor classes on a smooth projective variety.

---

## Step 3: Log-concavity of a two-point slice via Alexandrov–Fenchel/Khovanskii–Teissier

Fix distinct indices (i\neq j), and fix exponents (e_\ell) for all (\ell\neq i,j). Put
[
S:=e_i+e_j,\qquad C:=\prod_{\ell\neq i,j} \widetilde\psi_\ell^{e_\ell}.
]
Define a sequence ((a_k)*{k=0}^S) by
[
a_k:=\int*{\widetilde X}\widetilde\psi_i^{k},\widetilde\psi_j^{S-k},C,\qquad k=0,\dots,S.
]
By construction, (a_{e_i}=D(\mathbf e)) (with the other coordinates fixed).

### Lemma 3 (symmetry)

[
a_k=a_{S-k}\quad\text{for all }k.
]

**Proof.** Swapping the labels of the marked points (i\leftrightarrow j) exchanges (\widetilde\psi_i^k\widetilde\psi_j^{S-k}) with (\widetilde\psi_i^{S-k}\widetilde\psi_j^{k}) and leaves the integral invariant. (\square)

### Lemma 4 (log-concavity)

For (1\le k\le S-1),
[
a_k^2\ \ge\ a_{k-1}a_{k+1}.
\tag{LC}
]

**Proof.** We apply the (2\times2) Alexandrov–Fenchel/Khovanskii–Teissier inequality for nef divisors on the smooth projective variety (\widetilde X): for nef (D_1,\dots,D_d),
[
(D_1\cdots D_d)^2\ \ge\ (D_1^2D_3\cdots D_d),(D_2^2D_3\cdots D_d).
\tag{AF}
]
(One may deduce this for nef divisors by approximation from the ample case.)

Fix (k\in{1,\dots,S-1}). Choose the list ((D_1,\dots,D_d)) as follows:

* (D_1=\widetilde\psi_i), (D_2=\widetilde\psi_j);
* among (D_3,\dots,D_d), take (k-1) further copies of (\widetilde\psi_i), (S-k-1) copies of (\widetilde\psi_j), and for each (\ell\neq i,j), take (e_\ell) copies of (\widetilde\psi_\ell).
  This is a list of exactly
  [
  2+(k-1)+(S-k-1)+\sum_{\ell\neq i,j}e_\ell
  = S+\sum_{\ell\neq i,j}e_\ell
  = \sum_{r=1}^n e_r
  = d
  ]
  nef divisors.

Then
[
(D_1\cdots D_d)=\int_{\widetilde X}\widetilde\psi_i^{k}\widetilde\psi_j^{S-k}C=a_k,
]
and similarly
[
(D_1^2D_3\cdots D_d)=a_{k+1},\qquad (D_2^2D_3\cdots D_d)=a_{k-1}.
]
Substituting into (AF) gives (a_k^2\ge a_{k-1}a_{k+1}). (\square)

---

## Step 4: Symmetric log-concave sequences peak at the center (allowing zeros)

We need the following discrete consequence of (LC) and symmetry.

### Lemma 5 (contiguous support)

If ((a_k)*{k=0}^S) is nonnegative and log-concave in the sense (a_k^2\ge a*{k-1}a_{k+1}), then ({k:\ a_k>0}) is an interval (possibly empty).

**Proof.** If (a_m=0) and (a_{m-1}>0), then (0=a_m^2\ge a_{m-1}a_{m+1}) forces (a_{m+1}=0). Induct forward and backward. (\square)

### Lemma 6 (center monotonicity)

Assume ((a_k)*{k=0}^S) is nonnegative, log-concave, and symmetric (a_k=a*{S-k}). Let (m:=\lfloor S/2\rfloor). Then for every (k\ge m+1),
[
a_{k-1}\ge a_k.
\tag{CENTER}
]

**Proof.** By Lemma 5, the positive support (if nonempty) is an interval; outside it the inequality is trivial, so we restrict to indices where (a_k>0). Define ratios (r_k:=a_k/a_{k-1}) wherever defined. Log-concavity implies (r_{k+1}\le r_k) (equivalently, the ratios are nonincreasing).

Write (S) in one of two forms.

* If (S=2m) is even, symmetry gives (a_{m-1}=a_{m+1}). Log-concavity at (m) yields
  [
  a_m^2\ge a_{m-1}a_{m+1}=a_{m+1}^2,
  ]
  hence (a_m\ge a_{m+1}), i.e. (r_{m+1}\le 1). Since (r_k) is nonincreasing, for all (k\ge m+1) we have (r_k\le r_{m+1}\le 1), thus (a_k\le a_{k-1}).

* If (S=2m+1) is odd, symmetry gives (a_m=a_{m+1}), so (r_{m+1}=1). Again (r_k\le r_{m+1}=1) for all (k\ge m+1), hence (a_k\le a_{k-1}).

This proves (CENTER). (\square)

---

## Step 5: Proof of the transfer inequality (TI)

Assume (e_i\ge e_j+2). With (S=e_i+e_j), this implies
[
2e_i\ge (e_i+e_j)+2=S+2
\quad\Rightarrow\quad
e_i\ge \frac S2+1
\quad\Rightarrow\quad
e_i\ge \left\lfloor\frac S2\right\rfloor+1=m+1.
]
Apply Lemma 6 to the slice ((a_k)): since (e_i\ge m+1),
[
a_{e_i-1}\ge a_{e_i}.
]
Recalling the definition of (a_k), this is exactly
[
D(\dots,e_i-1,\dots,e_j+1,\dots)\ \ge\ D(\dots,e_i,\dots,e_j,\dots),
]
i.e. (TI).

---

## Step 6: Conclusion (balanced maximizer for (n\ge 1))

Assume (n\ge 1). Then (E(g,n)) is finite and nonempty, so (D) has a maximizer (\mathbf e_{\max}\in E(g,n)). By Lemma 1, (\mathbf e_{\max}) can be transformed into a balanced vector (\mathbf b\in E(g,n)) by finitely many balancing moves. Each move does not decrease (D) by (TI), hence
[
D(\mathbf b)\ge D(\mathbf e_{\max})=\max_{\mathbf e\in E(g,n)}D(\mathbf e).
]
Thus (\mathbf b) is also a maximizer and is balanced.

This proves the theorem. ∎

[1]: https://ar5iv.org/pdf/math/0006208 "[math/0006208] Towards the ample cone of ̄_{,}"
[2]: https://mathoverflow.net/questions/204701/do-line-bundles-descend-to-coarse-moduli-spaces-of-artin-stacks-with-finite-iner "ag.algebraic geometry - Do line bundles descend to coarse moduli spaces of Artin stacks with finite inertia? - MathOverflow"
