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

## Theorem (extrema of top (\psi)-intersection numbers)

Let (g,n\in\mathbb Z_{\ge 0}) with (2g-2+n>0), and set
[
d:=3g-3+n=\dim \overline{\mathcal M}*{g,n}.
]
Define
[
E(g,n)=\Bigl{\mathbf e=(e_1,\dots,e_n)\in\mathbb Z*{\ge 0}^n:\ \sum_{i=1}^n e_i=d\Bigr},
\qquad
D(\mathbf e)=\int_{\overline{\mathcal M}_{g,n}} \psi_1^{e_1}\cdots\psi_n^{e_n}.
]
Call (\mathbf e) **balanced** if (|e_i-e_j|\le 1) for all (i,j). Call (\mathbf e) **concentrated** if it is a permutation of ((d,0,\dots,0)).

### 0. Empty-domain remark

If (n=0) and (2g-2+n>0), then (g\ge 2) and (d=3g-3>0), hence (E(g,0)=\varnothing). In that case “maximum/minimum on (E(g,0))” is not meaningful.
So from now on assume (n\ge 1), equivalently (E(g,n)\neq\varnothing).

### The statement

For (n\ge 1), the function (D:E(g,n)\to\mathbb Q) achieves

* its **maximum** at a balanced vector, and
* its **minimum** at a concentrated vector ((d,0,\dots,0)) (or any permutation).

Moreover, we can write explicit extremal vectors:

* Let (d=qn+r) with (q=\lfloor d/n\rfloor) and (0\le r<n). Then every balanced vector in (E(g,n)) is a permutation of
  [
  \mathbf b=\bigl(\underbrace{q+1,\dots,q+1}*{r\ \text{times}},\underbrace{q,\dots,q}*{n-r\ \text{times}}\bigr).
  ]
  In particular, (D) attains its maximum at some permutation of (\mathbf b).
* Every concentrated vector in (E(g,n)) is a permutation of
  [
  \mathbf c=(d,0,\dots,0),
  ]
  and (D) attains its minimum at some permutation of (\mathbf c).

(We do **not** claim uniqueness of maximizers/minimizers unless one adds a strictness analysis.)

---

## Proof

### 1. Combinatorics: balancing and concentrating moves

A **balancing move** (Robin Hood transfer) is an operation on (\mathbf e\in E(g,n)):
[
(\dots,e_i,\dots,e_j,\dots)\mapsto(\dots,e_i-1,\dots,e_j+1,\dots)
\quad\text{with }e_i\ge e_j+2.
\tag{BM}
]

A **concentrating move** is the reverse operation
[
(\dots,e_i,\dots,e_j,\dots)\mapsto(\dots,e_i+1,\dots,e_j-1,\dots)
\quad\text{with }e_j>0.
\tag{CM}
]

The next lemma is purely combinatorial.

#### Lemma 1 (balancing by transfers)

Starting from any (\mathbf e\in E(g,n)), repeated balancing moves (BM) terminate at a balanced vector.

