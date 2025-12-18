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


---

# Expert evaluator's assessment and feedback on Solution Attempt 1

## Status
Status: Partial

## Score
Score (0–100): 55

## Major issues

- **MAJOR-ISSUE-ID-MINIMUM-MISSING**
  - **Severity:** local/patchable  
  - **Location:** Global—problem requirement “achieves its minimum on a concentrated vector …” is not proved  
  - **Issue type:** missing required part / missing conclusion  
  - **Description:** The attempt proves (essentially) that *balancing moves* weakly increase \(D(\mathbf e)\), hence a maximizer can be taken balanced. But it never proves the second half of the problem: that a minimizer occurs at a concentrated vector \((d,0,\dots,0)\) (up to permutation), where \(d=3g-3+n\).  
  - **Suggested direction for fix:** Use the same transfer inequality (TI) to show **Schur-concavity** with respect to majorization, or argue that any \(\mathbf e\) can be reached from \((d,0,\dots,0)\) by a sequence of balancing moves; then (TI) implies
    \[
    D(d,0,\dots,0)\le D(\mathbf e)
    \]
    for all \(\mathbf e\in E(g,n)\). Concretely, you should:
    1. Note that \((d,0,\dots,0)\) **majorizes** every \(\mathbf e\) with sum \(d\).
    2. Recall/quote the standard theorem: \(x\succ y\) iff \(y\) can be obtained from \(x\) by a finite sequence of Robin Hood transfers.
    3. Since (TI) says each Robin Hood transfer increases \(D\), deduce \(D\) is Schur-concave, hence minimum at the majorization-maximal vector \((d,0,\dots,0)\).

- **MAJOR-ISSUE-ID-SYMMETRY-RESOLUTION-GAP**
  - **Severity:** local/patchable  
  - **Location:** Lemma 3 (“symmetry”) and its use in Lemma 6 / Step 5  
  - **Issue type:** logical gap / unjustified invariance claim  
  - **Description:** You define
    \[
    a_k=\int_{\widetilde X}\widetilde\psi_i^{k}\,\widetilde\psi_j^{S-k}\,C
    \]
    on a fixed resolution \(\pi:\widetilde X\to X\). You then claim \(a_k=a_{S-k}\) by “swapping labels \(i\leftrightarrow j\).”  
    The swap \(i\leftrightarrow j\) is an automorphism of \(\overline M_{g,n}\) (or the stack), but your chosen resolution \(\widetilde X\) need not be \(S_n\)-equivariant, so it is not legitimate to assert symmetry directly at the level of \(\widetilde X\) without an argument.
  - **Suggested direction for fix:** Prove symmetry **on the coarse space \(X\)** first:
    \[
    \int_X \psi_i^{k}\psi_j^{S-k}C = \int_X \psi_i^{S-k}\psi_j^{k}C,
    \]
    using \(S_n\)-invariance of intersection numbers on \(X\). Then invoke Lemma 2 to transport equality to \(\widetilde X\). Alternatively, choose an \(S_n\)-equivariant resolution (possible after modifications, but this is heavier than needed).

- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION**
  - **Severity:** local/patchable  
  - **Location:** Step 2.1–2.2 (passage from stack to coarse moduli; descent and nefness)  
  - **Issue type:** missing critical justification / reliance on nonstandard citations  
  - **Description:** The reduction “\(D(\mathbf e)\) is a mixed intersection number of nef divisors on a smooth projective variety” is plausible but not written at the level of rigor you need for an exam-quality solution. In particular:
    1. The claim “\(A_*(\mathcal X)\otimes\mathbb Q \cong A_*(X)\otimes\mathbb Q\)” for the relevant \(\mathcal X=\overline{\mathcal M}_{g,n}\) and its coarse space \(X=\overline M_{g,n}\) needs a precise statement and reference (or at least a correct theorem with hypotheses verified).
    2. The descent of \(L_i^{\otimes m_i}\) and the implication “nef on stack \(\Rightarrow\) nef on coarse moduli” is sketched but not fully justified; citing MathOverflow is not appropriate as a primary reference in a final proof.
  - **Suggested direction for fix:** Either:
    - Replace Step 2.1–2.2 with a clean standard reference: e.g. a theorem that on a smooth DM stack with coarse moduli having only quotient singularities, intersection numbers of line bundles can be computed on the coarse space with \(\mathbb Q\)-coefficients; and that a line bundle descends after a tensor power.  
    **OR**
    - Avoid coarse space entirely: work in the Chow ring of the smooth proper DM stack directly and cite an Alexandrov–Fenchel/Khovanskii–Teissier type inequality available for stacks (if you know a correct reference), or reduce via a global quotient presentation \([Y/G]\) in a way that makes all steps precise.

## Counterexamples / impossible claims (OPTIONAL)

No counterexamples found, no impossible or overly ambitious claims were proposed beyond what is already covered above.  
(Your observation that \(E(g,0)=\varnothing\) under the stated stability hypothesis is correct and important, not a counterexample to your own reasoning.)

## Minor issues

- **Location:** End of the attempt / theorem statement  
  **Nature:** missing “explicit maximizer/minimizer vectors” requested by the problem  
  **Suggestion:** State the explicit balanced vector formula: if \(d=3g-3+n\), write \(d=qn+r\) with \(0\le r<n\). Then balanced vectors are permutations of
  \[
  (\underbrace{q+1,\dots,q+1}_{r\text{ times}},\underbrace{q,\dots,q}_{n-r\text{ times}}).
  \]

- **Location:** Step 3, inequality (AF)  
  **Nature:** slightly imprecise notation (“\((D_1\cdots D_d)^2\ge (D_1^2\cdots)(D_2^2\cdots)\)” without writing intersection numbers explicitly)  
  **Suggestion:** Write it unambiguously as a statement about numbers:
  \[
  (D_1\cdots D_d)^2 \ge (D_1^2D_3\cdots D_d)\,(D_2^2D_3\cdots D_d).
  \]

- **Location:** Step 4  
  **Nature:** the unimodality argument is fine, but you should explicitly note that log-concavity + nonnegativity implies unimodality; you essentially prove it via ratio monotonicity.  
  **Suggestion:** Add a one-line statement: “Hence \((a_k)\) is unimodal with peak at the center.”

- **Location:** n=0 discussion  
  **Nature:** You correctly note ill-posedness, but the problem asks “Discuss what happens.”  
  **Suggestion:** Explicitly state: under \(2g-2+n>0\), \(n=0\Rightarrow g\ge 2\Rightarrow d>0\Rightarrow E(g,0)=\varnothing\), so \(D\) is a function on the empty set; maxima/minima are not defined.

## Established building blocks

- **EBB-ID-TRANSFER-POTENTIAL-LEMMA1**  
  Lemma 1 (balancing moves terminate at a balanced vector) via the strictly decreasing quadratic potential \(\Phi(\mathbf e)\). This is standard, correct, and reusable.

- **EBB-ID-KT-LOGCONCAVITY-SLICE**  
  The two-variable slice \(\{a_k\}\) is log-concave by an Alexandrov–Fenchel/Khovanskii–Teissier inequality for nef divisor classes on a smooth projective variety (after reduction to \(\widetilde X\)). The combinatorial setup in Lemma 4 is correct.

- **EBB-ID-SYMM-LOGCONCAVE-UNIMODAL**  
  Lemmas 5–6: nonnegative log-concave sequences have contiguous support and, combined with symmetry, are monotone away from the center. This discrete argument is correct as a pure sequence lemma (once symmetry is justified in the geometric setup).

## Gap assessment

- **Gap: Minimum at concentrated vector** (not explicitly stated as a gap by the solver, but required by the problem)  
  **Assessment:** Moderate.  
  You already have essentially the key monotonicity tool (TI). The remaining work is to connect TI to majorization / reachability from \((d,0,\dots,0)\), or to prove endpoints are minima along every 2-variable slice and then globalize.

- **Gap: Explicit maximizer/minimizer vectors**  
  **Assessment:** Minor.  
  This is a straightforward number-theory description of balanced distributions (quotient/remainder).

- **Gap: n=0 discussion**  
  **Assessment:** Minor.  
  You already have the key observation; just phrase the conclusion in “max/min on empty domain is undefined” terms.

- **Gap: symmetry on \(\widetilde X\)**  
  **Assessment:** Minor-to-moderate.  
  The fix is short: prove symmetry on \(X\) then pull back. No need for equivariant resolution.

## Coverage assessment

All subparts addressed: **No**.

- **Solved/mostly solved:** Maximum occurs at a balanced vector (for \(n>0\)), modulo the symmetry-on-resolution justification and the stack/coarse-space rigor polishing.
- **Partially handled:** \(n=0\) discussed (correctly notes empty domain), but needs a clearer “so the question is vacuous/undefined” statement.
- **Untouched:** Minimum at concentrated vector and the requested explicit vector formulae.

## Summary

You have a strong and largely correct high-level strategy: interpret \(D(\mathbf e)\) as a mixed intersection number of nef divisor classes and use Alexandrov–Fenchel/Khovanskii–Teissier to obtain log-concavity along 2-variable slices. From that you derive a “Robin Hood transfer increases \(D\)” inequality (TI), which is exactly the right monotonicity principle to force a maximizer to be balanced.

However, the write-up stops after proving the balanced maximizer; it does not establish the claimed minimizer at the concentrated vector, and it does not provide the explicit balanced/concentrated vectors asked for. There is also a technical gap where you claim symmetry \(a_k=a_{S-k}\) at the level of a non-equivariant resolution; this can be fixed but must be fixed. Finally, the stack-to-coarse-space reduction is plausible but currently under-referenced and too reliant on informal sources.

The approach is promising: once you globalize (TI) via majorization, you should get both the maximum and the minimum with essentially no new geometry.

## Recommendations for next iteration (prioritized)

1. **Prove the minimum statement using majorization + (TI).**  
   Write: concentrated \((d,0,\dots,0)\) majorizes every \(\mathbf e\) with sum \(d\), and every \(\mathbf e\) can be obtained from \((d,0,\dots,0)\) by Robin Hood transfers; since each transfer weakly increases \(D\), concentrated is a minimizer.

2. **Fix Lemma 3 rigorously.**  
   Prove symmetry of \(a_k\) on the coarse space \(X\) using the \(S_n\)-action, then invoke Lemma 2 to move to \(\widetilde X\).

3. **State explicit maximizer/minimizer vectors.**  
   Include the quotient–remainder formula \(d=qn+r\) and give the balanced vector with \(r\) entries \(q+1\), \(n-r\) entries \(q\); minimizer is \((d,0,\dots,0)\) up to permutation.

4. **Tighten Step 2 with proper references or simplify it.**  
   Replace MathOverflow and ar5iv with standard literature where possible, or avoid coarse moduli altogether if you can cite AF/KT for stacks or for global quotients \([Y/G]\).

5. **Clarify the \(n=0\) case in the final statement.**  
   Explicitly conclude: under the hypotheses, \(E(g,0)=\varnothing\), so “maximum/minimum” is not defined (or the statement is vacuous depending on conventions).

## Meta-level guidance for both the problem solver and the orchestrator

### Strategy-level assessment
The overall line of attack is **promising and close to complete**, not misguided. The AF/KT log-concavity mechanism is well-matched to the “balanced maximizes” phenomenon.

### Structural blockers
- **MAJOR-ISSUE-ID-MINIMUM-MISSING** is a genuine blocker because the problem explicitly requires the minimizer characterization; without it, the solution is incomplete.
- **MAJOR-ISSUE-ID-SYMMETRY-RESOLUTION-GAP** is a genuine blocker because the transfer inequality (TI) as written depends on symmetry; if symmetry is not justified, the monotonicity chain can fail.

### Dead directions / approaches to abandon
No dead directions are clearly identified. The AF/KT route is not dead; it just needs completion and tightening.

### Promising lines and subproblems
- **Promising:** Globalize (TI) via **majorization / Schur-concavity** to simultaneously conclude both the maximum and minimum claims.
- **Subproblem to isolate:** A clean, citation-backed lemma: “\(\psi_i\) is nef (as a \(\mathbb Q\)-Cartier divisor) on \(\overline M_{g,n}\), and \(D(\mathbf e)\) is the top intersection number of nef divisors on some smooth projective model.” If this is packaged cleanly, the rest is purely convexity/majorization.

### Recommendations for the orchestrator (prioritized)
1. **Treat EBB-ID-TRANSFER-POTENTIAL-LEMMA1 and EBB-ID-KT-LOGCONCAVITY-SLICE as established and reuse them.**
2. **In the next attempt, force the solver to add the majorization step** to obtain the minimum at \((d,0,\dots,0)\) and the explicit maximizer vector formula.
3. **Do not allow the symmetry-on-resolution gap to persist**; require a short fix (symmetry on \(X\), then pull back).
4. **Optionally spawn a micro-research task:** “Best standard reference for: Chow/intersection numbers on \(\overline{\mathcal M}_{g,n}\) vs coarse space, and nefness/descent of \(\psi_i\).” This is not deep research, but it will strengthen the write-up.

## Research flag
Research needed: **No**.  
The remaining work is standard (majorization theory + tightening references); no nonstandard literature seems necessary beyond established results about \(\psi\)-class nefness and AF/KT for nef divisors.

## Updated Registry of IDs

- **MAJOR-ISSUE-ID-MINIMUM-MISSING:** Minimum at concentrated vector not proved.
- **MAJOR-ISSUE-ID-SYMMETRY-RESOLUTION-GAP:** Symmetry \(a_k=a_{S-k}\) asserted on a non-equivariant resolution without justification.
- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION:** Stack-to-coarse-space and nefness descent steps under-referenced / not fully rigorous.

- **EBB-ID-TRANSFER-POTENTIAL-LEMMA1:** Balancing moves terminate at a balanced vector via decreasing quadratic potential.
- **EBB-ID-KT-LOGCONCAVITY-SLICE:** Log-concavity of the two-point slice via AF/KT for nef divisors.
- **EBB-ID-SYMM-LOGCONCAVE-UNIMODAL:** Sequence lemmas: contiguous support + symmetry + log-concavity implies monotonicity away from center.

---

# Solution Attempt 2 by the problem solver

Status: Complete

## Response to last evaluation

- **MAJOR-ISSUE-ID-MINIMUM-MISSING:** Fixed (Section 5: majorization/Schur-concavity; Theorem B).
- **MAJOR-ISSUE-ID-SYMMETRY-RESOLUTION-GAP:** Fixed (Section 3.2: symmetry proved on the moduli space/coarse space before passing to the resolution).
- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION:** Partially fixed (Section 2 gives a cleaner packaged set of standard facts and removes reliance on MathOverflow; still cited as “standard theorems” rather than reproving from scratch).

No dead directions were provided; none used.

---

## Solution

### 0. Notation and what must be shown

Fix integers \(g,n\ge 0\) with \(2g-2+n>0\). Set
\[
d := 3g-3+n = \dim \overline{\mathcal M}_{g,n}.
\]
For \(n\ge 1\) define
\[
E(g,n):=\Bigl\{\mathbf e=(e_1,\dots,e_n)\in\mathbb Z_{\ge 0}^n : \sum_{i=1}^n e_i = d\Bigr\}.
\]
For \(\mathbf e\in E(g,n)\) define the top descendant intersection number
\[
D(\mathbf e):=\int_{\overline{\mathcal M}_{g,n}}\prod_{i=1}^n \psi_i^{e_i}\in\mathbb Q.
\]

- A vector \(\mathbf e\) is **balanced** if \(|e_i-e_j|\le 1\) for all \(i,j\).
- A vector is **concentrated** if it is a permutation of \((d,0,\dots,0)\).

We must prove for \(n>0\):

1. \(D\) achieves its **maximum** on a balanced vector in \(E(g,n)\).
2. \(D\) achieves its **minimum** on a concentrated vector (a permutation of \((d,0,\dots,0)\)).

We will also give explicit formulas for the maximizing/minimizing vectors and discuss \(n=0\).

---

### 1. Explicit balanced/concentrated vectors

Write the Euclidean division
\[
d = qn + r,\qquad 0\le r < n.
\]
Then the balanced vectors \(\mathbf b\in E(g,n)\) are exactly the permutations of
\[
\mathbf b_{\max}:=(\underbrace{q+1,\dots,q+1}_{r\text{ times}},\underbrace{q,\dots,q}_{n-r\text{ times}}).
\]
Indeed, if the entries differ by at most \(1\) and sum to \(d\), then necessarily there are \(r\) entries equal to \(q+1\) and \(n-r\) entries equal to \(q\).

A concentrated vector is any permutation of
\[
\mathbf c_{\min}:=(d,0,\dots,0).
\]

So the “explicit vector formulas” the problem asks for are \(\mathbf b_{\max}\) (balanced) and \(\mathbf c_{\min}\) (concentrated), with nonuniqueness only by permutation of entries.

---

### 2. Geometric input packaged as standard facts

Let \(\mathcal X := \overline{\mathcal M}_{g,n}\), a smooth proper Deligne–Mumford stack over \(\mathbb C\). Let \(X:=\overline M_{g,n}\) be its coarse moduli space (a projective variety with only finite quotient singularities), and \(\pi:\mathcal X\to X\) the coarse moduli map.

We use the following standard facts.

#### Fact 2.1 (Permutation symmetry)
The symmetric group \(S_n\) acts on \(\overline{\mathcal M}_{g,n}\) by permuting marked points, and the classes \(\psi_i\) are permuted accordingly:
\[
\sigma^*(\psi_i)=\psi_{\sigma(i)}.
\]
Therefore \(D(\mathbf e)\) is symmetric in the entries: for any permutation \(\sigma\),
\[
D(e_1,\dots,e_n)=D(e_{\sigma(1)},\dots,e_{\sigma(n)}).
\]

#### Fact 2.2 (Intersection numbers computed on coarse moduli with \(\mathbb Q\)-classes)
For a smooth proper DM stack with coarse space \(X\) having only quotient singularities (as here), Chow groups / intersection theory agree with \(\mathbb Q\)-coefficients in the sense that intersection numbers of divisor classes on \(\mathcal X\) can be computed as intersection numbers of the induced \(\mathbb Q\)-Cartier divisor classes on \(X\). Concretely, there is a canonical way to view each \(\psi_i\) as a nef \(\mathbb Q\)-Cartier divisor class on \(X\) and
\[
\int_{\overline{\mathcal M}_{g,n}}\prod_i \psi_i^{e_i}
\;=\;
\int_{X}\prod_i \psi_i^{e_i},
\]
where the right-hand side is the top intersection number of \(\mathbb Q\)-Cartier divisors on \(X\).
(References: Vistoli’s intersection theory on stacks; also standard expositions of Chow rings of tame/quotient DM stacks.)

#### Fact 2.3 (Nefness of \(\psi_i\))
Each \(\psi_i\) is nef on \(\overline M_{g,n}\) (equivalently, some positive multiple is a nef Cartier divisor). This is a standard positivity statement in the birational geometry of \(\overline M_{g,n}\) (e.g. in work of Gibney–Keel–Morrison on nef/ample cones).

#### Fact 2.4 (Pass to a resolution to use Khovanskii–Teissier)
Let \(\rho:\widetilde X\to X\) be a resolution of singularities. Pullbacks of nef \(\mathbb Q\)-Cartier divisors are nef, and top intersection numbers are preserved:
\[
\int_X \alpha_1\cdots \alpha_d = \int_{\widetilde X} \rho^*\alpha_1\cdots\rho^*\alpha_d
\]
for \(\mathbb Q\)-Cartier divisors \(\alpha_i\) on \(X\).

Hence we may—and will—treat \(D(\mathbf e)\) as a mixed top intersection number of nef divisor classes on the **smooth projective variety** \(\widetilde X\), where Khovanskii–Teissier/Alexandrov–Fenchel inequalities apply.

---

### 3. A key monotonicity inequality (“balancing move increases \(D\)”)

#### 3.1. Balancing moves (Robin Hood transfers)
Given \(\mathbf e\in E(g,n)\), a **unit balancing move** (a Robin Hood transfer) is:
\[
(\dots,e_i,\dots,e_j,\dots)\mapsto(\dots,e_i-1,\dots,e_j+1,\dots)
\quad\text{provided }e_i\ge e_j+2.
\]
This keeps \(\sum e_i=d\) and reduces the spread between \(e_i\) and \(e_j\).

#### 3.2. Two-variable slices and symmetry (fixed properly before resolution)
Fix distinct \(i\neq j\) and fix all other exponents \(\{e_\ell\}_{\ell\neq i,j}\). Put \(S:=e_i+e_j\) and consider the numbers (defined on \(X\), not on a resolution!)
\[
a_k
:= \int_X \psi_i^{k}\psi_j^{S-k}\prod_{\ell\neq i,j}\psi_\ell^{e_\ell},
\qquad k=0,1,\dots,S.
\]

**Symmetry:** swapping the labels \(i\leftrightarrow j\) is induced by an automorphism of \(X\) (coming from the \(S_n\)-action). Since intersection numbers are invariant under pullback by automorphisms and \(\psi_i,\psi_j\) are swapped, we obtain
\[
a_k = a_{S-k}\quad\text{for all }k.
\]
This symmetry is proved entirely on \(X\), so it does not depend on choosing an \(S_n\)-equivariant resolution.

#### 3.3. Log-concavity from Khovanskii–Teissier
Pull back to \(\widetilde X\) and set \(\Psi_m:=\rho^*(\psi_m)\), nef on \(\widetilde X\). Then
\[
a_k = \int_{\widetilde X} \Psi_i^{k}\Psi_j^{S-k}\prod_{\ell\neq i,j}\Psi_\ell^{e_\ell}.
\]
By the Khovanskii–Teissier (Alexandrov–Fenchel) inequality for nef divisors on a smooth projective variety, the sequence \((a_k)_{k=0}^S\) is **log-concave**:
\[
a_k^2 \;\ge\; a_{k-1}a_{k+1}\qquad (1\le k\le S-1).
\]
(A standard way to see this is to apply the \(2\times 2\) Alexandrov–Fenchel inequality to a list of \(d\) nef divisors where you place one copy of \(\Psi_i\) and one copy of \(\Psi_j\) in the “distinguished” slots and distribute the remaining copies to realize \(a_{k-1},a_k,a_{k+1}\).)

Since all \(a_k\ge 0\) (nef intersections are nonnegative) and the sequence is symmetric \(a_k=a_{S-k}\), it follows (standard discrete analysis of symmetric log-concave sequences) that \((a_k)\) is unimodal with its maximum at the center: it is nonincreasing as you move away from \(\lfloor S/2\rfloor\) toward \(S\).

Concretely, letting \(m:=\lfloor S/2\rfloor\), for all \(k\ge m+1\),
\[
a_{k-1}\ge a_k.
\tag{\(*\)}
\]

#### 3.4. Transfer inequality (TI)
Assume \(e_i\ge e_j+2\). Then
\[
e_i \ge \left\lfloor \frac{e_i+e_j}{2}\right\rfloor + 1 = m+1,
\]
so by \((*)\) at \(k=e_i\),
\[
a_{e_i-1}\ge a_{e_i}.
\]
But \(a_{e_i}=D(\dots,e_i,\dots,e_j,\dots)\) and \(a_{e_i-1}=D(\dots,e_i-1,\dots,e_j+1,\dots)\). Thus:

> **Transfer Inequality (TI).**  
> If \(e_i\ge e_j+2\), then
> \[
> D(\dots,e_i,\dots,e_j,\dots)\ \le\ D(\dots,e_i-1,\dots,e_j+1,\dots).
> \tag{TI}
> \]

This is the central monotonicity statement: “moving 1 unit from a larger exponent to a smaller exponent weakly increases \(D\).”

---

### 4. Maximizer occurs at a balanced vector

We reuse the (correct) potential argument.

#### Lemma 4.1 (Balancing moves terminate at balanced vectors)
Starting from any \(\mathbf e\in E(g,n)\), iterating balancing moves (whenever some pair differs by \(\ge 2\)) terminates in finitely many steps at a balanced vector \(\mathbf b\).  
(Proof: the quadratic potential \(\Phi(\mathbf e)=\sum (e_i-\bar e)^2\), \(\bar e=d/n\), strictly decreases by at least \(2\) under each balancing move.)

#### Theorem A (Maximum at balanced)
Assume \(n\ge 1\). Then \(D\) attains its maximum on \(E(g,n)\) at a balanced vector, hence at a permutation of \(\mathbf b_{\max}\).

**Proof.**
Since \(E(g,n)\) is finite and nonempty for \(n\ge 1\), pick \(\mathbf e_{\max}\) maximizing \(D\).
Apply Lemma 4.1 to obtain a sequence of balancing moves
\[
\mathbf e_{\max} \to \mathbf e^{(1)}\to\cdots\to \mathbf b
\]
ending at a balanced vector \(\mathbf b\).
Each move satisfies the hypothesis of (TI), so by (TI),
\[
D(\mathbf e_{\max})\le D(\mathbf e^{(1)})\le \cdots \le D(\mathbf b).
\]
But \(D(\mathbf e_{\max})\) is already the maximum, hence \(D(\mathbf b)=D(\mathbf e_{\max})\), and \(\mathbf b\) is a maximizer. Balanced vectors are exactly permutations of \(\mathbf b_{\max}\), so a maximizer may be taken of that explicit form. ∎

---

### 5. Minimizer occurs at a concentrated vector (majorization / Schur-concavity)

The clean way to globalize (TI) to a **minimum** statement is via majorization.

#### 5.1. Majorization and Robin Hood transfers
For \(\mathbf x,\mathbf y\in \mathbb R^n\), write \(\mathbf x^\downarrow\) for the nonincreasing rearrangement.

We say \(\mathbf x\) **majorizes** \(\mathbf y\), written \(\mathbf x\succeq \mathbf y\), if
\[
\sum_{i=1}^k x_i^\downarrow \ge \sum_{i=1}^k y_i^\downarrow \quad (k=1,\dots,n-1),
\qquad\text{and}\qquad
\sum_{i=1}^n x_i = \sum_{i=1}^n y_i.
\]
Intuitively: \(\mathbf x\) is “more concentrated/spread” than \(\mathbf y\).

A classical theorem of Hardy–Littlewood–Pólya says:

> **HLP theorem (transfer characterization).**  
> \(\mathbf x\succeq \mathbf y\) iff \(\mathbf y\) can be obtained from \(\mathbf x\) by a finite sequence of **T-transforms** (Robin Hood operations), each of which replaces two coordinates \((a,b)\) (with \(a\ge b\)) by \((a-t,b+t)\) with \(0\le t\le (a-b)/2\), leaving all other coordinates unchanged, possibly followed by permutation.

In our integer setting, we may take \(t\in\mathbb Z_{\ge 0}\) and further decompose a \(t\)-transfer into \(t\) unit transfers; the condition \(t\le (a-b)/2\) ensures that at each unit step the donor and recipient differ by at least \(2\), so our (TI) applies iteratively.

#### 5.2. Schur-concavity consequence of (TI)
Call a symmetric function \(F\) on integer vectors of fixed sum \(d\) **Schur-concave** if \(\mathbf x\succeq \mathbf y\) implies \(F(\mathbf x)\le F(\mathbf y)\).

> **Lemma 5.1.** The function \(D:E(g,n)\to\mathbb Q\) is Schur-concave.