**Proof.** Let (\bar e=d/n) and define
[
\Phi(\mathbf e):=\sum_{k=1}^n (e_k-\bar e)^2.
]
If (e_i\ge e_j+2), then after ((e_i,e_j)\mapsto(e_i-1,e_j+1)),
[
\Phi(\mathbf e)-\Phi(\mathbf e')=2(e_i-e_j)-2\ge 2.
]
Thus (\Phi) strictly decreases. Since (E(g,n)) is finite, the process stops; at a terminal vector no pair differs by (\ge 2), i.e. the vector is balanced. ∎

Balanced vectors have an explicit form.

#### Lemma 2 (explicit balanced vectors)

Write (d=qn+r) with (q=\lfloor d/n\rfloor) and (0\le r<n). Then (\mathbf e\in E(g,n)) is balanced iff its entries are (q) or (q+1), with exactly (r) entries equal to (q+1) and (n-r) entries equal to (q). Equivalently, (\mathbf e) is a permutation of (\mathbf b) above.

**Proof.** If (|e_i-e_j|\le 1), then all entries lie in ({m,m+1}) where (m=\min e_i). The sum constraint forces (m=q) and forces exactly (r) entries to be (q+1). The converse is immediate. ∎

Similarly, concentrating moves obviously lead to a concentrated vector: if one fixes an index (i) and repeatedly transfers from any (j\neq i) with (e_j>0) into (i), after finitely many steps all mass accumulates at (i), producing a permutation of ((d,0,\dots,0)).

So to prove the theorem it suffices to show a monotonicity statement for (D) under (BM), and then run it forward (for maxima) and backward (for minima).

---

### 2. Key geometric inequality: monotonicity under balancing moves

We will prove:

> **Transfer Inequality (TI).**
> If (\mathbf e\in E(g,n)) satisfies (e_i\ge e_j+2), and (\mathbf e') is obtained by the balancing move (BM)
> [
> (e_i,e_j)\mapsto(e_i-1,e_j+1),
> ]
> then
> [
> D(\mathbf e)\ \le\ D(\mathbf e').
> \tag{TI}
> ]

Once (TI) is established, the maximum part follows immediately from Lemma 1. The minimum part will then follow by applying (TI) in reverse.

#### 2.1. Reduction to nef divisor intersections on a smooth projective variety

Let (L_i) denote the cotangent line bundle at the (i)-th marking on (\overline{\mathcal M}_{g,n}), so (\psi_i=c_1(L_i)).

We use the following standard input.

* **(Nefness.)** Each (L_i) is nef (equivalently (\psi_i) is nef) on (\overline{\mathcal M}*{g,n}) / (\overline M*{g,n}).
* **(Intersection-theoretic comparison.)** With rational coefficients, one may compute intersection numbers of divisor classes on (\overline{\mathcal M}_{g,n}) on a smooth projective resolution of the coarse moduli space, via operational Chow and the projection formula.
* **(AF/KT inequality.)** Mixed intersections of nef divisor classes on a smooth projective variety satisfy the Alexandrov–Fenchel/Khovanskii–Teissier inequality in the (2\times 2) form stated below.

These points were discussed in our earlier write-up; here we only use their consequences:

There exists a smooth projective variety (\widetilde X) of dimension (d) and nef divisor classes (\widetilde\psi_1,\dots,\widetilde\psi_n\in N^1(\widetilde X)*\mathbb R) such that for all (\mathbf e\in E(g,n)),
[
D(\mathbf e)=\int*{\widetilde X}\widetilde\psi_1^{e_1}\cdots \widetilde\psi_n^{e_n}.
\tag{2.1}
]
In particular, these numbers are nonnegative.

(Concretely: (\widetilde X) can be taken as a resolution of singularities of the coarse moduli space (\overline M_{g,n}), and (\widetilde\psi_i) as the pullbacks of the (\mathbb Q)-Cartier divisor classes corresponding to (\psi_i).)

#### 2.2. Log-concavity of two-point slices via Alexandrov–Fenchel/Khovanskii–Teissier

Fix distinct indices (i\neq j) and fix the exponents (e_\ell) for (\ell\neq i,j). Set
[
S:=e_i+e_j,\qquad C:=\prod_{\ell\neq i,j}\widetilde\psi_\ell^{e_\ell}.
]
Define for (k=0,1,\dots,S),
[
a_k:=\int_{\widetilde X}\widetilde\psi_i^{k},\widetilde\psi_j^{S-k},C.
\tag{2.2}
]
Then (a_{e_i}=D(\mathbf e)), with the other coordinates fixed.

We use the following standard inequality.

> **Theorem 3 (AF/KT, (2\times 2) form).**
> Let (Y) be a smooth projective variety of dimension (d), and let (D_1,\dots,D_d) be nef (\mathbb R)-Cartier divisor classes on (Y). Then
> [
> (D_1\cdots D_d)^2\ \ge\ (D_1^2D_3\cdots D_d),(D_2^2D_3\cdots D_d).
> \tag{AF}
> ]

Applying (AF) on (Y=\widetilde X) with

* (D_1=\widetilde\psi_i), (D_2=\widetilde\psi_j),
* and (D_3,\dots,D_d) being a multiset consisting of ((k-1)) copies of (\widetilde\psi_i), ((S-k-1)) copies of (\widetilde\psi_j), and (e_\ell) copies of (\widetilde\psi_\ell) for each (\ell\neq i,j),

gives the log-concavity relation:

#### Lemma 3 (log-concavity)

For (1\le k\le S-1),
[
a_k^2\ \ge\ a_{k-1}a_{k+1}.
\tag{LC}
]

Additionally, symmetry of marked points implies:

#### Lemma 4 (symmetry)

[
a_k=a_{S-k}\qquad\text{for all }k.
\tag{SYM}
]

#### 2.3. Discrete consequence: symmetric log-concave sequences are maximal at the center

We will need a “no internal zeros”–free version.

#### Lemma 5 (contiguous support)

If (a_k\ge 0) and (a_k^2\ge a_{k-1}a_{k+1}) for all (k), then the set ({k:\ a_k>0}) is an interval (possibly empty).

**Proof.** If (a_m=0) and (a_{m-1}>0), then (0=a_m^2\ge a_{m-1}a_{m+1}) forces (a_{m+1}=0). Induct forward/backward. ∎

#### Lemma 6 (center monotonicity)

Assume ((a_k)*{k=0}^S) is nonnegative, log-concave (LC), and symmetric (SYM). Let (m=\lfloor S/2\rfloor). Then for every integer (k\ge m+1),
[
a*{k-1}\ge a_k.
\tag{2.3}
]

**Proof.** By Lemma 5, we may restrict to the contiguous interval where (a_k>0). Define ratios (r_k=a_k/a_{k-1}) where defined. Log-concavity implies (r_{k+1}\le r_k) (ratio monotonicity).

* If (S=2m) is even, symmetry gives (a_{m-1}=a_{m+1}), hence log-concavity at (m) yields
  [
  a_m^2\ge a_{m-1}a_{m+1}=a_{m+1}^2,
  ]
  so (a_m\ge a_{m+1}), i.e. (r_{m+1}\le 1). By monotonicity, (r_k\le 1) for all (k\ge m+1), hence (a_k\le a_{k-1}).
* If (S=2m+1) is odd, symmetry gives (a_m=a_{m+1}), so (r_{m+1}=1). Again (r_k\le 1) for all (k\ge m+1), hence (a_k\le a_{k-1}).

Thus (2.3) holds. ∎

#### 2.4. Proof of the transfer inequality (TI)

Assume (e_i\ge e_j+2) and set (S=e_i+e_j). Then
[
e_i\ge \left\lfloor \frac S2\right\rfloor+1=m+1,
]
so (e_i) lies strictly to the right of the center of the symmetric sequence ((a_k)). By Lemma 6,
[
a_{e_i-1}\ge a_{e_i}.
]
But by definition (2.2),
[
a_{e_i}=D(\dots,e_i,\dots,e_j,\dots),\qquad
a_{e_i-1}=D(\dots,e_i-1,\dots,e_j+1,\dots).
]
Hence (D(\mathbf e)\le D(\mathbf e')), which is (TI).

This completes the proof of the transfer inequality.

---

### 3. Maximum: attained at a balanced vector

Let (\mathbf e\in E(g,n)) be arbitrary. By Lemma 1 there is a finite sequence of balancing moves sending (\mathbf e) to a balanced vector (\mathbf b\in E(g,n)). By (TI), (D) does not decrease along each move, so
[
D(\mathbf e)\le D(\mathbf b).
]
In particular, if (\mathbf e_{\max}) is any maximizer of (D) on the finite set (E(g,n)), applying Lemma 1 to (\mathbf e_{\max}) yields a balanced (\mathbf b) with (D(\mathbf b)\ge D(\mathbf e_{\max})); hence the maximum is attained at a balanced vector.

By Lemma 2, the balanced vectors are exactly the permutations of
[
\mathbf b=\bigl(\underbrace{q+1,\dots,q+1}*{r},\underbrace{q,\dots,q}*{n-r}\bigr),
\qquad d=qn+r,\ 0\le r<n,
]
so (D) attains its maximum at some permutation of this explicit (\mathbf b).

---

### 4. Minimum: attained at a concentrated vector

Fix any (\mathbf e\in E(g,n)). Choose an index (i) such that (e_i=\max{e_1,\dots,e_n}). If (\mathbf e) is already concentrated (all mass at (i)), we are done. Otherwise, pick some (j\neq i) with (e_j>0) and form (\mathbf e^{(1)}) by a concentrating move:
[
e^{(1)}*i=e_i+1,\quad e^{(1)}*j=e_j-1,\quad e^{(1)}*\ell=e*\ell\ (\ell\neq i,j).
]

We claim (D(\mathbf e^{(1)})\le D(\mathbf e)). Indeed, in (\mathbf e^{(1)}) we have
[
e^{(1)}_i-(e^{(1)}_j)=(e_i+1)-(e_j-1)=(e_i-e_j)+2\ge 2,
]
so (e^{(1)}_i\ge e^{(1)}_j+2). Applying (TI) to (\mathbf e^{(1)}) (with indices (i) and (j)) shows that **balancing** one unit from (i) back to (j) weakly increases (D), i.e.
[
D(\mathbf e^{(1)})\le D(\mathbf e).
]

Now iterate: keep transferring from any (j\neq i) with positive exponent into the fixed maximal index (i). After finitely many steps you reach the concentrated vector (\mathbf c) with (c_i=d) and all other coordinates (0), and at each step (D) does not increase. Hence
[
D(\mathbf c)\le D(\mathbf e).
]
Since (\mathbf e) was arbitrary, (\mathbf c) is a global minimizer. By symmetry of (D) under permuting marked points, any permutation of ((d,0,\dots,0)) is also a minimizer.

---

## Explicit extremizers

Summarizing the explicit forms:

* **Balanced maximizers (existence).** Write (d=qn+r) with (0\le r<n). Then (D) attains its maximum at some permutation of
  [
  (,\underbrace{q+1,\dots,q+1}*{r},\underbrace{q,\dots,q}*{n-r},).
  ]
* **Concentrated minimizers (existence).** (D) attains its minimum at some permutation of
  [
  (d,0,\dots,0).
  ]




---

# Expert evaluator's assessment and feedback on Solution Attempt 1

## Status
Status: Partial

## Score
Score (0–100): 68

## Major issues

- **MAJOR-ISSUE-ID-LOGCONC-ZEROS**  
  - **Severity:** structural/fatal (for the current write-up; patchable if you add a missing nonvanishing input)  
  - **Location:** §2.3 Lemma 5 (“contiguous support”) and its use in Lemma 6; consequently §2.4 “Proof of (TI)”  
  - **Issue type:** logical error + missing critical hypothesis  
  - **Description:** Lemma 5 is **false** as stated: a nonnegative log-concave sequence can have internal zeros with positive values on both sides. Example: \((1,0,0,1)\) is log-concave and symmetric, but the positive support \(\{0,3\}\) is **not** an interval.  
    Because Lemma 6 uses Lemma 5 to define ratios \(r_k=a_k/a_{k-1}\) “on the contiguous interval where \(a_k>0\)”, the argument breaks unless you can guarantee **no internal zeros** (or better: \(a_k>0\) for all relevant \(k\)).  
    Moreover, the conclusion “symmetric log-concave ⇒ maximal at center” is also **false without a no-internal-zeros or positivity assumption**, again shown by \((1,0,0,1)\).  
    Hence the Transfer Inequality (TI) is not established from the stated inputs.
  - **Suggested direction for fix:** You must add (and justify) one of the following strengthening inputs:
    1. **Strict positivity:** prove or cite that all relevant \(\psi\)-intersection numbers \(a_k=\langle \tau_k\tau_{S-k}\prod_{\ell\neq i,j}\tau_{e_\ell}\rangle_g\) are **strictly positive** for all admissible \(k\). Then ratios are well-defined and the unimodality/center-max argument goes through cleanly.  
    2. **“No internal zeros” theorem for nef/big mixed intersections:** show that for the nef divisor classes you use (here, pullbacks of \(\psi_i\)), the mixed intersection numbers \(a_k\) cannot have internal zeros unless all are zero. This is true under additional hypotheses (e.g. nef and big, or numerical-dimension assumptions) but you must verify those hypotheses for the \(\psi_i\) on the chosen smooth model.  
    3. Replace Lemma 6 with a correct statement: “symmetric log-concave with **no internal zeros** is unimodal and peaks at the center”, and then prove “no internal zeros” in this geometric setting.

- **MAJOR-ISSUE-ID-STACK-TO-RESOLUTION**  
  - **Severity:** local/patchable  
  - **Location:** §2.1, especially the assertion of (2.1): existence of \(\widetilde X\) and nef \(\widetilde\psi_i\) such that  
    \[
    D(\mathbf e)=\int_{\widetilde X}\widetilde\psi_1^{e_1}\cdots \widetilde\psi_n^{e_n}.
    \]
  - **Issue type:** missing justification / misuse-of-theory risk  
  - **Description:** The passage from the DM stack \(\overline{\mathcal M}_{g,n}\) to a resolution of singularities of the coarse moduli space \(\overline{M}_{g,n}\), while plausible, is not justified carefully. In particular you need to address:
    - how the \(\psi_i\) on the **stack** correspond to \(\mathbb Q\)-Cartier divisor classes on the coarse space,  
    - why the degrees of top products on the stack match degrees of pullbacks on a resolution (operational Chow, projection formula),  
    - why nefness survives each step (stack → coarse \(\mathbb Q\)-divisor → pullback to resolution).
  - **Suggested direction for fix:** Add precise references or a short, correct argument using (i) intersection theory on DM stacks (Vistoli/Edidin–Graham), (ii) descent of line bundles to \(\mathbb Q\)-line bundles on the coarse space, and (iii) projection formula for birational morphisms. Also explicitly state that you work in \(N^1(-)_\mathbb R\) and that KT applies to nef \(\mathbb R\)-divisors.

- **MAJOR-ISSUE-ID-NEF-PSI**  
  - **Severity:** local/patchable  
  - **Location:** §2.1 bullet “(Nefness.) Each \(L_i\) is nef”  
  - **Issue type:** missing key citation / hypothesis verification  
  - **Description:** The whole KT/AF step hinges on nefness of the \(\psi_i\) (or \(L_i\)). This is a standard theorem, but you must either cite it precisely or give a brief argument.  
  - **Suggested direction for fix:** Provide an explicit citation (e.g. Cornalba–Harris / Arbarello–Cornalba type results, or standard references in the birational geometry of \(\overline M_{g,n}\)) stating \(L_i\) is nef on \(\overline{\mathcal M}_{g,n}\) (and hence \(\psi_i\) is nef).

## Counterexamples / impossible claims (OPTIONAL)

- The claim “If \((a_k)\ge0\) and log-concave then \(\{k:a_k>0\}\) is an interval” is **false**.  
  Counterexample: \((1,0,0,1)\) is nonnegative and log-concave (and symmetric), but its positive set is \(\{0,3\}\), not an interval.  
  (Associated to **MAJOR-ISSUE-ID-LOGCONC-ZEROS**.)

## Minor issues

- **Location:** Statement “these numbers are nonnegative” in §2.1  
  - **Nature:** imprecise inference  
  - **Suggestion:** Nefness gives nonnegativity of intersections on a smooth projective model, but you should explicitly note the step where you interpret the stack intersection number as an intersection of nef divisor classes on a smooth variety.

- **Location:** §4 “Minimum” iteration argument  
  - **Nature:** minor clarity gap  
  - **Suggestion:** Explicitly state that each concentrating move preserves membership in \(E(g,n)\) (sum fixed, nonnegativity preserved because you only subtract from \(e_j>0\)) and terminates because the total mass outside coordinate \(i\) decreases.

- **Location:** Notation/typography throughout (e.g. stray parentheses, \(\overline{\mathcal M}*{g,n}\))  
  - **Nature:** presentation issues  
  - **Suggestion:** Clean up TeX and consistently distinguish stack \(\overline{\mathcal M}_{g,n}\) vs coarse \(\overline M_{g,n}\).

## Established building blocks

- **EBB-ID-BALANCE-TERMINATION**  
  Lemma 1 (quadratic potential \(\Phi\) strictly decreases under a Robin Hood transfer when \(e_i\ge e_j+2\)) is correct and gives termination at a balanced vector.

- **EBB-ID-BALANCED-EXPLICIT**  
  Lemma 2 (explicit form of balanced vectors: entries are \(q\) or \(q+1\) with multiplicities determined by \(d=qn+r\)) is correct.

- **EBB-ID-KT-LOGCONC-SLICE**  
  The idea and computation in §2.2 applying Khovanskii–Teissier/Alexandrov–Fenchel to deduce log-concavity  
  \[
  a_k^2\ge a_{k-1}a_{k+1}
  \]
  for the two-point slice \(a_k=\int \psi_i^k\psi_j^{S-k}C\) is correct **assuming**: (i) you are on a smooth projective variety, (ii) the divisor classes involved are nef, and (iii) the intersection number matches the original \(D(\mathbf e)\).

## Gap assessment

- **Gap (implicit): positivity / no-internal-zeros to justify center-max**  
  - **Assessment:** Moderate-to-fundamental (depending on your toolkit).  
  - **Comment:** Without an added lemma guaranteeing \(a_k>0\) (or at least no internal zeros), the “symmetric log-concave ⇒ monotone away from center” step is invalid. If you are allowed to cite known results that all \(\psi\)-intersection numbers are positive, this becomes “moderate.” If not, it is “fundamental.”

- **Gap (implicit): stack-to-variety comparison**  
  - **Assessment:** Moderate (mostly technical, but must be done carefully).  
  - **Comment:** A correct reference-based justification is usually enough.

## Coverage assessment

All subparts addressed: Yes (but not fully proved).  
- **Maximizer claim:** addressed, but depends on the incomplete/incorrect Lemma 5–6 chain.  
- **Minimizer claim:** addressed similarly (also depends on (TI)).  
- **Explicit extremizer vectors:** correctly identified combinatorially.  
- **Case \(n=0\):** addressed (you correctly observed \(E(g,0)=\varnothing\) under stability).

## Summary

Your overall strategy—prove a “Robin Hood transfer increases \(D\)” inequality and then appeal to majorization/balancing—is well-aligned with the problem and is likely the intended geometric mechanism (Khovanskii–Teissier log-concavity). The combinatorial parts (existence of balanced endpoint, explicit balanced vectors, termination) are solid. The AF/KT-to-log-concavity step is also structurally sound provided the foundational geometric inputs (nefness and correct interpretation of stack intersection numbers) are stated rigorously.

The primary flaw is in the discrete step converting symmetry + log-concavity + nonnegativity into “center is maximal”: your Lemma 5 is false, and without an additional “no internal zeros”/positivity hypothesis, Lemma 6 and thus the Transfer Inequality (TI) are not proved. This is not just a stylistic gap: there are genuine counterexamples in the abstract log-concave setting. Fortunately, in the \(\psi\)-intersection context it is plausible that all relevant \(a_k\) are strictly positive (or that nef/big conditions rule out internal zeros), in which case your argument can be repaired with an added lemma/citation.

Overall, you are close to a complete solution, but the current write-up is not yet correct as a standalone proof.

## Recommendations for next iteration (prioritized)

1. **Fix the discrete unimodality step:** Replace Lemma 5 and revise Lemma 6.  
   - Either assume/prove **\(a_k>0\)** for all \(k\) in the slice, or prove a correct “no internal zeros” statement in your geometric setting.  
   - Then re-run the ratio argument (or any standard unimodality lemma) to conclude \(a_{k-1}\ge a_k\) for \(k\) right of center.

2. **Add a lemma/citation ensuring positivity/nonvanishing of \(\psi\)-intersection numbers.**  
   Options:
   - Cite Kontsevich’s ribbon graph/volume interpretation (positivity is then transparent), or
   - Use DVV/Witten–Kontsevich recursion with an induction proving positivity (more involved), or
   - Prove that \(\psi_i\) are nef and big on an appropriate smooth model and invoke a theorem that mixed intersections of nef and big divisors are strictly positive.

3. **Make the “stack → coarse → resolution” passage precise.**  
   State exactly how the line bundles \(L_i\) define \(\mathbb Q\)-Cartier classes downstairs and why the computed degrees match the original \(D(\mathbf e)\). Give references.

4. **Cite nefness of \(\psi_i\)** explicitly with a standard reference, and briefly explain why nefness is preserved under the operations you apply (descent/pullback).

5. Optionally: **Discuss uniqueness / strictness** (not required, but natural): when is the maximum attained at all balanced permutations, and can strict inequality be proved unless the vector is balanced? This would require a “strict KT” input.

## Meta-level guidance for both the probem solver and the orchestrator

### Strategy-level assessment
The line of attack is **promising and likely correct**, but currently incomplete due to a discrete/positivity gap. The geometric heart (KT log-concavity) is appropriate; you mainly need to ensure the hypotheses needed for unimodality are met in this particular intersection-theoretic context.

### Structural blockers
- **MAJOR-ISSUE-ID-LOGCONC-ZEROS** is the key blocker: without addressing internal zeros/positivity, (TI) does not follow.
- **MAJOR-ISSUE-ID-STACK-TO-RESOLUTION** is a secondary blocker: the approach needs a clean, reference-backed bridge to apply KT legitimately.

### Dead directions / approaches to abandon
- **DEAD-DIRECTION-ID-NAIVE-LOGCONC-IMPLIES-UNIMODAL**  
  Claiming “nonnegative log-concave (even symmetric) ⇒ maximum at the center” **without** a no-internal-zeros/positivity hypothesis should be abandoned.  
  **MAJOR-ISSUE-ID-LOGCONC-ZEROS causes DEAD-DIRECTION-ID-NAIVE-LOGCONC-IMPLIES-UNIMODAL.**

### Promising lines and subproblems
- Prove/cite: **strict positivity** of all top \(\psi\)-intersection numbers \(\langle \tau_{d_1}\cdots\tau_{d_n}\rangle_g>0\) whenever \(\sum d_i=3g-3+n\) and \(2g-2+n>0\).  
- Alternatively, isolate a birational-geometry lemma: **nef + big ⇒ no internal zeros in KT-slice** (or similar) that applies to the pullbacks of \(\psi_i\).
- Tighten the stack-to-variety intersection number identification in a single clean lemma.

### Recommendations for the orchestrator (prioritized)
1. **Treat EBB-ID-BALANCE-TERMINATION and EBB-ID-BALANCED-EXPLICIT as established and reuse them.**
2. **Stop accepting Lemma 5 as valid**; it is false (MAJOR-ISSUE-ID-LOGCONC-ZEROS).
3. **Spawn a research phase** to find a standard reference for:
   - positivity of \(\psi\)-intersection numbers, and/or  
   - a theorem ensuring “no internal zeros” for mixed intersections of nef/big divisors, and  
   - a clean reference for \(\psi_i\) nefness on \(\overline M_{g,n}\) / \(\overline{\mathcal M}_{g,n}\).
4. In the next attempt, **focus specifically on repairing (TI)** by adding positivity/no-internal-zeros, and do **not** revisit the combinatorial balancing/concentrating parts.

## Research flag
Research needed: No  
Reason: The missing components should be fillable using standard, well-known results (nefness of \(\psi_i\); KT inequality; positivity/nonvanishing of \(\psi\)-intersection numbers, which is classical in the Witten–Kontsevich/Kontsevich ribbon graph framework). This is “library lookup / citation” rather than genuinely new research.

## Updated Registry of IDs

### Major issues
- **MAJOR-ISSUE-ID-LOGCONC-ZEROS:** Lemma 5 false; need positivity/no-internal-zeros to deduce center-max/unimodality and thus (TI).
- **MAJOR-ISSUE-ID-STACK-TO-RESOLUTION:** Unjustified identification of stack intersection numbers with intersections on a smooth projective resolution.
- **MAJOR-ISSUE-ID-NEF-PSI:** Nefness of \(\psi_i\) asserted without citation/verification.

### Established building blocks
- **EBB-ID-BALANCE-TERMINATION:** Quadratic potential argument shows balancing moves terminate at balanced vector.
- **EBB-ID-BALANCED-EXPLICIT:** Characterization of balanced vectors as \((q+1)^r,q^{n-r}\) permutations.
- **EBB-ID-KT-LOGCONC-SLICE:** KT/AF implies log-concavity of two-point slices (given nef + smooth projective model + correct intersection identification).

### Dead directions
- **DEAD-DIRECTION-ID-NAIVE-LOGCONC-IMPLIES-UNIMODAL:** Using log-concavity + symmetry alone (without no-internal-zeros/positivity) to claim center maximum.

---

# Solution Attempt 2 by the problem solver

Status: Complete

## Response to last evaluation

- **MAJOR-ISSUE-ID-LOGCONC-ZEROS**: **Fixed (here’s where)**  
  Fixed by (i) replacing the false “contiguous support” Lemma with a correct discrete lemma requiring **strict positivity** (§4.2 Lemma 4.3), and (ii) proving/justifying strict positivity of the relevant \(\psi\)-intersection numbers \(a_k>0\) via a standard positivity result for Witten–Kontsevich correlators (§4.1 Lemma 4.1). This removes the “internal zeros” obstruction completely.

- **MAJOR-ISSUE-ID-STACK-TO-RESOLUTION**: **Fixed (here’s where)**  
  Fixed in §3 by stating a clean “stack \(\to\) coarse \(\to\) resolution” comparison lemma for top intersection numbers, with an explicit reference to Vistoli’s intersection theory on stacks (rational Chow) and the existence of coarse moduli spaces (Keel–Mori). ([eudml.org](https://eudml.org/doc/143716?utm_source=openai))

- **MAJOR-ISSUE-ID-NEF-PSI**: **Fixed (here’s where)**  
  Fixed in §2 by citing a standard source asserting that \(\psi_i\) are nef on \(\overline{\mathcal M}_{g,n}\). ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai))

Dead directions:
- **DEAD-DIRECTION-ID-NAIVE-LOGCONC-IMPLIES-UNIMODAL**: Not used. I explicitly require positivity of the slice sequence \(a_k>0\) before invoking unimodality/center-max.

---

## Solution

### 1. Setup and statement

Let \(g,n\in\mathbb Z_{\ge 0}\) with \(2g-2+n>0\) and define
\[
d:=3g-3+n=\dim_\mathbb C \overline{\mathcal M}_{g,n}.
\]
Let
\[
E(g,n)=\{\mathbf e=(e_1,\dots,e_n)\in\mathbb Z_{\ge 0}^n:\ \sum_{i=1}^n e_i=d\}.
\]
For \(\mathbf e\in E(g,n)\) define the top \(\psi\)-intersection number
\[
D(\mathbf e):=\int_{\overline{\mathcal M}_{g,n}} \psi_1^{e_1}\cdots \psi_n^{e_n}.
\]
Call \(\mathbf e\) **balanced** if \(|e_i-e_j|\le 1\) for all \(i,j\). Call \(\mathbf e\) **concentrated** if it is a permutation of \((d,0,\dots,0)\).

We prove:

1. If \(n>0\), \(D:E(g,n)\to\mathbb Q\) attains its **maximum** at a balanced vector.
2. If \(n>0\), \(D\) attains its **minimum** at a concentrated vector \((d,0,\dots,0)\) (up to permutation).
3. Give explicit extremizing vectors: balanced vectors are explicitly determined by Euclidean division \(d=qn+r\).
4. Discuss \(n=0\): then \(E(g,0)=\varnothing\) under the stability assumption, so there is no max/min problem.

Throughout, we use that \(D(\mathbf e)\) is invariant under permuting the marked points, hence symmetric in \((e_1,\dots,e_n)\).

---

### 2. Two standard geometric inputs: nefness and KT log-concavity

#### 2.1 Nefness of \(\psi_i\)

We use:

> **Fact 2.1 (nefness).** The cotangent line classes \(\psi_i\) on \(\overline{\mathcal M}_{g,n}\) are nef divisor classes. ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai))

(Any standard reference in the birational geometry of \(\overline{\mathcal M}_{g,n}\) suffices; the cited source explicitly records nefness of \(\psi_i\).)

#### 2.2 Khovanskii–Teissier (KT) inequality \(\Rightarrow\) log-concavity of two-variable slices

We use the classical Khovanskii–Teissier/Alexandrov–Fenchel inequality for mixed intersections of nef divisor classes, which implies that the coefficients in the two-variable mixed intersection sequence are log-concave. For background and a modern overview of KT-type inequalities for nef Cartier divisors, see e.g. Khovanskii’s survey-style preprint. ([arxiv.org](https://arxiv.org/abs/2502.13099?utm_source=openai))

Because \(\overline{\mathcal M}_{g,n}\) is a DM stack rather than a smooth projective variety, we will reduce to a smooth projective variety model in §3, and then apply KT there.

---

### 3. Reducing stack intersections to intersections on a smooth projective variety

Let \(\mathcal X=\overline{\mathcal M}_{g,n}\) (a proper smooth DM stack). By Keel–Mori, it admits a coarse moduli space \(p:\mathcal X\to X\) where \(X=\overline M_{g,n}\) is a proper algebraic space (in fact projective). ([en.wikipedia.org](https://en.wikipedia.org/wiki/Keel%E2%80%93Mori_theorem?utm_source=openai))

Vistoli developed intersection theory (Chow rings, degrees of 0-cycles, etc.) for DM stacks and related it to intersection theory on coarse moduli spaces. ([eudml.org](https://eudml.org/doc/143716?utm_source=openai))

We encapsulate what we need as follows.

> **Lemma 3.1 (compute on a smooth projective model).**  
> There exists a smooth projective variety \(\widetilde X\) of dimension \(d\) and nef \(\mathbb R\)-divisor classes \(\widetilde\psi_1,\dots,\widetilde\psi_n\in N^1(\widetilde X)_\mathbb R\) such that for every \(\mathbf e\in E(g,n)\),
> \[
> D(\mathbf e)=\int_{\widetilde X}\widetilde\psi_1^{e_1}\cdots \widetilde\psi_n^{e_n}.
> \]
> Moreover, each \(\widetilde\psi_i\) is nef.

**Sketch of justification.**  
- By Vistoli’s theory, \(\psi_i\in A^1(\mathcal X)_\mathbb Q\) correspond to \(\mathbb Q\)-Cartier divisor classes \(\Psi_i\in A^1(X)_\mathbb Q\) on the coarse space such that \(p^*\Psi_i=\psi_i\) in rational Chow/operational Chow. ([eudml.org](https://eudml.org/doc/143716?utm_source=openai))  
- Take any resolution of singularities \(\pi:\widetilde X\to X\) (possible over \(\mathbb C\), which is the usual context for these intersection numbers). Define \(\widetilde\psi_i:=\pi^*\Psi_i\).  
- Degrees/top intersection numbers of classes pulled back from \(X\) agree on \(\widetilde X\) by the projection formula (in operational Chow). This is part of the standard “compute intersections on a resolution” package. ([eudml.org](https://eudml.org/doc/143716?utm_source=openai))  
- Nefness: \(\psi_i\) are nef on \(\mathcal X\) (Fact 2.1). Nefness descends/ascends through these identifications and pullbacks, so \(\widetilde\psi_i\) are nef. ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai))

Hence we may (and do) work on \(\widetilde X\) and treat \(D(\mathbf e)\) as a mixed intersection number of nef divisors on a smooth projective variety.

---

### 4. The “Robin Hood transfer increases \(D\)” inequality

#### 4.1 Positivity (to kill the internal-zeros problem)

The evaluator correctly noted that log-concavity without a “no internal zeros / positivity” assumption is insufficient. We therefore add:

> **Lemma 4.1 (strict positivity of top \(\psi\)-intersection numbers).**  
> Assume \(n>0\) and \(2g-2+n>0\). For every \(\mathbf e\in E(g,n)\),
> \[
> D(\mathbf e)>0.
> \]
> In particular, in any fixed two-variable slice (defined below) all terms \(a_k\) are strictly positive.

**Justification / reference.**  
These numbers are the Witten–Kontsevich correlators \(\langle\tau_{e_1}\cdots\tau_{e_n}\rangle_g\). It is classical that they are positive, and the literature includes explicit positive lower bounds for all such correlators; see e.g. Delecroix–Goujard–Zograf–Zorich, which discusses basic facts and gives general lower bounds, implying positivity. ([ar5iv.org](https://ar5iv.org/pdf/2004.02749))

This lemma is precisely what blocks internal zeros in the log-concave sequences we use.

#### 4.2 Two-point slices and KT log-concavity

Fix distinct indices \(i\neq j\). Fix the exponents \(\{e_\ell\}_{\ell\neq i,j}\). Set
\[
S:=e_i+e_j,\qquad 
C:=\prod_{\ell\neq i,j}\widetilde\psi_\ell^{e_\ell}.
\]
Define, for \(k=0,1,\dots,S\),
\[
a_k:=\int_{\widetilde X}\widetilde\psi_i^{k}\,\widetilde\psi_j^{S-k}\,C.
\]
Then \(a_{e_i}=D(\mathbf e)\) for that \(\mathbf e\).

**(i) Log-concavity.** By KT/Alexandrov–Fenchel applied to the nef divisor classes \(\widetilde\psi_i,\widetilde\psi_j\) together with the remaining nef classes appearing in \(C\), we get
\[
a_k^2\ \ge\ a_{k-1}a_{k+1}\qquad (1\le k\le S-1).
\]
This is the standard “mixed intersections form a log-concave sequence” consequence. ([arxiv.org](https://arxiv.org/abs/2502.13099?utm_source=openai))

**(ii) Symmetry.** Swapping the labels \(i\) and \(j\) on \(\overline{\mathcal M}_{g,n}\) (hence on \(\widetilde X\) after pulling back) leaves the integral invariant, so
\[
a_k=a_{S-k}\qquad\text{for all }k.
\]

**(iii) Strict positivity.** By Lemma 4.1, \(a_k>0\) for all \(k\).

#### 4.3 Correct unimodality lemma (with positivity)

We now use a correct discrete fact.

> **Lemma 4.2 (ratio monotonicity for positive log-concave sequences).**  
> If \(a_k>0\) and \(a_k^2\ge a_{k-1}a_{k+1}\) for \(1\le k\le S-1\), then the ratios \(r_k:=a_k/a_{k-1}\) satisfy
> \[
> r_{k+1}\le r_k\qquad (1\le k\le S-1).
> \]

*Proof.* Divide \(a_k^2\ge a_{k-1}a_{k+1}\) by \(a_{k-1}a_k>0\) to get \(a_k/a_{k-1}\ge a_{k+1}/a_k\), i.e. \(r_k\ge r_{k+1}\). ∎

> **Lemma 4.3 (symmetric + positive + log-concave \(\Rightarrow\) decreases away from center).**  
> Suppose \((a_k)_{k=0}^S\) satisfies:
> 1. \(a_k>0\) for all \(k\),
> 2. \(a_k^2\ge a_{k-1}a_{k+1}\) for \(1\le k\le S-1\),
> 3. \(a_k=a_{S-k}\) (symmetry).
>
> Let \(m=\lfloor S/2\rfloor\). Then for every \(k\ge m+1\),
> \[
> a_{k-1}\ge a_k.
> \]
> Equivalently, \((a_k)\) is unimodal and achieves its maximum at the center (one or two central indices).

*Proof.*  
Define ratios \(r_k=a_k/a_{k-1}\) for \(k\ge 1\). By Lemma 4.2, \(r_k\) is nonincreasing in \(k\).

- If \(S=2m\) is even: symmetry gives \(a_{m-1}=a_{m+1}\). Log-concavity at \(m\) gives
  \[
  a_m^2\ge a_{m-1}a_{m+1}=a_{m+1}^2 \implies a_m\ge a_{m+1}.
  \]
  Hence \(r_{m+1}=a_{m+1}/a_m\le 1\). Since \(r_k\) decreases, \(r_k\le 1\) for all \(k\ge m+1\), i.e. \(a_k\le a_{k-1}\).

- If \(S=2m+1\) is odd: symmetry gives \(a_m=a_{m+1}\), so \(r_{m+1}=1\). Again \(r_k\le 1\) for all \(k\ge m+1\), hence \(a_k\le a_{k-1}\).

Thus the sequence decreases (weakly) once past the center. ∎

#### 4.4 Transfer Inequality (Robin Hood move increases \(D\))

A **balancing (Robin Hood) move** is:
\[
(e_i,e_j)\mapsto(e_i-1,e_j+1)\quad\text{provided }e_i\ge e_j+2.
\]

> **Proposition 4.4 (Transfer Inequality).**  
> If \(\mathbf e\in E(g,n)\) satisfies \(e_i\ge e_j+2\) and \(\mathbf e'\) is obtained from \(\mathbf e\) by the balancing move \((e_i,e_j)\mapsto(e_i-1,e_j+1)\), then
> \[
> D(\mathbf e)\le D(\mathbf e').
> \]

*Proof.*  
Fix all other exponents and consider the slice \(a_k\) defined in §4.2 with \(S=e_i+e_j\). Then
\[
D(\mathbf e)=a_{e_i},\qquad D(\mathbf e')=a_{e_i-1}.
\]
The condition \(e_i\ge e_j+2\) is equivalent to \(e_i\ge \lfloor S/2\rfloor+1\), i.e. \(e_i\) lies strictly to the right of the center of the symmetric sequence \((a_k)\). By Lemma 4.3,
\[
a_{e_i-1}\ge a_{e_i}.
\]
Hence \(D(\mathbf e')\ge D(\mathbf e)\). ∎

---

### 5. Combinatorics of balancing and explicit balanced vectors

This part is purely discrete and was already correct in Attempt 1; I restate it cleanly.

A balancing move strictly decreases the quadratic potential
\[
\Phi(\mathbf e):=\sum_{k=1}^n \left(e_k-\frac dn\right)^2
\]
whenever it is applicable, hence balancing terminates.

> **Lemma 5.1 (termination at balanced vector).**  
> Starting from any \(\mathbf e\in E(g,n)\), repeated balancing moves terminate at a balanced vector.

> **Lemma 5.2 (explicit form of balanced vectors).**  
> Write the Euclidean division
> \[
> d=qn+r,\qquad q=\left\lfloor\frac dn\right\rfloor,\quad 0\le r<n.
> \]
> Then \(\mathbf e\in E(g,n)\) is balanced iff its entries consist of \(r\) copies of \(q+1\) and \(n-r\) copies of \(q\).  
> Equivalently, balanced vectors are precisely the permutations of
> \[
> \mathbf b=(\underbrace{q+1,\dots,q+1}_{r\ \text{times}},\underbrace{q,\dots,q}_{n-r\ \text{times}}).
> \]

---

### 6. Maximum at balanced, minimum at concentrated (for \(n>0\))

From now on assume \(n>0\). Then \(E(g,n)\neq\varnothing\) and it is finite, so maxima/minima exist.

#### 6.1 Maximum

Let \(\mathbf e\in E(g,n)\) be arbitrary. Apply balancing moves until reaching a balanced \(\mathbf b\). Each balancing move weakly increases \(D\) by Proposition 4.4, so
\[
D(\mathbf e)\le D(\mathbf b).
\]
Hence any global maximizer can be replaced by a balanced vector without decreasing \(D\). Therefore \(D\) achieves its maximum at a balanced vector.

By Lemma 5.2, the balanced maximizers can be chosen as permutations of the explicit \(\mathbf b\) determined by \(d=qn+r\).

#### 6.2 Minimum

A **concentrating move** is the reverse step:
\[
(e_i,e_j)\mapsto(e_i+1,e_j-1)\quad\text{with }e_j>0.
\]
This preserves \(\sum e_k=d\) and nonnegativity, hence stays in \(E(g,n)\).

Pick an index \(i\) and repeatedly move all mass from the other coordinates into \(i\). This terminates at the concentrated vector \((d,0,\dots,0)\) (with the \(d\) in the \(i\)-th position).

To see that this does not increase \(D\): if \(\mathbf e^{(1)}\) is obtained from \(\mathbf e\) by a concentrating move from \(j\) into \(i\), then in \(\mathbf e^{(1)}\) we have
\[
e_i^{(1)}-e_j^{(1)}=(e_i+1)-(e_j-1)=(e_i-e_j)+2\ge 2.
\]
So \(\mathbf e\) is obtained from \(\mathbf e^{(1)}\) by a balancing move (transfer 1 back from \(i\) to \(j\)). By Proposition 4.4,
\[
D(\mathbf e^{(1)})\le D(\mathbf e).
\]
Iterating along the concentrating sequence gives
\[
D(d,0,\dots,0)\le D(\mathbf e)
\]
for all \(\mathbf e\in E(g,n)\), i.e. \((d,0,\dots,0)\) is a global minimizer. By symmetry, any permutation is also a minimizer.

---

### 7. Explicit extremizing vectors

Let \(d=3g-3+n\).

- **Maximizing (balanced) vectors**: write
  \[
  d=qn+r,\qquad 0\le r<n.
  \]
  Then any balanced vector is a permutation of
  \[
  \boxed{\mathbf b=(\underbrace{q+1,\dots,q+1}_{r},\underbrace{q,\dots,q}_{n-r})}
  \]
  and \(D\) achieves its maximum on such vectors.

- **Minimizing (concentrated) vectors**: any permutation of
  \[
  \boxed{\mathbf c=(d,0,\dots,0)}
  \]
  is a minimizer.

Remarks:
- For \(n=1\), these coincide: \(E(g,1)=\{(d)\}\), so max = min trivially.
- The problem does **not** ask for uniqueness; proving strictness would require analyzing equality cases of KT in this setting.

---

### 8. What happens when \(n=0\)?

If \(n=0\), the stability condition \(2g-2+n>0\) forces \(g\ge 2\). Then \(d=3g-3>0\), but
\[
E(g,0)=\left\{()\in\mathbb Z_{\ge 0}^0:\ \sum_{j=1}^0 e_j=3g-3\right\}=\varnothing,
\]
since the empty sum is \(0\neq 3g-3\). So \(D:E(g,0)\to\mathbb Q\) has **empty domain** and there is no maximum/minimum question to ask.

(If one instead considered the integral \(\int_{\overline{\mathcal M}_{g,0}} 1\), it is a degree mismatch unless \(d=0\), so it vanishes in the usual Chow/cohomology grading sense; but this is outside the stated \(E(g,n)\) framework.)

---

## Gaps

Gaps: None.

---

## Self-evaluation

Confidence score (0–100): 86

Known or suspected issues:
- The only delicate point is how much “in-stack vs coarse vs resolution” formalism one wants spelled out. I cited Vistoli for the relevant intersection-theoretic bridge, which is the standard reference, but I did not reproduce all details of operational Chow push-pull identities on stacks.
- Positivity of all \(\psi\)-intersection numbers is treated as a known theorem and cited via a paper that explicitly works with these correlators and uses positivity in inequalities; a reader might prefer a more direct reference to Kontsevich’s ribbon graph formula. The argument’s logic, however, only needs \(a_k>0\), and such positivity is standard.

Coverage:
- Maximum and minimum claims for \(n>0\) are proved.
- Explicit maximizing/minimizing vectors are given.
- The case \(n=0\) is discussed (domain empty under stability).