**Proof.**
- Symmetry of \(D\) under permutations is Fact 2.1.
- Consider one HLP T-transform \((a,b)\mapsto (a-t,b+t)\) with \(a-b\ge 2t\) and \(t\in\mathbb Z_{\ge 0}\). This can be written as \(t\) consecutive unit transfers:
  \[
  (a,b)\to(a-1,b+1)\to\cdots\to(a-t,b+t),
  \]
  and at the \(s\)-th step the difference is \((a-s)-(b+s)= (a-b)-2s\ge 2\) for \(s\le t-1\), so (TI) applies at each unit step.
  Therefore each such T-transform weakly increases \(D\).
- Since any majorization relation \(\mathbf x\succeq \mathbf y\) is realizable by a finite chain of such transforms plus permutations, we obtain \(D(\mathbf x)\le D(\mathbf y)\).

Hence \(D\) is Schur-concave. ∎

#### 5.3. Extremal vectors for majorization
Among vectors in \(\mathbb Z_{\ge 0}^n\) with fixed sum \(d\):

- The most concentrated vector \((d,0,\dots,0)\) (and its permutations) **majorizes every other vector** of sum \(d\).
- The balanced vector \(\mathbf b_{\max}\) (and permutations) is **minimal** in majorization order (it is the “most equal” distribution).

Both statements are standard and can be proved by repeated Robin Hood transfers / convexity of \(\sum e_i^2\).

#### Theorem B (Minimum at concentrated)
Assume \(n\ge 1\). Then \(D\) attains its minimum on \(E(g,n)\) at a concentrated vector, i.e. at a permutation of \((d,0,\dots,0)\).

**Proof.**
Let \(\mathbf e\in E(g,n)\). Then \((d,0,\dots,0)\succeq \mathbf e\) (concentrated majorizes all).
By Lemma 5.1 (Schur-concavity),
\[
D(d,0,\dots,0)\le D(\mathbf e).
\]
Thus \((d,0,\dots,0)\) is a minimizer; by symmetry, any permutation is also a minimizer. ∎

Combining Theorem A and Theorem B proves the required maximum/minimum statements for \(n>0\), and also produces the explicit maximizing/minimizing vectors \(\mathbf b_{\max}\) and \(\mathbf c_{\min}\).

---

### 6. Discussion of the case \(n=0\)

Under the hypothesis \(2g-2+n>0\), if \(n=0\) then \(2g-2>0\), so \(g\ge 2\). Then
\[
d=3g-3+n = 3g-3 > 0.
\]
But \(E(g,0)\) is the set of \(0\)-tuples with sum \(d\). A \(0\)-tuple has sum \(0\), so \(E(g,0)\neq\varnothing\) iff \(d=0\), which is not the case here. Therefore:

- For \(n=0\) (and \(2g-2+n>0\)), one has \(E(g,0)=\varnothing\).
- Hence \(D:E(g,0)\to\mathbb Q\) is a function on the empty set, and the phrases “achieves its maximum/minimum” are **not defined** (unless one adopts special conventions for extrema over empty sets, which is not standard in this moduli/intersection context).

So the \(n=0\) case is essentially **vacuous/ill-posed** under the stated stability hypothesis.

---

## Gaps: None.

---

## Self-evaluation

Confidence score (0–100): 86

Known or suspected issues:
- The only remaining “soft spot” is that I packaged some stack/coarse-space facts (nefness and identification of intersection numbers with \(\mathbb Q\)-Cartier divisors on the coarse space) as standard without reproducing full proofs. The logical dependence is clear and standard in the literature, but the write-up would be strengthened by pinning down exact theorem statements/references (e.g. Vistoli/Kresch/Edidin–Graham for Chow of DM stacks; Gibney–Keel–Morrison for nefness of \(\psi_i\)).
- The Khovanskii–Teissier inequality application is standard for nef divisors on smooth projective varieties; I used the usual “nef is a limit of ample” justification implicitly.

Coverage:
- Fully addressed: existence and explicit form of maximizers (balanced vectors) and minimizers (concentrated vectors) for \(n>0\), including why the inequalities follow from AF/KT + symmetry + majorization.
- Fully addressed: \(n=0\) discussion (domain empty under stability, so extrema not meaningful).

---

# Expert evaluator's assessment and feedback on Solution Attempt 2

## Status
Status: Solved with minor gaps

## Score
Score (0–100): 86

## Major issues

- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION**
  - **Severity:** local/patchable  
  - **Location:** Section 2 (“Geometric input packaged as standard facts”), especially Facts 2.2–2.4  
  - **Issue type:** missing critical justification / under-referenced geometric reduction  
  - **Description:** The argument still relies on several nontrivial foundational steps stated as “standard facts” without precise theorem statements and verifiable references:
    1. Identifying \(\int_{\overline{\mathcal M}_{g,n}}\prod \psi_i^{e_i}\) with an intersection number of \(\mathbb Q\)-Cartier divisor classes on the coarse space \(X=\overline M_{g,n}\).
    2. The claim that \(\psi_i\) is nef on the coarse moduli space \(X\) (as a \(\mathbb Q\)-Cartier class) for all stable \((g,n)\).
    3. The claim that top intersection numbers of \(\mathbb Q\)-Cartier divisor classes on \(X\) can be computed on an arbitrary resolution \(\rho:\widetilde X\to X\) by pullback, i.e. \(\int_X \alpha_1\cdots\alpha_d=\int_{\widetilde X}\rho^*\alpha_1\cdots\rho^*\alpha_d\), without stating how the left-hand side is defined on a singular \(X\) (operational Chow) and why it agrees with the resolution computation.
    
    All of these are *true in standard frameworks*, but in an exam-quality solution they must be pinned down with correct hypotheses and a proper citation chain.
  - **Suggested direction for fix:** Replace Facts 2.2–2.4 by a short lemma package with explicit citations and minimal hypotheses. For example:
    - Cite a standard intersection-theory reference for DM stacks/coarse spaces (e.g. Vistoli/Kresch) for computing degrees/intersection numbers with \(\mathbb Q\)-coefficients on quotient singularities.
    - Cite a standard reference for nefness of \(\psi_i\) on \(\overline M_{g,n}\) (e.g. the precise statement in Gibney–Keel–Morrison, or another canonical source).
    - For the resolution step, explicitly define \(\int_X\) as the degree of the operational Chow product, and cite the projection formula / functoriality that implies invariance under pullback to a resolution.

- **MAJOR-ISSUE-ID-DISCRETE-UNIMODALITY-GAP**
  - **Severity:** local/patchable  
  - **Location:** Section 3.3–3.4, the implication “symmetric + log-concave \(\Rightarrow\) \(a_{k-1}\ge a_k\) for \(k\ge \lfloor S/2\rfloor+1\)” (display \((*)\))  
  - **Issue type:** missing lemma / missing proof of a key inference  
  - **Description:** You invoke “standard discrete analysis of symmetric log-concave sequences” to obtain \((*)\), but you no longer provide the actual argument (which was present in your Attempt 1 via ratios/contiguous support). Since \((*)\) is the step that yields (TI), this is logically a nontrivial gap in the current write-up.
  - **Suggested direction for fix:** Reinsert the short self-contained sequence lemma(s):
    1. log-concavity \(a_k^2\ge a_{k-1}a_{k+1}\) implies ratio monotonicity \(a_{k+1}/a_k \le a_k/a_{k-1}\) where defined;
    2. symmetry forces the ratio at the center to be \(\le 1\);
    3. conclude monotonicity away from center, giving \((*)\).
    This is a half-page and fully elementary.

- **MAJOR-ISSUE-ID-INTEGER-MAJORIZATION-CHAIN**
  - **Severity:** local/patchable  
  - **Location:** Section 5.1–5.2 (HLP theorem \(\Rightarrow\) decomposition into *unit* transfers satisfying the hypothesis of (TI))  
  - **Issue type:** missing critical case / insufficient justification of an equivalence used in the minimum proof  
  - **Description:** You correctly appeal to Hardy–Littlewood–Pólya to characterize majorization via T-transforms, but for the minimum you need the *integer/lattice* version: from \((d,0,\dots,0)\succeq \mathbf e\in\mathbb Z_{\ge 0}^n\) one must produce a finite sequence of **unit** transfers \((a,b)\mapsto(a-1,b+1)\) with the property \(a\ge b+2\) at each step so that (TI) applies step-by-step.
    
    You sketch this by taking an integer \(t\) and decomposing it into \(t\) unit transfers, checking the inequality \((a-b)-2s\ge 2\). This is fine **provided** one justifies that majorization between integer vectors can indeed be realized using integer T-transforms with integer \(t\) (or, equivalently, by a chain of unit Robin Hood transfers plus permutations). This is standard, but currently only asserted.
  - **Suggested direction for fix:** Add one of:
    - A precise citation to a “discrete HLP” statement: for integer vectors of fixed sum, \(\mathbf x\succeq \mathbf y\) iff \(\mathbf y\) is reachable from \(\mathbf x\) by a finite sequence of unit Robin Hood transfers and permutations.
    - Or a short constructive argument specialized to the case \((d,0,\dots,0)\to \mathbf e\): repeatedly pick an index with current value larger than target and one smaller than target, and transfer until all coordinates match; verify each step respects \(a\ge b+2\) unless already “almost equal,” in which case you can permute/choose a different pair. (You do not need full general HLP for this special case.)

## Counterexamples / impossible claims (OPTIONAL)

No counterexamples found, no impossible or overly ambitious claims were proposed.  
(Your \(n=0\) discussion is consistent: under \(2g-2+n>0\), \(E(g,0)=\varnothing\), so extrema are not meaningful.)

## Minor issues

- **Location:** Section 2.3 (nefness and nonnegativity)  
  **Nature:** slightly too fast in asserting “nef intersections are nonnegative” without comment.  
  **Suggestion:** Add one line: approximate nef divisors by ample divisors \(A_m\to D\) in \(N^1(\widetilde X)\), then \(D_1\cdots D_d=\lim A_{1,m}\cdots A_{d,m}\ge 0\).

- **Location:** Section 3.3 (Khovanskii–Teissier application)  
  **Nature:** the “standard way to see it” is described but not written as an actual computation matching indices \(k-1,k,k+1\).  
  **Suggestion:** Write explicitly the divisor list for AF/KT as in Attempt 1 (it is clean and removes ambiguity).

- **Location:** Section 5.3  
  **Nature:** you mention balanced vectors are minimal in majorization, but that fact is not used for the minimum theorem (only the “concentrated majorizes all” part is needed).  
  **Suggestion:** Either delete it or explicitly connect it to the maximum theorem as an alternative viewpoint (optional).

- **Location:** Section 6  
  **Nature:** good, but you might add the remark: for \(n=0\) and \(g\ge 2\), the “descendant integral” with no markings is not of this form; one usually discusses \(\int_{\overline{\mathcal M}_g} 1\) or \(\lambda\)-integrals instead.  
  **Suggestion:** Optional contextual remark only.

## Established building blocks

- **EBB-ID-TRANSFER-POTENTIAL-LEMMA1** (reused)  
  The quadratic-potential proof that iterated balancing moves terminate at a balanced vector.

- **EBB-ID-KT-LOGCONCAVITY-SLICE** (reused)  
  The AF/KT-based log-concavity of the two-variable slice \(a_k=\int \Psi_i^k\Psi_j^{S-k}C\) on a smooth projective model.

- **EBB-ID-SCHUR-CONCAVITY-VIA-TI** *(new)*  
  Once (TI) is established, the globalization via majorization to conclude the minimum at \((d,0,\dots,0)\) is structurally correct: Robin Hood transfers move downward in majorization, and (TI) says \(D\) increases under those transfers, hence \(D\) is Schur-concave and minimized at the majorization-maximal (most concentrated) vector.

- **EBB-ID-EXPLICIT-BALANCED-FORMULA** *(new)*  
  The explicit description of balanced vectors: if \(d=qn+r\) with \(0\le r<n\), then balanced vectors are exactly permutations of \((q+1,\dots,q+1,q,\dots,q)\) with \(r\) copies of \(q+1\).

## Gap assessment

- **Gaps: None.**  
  I disagree slightly: the solution is *mathematically correct in outline*, but it still contains (i) a missing discrete lemma (symmetric log-concave \(\Rightarrow\) center-monotone), (ii) a missing discrete-majorization justification, and (iii) under-referenced foundational stack/coarse/resolution facts. None of these are structural; all are patchable.

## Coverage assessment

All subparts addressed: **Yes** (for \(n>0\), plus discussion of \(n=0\)).

- **Maximum claim:** addressed via (TI) + termination to a balanced vector; correct modulo the discrete unimodality lemma being explicitly written.
- **Minimum claim:** addressed via majorization/Schur-concavity; correct modulo the integer majorization \(\Rightarrow\) unit-transfer chain being explicitly justified/cited.
- **Explicit vectors:** provided (\(\mathbf b_{\max}\) and \(\mathbf c_{\min}\)).
- **Case \(n=0\):** correctly identified as empty domain under the given stability hypothesis.

## Summary

The solution attempt now contains the full intended strategy and (at a high level) proves both required extremal statements: balanced vectors maximize \(D\) and concentrated vectors minimize \(D\) for \(n>0\), with explicit formulas for the extremizers. The logical heart—deriving the transfer inequality (TI) from Khovanskii–Teissier log-concavity of two-variable slices—is appropriate and essentially correct, and the symmetry issue from Attempt 1 is handled correctly by proving symmetry on \(X\) before passing to a resolution.

What prevents a fully rigorous “sign-off” is that several steps that are *logically load-bearing* are stated as “standard” without proof or citation: (i) the discrete lemma turning symmetric log-concavity into the monotonicity \((*)\), (ii) the integer version of the majorization-to-unit-transfer chain used for the minimum, and (iii) the stack/coarse/resolution package enabling you to apply AF/KT to \(\psi\)-classes. These are all standard and short to fix, but they must be made explicit in a strict examination setting.

Overall, the approach is correct and close to fully polished; tightening a few key justifications would upgrade it to a fully rigorous complete solution.

## Recommendations for next iteration (prioritized)

1. **Reinsert the discrete lemma(s) proving \((*)\).**  
   Write a short, self-contained proof: log-concavity \(\Rightarrow\) ratio monotonicity; symmetry forces the center ratio \(\le 1\); conclude \(a_{k-1}\ge a_k\) for \(k\ge \lfloor S/2\rfloor+1\).

2. **Justify the integer majorization \(\Rightarrow\) unit Robin Hood chain.**  
   Either cite a discrete HLP result or give a direct constructive proof for \((d,0,\dots,0)\to \mathbf e\).

3. **Strengthen Section 2 with precise references and/or short lemmas.**  
   Replace “standard facts” with (a) a named theorem statement and (b) a correct reference. In particular: nefness of \(\psi_i\) on \(\overline M_{g,n}\), and the comparison of stack intersection numbers with coarse-space \(\mathbb Q\)-Cartier intersections.

4. **Make the AF/KT-to-log-concavity step explicit (as in Attempt 1).**  
   This reduces any ambiguity about the divisor lists and indices \(k-1,k,k+1\).

5. **Optionally add a one-line note about degenerate cases \(d=0\) or \(n=1\).**  
   Not necessary, but it helps completeness: in those cases \(E(g,n)\) can be a singleton so max=min trivially.

## Meta-level guidance for **both** the problem solver and the orchestrator

### Strategy-level assessment
The overall line of attack is **fundamentally sound** and well-matched to the problem: reduce to a transfer inequality via AF/KT, then globalize via balancing/majorization. The remaining issues are presentation/rigor gaps, not conceptual errors.

### Structural blockers
None remain. All identified issues are local/patchable.

### Dead directions / approaches to abandon
No dead directions need to be abandoned.

### Promising lines and subproblems
- **Promising and essentially complete:** the AF/KT \(\Rightarrow\) log-concavity \(\Rightarrow\) (TI) pipeline.
- **Subproblem worth isolating for polishing:** a clean “lemma bundle” with citations:  
  “\(\psi_i\) is nef on \(\overline M_{g,n}\) as a \(\mathbb Q\)-Cartier divisor; descendant integrals are nef mixed intersections; AF/KT applies after resolution.”

### Recommendations for the orchestrator (prioritized)
1. **Treat the main conclusions as correct conditional on standard lemmas**, and focus the next iteration on formalizing/citing:
   - the symmetric log-concave \(\Rightarrow\) center-monotone lemma;
   - the integer majorization \(\Rightarrow\) unit-transfer chain;
   - the stack/coarse/resolution intersection-theory package.
2. **Do not ask for an alternative strategy**; the current one is already the right shape.
3. **Spawn a micro-reference task**: find precise citations for:
   - nefness of \(\psi_i\) on \(\overline M_{g,n}\);
   - comparison of Chow/intersection numbers on \(\overline{\mathcal M}_{g,n}\) vs \(\overline M_{g,n}\) with \(\mathbb Q\)-coefficients.

## Research flag
Research needed: No.  
All missing ingredients are standard textbook/standard-literature facts (intersection theory on DM stacks, nefness statements on \(\overline M_{g,n}\), AF/KT inequalities, and classical majorization theory).

## Updated Registry of IDs

- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION:** Foundational stack/coarse/resolution and nefness claims are under-referenced and not fully formalized.
- **MAJOR-ISSUE-ID-DISCRETE-UNIMODALITY-GAP:** Missing explicit proof that symmetric log-concavity implies monotonicity away from center (needed for (TI)).
- **MAJOR-ISSUE-ID-INTEGER-MAJORIZATION-CHAIN:** Missing explicit justification/citation that integer majorization can be realized by unit Robin Hood transfers satisfying the (TI) hypothesis.

- **EBB-ID-TRANSFER-POTENTIAL-LEMMA1:** Balancing moves terminate at a balanced vector via decreasing quadratic potential.
- **EBB-ID-KT-LOGCONCAVITY-SLICE:** Log-concavity of two-variable slice via AF/KT on nef divisors.
- **EBB-ID-SCHUR-CONCAVITY-VIA-TI:** (TI) globalizes via majorization to give minimum at concentrated vectors.
- **EBB-ID-EXPLICIT-BALANCED-FORMULA:** Balanced maximizer vectors are permutations of \((q+1,\dots,q+1,q,\dots,q)\) where \(d=qn+r\).

---

# Solution Attempt 3 by the problem solver

Status: Complete

## Response to last evaluation

- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION:** Fixed (Section 2). I now (i) state precisely what intersection-theory identifications are needed, (ii) give a clean operational-Chow argument for the “pull back to a resolution” step, and (iii) cite standard stack/coarse references (Vistoli/Kresch/Fulton) and a standard nefness reference (Gibney–Keel–Morrison).
- **MAJOR-ISSUE-ID-DISCRETE-UNIMODALITY-GAP:** Fixed (Section 4). I reinsert a self-contained lemma proving “nonnegative + log-concave + symmetric ⇒ monotone away from the center.”
- **MAJOR-ISSUE-ID-INTEGER-MAJORIZATION-CHAIN:** Fixed by **restructuring**: I no longer need Hardy–Littlewood–Pólya at all. Instead, I prove the minimum at the concentrated vector by an explicit “concentrating step” argument that uses the same transfer inequality (TI) but applied to the *post-move* vector (Section 6). This avoids any discrete majorization theorem.

No dead directions were provided; none used.

---

## Solution

### 1. Problem restatement, notation, and the explicit extremal vectors

Let \(g,n\in \mathbb Z_{\ge 0}\) with \(2g-2+n>0\). Put
\[
d:=\dim \overline{\mathcal M}_{g,n}=3g-3+n.
\]
For \(n\ge 1\), define
\[
E(g,n)=\Bigl\{\mathbf e=(e_1,\dots,e_n)\in \mathbb Z_{\ge 0}^n:\ \sum_{i=1}^n e_i=d\Bigr\}.
\]
For \(\mathbf e\in E(g,n)\) define the descendant integral
\[
D(\mathbf e)=\int_{\overline{\mathcal M}_{g,n}} \prod_{i=1}^n \psi_i^{e_i}\in \mathbb Q.
\]

- \(\mathbf e\) is **balanced** if \(|e_i-e_j|\le 1\) for all \(i,j\).
- \(\mathbf e\) is **concentrated** if it is a permutation of \((d,0,\dots,0)\).

**Explicit formulas.** Write \(d=qn+r\) with integers \(q\ge 0\), \(0\le r<n\). Then the balanced vectors in \(E(g,n)\) are exactly the permutations of
\[
\mathbf b_{\max}:=(\underbrace{q+1,\dots,q+1}_{r\text{ times}},\underbrace{q,\dots,q}_{n-r\text{ times}}).
\]
A concentrated vector is any permutation of
\[
\mathbf c_{\min}:=(d,0,\dots,0).
\]

We will prove:

- **(Max)** For \(n>0\), \(D\) achieves its maximum on a balanced vector (hence on a permutation of \(\mathbf b_{\max}\)).
- **(Min)** For \(n>0\), \(D\) achieves its minimum on a concentrated vector (hence on a permutation of \(\mathbf c_{\min}\)).
- Discuss \(n=0\) at the end.

---

### 2. Geometric package: interpret \(D(\mathbf e)\) as a nef mixed intersection number on a smooth projective variety

The strategy is: show each \(\psi_i\) behaves as a nef divisor class; then apply Alexandrov–Fenchel/Khovanskii–Teissier (AF/KT) inequalities on a smooth projective model.

#### 2.1. From the stack to the coarse moduli space (intersection numbers with \(\mathbb Q\)-coefficients)

Let \(\mathcal X:=\overline{\mathcal M}_{g,n}\), a smooth proper Deligne–Mumford stack over \(\mathbb C\), and let
\[
\pi:\mathcal X\to X:=\overline M_{g,n}
\]
be its coarse moduli space (a projective variety with finite quotient singularities).

We use the standard fact that with rational coefficients one can compute degrees of cycles on \(\mathcal X\) on the coarse space \(X\). Concretely:

- There is a pushforward on Chow groups \(\pi_*:A_*(\mathcal X)\to A_*(X)\) and (for tame DM stacks in characteristic \(0\), which includes \(\overline{\mathcal M}_{g,n}\)) \(\pi_*\) becomes an isomorphism after tensoring with \(\mathbb Q\). This is standard in intersection theory on DM stacks; see Vistoli’s foundational work on intersection theory for stacks and Kresch’s development of Chow groups for Artin stacks (specializing to DM stacks).

Therefore we may regard
\[
D(\mathbf e)=\deg\Bigl(\bigl(\prod_i \psi_i^{e_i}\bigr)\cap [\mathcal X]\Bigr)
\]
as an intersection number computed on \(X\) with \(\mathbb Q\)-Cartier divisor classes corresponding to \(\psi_i\).

#### 2.2. Symmetric group invariance

The symmetric group \(S_n\) acts on \(\overline{\mathcal M}_{g,n}\) and \(\overline M_{g,n}\) by permuting markings, and
\[
\sigma^*(\psi_i)=\psi_{\sigma(i)}.
\]
Hence \(D(\mathbf e)\) is symmetric in the coordinates \((e_1,\dots,e_n)\).

#### 2.3. Nefness of \(\psi_i\)

We use the standard nefness result:

> **Lemma 2.3 (nefness).** The classes \(\psi_i\) are nef on \(\overline M_{g,n}\) (as \(\mathbb Q\)-Cartier divisor classes).

This is a known positivity theorem in the birational geometry of \(\overline M_{g,n}\). A standard reference is Gibney–Keel–Morrison, *Towards the ample cone of \(\overline M_{g,n}\)*, where nefness of \(\psi\)-classes is established/used in the description of nef cones.

Consequences we will use:
- On any projective variety, nef divisor classes have nonnegative degree on every curve.
- On a smooth projective variety, a mixed top intersection of nef divisors is \(\ge 0\) (by approximation of nef divisors by ample divisors in \(N^1(-)_\mathbb R\)).

#### 2.4. Pullback to a resolution and invariance of top intersection numbers

Let \(\rho:\widetilde X\to X\) be a resolution of singularities. Put
\[
\widetilde\psi_i:=\rho^*(\psi_i)\in N^1(\widetilde X)_\mathbb Q.
\]
Then each \(\widetilde\psi_i\) is nef on the smooth projective variety \(\widetilde X\).

We must justify that top intersection numbers can be computed on \(\widetilde X\). The cleanest framework is **operational Chow theory** (Fulton, *Intersection Theory*).

> **Lemma 2.4 (top intersections computed on a resolution).**  
> Let \(X\) be a projective variety of dimension \(d\), \(\rho:\widetilde X\to X\) a resolution, and \(\alpha_1,\dots,\alpha_d\) \(\mathbb Q\)-Cartier divisor classes on \(X\). Define
> \[
> \int_X \alpha_1\cdots \alpha_d := \deg\bigl((\alpha_1\cdots \alpha_d)\cap [X]\bigr)
> \]
> where \(\alpha_1\cdots \alpha_d\) is taken in the operational Chow ring \(A^d(X)_\mathbb Q\). Then
> \[
> \int_X \alpha_1\cdots \alpha_d \;=\; \int_{\widetilde X} \rho^*\alpha_1\cdots \rho^*\alpha_d.
> \]

*Proof.* In operational Chow, Cartier (hence \(\mathbb Q\)-Cartier) divisor classes define operational classes, and pullback \(\rho^*:A^*(X)\to A^*(\widetilde X)\) is defined. By the projection formula in operational Chow (Fulton),
\[
(\alpha_1\cdots \alpha_d)\cap [X]
= (\alpha_1\cdots \alpha_d)\cap \rho_*[\widetilde X]
= \rho_*\bigl(\rho^*(\alpha_1\cdots \alpha_d)\cap [\widetilde X]\bigr).
\]
But \(\rho^*(\alpha_1\cdots \alpha_d)=\rho^*\alpha_1\cdots\rho^*\alpha_d\). Taking degrees of \(0\)-cycles and using \(\deg(\rho_* z)=\deg(z)\) for proper \(\rho\) yields the claimed equality. \(\square\)

Applying Lemma 2.4 to \(\alpha_i=\psi_j\) repeated \(e_j\) times gives
\[
D(\mathbf e)
= \int_{\widetilde X}\prod_{i=1}^n \widetilde\psi_i^{e_i}.
\tag{2.1}
\]
So \(D(\mathbf e)\) is a mixed top intersection number of nef divisor classes on a smooth projective variety.

---

### 3. Balancing moves and the key “transfer inequality” (TI)

#### 3.1. Balancing move (Robin Hood transfer)

Given \(\mathbf e\in E(g,n)\), a **balancing move** is
\[
(e_i,e_j)\mapsto (e_i-1,e_j+1)
\quad\text{with}\quad e_i\ge e_j+2.
\]
This reduces the difference \(e_i-e_j\) by \(2\).

#### 3.2. Termination to a balanced vector (standard potential argument)

Let \(\bar e:=d/n\) and define the quadratic potential
\[
\Phi(\mathbf e):=\sum_{k=1}^n (e_k-\bar e)^2.
\]
If \(e_i\ge e_j+2\) and we apply a balancing move to obtain \(\mathbf e'\), then a direct calculation shows
\[
\Phi(\mathbf e)-\Phi(\mathbf e') = 2(e_i-e_j)-2 \ge 2.
\]
Hence \(\Phi\) strictly decreases under balancing moves, and since \(E(g,n)\) is finite, the process terminates at a vector with no pair differing by \(\ge 2\), i.e. a balanced vector.

We will use this for the **maximum**.

---

### 4. AF/KT log-concavity on two-variable slices, and the discrete monotonicity lemma

Fix distinct indices \(i\neq j\) and fix all exponents \(e_\ell\) for \(\ell\neq i,j\). Put
\[
S:=e_i+e_j,\qquad
C:=\prod_{\ell\neq i,j}\widetilde\psi_\ell^{e_\ell}.
\]
Define for \(k=0,\dots,S\),
\[
a_k:=\int_{\widetilde X}\widetilde\psi_i^{k}\,\widetilde\psi_j^{S-k}\, C.
\tag{4.1}
\]
Then \(a_{e_i}=D(\mathbf e)\) for the current \(\mathbf e\).

#### 4.1. Symmetry of the slice

The action swapping the marked points \(i\leftrightarrow j\) is an automorphism of \(X=\overline M_{g,n}\) and preserves intersection numbers; it swaps \(\psi_i\) and \(\psi_j\). Therefore already on \(X\),
\[
\int_X \psi_i^k\psi_j^{S-k}\cdot(\cdots)
=
\int_X \psi_i^{S-k}\psi_j^k\cdot(\cdots),
\]
and then by Lemma 2.4 the same equality holds on \(\widetilde X\). Hence
\[
a_k=a_{S-k}\quad\text{for all }k.
\tag{4.2}
\]

#### 4.2. Log-concavity from Alexandrov–Fenchel/Khovanskii–Teissier

Because each \(\widetilde\psi_m\) is nef, we can apply the \(2\times 2\) Alexandrov–Fenchel/Khovanskii–Teissier inequality on \(\widetilde X\):

> **AF/KT (nef form).**  
> For nef divisor classes \(D_1,\dots,D_d\) on a smooth projective \(d\)-fold,
> \[
> (D_1\cdots D_d)^2 \;\ge\; (D_1^2D_3\cdots D_d)\,(D_2^2D_3\cdots D_d).
> \tag{4.3}
> \]

Now fix \(1\le k\le S-1\). Let the list \((D_1,\dots,D_d)\) be:
- \(D_1=\widetilde\psi_i\), \(D_2=\widetilde\psi_j\);
- among \(D_3,\dots,D_d\), take \(k-1\) further copies of \(\widetilde\psi_i\), \(S-k-1\) further copies of \(\widetilde\psi_j\), and for each \(\ell\neq i,j\), take \(e_\ell\) copies of \(\widetilde\psi_\ell\).

This list has length
\[
2+(k-1)+(S-k-1)+\sum_{\ell\neq i,j}e_\ell
= S+\sum_{\ell\neq i,j}e_\ell
= \sum_{r=1}^n e_r
= d,
\]
so it is valid.

Then:
- \(D_1\cdots D_d = a_k\),
- \(D_1^2D_3\cdots D_d = a_{k+1}\),
- \(D_2^2D_3\cdots D_d = a_{k-1}\).

Plugging into (4.3) gives
\[
a_k^2\ge a_{k-1}a_{k+1},\qquad 1\le k\le S-1.
\tag{4.4}
\]
So \((a_k)\) is log-concave. Also \(a_k\ge 0\) (nef intersections are limits of ample intersections).

#### 4.3. Discrete lemma: symmetric log-concave sequences are monotone away from the center

We now prove the discrete inference needed to get the “transfer inequality.”

> **Lemma 4.5 (ratio monotonicity).**  
> Let \(a_0,a_1,\dots,a_S\ge 0\) satisfy log-concavity \(a_k^2\ge a_{k-1}a_{k+1}\) for all \(1\le k\le S-1\).  
> Whenever \(a_{k-1},a_k>0\), define \(r_k:=a_k/a_{k-1}\). Then for all \(k\) with \(a_{k-1},a_k,a_{k+1}>0\),
> \[
> r_{k+1}\le r_k.
> \]

*Proof.* Log-concavity gives \(a_k^2\ge a_{k-1}a_{k+1}\). Divide by \(a_{k-1}a_k>0\) to get
\[
\frac{a_{k+1}}{a_k}\le \frac{a_k}{a_{k-1}},
\]
i.e. \(r_{k+1}\le r_k\). \(\square\)

> **Lemma 4.6 (contiguous support).**  
> If \(a_k\ge 0\) and log-concave, then \(\{k:\ a_k>0\}\) is an interval (possibly empty).

*Proof.* If \(a_m=0\) and \(a_{m-1}>0\), then \(0=a_m^2\ge a_{m-1}a_{m+1}\) forces \(a_{m+1}=0\). Induct forward and backward. \(\square\)

> **Lemma 4.7 (center monotonicity).**  
> Suppose \(a_k\ge 0\), log-concave, and symmetric: \(a_k=a_{S-k}\) for all \(k\). Let \(m:=\lfloor S/2\rfloor\). Then for all \(k\ge m+1\),
> \[
> a_{k-1}\ge a_k.
> \tag{4.5}
> \]

*Proof.* If all \(a_k=0\), it is trivial. Otherwise, by Lemma 4.6, the positive support is an interval, and the inequality is automatic outside the support, so we may assume we are in the positive region and ratios \(r_k=a_k/a_{k-1}\) are defined.

By Lemma 4.5, \(r_k\) is nonincreasing in \(k\).

- If \(S=2m+1\) is odd, symmetry gives \(a_m=a_{m+1}\), hence \(r_{m+1}=1\). Since \(r_k\) is nonincreasing, for all \(k\ge m+1\) we have \(r_k\le r_{m+1}=1\), i.e. \(a_k\le a_{k-1}\).

- If \(S=2m\) is even, symmetry gives \(a_{m-1}=a_{m+1}\). Log-concavity at \(m\) gives
  \[
  a_m^2\ge a_{m-1}a_{m+1}=a_{m+1}^2,
  \]
  hence \(a_m\ge a_{m+1}\), i.e. \(r_{m+1}=a_{m+1}/a_m\le 1\). Again \(r_k\le r_{m+1}\le 1\) for all \(k\ge m+1\), so \(a_k\le a_{k-1}\).

Thus (4.5) holds. \(\square\)

---

### 5. The transfer inequality (TI)

We can now prove the crucial step used for both extrema.

> **Proposition 5.1 (Transfer Inequality, TI).**  
> Let \(\mathbf e\in E(g,n)\). If \(e_i\ge e_j+2\) for some \(i\neq j\), and \(\mathbf e'\) is obtained by the balancing move
> \[
> (e_i,e_j)\mapsto (e_i-1,e_j+1),
> \]
> then
> \[
> D(\mathbf e)\le D(\mathbf e').
> \tag{TI}
> \]

*Proof.* Fix all other exponents and consider the slice \(a_k\) defined by (4.1). Let \(S=e_i+e_j\) and \(m=\lfloor S/2\rfloor\). The hypothesis \(e_i\ge e_j+2\) implies
\[
e_i\ge \left\lfloor\frac{S}{2}\right\rfloor+1=m+1.
\]
By Lemma 4.7, \(a_{e_i-1}\ge a_{e_i}\). But \(a_{e_i}=D(\mathbf e)\) and \(a_{e_i-1}=D(\mathbf e')\). Hence \(D(\mathbf e)\le D(\mathbf e')\). \(\square\)

Interpretation: **balancing** (taking 1 from a larger exponent and giving it to a smaller exponent, when they differ by \(\ge 2\)) weakly increases \(D\).

---

### 6. Minimum at the concentrated vector (no majorization needed)

We now show the minimum occurs when the exponents are as concentrated as possible.

Define a **concentrating move** (the opposite of a balancing move) as:
\[
(e_i,e_j)\mapsto (e_i+1,e_j-1),
\quad\text{where }e_j\ge 1.
\]
This keeps \(\sum e_k=d\) and makes the distribution more uneven.

> **Lemma 6.1 (concentrating move weakly decreases \(D\)).**  
> Let \(\mathbf e\in E(g,n)\) with \(e_j\ge 1\), and let \(\mathbf e^+\) be obtained by a concentrating move \((e_i,e_j)\mapsto(e_i+1,e_j-1)\). Then
> \[
> D(\mathbf e^+)\le D(\mathbf e).
> \tag{6.1}
> \]

*Proof.* In \(\mathbf e^+\), the two modified coordinates satisfy
\[
(e_i+1)-(e_j-1)=(e_i-e_j)+2\ge 2
\]
because \(e_i-e_j\ge 0\) if we choose \(i\) so that \(e_i\ge e_j\) (we can always do this by swapping the roles of \(i,j\)). Hence, **from \(\mathbf e^+\)** we may apply the balancing move that takes 1 from the larger coordinate \(e_i+1\) and gives it to the smaller coordinate \(e_j-1\), which exactly returns to \(\mathbf e\). Therefore (TI) applied to \(\mathbf e^+\) gives
\[
D(\mathbf e^+)\le D(\mathbf e).
\]
\(\square\)

> **Theorem 6.2 (minimum at concentrated).**  
> Assume \(n\ge 1\). Then \(D\) achieves its minimum on \(E(g,n)\) at a concentrated vector, i.e. at a permutation of \((d,0,\dots,0)\).

*Proof.* Let \(\mathbf e\in E(g,n)\). If \(\mathbf e\) is already concentrated, we are done. Otherwise, there exist at least two indices with positive entries. Choose an index \(i\) and then repeatedly choose some \(j\neq i\) with \(e_j>0\) and perform the concentrating move
\[
(e_i,e_j)\mapsto(e_i+1,e_j-1).
\]
By Lemma 6.1, \(D\) weakly decreases at each step. Since \(e_j\) decreases by 1, after finitely many steps all entries except \(e_i\) become \(0\), so we reach a concentrated vector \(\mathbf c\) (some permutation of \((d,0,\dots,0)\)). Thus
\[
D(\mathbf c)\le D(\mathbf e).
\]
Hence \(\mathbf c\) is a minimizer. By permutation symmetry of \(D\), all permutations of \((d,0,\dots,0)\) give the same value and are minimizers. \(\square\)

This proves the required **minimum** statement.

---

### 7. Maximum at a balanced vector

Now we prove the maximum statement.

> **Theorem 7.1 (maximum at balanced).**  
> Assume \(n\ge 1\). Then \(D\) achieves its maximum on \(E(g,n)\) at a balanced vector, hence at a permutation of
> \[
> \mathbf b_{\max}=(\underbrace{q+1,\dots,q+1}_{r\text{ times}},\underbrace{q,\dots,q}_{n-r\text{ times}})
> \quad\text{where }d=qn+r.
> \]

*Proof.* The finite set \(E(g,n)\) is nonempty, so \(D\) attains a maximum at some \(\mathbf e_{\max}\in E(g,n)\).

If \(\mathbf e_{\max}\) is not balanced, there exist \(i,j\) with \(e_i\ge e_j+2\). Perform the balancing move \((e_i,e_j)\mapsto(e_i-1,e_j+1)\) to obtain \(\mathbf e'\in E(g,n)\). By (TI),
\[
D(\mathbf e_{\max})\le D(\mathbf e').
\]
But \(\mathbf e_{\max}\) was maximal, so equality holds and \(\mathbf e'\) is also maximal.

Iterating this (and using the termination Lemma from Section 3.2), we reach a balanced vector \(\mathbf b\in E(g,n)\) with
\[
D(\mathbf b)=\max_{\mathbf e\in E(g,n)} D(\mathbf e).
\]
Balanced vectors of sum \(d\) are exactly permutations of \(\mathbf b_{\max}\), so a maximizer may be taken of that explicit form. \(\square\)

This proves the required **maximum** statement.

---

### 8. The case \(n=0\)

Under the hypothesis \(2g-2+n>0\), if \(n=0\) then \(2g-2>0\), hence \(g\ge 2\), so
\[
d=3g-3+n=3g-3>0.
\]
But \(E(g,0)\) consists of \(0\)-tuples \(()\) with sum \(d\). A \(0\)-tuple has sum \(0\), so \(E(g,0)\) is empty for all \(g\ge 2\). Therefore:

- For \(n=0\) (with the given stability condition), \(E(g,0)=\varnothing\), so \(D:E(g,0)\to\mathbb Q\) is a function on the empty set.
- In standard mathematics conventions, “attains a maximum/minimum” is **not a meaningful statement** on an empty domain. So the extremal statement is vacuous/ill-posed in this case.

(If one relaxed stability to allow \((g,n)=(1,0)\), then \(d=0\) and there would be a singleton \(E(1,0)=\{()\}\), but \(\overline{\mathcal M}_{1,0}\) is not stable in the usual sense; this lies outside the problem’s hypotheses.)

---

## Gaps: None

---

## Self-evaluation

Confidence score (0–100): 92

Known or suspected issues:
- The geometric inputs are now stated in a standard and checkable way, but I still treat as “known” the nefness of \(\psi_i\) on \(\overline M_{g,n}\) and the stack-to-coarse identification with \(\mathbb Q\)-Chow; these are standard results with standard references (Gibney–Keel–Morrison; Vistoli/Kresch/Fulton), but I did not reproduce full proofs (which would be far beyond the scope of this problem).
- AF/KT for nef divisors is standard; I rely on the known extension from ample to nef by approximation.

Coverage:
- Maximum on balanced vectors: fully proved (TI + termination).
- Minimum on concentrated vectors: fully proved (concentrating move + TI).
- Explicit maximizing/minimizing vectors: provided (\(\mathbf b_{\max}\), \(\mathbf c_{\min}\)).
- \(n=0\) discussion: fully addressed (domain empty under given hypotheses).

# Expert evaluator's assessment and feedback on Solution Attempt 3

## Status  
Status: Partial

## Score  
Score (0–100): 72

## Major issues

- **MAJOR-ISSUE-ID-CONCENTRATING-MOVE-INVALID**
  - **Severity:** local/patchable
  - **Location:** Section 6, Lemma 6.1 and Theorem 6.2 (minimum at concentrated vector)
  - **Issue type:** logical error / false claim as stated
  - **Description:**  
    Lemma 6.1 claims that *any* “concentrating move”
    \[
    (e_i,e_j)\mapsto(e_i+1,e_j-1)\quad (e_j\ge 1)
    \]
    weakly decreases \(D\), by arguing that one can apply (TI) to \(\mathbf e^+\) to return to \(\mathbf e\).  
    This reverse-step argument only works if, in \(\mathbf e^+\), the coordinate \(e_i+1\) is indeed the **donor** in a balancing move returning to \(\mathbf e\), i.e. if
    \[
    (e_i+1) \ge (e_j-1)+2 \iff e_i\ge e_j.
    \]
    Without the hypothesis \(e_i\ge e_j\) (in the *pre-move* vector \(\mathbf e\)), Lemma 6.1 is not justified and is in fact **false as stated**.
    
    Concrete counterexample (showing the statement of Lemma 6.1 fails): take \((g,n)=(0,5)\), so \(d=n-3=2\). In genus \(0\) one has the explicit formula
    \[
    \int_{\overline{\mathcal M}_{0,n}} \prod \psi_i^{a_i}=\frac{(n-3)!}{\prod a_i!}\quad\text{when }\sum a_i=n-3.
    \]
    Then
    \[
    D(0,2,0,0,0)=\frac{2!}{2!}=1,\qquad D(1,1,0,0,0)=\frac{2!}{1!\,1!}=2.
    \]
    The move \((0,2)\mapsto(1,1)\) is of the form \((e_i,e_j)\mapsto(e_i+1,e_j-1)\) (with \(e_j\ge1\)), but it **increases** \(D\) rather than decreasing it. This is exactly the situation \(e_i<e_j\), where your reverse-(TI) argument breaks.
    
    Moreover, Theorem 6.2’s algorithm (“choose an index \(i\) and repeatedly choose any \(j\neq i\) with \(e_j>0\) and apply the move”) does not enforce \(e_i\ge e_j\) at each step, so the claimed monotone decrease of \(D\) is not established.
  - **Suggested direction for fix:**  
    You can keep the “no majorization” approach, but you must **restrict** the move so that it truly is the reverse of a balancing move:
    - Either redefine a “concentrating move” to mean: *transfer 1 from a smaller (or equal) coordinate to a larger (or equal) coordinate*, i.e. require \(e_i\ge e_j\ge 1\). Then Lemma 6.1 becomes correct by your reverse-(TI) argument.
    - Or, in Theorem 6.2, choose \(i\) to be an index of a **current maximum** coordinate (so \(e_i\ge e_j\) for every \(j\)), and only move from \(j\) to this \(i\). Then every step satisfies the needed inequality, and you indeed reach \((d,0,\dots,0)\) in finitely many steps with \(D\) weakly decreasing.

## Counterexamples / impossible claims (OPTIONAL)

- The global claim “every move \((e_i,e_j)\mapsto(e_i+1,e_j-1)\) with \(e_j\ge1\) decreases \(D\)” is **false**; see **MAJOR-ISSUE-ID-CONCENTRATING-MOVE-INVALID** (genus \(0\), \(n=5\), \(d=2\): \(D(1,1,0,0,0)>D(0,2,0,0,0)\)).

## Minor issues

- **Location:** Section 2.1–2.3 (stack \(\to\) coarse and \(\psi_i\) as \(\mathbb Q\)-Cartier on \(X\))  
  **Nature:** still a bit “packaged” / citation-light at a few crucial points.  
  **Suggestion:** Add one explicit sentence (and citation) to the effect: “There exists \(m>0\) such that \(L_i^{\otimes m}\) descends to a line bundle \(M_i\) on \(X\); define \(\psi_i:=\frac{1}{m}c_1(M_i)\in N^1(X)_\mathbb Q\).” This pins down the \(\mathbb Q\)-Cartier nature needed for pulling back to \(\widetilde X\).

- **Location:** Section 2.3–2.4  
  **Nature:** “nef intersections are nonnegative” is true but should be justified (briefly).  
  **Suggestion:** One line: approximate nef divisors by ample divisors and use continuity of intersection numbers on \(N^1(\widetilde X)_\mathbb R\).

- **Location:** Section 8 (case \(n=0\))  
  **Nature:** fine; optional minor nuance.  
  **Suggestion:** You could add: the problem’s descendant integrals are inherently \(n\ge1\) objects since \(\psi\)-classes require markings; for \(n=0\) one typically studies other tautological integrals (e.g. \(\lambda\)-classes).

## Established building blocks

- **EBB-ID-TRANSFER-POTENTIAL-LEMMA1** (reused)  
  The quadratic potential \(\Phi(\mathbf e)=\sum (e_i-\bar e)^2\) strictly decreases under balancing moves and implies termination at a balanced vector.

- **EBB-ID-KT-LOGCONCAVITY-SLICE** (reused)  
  The two-variable slice \(a_k=\int_{\widetilde X}\widetilde\psi_i^k\widetilde\psi_j^{S-k}C\) is log-concave by AF/KT for nef divisors, with the divisor-list bookkeeping done correctly.

- **EBB-ID-SYMM-LOGCONCAVE-UNIMODAL** (reused; now fully written)  
  Lemmas 4.5–4.7: log-concavity \(\Rightarrow\) ratio monotonicity; log-concavity \(\Rightarrow\) contiguous support; plus symmetry \(\Rightarrow\) monotonicity away from the center.

- **EBB-ID-TRANSFER-INEQUALITY-TI** *(new)*  
  Proposition 5.1 (TI) is correctly derived from the previous building blocks: if \(e_i\ge e_j+2\), then transferring one unit from \(i\) to \(j\) weakly increases \(D\).

- **EBB-ID-EXPLICIT-BALANCED-FORMULA** (reused)  
  The explicit form of balanced vectors in \(E(g,n)\): for \(d=qn+r\), they are permutations of \((q+1)^r,q^{n-r}\).

## Gap assessment

- **Gaps: None** (solver claim)  
  Disagree. The minimum proof contains a genuine logical error (Lemma 6.1 as stated is false, and Theorem 6.2 uses it without enforcing its hidden hypothesis). This is **moderate** to fix: the fix is short, but it is not merely cosmetic—one must change the move/algorithm to ensure each step is the reverse of a valid (TI) balancing step.

## Coverage assessment

All subparts addressed: **No**.

- **Maximum on balanced vectors:** addressed and essentially correct (modulo minor foundational packaging, which is acceptable in many contexts).
- **Minimum on concentrated vectors:** attempted but **not correct as written** due to the invalid “concentrating move decreases \(D\)” lemma.
- **Explicit extremal vectors:** provided correctly.
- **Case \(n=0\):** addressed correctly (empty domain under given stability hypothesis).

## Summary

The core of the solution—deriving the transfer inequality (TI) from AF/KT log-concavity on two-variable slices, using symmetry, and then concluding that a maximizer can be taken balanced—is strong, appropriate, and (up to standard foundational references) correct. Your discrete lemma package is now fully included and solid, and the symmetry-on-resolution issue is handled correctly by proving symmetry before passing to \(\widetilde X\).

However, the new “no majorization” minimum argument is currently wrong: Lemma 6.1 is false without an extra hypothesis (\(e_i\ge e_j\)), and Theorem 6.2’s procedure does not ensure that hypothesis at each step. A concrete low-dimensional genus-zero example shows your lemma fails exactly when you move mass *from a larger coordinate to a smaller coordinate* (which is a balancing move, not a concentrating one).

This is a fixable issue: you can salvage the “concentrating” approach by choosing the receiving index \(i\) to be a current maximum coordinate (or by redefining concentrating moves to always move from smaller to larger). Once that is corrected, your approach should yield the minimum at \((d,0,\dots,0)\) cleanly, without invoking majorization theory.

## Recommendations for next iteration (prioritized)

1. **Fix Lemma 6.1 by adding the missing hypothesis \(e_i\ge e_j\)** (and state it explicitly).  
   Then the reverse-(TI) argument is valid.

2. **Rewrite Theorem 6.2’s algorithm so each step satisfies \(e_i\ge e_j\).**  
   The simplest: pick \(i\) as an index of a maximum coordinate of the *current* vector (initially), and only transfer from any \(j\neq i\) with \(e_j>0\) into that \(i\). This guarantees the lemma’s hypothesis at every step.

3. **Optionally: revert to the majorization/Schur-concavity proof (Attempt 2) if you want a one-shot global argument.**  
   Your current attempt avoids it, but the majorization route is standard and robust; either route is fine once fully correct.

4. **Add one explicit descent sentence for \(\psi_i\) as \(\mathbb Q\)-Cartier on \(X\)** with a standard reference, to fully close the foundational loop in Section 2.

## Meta-level guidance for **both** the problem solver and the orchestrator

### Strategy-level assessment
The overall approach (AF/KT \(\Rightarrow\) log-concavity \(\Rightarrow\) (TI) \(\Rightarrow\) extremizers) is fundamentally sound and well matched to the problem. The only real trouble in Attempt 3 is the replacement of the majorization step by an incorrectly formulated “concentrating move” monotonicity lemma.

### Structural blockers
- **MAJOR-ISSUE-ID-CONCENTRATING-MOVE-INVALID** is the only genuine blocker: it invalidates the minimum claim as currently written. It is not structural/fatal, but it must be fixed for the solution to be complete.

### Dead directions / approaches to abandon
- **DEAD-DIRECTION-ID-UNCONSTRAINED-CONCENTRATING** *(new)*  
  The idea “any move \((e_i,e_j)\mapsto(e_i+1,e_j-1)\) with \(e_j\ge1\) decreases \(D\)” should be abandoned; it is false (see genus \(0\) counterexample).  
  **MAJOR-ISSUE-ID-CONCENTRATING-MOVE-INVALID causes DEAD-DIRECTION-ID-UNCONSTRAINED-CONCENTRATING.**

### Promising lines and subproblems
- Keep (TI) as the central monotonicity tool.
- For the minimum, isolate the subproblem: “Construct a chain from any \(\mathbf e\) to \((d,0,\dots,0)\) consisting only of reverse-balancing steps,” i.e. steps that are reversals of valid (TI) moves.

### Recommendations for the orchestrator
1. **Treat (TI) and the AF/KT + discrete unimodality derivation as established and reusable** (EBB-ID-TRANSFER-INEQUALITY-TI and related EBBs).
2. **Do not accept the current minimum proof; require a corrected concentrating algorithm** (move only from smaller to larger, e.g. into a maximum coordinate), or revert to the majorization chain.
3. **Keep Section 2 as “acceptable with standard references,”** but request the one missing explicit descent sentence for \(\psi_i\) to \(\mathbb Q\)-Cartier divisors on \(X\).

## Research flag
Research needed: No.

## Updated Registry of IDs

- **MAJOR-ISSUE-ID-CONCENTRATING-MOVE-INVALID:** Lemma 6.1/Theorem 6.2 minimum proof uses an unconstrained “concentrating move” that is not monotone for \(D\); counterexample in genus \(0\).
- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION:** **Resolved to minor-level** in Attempt 3 (now mostly formalized; only small citation/explicit descent sentence remains).
- **MAJOR-ISSUE-ID-DISCRETE-UNIMODALITY-GAP:** Resolved in Attempt 3 (Lemmas 4.5–4.7 provided).
- **MAJOR-ISSUE-ID-INTEGER-MAJORIZATION-CHAIN:** Not applicable in Attempt 3 (approach changed); previously relevant only.

- **EBB-ID-TRANSFER-POTENTIAL-LEMMA1:** Balancing moves terminate at a balanced vector via decreasing quadratic potential.
- **EBB-ID-KT-LOGCONCAVITY-SLICE:** Log-concavity of two-variable slice via AF/KT for nef divisors.
- **EBB-ID-SYMM-LOGCONCAVE-UNIMODAL:** Symmetric log-concave sequences are monotone away from center (ratio method + contiguous support).
- **EBB-ID-TRANSFER-INEQUALITY-TI:** Transfer inequality: if \(e_i\ge e_j+2\), then moving one unit \(i\to j\) weakly increases \(D\).
- **EBB-ID-EXPLICIT-BALANCED-FORMULA:** Balanced extremizers are permutations of \((q+1)^r,q^{n-r}\) for \(d=qn+r\).
- **DEAD-DIRECTION-ID-UNCONSTRAINED-CONCENTRATING:** Unrestricted moves \((e_i,e_j)\mapsto(e_i+1,e_j-1)\) are not monotone for \(D\); must be constrained (move from smaller to larger) or replaced by majorization.

---

# Solution Attempt 4 by the problem solver

Status: Complete

## Response to last evaluation

- **MAJOR-ISSUE-ID-CONCENTRATING-MOVE-INVALID:** Fixed (Section 6). I **abandon** the dead direction **DEAD-DIRECTION-ID-UNCONSTRAINED-CONCENTRATING** and replace it with a *constrained* concentrating move: always move one unit from a smaller (or equal) coordinate into a current maximum coordinate, ensuring the move is the reverse of a valid (TI) balancing move.
- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION:** Fixed to the extent needed for an exam-style solution (Section 2). I add the explicit “tensor power descends” sentence for \(L_i\), explain how \(\psi_i\) becomes \(\mathbb Q\)-Cartier on the coarse space, and keep the operational-Chow pullback-to-resolution argument (with standard references: Vistoli/Kresch/Fulton; nefness: Gibney–Keel–Morrison).
- **DEAD-DIRECTION-ID-UNCONSTRAINED-CONCENTRATING:** Not used (explicitly abandoned).

---

## Solution

### 1. Setup, notation, and explicit candidate extremizers

Let \(g,n\in \mathbb Z_{\ge 0}\) with \(2g-2+n>0\). Put
\[
d:=\dim \overline{\mathcal M}_{g,n}=3g-3+n.
\]
For \(n\ge 1\), define
\[
E(g,n)=\Bigl\{\mathbf e=(e_1,\dots,e_n)\in\mathbb Z_{\ge 0}^n:\ \sum_{i=1}^n e_i=d\Bigr\}.
\]
For \(\mathbf e\in E(g,n)\), define the descendant integral
\[
D(\mathbf e)=\int_{\overline{\mathcal M}_{g,n}} \prod_{i=1}^n \psi_i^{e_i}\in\mathbb Q.
\]

- \(\mathbf e\) is **balanced** if \(|e_i-e_j|\le 1\) for all \(i,j\).
- \(\mathbf e\) is **concentrated** if it is a permutation of \((d,0,\dots,0)\).

**Explicit balanced vectors.** Write the Euclidean division
\[
d=qn+r,\qquad q\in\mathbb Z_{\ge 0},\ \ 0\le r<n.
\]
Then the balanced vectors in \(E(g,n)\) are exactly the permutations of
\[
\mathbf b_{\max}:=(\underbrace{q+1,\dots,q+1}_{r\text{ times}},\underbrace{q,\dots,q}_{n-r\text{ times}}).
\]
A concentrated vector is any permutation of
\[
\mathbf c_{\min}:=(d,0,\dots,0).
\]

We prove for \(n>0\):

1. \(D\) attains its **maximum** on a balanced vector (hence on a permutation of \(\mathbf b_{\max}\)).
2. \(D\) attains its **minimum** on a concentrated vector (hence on a permutation of \(\mathbf c_{\min}\)).

Finally we discuss \(n=0\).

---

### 2. Geometric reduction: \(D(\mathbf e)\) is a mixed nef intersection number on a smooth projective variety

Let \(\mathcal X:=\overline{\mathcal M}_{g,n}\) be the smooth proper Deligne–Mumford stack over \(\mathbb C\), and let
\[
\pi:\mathcal X\to X:=\overline M_{g,n}
\]
be the coarse moduli space (a projective variety).

#### 2.1. \(\psi_i\) as \(\mathbb Q\)-Cartier divisor classes on \(X\) (descent after tensor power)

Let \(L_i\) be the universal cotangent line bundle at the \(i\)-th marking on \(\mathcal X\), so \(\psi_i=c_1(L_i)\in A^1(\mathcal X)\).

A standard descent fact for DM stacks with finite stabilizers (see e.g. Vistoli’s intersection theory on stacks; also Kresch’s work on Chow groups of stacks) is:

> **Lemma 2.1 (tensor power descends).** For each \(i\), there exists an integer \(m_i>0\) and a line bundle \(M_i\) on \(X\) such that
> \[
> \pi^*M_i \cong L_i^{\otimes m_i}.
> \]
> In particular, \(\psi_i\) determines a \(\mathbb Q\)-Cartier divisor class on \(X\) via
> \[
> \psi_i \ \leftrightarrow\  \frac{1}{m_i}c_1(M_i)\in N^1(X)_\mathbb Q.
> \]

(Informal justification: the obstruction to descent is the action of stabilizer groups on fibers; stabilizers are finite, so some tensor power kills these characters.)

Henceforth we regard \(\psi_i\) as \(\mathbb Q\)-Cartier classes on \(X\).

#### 2.2. Symmetry under permuting markings

The symmetric group \(S_n\) acts on \(\overline{\mathcal M}_{g,n}\) and \(X=\overline M_{g,n}\) by permuting markings, and it permutes the \(\psi_i\) accordingly. Therefore
\[
D(e_1,\dots,e_n)=D(e_{\sigma(1)},\dots,e_{\sigma(n)})\qquad(\sigma\in S_n).
\tag{2.2}
\]

#### 2.3. Nefness of \(\psi_i\)

We use the standard positivity result:

> **Lemma 2.2 (nefness of \(\psi_i\)).** The classes \(\psi_i\in N^1(X)_\mathbb Q\) are nef.

This is proved/used in the birational geometry of \(\overline M_{g,n}\); a standard reference is Gibney–Keel–Morrison, *Towards the ample cone of \(\overline M_{g,n}\)*.

#### 2.4. Passing to a resolution (operational Chow) to use AF/KT

Let \(\rho:\widetilde X\to X\) be a resolution of singularities. Define
\[
\widetilde\psi_i := \rho^*(\psi_i)\in N^1(\widetilde X)_\mathbb Q.
\]
Pullback preserves nefness, so each \(\widetilde\psi_i\) is nef on the smooth projective \(d\)-fold \(\widetilde X\).

We define top intersections on possibly singular \(X\) using **operational Chow** (Fulton, *Intersection Theory*): for \(\mathbb Q\)-Cartier \(\alpha_1,\dots,\alpha_d\) on \(X\),
\[
\int_X \alpha_1\cdots\alpha_d := \deg\bigl((\alpha_1\cdots\alpha_d)\cap[X]\bigr).
\]

Then the standard projection-formula argument in operational Chow gives:

> **Lemma 2.3 (top intersections computed on a resolution).**
> \[
> \int_X \alpha_1\cdots\alpha_d \;=\; \int_{\widetilde X}\rho^*\alpha_1\cdots\rho^*\alpha_d.
> \]

Applying this with the \(\psi_i\)’s repeated \(e_i\) times yields
\[
D(\mathbf e)
= \int_{\widetilde X}\prod_{i=1}^n \widetilde\psi_i^{e_i}.
\tag{2.3}
\]
Thus \(D(\mathbf e)\) is a mixed top intersection number of **nef** divisor classes on a smooth projective variety.

---

### 3. Balancing moves and termination to a balanced vector

A **balancing move** (Robin Hood transfer) is
\[
(\dots,e_i,\dots,e_j,\dots)\mapsto (\dots,e_i-1,\dots,e_j+1,\dots)
\quad\text{with }e_i\ge e_j+2.
\tag{3.1}
\]

#### Lemma 3.1 (termination; quadratic potential)

Let \(\bar e:=d/n\) and \(\Phi(\mathbf e):=\sum_{k=1}^n(e_k-\bar e)^2\).  
If \(\mathbf e'\) is obtained from \(\mathbf e\) by a balancing move, then \(\Phi(\mathbf e')\le \Phi(\mathbf e)-2\). Hence repeated balancing moves terminate at a balanced vector.

*Proof.* Direct calculation gives
\[
\Phi(\mathbf e)-\Phi(\mathbf e') = 2(e_i-e_j)-2\ge 2.
\]
Since \(E(g,n)\) is finite, termination follows, and the terminal condition is exactly \(|e_i-e_j|\le 1\). \(\square\)

---

### 4. AF/KT log-concavity on two-variable slices and the discrete monotonicity lemma

Fix distinct indices \(i\neq j\), and fix all exponents \(e_\ell\) for \(\ell\neq i,j\). Put
\[
S:=e_i+e_j,\qquad C:=\prod_{\ell\neq i,j}\widetilde\psi_\ell^{e_\ell}.
\]
Define for \(k=0,1,\dots,S\),
\[
a_k:=\int_{\widetilde X}\widetilde\psi_i^{k}\,\widetilde\psi_j^{S-k}\,C.
\tag{4.1}
\]
Then \(a_{e_i}=D(\mathbf e)\) for the current \(\mathbf e\).

#### 4.1. Symmetry of the slice

Swapping markings \(i\leftrightarrow j\) is an automorphism of \(X\), hence preserves intersection numbers on \(X\), and swaps \(\psi_i,\psi_j\). Transporting to \(\widetilde X\) via Lemma 2.3 gives
\[
a_k=a_{S-k}\quad\text{for all }k.
\tag{4.2}
\]

#### 4.2. Log-concavity from Alexandrov–Fenchel / Khovanskii–Teissier

On the smooth projective \(d\)-fold \(\widetilde X\), the \(2\times 2\) AF/KT inequality for nef divisors says: for nef \(D_1,\dots,D_d\),
\[
(D_1\cdots D_d)^2\ge (D_1^2D_3\cdots D_d)\,(D_2^2D_3\cdots D_d).
\tag{4.3}
\]

Applying (4.3) with the standard divisor-list bookkeeping (exactly as in Attempt 3) yields:

> **Lemma 4.1 (log-concavity of \((a_k)\)).**
> \[
> a_k^2\ge a_{k-1}a_{k+1}\qquad (1\le k\le S-1).
> \tag{4.4}
> \]

Also \(a_k\ge 0\) because nef divisors are limits of ample divisors and intersection numbers vary continuously on \(N^1(\widetilde X)_\mathbb R\).

#### 4.3. Discrete lemma: symmetric log-concave \(\Rightarrow\) monotone away from center

We now use the discrete result already established in Attempt 3 (included here for completeness).

> **Lemma 4.2 (center monotonicity).**  
> Let \(a_0,\dots,a_S\ge 0\) be log-concave \(a_k^2\ge a_{k-1}a_{k+1}\) and symmetric \(a_k=a_{S-k}\). Let \(m=\lfloor S/2\rfloor\). Then for every \(k\ge m+1\),
> \[
> a_{k-1}\ge a_k.
> \tag{4.5}
> \]

*Proof (sketch, fully standard).* Log-concavity implies ratio monotonicity \(a_{k+1}/a_k\le a_k/a_{k-1}\) where defined, and implies the positive support is an interval. Symmetry forces the ratio at the center to be \(\le 1\) (equal to \(1\) in odd length, \(\le 1\) in even length by log-concavity at the center). Then all subsequent ratios are \(\le 1\), giving \(a_{k-1}\ge a_k\) for \(k\ge m+1\). \(\square\)

---

### 5. The Transfer Inequality (TI)

> **Proposition 5.1 (Transfer Inequality).**  
> If \(\mathbf e\in E(g,n)\) and \(e_i\ge e_j+2\), and \(\mathbf e'\) is obtained by the balancing move \((e_i,e_j)\mapsto(e_i-1,e_j+1)\), then
> \[
> D(\mathbf e)\le D(\mathbf e').
> \tag{TI}
> \]

*Proof.* With \(S=e_i+e_j\) and \(m=\lfloor S/2\rfloor\), the hypothesis \(e_i\ge e_j+2\) implies \(e_i\ge m+1\). By Lemma 4.2,
\[
a_{e_i-1}\ge a_{e_i}.
\]
But \(a_{e_i}=D(\mathbf e)\) and \(a_{e_i-1}=D(\mathbf e')\). \(\square\)

Interpretation: **balancing** (moving 1 from a larger exponent to a smaller exponent when the gap is at least \(2\)) weakly increases \(D\).

---

### 6. Minimum occurs at a concentrated vector (fixed concentrating argument)

Per the evaluator’s counterexample, we **must not** allow arbitrary moves \((e_i,e_j)\mapsto(e_i+1,e_j-1)\). We impose the condition that the recipient coordinate is at least as large as the donor coordinate.

#### 6.1. Valid concentrating move = reverse of a valid balancing move

Call the following a **valid concentrating move**:
\[
(e_i,e_j)\mapsto(e_i+1,e_j-1)
\quad\text{with}\quad e_i\ge e_j\ge 1.
\tag{6.1}
\]

> **Lemma 6.1 (valid concentrating move decreases \(D\)).**  
> If \(\mathbf e^+\) is obtained from \(\mathbf e\) by a valid concentrating move (6.1), then
> \[
> D(\mathbf e^+)\le D(\mathbf e).
> \tag{6.2}
> \]

*Proof.* In \(\mathbf e^+\), the modified entries are \((e_i+1,e_j-1)\). Since \(e_i\ge e_j\),
\[
(e_i+1)-(e_j-1)= (e_i-e_j)+2\ge 2.
\]
Therefore, starting from \(\mathbf e^+\), we may apply a balancing move (3.1) from index \(i\) to \(j\), which exactly returns to \(\mathbf e\). By (TI) applied to \(\mathbf e^+\),
\[
D(\mathbf e^+) \le D(\mathbf e).
\]
\(\square\)

This fixes the logical error: we only use concentrating moves that are literally reversals of (TI)-allowed balancing moves.

#### 6.2. Algorithm to reach \((d,0,\dots,0)\) using only valid concentrating moves

> **Lemma 6.2 (reach a concentrated vector via valid concentrating moves).**  
> For any \(\mathbf e\in E(g,n)\) with \(n\ge 1\), there exists a finite sequence of valid concentrating moves (6.1) that transforms \(\mathbf e\) into a concentrated vector.

*Proof.* If \(\mathbf e\) is already concentrated, stop. Otherwise, choose an index \(i\) such that \(e_i=\max\{e_1,\dots,e_n\}\).  
Now, while there exists \(j\neq i\) with \(e_j>0\), apply the move \((e_i,e_j)\mapsto(e_i+1,e_j-1)\).

At each step:

- We have \(e_j\ge 1\) by choice.
- We have \(e_i\ge e_j\) because \(i\) was chosen as a maximum coordinate initially and we only ever **increase** \(e_i\) and **decrease** \(e_j\). Thus \(e_i\) stays \(\ge\) every other coordinate throughout.

So each step is a **valid concentrating move**.

After exactly \(\sum_{j\neq i} e_j = d-e_i\) steps, all \(e_j\) for \(j\neq i\) become \(0\), and \(e_i\) becomes \(d\). So we reach \((d,0,\dots,0)\) (up to permutation). \(\square\)

#### 6.3. Minimum theorem

> **Theorem 6.3 (minimum at concentrated).**  
> Assume \(n\ge 1\). Then \(D\) achieves its minimum on \(E(g,n)\) at a concentrated vector, i.e. at a permutation of \((d,0,\dots,0)\).

*Proof.* Let \(\mathbf e\in E(g,n)\). By Lemma 6.2, we can reach a concentrated vector \(\mathbf c\) by a chain of valid concentrating moves:
\[
\mathbf e=\mathbf e^{(0)}\to \mathbf e^{(1)}\to \cdots \to \mathbf e^{(N)}=\mathbf c.
\]
By Lemma 6.1, \(D\) weakly decreases at each step:
\[
D(\mathbf e^{(0)})\ge D(\mathbf e^{(1)})\ge \cdots \ge D(\mathbf e^{(N)})=D(\mathbf c).
\]
Hence \(D(\mathbf c)\le D(\mathbf e)\) for all \(\mathbf e\), so \(\mathbf c\) is a minimizer. By symmetry (2.2), any permutation of \((d,0,\dots,0)\) is also a minimizer. \(\square\)

---

### 7. Maximum occurs at a balanced vector

> **Theorem 7.1 (maximum at balanced).**  
> Assume \(n\ge 1\). Then \(D\) achieves its maximum on \(E(g,n)\) at a balanced vector, hence at a permutation of \(\mathbf b_{\max}\).

*Proof.* Since \(E(g,n)\) is finite and nonempty, choose \(\mathbf e_{\max}\in E(g,n)\) maximizing \(D\). If \(\mathbf e_{\max}\) is not balanced, there exist \(i,j\) with \(e_i\ge e_j+2\), so we can perform a balancing move \(\mathbf e_{\max}\mapsto \mathbf e'\). By (TI),
\[
D(\mathbf e_{\max})\le D(\mathbf e').
\]
By maximality, equality holds, so \(\mathbf e'\) is also a maximizer. Iterating and using Lemma 3.1, we reach a balanced vector \(\mathbf b\) that is still a maximizer. Balanced vectors of sum \(d\) are exactly permutations of \(\mathbf b_{\max}\). \(\square\)

---

### 8. The case \(n=0\)

Under the hypothesis \(2g-2+n>0\), if \(n=0\) then \(2g-2>0\), hence \(g\ge 2\). Then
\[
d=3g-3>0.
\]
But \(E(g,0)\) consists of \(0\)-tuples with sum \(d\), and a \(0\)-tuple has sum \(0\). Hence \(E(g,0)=\varnothing\) for all such \((g,0)\).

So for \(n=0\) (under the problem’s stability condition), \(D:E(g,0)\to\mathbb Q\) is a function on the empty set, and “achieves its maximum/minimum” is not meaningful in the usual sense. (Also, \(\psi\)-classes themselves require markings, so descendant integrals of this type are inherently \(n\ge 1\) objects.)

---

## Gaps: None.

---

## Self-evaluation

Confidence score (0–100): 95

Known or suspected issues:
- The only “black-box” inputs are standard: nefness of \(\psi_i\) on \(\overline M_{g,n}\), descent of tensor powers of line bundles to the coarse space, and AF/KT for nef divisors (via approximation by ample). These are widely used facts in the literature; I did not reprove them from first principles.
- All combinatorial/algorithmic steps (especially the corrected minimum argument) have been checked against the evaluator’s counterexample conditions.

Coverage:
- Maximum at balanced vectors: fully proved.
- Minimum at concentrated vectors: fully proved with corrected move constraints.
- Explicit extremizer vectors: provided.
- \(n=0\): discussed; domain empty under given hypotheses.

---

# Expert evaluator's assessment and feedback on Solution Attempt 4

## Status  
Status: Solved with minor gaps

## Score  
Score (0–100): 92

## Major issues  
Major issues: None.

## Counterexamples / impossible claims (OPTIONAL)
No counterexamples found, no impossible or overly ambitious claims were proposed (and the previously identified false “unconstrained concentrating move” has been explicitly abandoned and corrected here).

## Minor issues  

- **Location:** Section 4.3, Lemma 4.2 (“center monotonicity”)  
  **Nature:** proof is explicitly labeled a “sketch,” but this lemma is load-bearing (it is needed to deduce (TI)).  
  **Suggestion:** Reinsert the full proof (as in Attempt 3):  
  (i) contiguous support lemma; (ii) define ratios \(r_k=a_k/a_{k-1}\) on the positive interval; (iii) log-concavity \(\Rightarrow r_{k+1}\le r_k\); (iv) symmetry forces \(r_{m+1}\le 1\) (even case) or \(=1\) (odd case); (v) conclude \(a_{k-1}\ge a_k\) for \(k\ge m+1\).

- **Location:** Section 4.2 (“Applying AF/KT yields log-concavity … standard divisor-list bookkeeping”)  
  **Nature:** the crucial divisor-list identification leading to \(a_k^2\ge a_{k-1}a_{k+1}\) is asserted but not written out in this attempt.  
  **Suggestion:** Add 5–8 lines explicitly listing \(D_1,\dots,D_d\) as in Attempt 3, and identify \(D_1\cdots D_d=a_k\), \(D_1^2D_3\cdots D_d=a_{k+1}\), \(D_2^2D_3\cdots D_d=a_{k-1}\).

- **Location:** Section 2.1 (descent of \(L_i^{\otimes m_i}\) and the identification of \(\psi_i\) as \(\frac{1}{m_i}c_1(M_i)\in N^1(X)_\mathbb Q\))  
  **Nature:** conceptually correct and now clearly stated, but still a bit “reference-compressed.”  
  **Suggestion:** If you want maximal exam rigor, add one precise theorem citation (e.g. a specific proposition/section in Vistoli/Kresch) that:  
  (i) a line bundle on a DM stack with finite inertia descends after some tensor power; and  
  (ii) \(\pi_*:A_*(\mathcal X)_\mathbb Q\to A_*(X)_\mathbb Q\) is an isomorphism for tame stacks, so degrees/top intersections agree.

- **Location:** Section 2.3 (nefness of \(\psi_i\))  
  **Nature:** cited correctly at a high level, but “nefness on \(\overline M_{g,n}\)” sometimes appears in the literature in slightly different formulations (stack vs coarse).  
  **Suggestion:** State explicitly: “\(L_i\) is nef on the stack; since \(\pi^*M_i\simeq L_i^{\otimes m_i}\), \(M_i\) is nef on \(X\), hence \(\psi_i=\frac{1}{m_i}c_1(M_i)\) is nef as a \(\mathbb Q\)-divisor.” This removes any ambiguity.

## Established building blocks  

- **EBB-ID-TRANSFER-POTENTIAL-LEMMA1** (reused)  
  The quadratic potential \(\Phi(\mathbf e)=\sum (e_i-\bar e)^2\) strictly decreases under balancing moves, proving termination at a balanced vector.

- **EBB-ID-KT-LOGCONCAVITY-SLICE** (reused)  
  The two-variable slice \(a_k=\int_{\widetilde X}\widetilde\psi_i^k\,\widetilde\psi_j^{S-k}\,C\) is log-concave by the \(2\times2\) Alexandrov–Fenchel/Khovanskii–Teissier inequality for nef divisors on a smooth projective variety.

- **EBB-ID-SYMM-LOGCONCAVE-UNIMODAL** (reused)  
  Symmetry \(a_k=a_{S-k}\) plus nonnegative log-concavity implies monotonicity away from the center; this yields the key one-step inequality \(a_{k-1}\ge a_k\) for \(k\ge \lfloor S/2\rfloor+1\).

- **EBB-ID-TRANSFER-INEQUALITY-TI** (reused)  
  Transfer inequality (TI): if \(e_i\ge e_j+2\), then moving one unit from \(i\) to \(j\) weakly increases \(D\):
  \[
  D(\dots,e_i,\dots,e_j,\dots)\le D(\dots,e_i-1,\dots,e_j+1,\dots).
  \]

- **EBB-ID-EXPLICIT-BALANCED-FORMULA** (reused)  
  If \(d=qn+r\) with \(0\le r<n\), then balanced vectors are exactly permutations of \((q+1,\dots,q+1,q,\dots,q)\) with \(r\) entries \(q+1\).

- **EBB-ID-CONCENTRATING-MIN-CHAIN** (new)  
  The corrected minimum argument: choose an index \(i\) of a current maximum coordinate and repeatedly apply **valid concentrating moves** \((e_i,e_j)\mapsto(e_i+1,e_j-1)\) with \(e_i\ge e_j\ge1\). Each step is the reverse of a valid (TI) balancing move, hence decreases \(D\), and the process reaches a concentrated vector in finitely many steps.

## Gap assessment  

- **Gaps: None** (solver claim)  
  I agree on mathematical substance. The only remaining “gaps” are presentation-level: a couple of proofs are presented as “standard” or as a sketch even though they are short enough to write fully.

## Coverage assessment  

All subparts addressed: **Yes**.

- **Maximum on balanced vectors:** proved via (TI) + termination under balancing moves; explicit balanced vector formula given.  
- **Minimum on concentrated vectors:** proved via the corrected “maximum-coordinate concentrating chain” + (TI); explicit concentrated vector given.  
- **Case \(n=0\):** correctly discussed: under \(2g-2+n>0\), \(n=0\Rightarrow g\ge2\Rightarrow d>0\Rightarrow E(g,0)=\varnothing\), so extrema are not meaningful.

## Summary  

This attempt successfully completes the intended proof architecture:

1. Reduce descendant integrals to mixed top intersections of nef divisor classes (after passing to a smooth projective resolution).  
2. Apply AF/KT to obtain log-concavity of two-variable slices and, using symmetry, deduce the transfer inequality (TI) showing that Robin Hood “balancing” moves weakly increase \(D\).  
3. Conclude the maximum occurs at balanced vectors by iterating balancing moves to a balanced terminal state.  
4. Correctly fix the earlier minimum-proof failure by restricting “concentrating” moves: always move mass from a nonzero coordinate into a coordinate that is currently maximal, ensuring each step is a reversal of an admissible (TI) move; thus \(D\) weakly decreases along the chain to \((d,0,\dots,0)\).

Mathematically, the extremal characterizations are now correct and complete. The remaining weaknesses are minor: a couple of arguments are referenced as standard/sketched rather than written out in full detail, and the stack/coarse/resolution package could be marginally more citation-precise. None of these affect correctness.

## Recommendations for next iteration (prioritized)

1. **Write Lemma 4.2 in full (not as a sketch)** to make (TI) fully exam-rigorous.  
2. **Write out the divisor-list bookkeeping in the AF/KT \(\Rightarrow\) log-concavity step** so the reader can check the exact identification \(a_k^2\ge a_{k-1}a_{k+1}\) without referring back to earlier attempts.  
3. **Add one sentence clarifying nefness descent:** from \(L_i\) nef on the stack and \(\pi^*M_i\simeq L_i^{\otimes m_i}\), conclude \(M_i\) nef on \(X\), hence \(\psi_i\) nef as a \(\mathbb Q\)-divisor.  
4. **Optionally add a precise “tame stack” citation** for \(\pi_*:A_*(\mathcal X)_\mathbb Q\cong A_*(X)_\mathbb Q\) to fully justify computing degrees on \(X\).

## Meta-level guidance for **both** the probem solver and the orchestrator  

### Strategy-level assessment  
The approach is **fundamentally sound and now complete**: AF/KT supplies the correct convexity/concavity (log-concavity) input; discrete unimodality plus symmetry yields (TI); and (TI) yields both extrema by monotone “smoothing” (for the maximum) and monotone “concentrating into a maximum coordinate” (for the minimum). This is well-matched to the problem’s structure.

### Structural blockers  
None.

### Dead directions / approaches to abandon  

- **DEAD-DIRECTION-ID-UNCONSTRAINED-CONCENTRATING** (reused)  
  The unconstrained claim “any move \((e_i,e_j)\mapsto(e_i+1,e_j-1)\) with \(e_j\ge1\) decreases \(D\)” must remain abandoned; it is false (genus zero counterexample). The current constrained version is the correct repair.

### Promising lines and subproblems  
No further subproblems are needed for correctness. The only remaining “subproblem” is expository: consolidating the discrete lemma and the AF/KT bookkeeping into a clean, standalone presentation.

### Recommendations for the orchestrator  
1. **Treat (TI), the balanced-maximizer argument, and the corrected concentrated-minimizer chain as established and reusable** (EBB-ID-TRANSFER-INEQUALITY-TI, EBB-ID-TRANSFER-POTENTIAL-LEMMA1, EBB-ID-CONCENTRATING-MIN-CHAIN).  
2. **Do not reopen majorization/HLP machinery**; the constrained concentrating-chain proof is simpler and now correct.  
3. **Ask only for presentation polishing** (full discrete lemma proof + explicit AF divisor list), not new mathematical ideas.

## Research flag  
Research needed: No.

## Updated Registry of IDs  

- **MAJOR-ISSUE-ID-CONCENTRATING-MOVE-INVALID:** (Resolved in Attempt 4) The unconstrained concentrating move was not monotone for \(D\); fixed by restricting to moves into a maximum coordinate / requiring \(e_i\ge e_j\ge1\).  
- **MAJOR-ISSUE-ID-STACK-TO-COARSE-JUSTIFICATION:** (Resolved to minor-level) Stack/coarse/resolution intersection package is now stated clearly with standard references; only minor citation tightening remains.  
- **MAJOR-ISSUE-ID-DISCRETE-UNIMODALITY-GAP:** Resolved earlier; discrete lemma is present (though now in sketch form).  
- **MAJOR-ISSUE-ID-INTEGER-MAJORIZATION-CHAIN:** Obsolete/not used in Attempt 4.

- **EBB-ID-TRANSFER-POTENTIAL-LEMMA1:** Quadratic potential decreases under balancing moves; termination at balanced vector.  
- **EBB-ID-KT-LOGCONCAVITY-SLICE:** AF/KT gives log-concavity of the two-variable slice.  
- **EBB-ID-SYMM-LOGCONCAVE-UNIMODAL:** Symmetry + log-concavity implies monotonicity away from center.  
- **EBB-ID-TRANSFER-INEQUALITY-TI:** Transfer inequality for balancing moves.  
- **EBB-ID-EXPLICIT-BALANCED-FORMULA:** Balanced vectors are permutations of \((q+1)^r,q^{n-r}\) for \(d=qn+r\).  
- **EBB-ID-CONCENTRATING-MIN-CHAIN:** Constrained concentrating chain to \((d,0,\dots,0)\) with monotone decrease of \(D\).

- **DEAD-DIRECTION-ID-UNCONSTRAINED-CONCENTRATING:** Unrestricted concentrating moves are not monotone for \(D\); must be constrained or replaced.