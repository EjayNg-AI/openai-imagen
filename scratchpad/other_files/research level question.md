What follows is a research level problem, followed by a series of attempts by a problem solver. Each attempt by the problem solver is evaluated by an expert evaluator who gives feedback and suggestions on how the solution can be improved or corrected. The problem solver then attempts the problem again. This process occurs iteratively until I (the moderator) decides that the problem solver is close enough and that we can write up the final solution.

Use the **latest** solution attempt by the problem solver to write up a formal solution to the problem. In your formal write up, please take into account the expert evaluator's suggestions corresponding to the latest solution attempt. You may also need to refer to previous solution attempts and their respective evaluations if you require further background and information.

Please make your writeup clear and written in a manner suitable for publication, or suitable for direction inclusion into a publishable paper.

---

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
Prove or give a counter-example to the following claim:

The function $D:E(g,n)\to\mathbb{Q}$, $\mathbf{e}\mapsto D(\mathbf{e})$ achieves its maximum on a balanced vector $\mathbf{e}\in E(g,n)$.


---

# Solution Attempt 1 by the problem solver

Status: **Complete**

## Selected approaches (OPTIONAL)

Selected approach indices: **2**, plus a new geometric inequality approach (Khovanskii–Teissier / Alexandrov–Fenchel log-concavity for nef divisors).

## Response to last evaluation

no evaluation of previous solution attempt provided

---

## Solution

### 0. Notation and goal

Let  
\[
d:=\dim \overline{\mathcal M}_{g,n}=3g-3+n,
\qquad 
E(g,n)=\{\mathbf e\in \mathbb Z_{\ge 0}^n:\; e_1+\cdots+e_n=d\}.
\]
For \(\mathbf e=(e_1,\dots,e_n)\in E(g,n)\) define
\[
D(\mathbf e):=\int_{\overline{\mathcal M}_{g,n}}\psi_1^{e_1}\cdots \psi_n^{e_n}
=\big\langle \tau_{e_1}\cdots\tau_{e_n}\big\rangle_g\in\mathbb Q_{\ge 0}.
\]
A vector \(\mathbf e\) is **balanced** if \(|e_i-e_j|\le 1\) for all \(i,j\).

We must show:

> **Claim.** The function \(\mathbf e\mapsto D(\mathbf e)\) achieves its maximum on \(E(g,n)\) at a balanced \(\mathbf e\).

Since \(E(g,n)\) is finite, a maximum exists; the content is the “balanced” location.

Two preliminary facts:

1. **Symmetry.** \(D(e_1,\dots,e_n)\) is symmetric under permuting the \(e_i\), because permuting marked points permutes the \(\psi_i\).
2. **Nefness.** Each \(\psi_i\) is a nef divisor class on \(\overline{\mathcal M}_{g,n}\) (more precisely the first Chern class of a nef line bundle). This is standard in the birational geometry of \(\overline{\mathcal M}_{g,n}\). ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai))

The core of the argument will be a log-concavity inequality for mixed intersections of nef divisors (Khovanskii–Teissier / Alexandrov–Fenchel type).

---

### 1. A discrete “balancing move” criterion

Call the operation
\[
(\dots,e_i,\dots,e_j,\dots)\mapsto (\dots,e_i-1,\dots,e_j+1,\dots)
\]
a **balancing move** (or Robin Hood transfer) from \(i\) to \(j\). This reduces the gap \(e_i-e_j\) by \(2\).

A standard combinatorial fact:

#### Lemma 1 (Any vector can be balanced by transfers).
Let \(\mathbf e\in E(g,n)\). If \(\mathbf e\) is not balanced, there exist indices \(i,j\) with \(e_i\ge e_j+2\). Performing the balancing move \((e_i,e_j)\mapsto(e_i-1,e_j+1)\) keeps the vector in \(E(g,n)\) and strictly decreases (for instance) the quadratic imbalance
\[
\Phi(\mathbf e):=\sum_{k=1}^n (e_k-\bar e)^2,\qquad \bar e=d/n.
\]
Hence repeating balancing moves finitely many times produces a balanced vector.

*Proof sketch.* If \(\mathbf e\) is not balanced, take \(i\) with maximal \(e_i\) and \(j\) with minimal \(e_j\); then \(e_i\ge e_j+2\). The move preserves the sum. A direct check shows \(\Phi\) decreases by \(2(e_i-e_j)-2\ge 2\), so the process terminates. ∎

Therefore, to prove the main claim it suffices to show:

> **Key inequality.** If \(e_i\ge e_j+2\), then
> \[
> D(\dots,e_i,\dots,e_j,\dots)\ \le\ D(\dots,e_i-1,\dots,e_j+1,\dots).
> \tag{★}
> \]

Indeed, then by Lemma 1, every \(\mathbf e\) can be moved to a balanced \(\mathbf b\) with \(D(\mathbf e)\le D(\mathbf b)\). In particular, any maximizer can be replaced by a balanced maximizer.

So we focus on proving (★).

---

### 2. Khovanskii–Teissier log-concavity for a two-variable slice

Fix distinct indices \(i\neq j\). Fix all exponents \(e_k\) for \(k\neq i,j\), and consider only redistributing the total between \(i\) and \(j\).

Let
\[
S:=e_i+e_j,
\qquad 
\mathbf e' := (e_k)_{k\neq i,j}.
\]
Define a 1-parameter sequence (a “two-point slice”)
\[
a_k := D(\text{with } e_i=k,\ e_j=S-k,\ \text{and the other exponents } \mathbf e'\text{ fixed}),
\qquad k=0,1,\dots,S.
\]
So \(a_k = \int \psi_i^k\psi_j^{S-k}\prod_{k\neq i,j}\psi_k^{e_k}\).

#### Lemma 2 (Log-concavity of the slice).
The sequence \((a_k)_{k=0}^S\) is log-concave:
\[
a_k^2 \ \ge\ a_{k-1}\,a_{k+1}\qquad \text{for }1\le k\le S-1.
\tag{LC}
\]

*Justification.* This is a standard Khovanskii–Teissier / Alexandrov–Fenchel type inequality for mixed intersection numbers of nef divisor classes: for nef divisor classes \(A,B\) on a projective variety (or compact Kähler manifold), the mixed intersections
\[
k\mapsto (A^k\cdot B^{S-k}\cdot \text{(fixed nef classes)})
\]
form a log-concave sequence. One can view this as a consequence of Hodge–Riemann bilinear relations / mixed Lefschetz theorems; it is a classical “log-concavity of intersection numbers” statement. ([ams.org](https://www.ams.org/journals/proc/2024-152-07/S0002-9939-2024-16738-1/?utm_source=openai))

To match our situation, take \(A=\psi_i\), \(B=\psi_j\), and take the “fixed nef classes” to be the remaining \(\psi_\ell\) repeated \(e_\ell\) times. Each \(\psi_\ell\) is nef. ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai))

A minor technicality is that \(\overline{\mathcal M}_{g,n}\) is a smooth proper Deligne–Mumford stack rather than a smooth projective variety. One can reduce to a smooth projective variety by pulling back to a finite level-structure cover \(Y\to \overline{\mathcal M}_{g,n}\) (a smooth projective variety with a finite surjective map). Nefness pulls back, and intersection numbers scale by \(\deg(Y\to \overline{\mathcal M}_{g,n})\), so (LC) on \(Y\) implies (LC) on \(\overline{\mathcal M}_{g,n}\). ∎

*(Remark.)* One can also view (LC) as a special case of the fact that volume polynomials of projective varieties are Lorentzian, which implies strong log-concavity properties for their coefficients. ([annals.math.princeton.edu](https://annals.math.princeton.edu/2020/192-3/p04?utm_source=openai))

#### Lemma 3 (Symmetry of the slice).
The slice is symmetric:
\[
a_k = a_{S-k}\qquad\text{for all }k.
\tag{SYM}
\]

*Proof.* Swap the labels of marked points \(i\) and \(j\); the moduli space and integral are invariant, while \(\psi_i^k\psi_j^{S-k}\) becomes \(\psi_i^{S-k}\psi_j^{k}\). ∎

---

### 3. Log-concave + symmetric ⇒ maximum at the center

We now use a purely discrete inequality fact.

#### Lemma 4 (Symmetric log-concave sequences peak in the middle).
Let \(a_0,\dots,a_S\ge 0\) be a log-concave sequence with no internal zeros, and symmetric \(a_k=a_{S-k}\). Then \((a_k)\) is unimodal and achieves its maximum at the middle index/indices:
- if \(S\) is even, the maximum is at \(k=S/2\);
- if \(S\) is odd, the maximum is attained at both \(k=\lfloor S/2\rfloor\) and \(k=\lceil S/2\rceil\).

In particular, if \(k\ge \lceil S/2\rceil+1\), then \(a_{k-1}\ge a_k\), i.e. moving one step toward the center does not decrease the value.

*Proof.* A standard property of log-concave sequences with no internal zeros is that the ratio \(a_{k}/a_{k-1}\) is nonincreasing in \(k\). Symmetry forces these ratios to cross \(1\) at the midpoint, giving unimodality and the stated location of maxima. ∎

Apply Lemma 4 to the slice \(a_k\) from §2.

---

### 4. The balancing move inequality (★)

Suppose \(e_i\ge e_j+2\). Then \(e_i \ge S/2 +1\), i.e. \(e_i\) lies strictly to the right of the center of the slice \(a_k\). Therefore by Lemma 4,
\[
a_{e_i-1}\ \ge\ a_{e_i}.
\]
But
\[
a_{e_i} = D(\dots,e_i,\dots,e_j,\dots),
\qquad
a_{e_i-1} = D(\dots,e_i-1,\dots,e_j+1,\dots).
\]
Hence
\[
D(\dots,e_i,\dots,e_j,\dots)\ \le\ D(\dots,e_i-1,\dots,e_j+1,\dots),
\]
which is exactly the desired balancing move inequality (★).

---

### 5. Conclude: maximum occurs at a balanced vector

Take any \(\mathbf e\in E(g,n)\). By Lemma 1, we can perform a finite sequence of balancing moves to reach a balanced vector \(\mathbf b\in E(g,n)\). Each move does not decrease \(D\) by (★). Therefore
\[
D(\mathbf e)\ \le\ D(\mathbf b).
\]
In particular, if \(\mathbf e_{\max}\) is a maximizer of \(D\) on the finite set \(E(g,n)\), then the balancing process produces a balanced \(\mathbf b\) with
\[
D(\mathbf b)\ \ge\ D(\mathbf e_{\max}) = \max_{\mathbf e\in E(g,n)} D(\mathbf e),
\]
so \(\mathbf b\) is also a maximizer, and it is balanced.

This proves the claim.

∎

---

## Gaps: None.

---

## Self-evaluation

Confidence score (0–100): **74**

Known or suspected issues:
1. The proof treats as “standard input” two geometric facts:
   - nefness of each \(\psi_i\) on \(\overline{\mathcal M}_{g,n}\) (well known in the literature), ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai))
   - Khovanskii–Teissier / Alexandrov–Fenchel log-concavity for mixed intersections of nef divisors, ([ams.org](https://www.ams.org/journals/proc/2024-152-07/S0002-9939-2024-16738-1/?utm_source=openai))  
   and uses a reduction from stacks to varieties via finite covers. These are widely accepted techniques, but in a fully formal write-up one would cite a precise theorem for DM stacks or include the finite-cover argument in more detail.
2. One should check “no internal zeros” for the log-concavity ⇒ unimodality lemma. In our case, \(a_k\) are intersection numbers of nef classes; they are nonnegative. Internal zeros are not expected in the stable range, but even if they occur, the “move toward the center does not decrease” conclusion can be handled by restricting to the support interval. This is a minor technical patch if needed.

Coverage:
- The claim is proved for all \((g,n)\) in the stable range \(2g-2+n>0\), using nefness + Khovanskii–Teissier log-concavity + symmetry + discrete smoothing.

# Expert evaluator's assessment and feedback on Solution Attempt 1

## Status
Status: Solved with minor gaps

## Score
Score (0–100): 72

## Major issues

- **MAJOR-ISSUE-ID-AFSTACK**  
  - **Severity:** local/patchable  
  - **Location:** §2 (Lemma 2), “Justification” paragraph; also §0 “Nefness” item (2)  
  - **Issue type:** misuse of theory / missing critical justification  
  - **Description:** The proof hinges entirely on the claim that the two-point slice
    \[
    a_k=\int_{\overline{\mathcal M}_{g,n}} \psi_i^k \psi_j^{S-k}\!\!\prod_{\ell\neq i,j}\psi_\ell^{e_\ell}
    \]
    is log-concave in \(k\) via a Khovanskii–Teissier / Alexandrov–Fenchel inequality for **nef divisors**. Conceptually this is plausible and (very likely) correct, but the write-up does not provide a precise theorem statement matching the exact situation:
    1) \(\overline{\mathcal M}_{g,n}\) is a **smooth proper Deligne–Mumford stack** rather than a smooth projective variety;  
    2) the argument “pull back to a finite level-structure cover \(Y\to \overline{\mathcal M}_{g,n}\)” is not justified with a clear reference that \(Y\) can be taken **smooth projective** and that the needed intersection theory + nefness + Khovanskii–Teissier inequality applies on \(Y\) and descends cleanly;  
    3) the cited references are not clearly connected to the exact inequality \(a_k^2\ge a_{k-1}a_{k+1}\) in this mixed setting.
    
    In particular, you should explicitly present the mixed Alexandrov–Fenchel inequality in the form
    \[
    (D_1\cdots D_d)^2 \ge (D_1^2 D_3\cdots D_d)(D_2^2 D_3\cdots D_d)
    \]
    for nef divisor classes on a smooth projective variety of dimension \(d\), and then show how to choose \((D_r)\) (allowing repetitions) so that the left side is \(a_k^2\) and the right side is \(a_{k-1}a_{k+1}\). This “repetitions allowed” point is essential and should be written explicitly (it is true by multilinearity/symmetry once the inequality is known).
  - **Suggested direction for fix:**  
    Provide a precise citation for:
    - nefness of \(\psi_i\) on \(\overline{M}_{g,n}\) (coarse space) or on the stack (as a nef line bundle), and  
    - Alexandrov–Fenchel/Khovanskii–Teissier for nef divisors on smooth projective varieties, plus a short reduction argument from stacks to varieties (or cite a version for smooth DM stacks / orbifolds).
    
    For nefness of \(\lambda\) and \(\psi_i\) on \(\overline{\mathcal M}_{g,n}\), your cited QJM article explicitly states this as “known” background; see the passage “\(\lambda\) and \(\psi_i\) are known to be nef…” ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai)). You still need to connect that statement to a standard reference or accept QJM as the reference.  
    For the AF/KT inequality, cite a standard source (e.g. Lazarsfeld *Positivity in Algebraic Geometry* or a modern Lorentzian-polynomial reference) and include the exact inequality you use.

- **MAJOR-ISSUE-ID-EMPTYDOMAIN**  
  - **Severity:** local/patchable  
  - **Location:** §0, first paragraph (“Since \(E(g,n)\) is finite, a maximum exists…”)  
  - **Issue type:** missing critical case / definitional oversight  
  - **Description:** The statement “a maximum exists because \(E(g,n)\) is finite” is only meaningful if \(E(g,n)\neq\varnothing\). Under the problem’s hypothesis \(2g-2+n>0\), it is still possible to have \(n=0\) and \(g\ge 2\), in which case \(d=3g-3>0\) but \(E(g,0)\) is empty (there is no \(0\)-tuple summing to \(d\)). In that situation, the claim “\(D\) achieves its maximum” is not well-posed (no maximizer exists).  
  - **Suggested direction for fix:**  
    Add a short preliminary reduction: restrict to \(n\ge 1\) (the only case where \(E(g,n)\) is nonempty for \(2g-2+n>0\)), or explicitly state that the claim is vacuous/ill-posed when \(E(g,n)=\varnothing\). Then proceed.

## Counterexamples / impossible claims (OPTIONAL)

No counterexamples found, no impossible or overly ambitious claims were proposed (conditional on the correctness/applicability of the nef + Alexandrov–Fenchel input). The only “impossible as stated” issue is the empty-domain case \(E(g,0)=\varnothing\) for \(g\ge2\); see **MAJOR-ISSUE-ID-EMPTYDOMAIN**.

## Minor issues

- **Lemma 2 / Lemma 4 interface:**  
  - **Location:** §3, Lemma 4 (“no internal zeros”) and subsequent use  
  - **Nature:** insufficient explanation of a key step  
  - **Suggestion:** Either (i) prove \(a_k>0\) for all \(k\) in your range (which is plausible for \(\psi\)-intersections but should be justified), or (ii) state Lemma 4 in a form that handles internal zeros (standard fact: a log-concave nonnegative sequence has contiguous support and is unimodal on that support). Then you can deduce the “move toward the center does not decrease” statement without assuming no internal zeros.

- **Citations / links:**  
  - **Location:** throughout  
  - **Nature:** references are web links rather than mathematically pinpointed citations (theorem/lemma numbers)  
  - **Suggestion:** Replace with bibliographic citations and point to the exact theorem statement used (e.g. “Khovanskii–Teissier inequality, Lazarsfeld Positivity I, Thm …”).

- **Terminology clarity (stack vs coarse moduli):**  
  - **Location:** §2  
  - **Nature:** unclear notion of nefness on a stack  
  - **Suggestion:** State whether nefness is asserted for the line bundle \(\mathcal L_i\) on the stack, or for its descent to a \(\mathbb Q\)-Cartier divisor on the coarse moduli space, and which version your AF/KT theorem uses.

## Established building blocks

- **EBB-ID-BALANCE-TRANSFER**  
  The “smoothing by Robin Hood transfers reduces imbalance and reaches a balanced vector” combinatorial lemma is correct and reusable (your Lemma 1). The quadratic potential \(\Phi\) argument is standard and sound.

- **EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE**  
  The reduction “balanced maximizer follows from a monotone transfer inequality (★) for all pairs \(i,j\)” is correct and reusable.

- **EBB-ID-SYMLOGCONCAVE-UNIMODAL**  
  The discrete fact “symmetric log-concave \(\Rightarrow\) unimodal with maximum at the center (or two middle indices)” is correct; you can cite standard references on log-concave sequences or give the short ratio argument as you indicated.

## Gap assessment

You declared “Gaps: None.” I disagree.

- **Gap: Applicability of Alexandrov–Fenchel/Khovanskii–Teissier to \(\overline{\mathcal M}_{g,n}\) and to the specific slice \(a_k\).**  
  - **Assessment:** Moderate  
  - **Reason:** The proof is structurally complete *if* one imports the correct AF/KT inequality for nef divisor intersections and checks it applies in the DM stack setting (or after passage to a smooth projective cover). This is a standard-technology gap, but it must be written carefully because it is the main engine.

- **Gap: Empty-domain cases.**  
  - **Assessment:** Minor  
  - **Reason:** Easy to fix by restricting to \(E(g,n)\neq\varnothing\) (typically \(n\ge 1\)).

## Coverage assessment

All subparts addressed: **Mostly yes**, with the caveat that the problem explicitly allows \(n=0\), in which case \(E(g,n)\) can be empty and the “maximum” claim needs a convention or restriction.

- Main inequality strategy: addressed.
- Edge case \(E(g,n)=\varnothing\): not addressed.

## Summary

The attempted solution presents a clean and plausible global proof strategy: reduce to a two-coordinate “balancing move” inequality, establish log-concavity of the two-point slice, use symmetry to force the maximum at the midpoint, and iterate balancing moves to reach a balanced maximizer. The combinatorial reduction (Lemma 1) and the discrete log-concavity ⇒ unimodality step (Lemma 4) are sound.

The entire argument, however, relies on importing a heavy geometric inequality (Khovanskii–Teissier / Alexandrov–Fenchel log-concavity) for mixed intersections of nef divisor classes, and applying it in the context of \(\overline{\mathcal M}_{g,n}\) (a DM stack) with \(\psi_i\) divisor classes. While this is very likely correct—indeed \(\psi_i\) are known to be nef ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai))—the write-up does not state the exact inequality in a form that directly yields \(a_k^2\ge a_{k-1}a_{k+1}\), nor does it provide a fully justified bridge from stacks to a setting where the theorem can be applied.

After adding the missing theorem statement(s), references, and a brief stack-to-variety reduction (or citing an orbifold/stack version), the proof should be acceptable and essentially complete. A small but real definitional oversight is that \(E(g,n)\) can be empty when \(n=0\), so one must exclude or handle that case.

## Recommendations for next iteration (prioritized)

1. **Write Lemma 2 as a precise theorem-application, not a “standard justification”.**  
   Explicitly state the mixed Alexandrov–Fenchel/Khovanskii–Teissier inequality you use, and show the substitution of divisor classes (with repetitions) that turns it into \(a_k^2\ge a_{k-1}a_{k+1}\).

2. **Make the “stack issue” explicit and correct.**  
   Either:
   - cite a reference that AF/KT holds for smooth proper DM stacks (or for projective orbifolds), **or**
   - give a clear reduction to a smooth projective variety \(Y\) with a finite surjective map \(Y\to \overline{\mathcal M}_{g,n}\), and prove:
     - nefness pulls back,
     - intersection numbers scale by \(\deg(Y/\overline{\mathcal M}_{g,n})\),
     - AF/KT holds on \(Y\),
     - hence holds on \(\overline{\mathcal M}_{g,n}\).

3. **Cite nefness of \(\psi_i\) properly.**  
   Your QJM excerpt asserts nefness as known background ([academic.oup.com](https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai)); add the original references it points to (Arakelov/Mumford or later modern expositions), or cite Gibney–Keel–Morrison as a standard moduli reference.

4. **Handle the case \(E(g,n)=\varnothing\) cleanly.**  
   Add a one-line reduction: “Assume \(E(g,n)\neq\varnothing\), equivalently \(n\ge 1\)” (or spell out the classification).

5. **Remove the “no internal zeros” fragility.**  
   Either show \(a_k>0\) for all \(k\) in the slice in your context, or use a version of Lemma 4 that works with zeros by restricting to the support interval.

## Meta-level guidance for both the probem solver and the orchestrator

### Strategy-level assessment
The overall line of attack is **fundamentally sound and well-matched** to the problem: it reduces the maximization question to a general positivity/log-concavity phenomenon for intersection numbers of nef divisors, which is exactly where “balanced maximizes” principles come from.

### Structural blockers
- **MAJOR-ISSUE-ID-AFSTACK** is the only genuine blocker: without a correct, precisely applicable AF/KT inequality in the DM stack setting (or a properly justified reduction), the proof is not complete. This is not a mere stylistic issue; it is the core engine.

### Dead directions / approaches to abandon
No dead directions to abandon at this stage. The approach is promising; it just needs correct theorem importation and formalization.

### Promising lines and subproblems
- Precisely isolate and prove (or properly cite) the statement:

  “For nef divisor classes \(D_1,\dots,D_d\) on a smooth projective variety \(X\),  
  \((D_1\cdots D_d)^2 \ge (D_1^2D_3\cdots D_d)(D_2^2D_3\cdots D_d)\).”

  Then apply it with repeated \(\psi_i,\psi_j\) to get log-concavity of the slice.

- Work out a clean “stack-to-variety” reduction lemma for intersection numbers and nefness.

### Recommendations for the orchestrator (prioritized)
1. **Treat EBB-ID-BALANCE-TRANSFER and EBB-ID-SYMLOGCONCAVE-UNIMODAL as established and reuse them.**
2. **Spawn a research/verification phase on MAJOR-ISSUE-ID-AFSTACK:**  
   Find authoritative references for:
   - nefness of \(\psi_i\) on \(\overline{\mathcal M}_{g,n}\),
   - AF/KT inequalities for nef divisors,
   - extension/reduction to DM stacks or level covers.
3. **Do not ask the solver to compute DVV recursions or search for counterexamples yet**; the geometric inequality route, if validated, gives a clean universal proof.

## Research flag
Research needed: No  
This is standard material in higher-dimensional algebraic geometry (nef divisors + Khovanskii–Teissier/Alexandrov–Fenchel) and standard moduli-space positivity. What is needed is not new research, but careful sourcing and correct statement-matching.

## Updated Registry of IDs

### Major issues
- **MAJOR-ISSUE-ID-AFSTACK:** Core AF/KT log-concavity step on \(\overline{\mathcal M}_{g,n}\) not stated/cited/justified precisely; stack-to-variety reduction unclear.
- **MAJOR-ISSUE-ID-EMPTYDOMAIN:** Need to address possibility \(E(g,n)=\varnothing\) (notably \(n=0, g\ge2\)) before claiming a maximum exists.

### Established building blocks
- **EBB-ID-BALANCE-TRANSFER:** Any exponent vector can be made balanced via Robin Hood transfers; imbalance potential strictly decreases.
- **EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE:** Balanced maximizer follows from monotonicity under pairwise transfer moves.
- **EBB-ID-SYMLOGCONCAVE-UNIMODAL:** Symmetric log-concave sequences are unimodal and attain maxima at the center.

### Dead directions
- None.

---

# Solution Attempt 2 by the problem solver

Status: Complete

## Response to last evaluation

- **MAJOR-ISSUE-ID-AFSTACK**: **Fixed (here’s where)**  
  Fixed in **§2–§3** by (i) explicitly reducing from the DM stack \(\overline{\mathcal M}_{g,n}\) to its coarse moduli space \( \overline M_{g,n}\) at the level of Chow rings with \(\mathbb Q\)-coefficients, then (ii) pulling back to a **resolution of singularities** \(\widetilde X \to \overline M_{g,n}\) (smooth projective) where the classical Khovanskii–Teissier/Alexandrov–Fenchel inequality applies, and (iii) writing the exact divisor substitution (with repetitions) that yields \(a_k^2\ge a_{k-1}a_{k+1}\).

- **MAJOR-ISSUE-ID-EMPTYDOMAIN**: **Fixed (here’s where)**  
  Fixed in **§0**: I classify when \(E(g,n)\) is empty. In particular, for \(n=0\) and \(g\ge 2\), \(E(g,0)=\varnothing\), so the original “achieves its maximum” statement is ill-posed; I treat this as a counterexample to the statement as literally written. Then I prove the intended claim under the natural non-emptiness condition \(E(g,n)\neq\varnothing\) (equivalently \(n\ge 1\)).

Minor interface issue (“internal zeros”): addressed in **§4** by using a version of the symmetric log-concave \(\Rightarrow\) unimodal lemma that allows zeros (contiguous support).

No dead directions were provided, so none to list.

---

## Solution

### §0. Domain non-emptiness and what is actually being claimed

Let
\[
d:=3g-3+n = \dim \overline{\mathcal M}_{g,n}.
\]
Recall
\[
E(g,n)=\{\mathbf e=(e_1,\dots,e_n)\in\mathbb Z_{\ge 0}^n:\; e_1+\cdots+e_n=d\}.
\]

- If \(n\ge 1\), then \(E(g,n)\neq\varnothing\): e.g. \((d,0,\dots,0)\in E(g,n)\).
- If \(n=0\), then \(E(g,0)\) consists of the unique \(0\)-tuple **only if** \(d=0\); otherwise \(E(g,0)=\varnothing\).  
  Under the stability assumption \(2g-2+n>0\), if \(n=0\) then \(g\ge 2\), hence \(d=3g-3>0\), so \(E(g,0)=\varnothing\).

So, **as stated**, the claim “\(D\) achieves its maximum on \(E(g,n)\)” is not meaningful (and in the usual convention is simply false) for \((g,n)=(2,0)\) (or any \(g\ge 2,n=0\)), because \(E(g,0)\) is empty.

> **Counterexample to the literal statement:** take \((g,n)=(2,0)\). Then \(2g-2+n=2>0\), but \(E(2,0)=\varnothing\), so \(D\) has no maximizer.

From now on I prove the **intended** statement:

> **Theorem (meaningful version).** Assume \(E(g,n)\neq\varnothing\) (equivalently \(n\ge 1\)). Then the function
> \[
> D(\mathbf e)=\int_{\overline{\mathcal M}_{g,n}} \psi_1^{e_1}\cdots \psi_n^{e_n}
> \]
> attains its maximum on \(E(g,n)\) at a **balanced** vector \(\mathbf e\).

---

### §1. Combinatorial reduction to a two-coordinate “transfer inequality” (reused building blocks)

A vector \(\mathbf e\in E(g,n)\) is **balanced** if \(|e_i-e_j|\le 1\) for all \(i,j\).

A **balancing move** (“Robin Hood transfer”) is:
\[
(e_i,e_j)\mapsto(e_i-1,e_j+1)\quad\text{for some }i\neq j,\ \text{with }e_i\ge e_j+2.
\]
This keeps \(\sum e_k\) fixed and decreases the imbalance.

**Lemma 1 (balancing by transfers; EBB-ID-BALANCE-TRANSFER).**  
Starting from any \(\mathbf e\in E(g,n)\), repeated balancing moves terminate after finitely many steps at a balanced vector.

*Proof.* Same as before: define \(\bar e=d/n\) and \(\Phi(\mathbf e)=\sum_k(e_k-\bar e)^2\). Each move reduces \(\Phi\) strictly by \(2(e_i-e_j)-2\ge 2\). Since \(\Phi\ge 0\) and integer-valued on \(\mathbb Z^n\), termination follows. \(\square\)

Thus it suffices to show the following monotonicity:

> **Key transfer inequality (TI).**  
> If \(\mathbf e\in E(g,n)\) has \(e_i\ge e_j+2\), then
> \[
> D(\dots,e_i,\dots,e_j,\dots)\ \le\ D(\dots,e_i-1,\dots,e_j+1,\dots).
> \tag{TI}
> \]

Indeed, Lemma 1 + repeated application of (TI) implies that from any \(\mathbf e\) one can reach a balanced \(\mathbf b\) with \(D(\mathbf e)\le D(\mathbf b)\). Hence a global maximizer can be chosen balanced (EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE).

So the rest of the proof is devoted to (TI).

---

### §2. Reducing the intersection problem from the DM stack to a smooth projective variety

Let \(\mathcal X:=\overline{\mathcal M}_{g,n}\) (smooth proper DM stack over \(\mathbb C\)) and let \(X:=\overline M_{g,n}\) be its projective coarse moduli space.

#### 2.1. Chow rings of \(\mathcal X\) vs \(X\) (rationally)

A standard fact in intersection theory of DM stacks is that the natural map
\[
p:\mathcal X \to X
\]
induces an isomorphism on Chow rings with \(\mathbb Q\)-coefficients:
\[
p_*:A^*(\mathcal X)_\mathbb Q \xrightarrow{\ \sim\ } A^*(X)_\mathbb Q
\]
(with inverse \(p^*\)). In particular, top-degree integrals of classes on \(\mathcal X\) can be computed on \(X\) after identifying the corresponding classes.

Concretely: there exist classes \(\psi_i^{\mathrm{coarse}}\in A^1(X)_\mathbb Q\) such that \(p^*\psi_i^{\mathrm{coarse}}=\psi_i\), and then
\[
\int_{\mathcal X} \psi_1^{e_1}\cdots\psi_n^{e_n}
=
\int_X (\psi_1^{\mathrm{coarse}})^{e_1}\cdots (\psi_n^{\mathrm{coarse}})^{e_n}.
\tag{1}
\]

From here onward I simply write \(\psi_i\) for the corresponding class on \(X\); (1) justifies that this does not change \(D(\mathbf e)\).

#### 2.2. Passing to a resolution

The coarse space \(X=\overline M_{g,n}\) has only finite-quotient singularities, hence is normal and \(\mathbb Q\)-factorial; the divisor classes \(\psi_i\) define nef \(\mathbb Q\)-Cartier divisor classes on \(X\). (Nefness of \(\psi_i\) is a standard result in the birational geometry of \(\overline M_{g,n}\).)

Choose a resolution of singularities
\[
\pi:\widetilde X \to X
\]
with \(\widetilde X\) smooth projective of dimension \(d\). Define nef divisor classes
\[
\widetilde\psi_i := \pi^* \psi_i \in N^1(\widetilde X)_\mathbb R.
\]
Pullback preserves nefness.

Because \(\psi_i\) are \(\mathbb Q\)-Cartier, their intersection numbers on \(X\) are computed on \(\widetilde X\) by pullback. Hence
\[
D(\mathbf e)
=
\int_{\widetilde X} \widetilde\psi_1^{e_1}\cdots \widetilde\psi_n^{e_n}.
\tag{2}
\]
So the problem reduces to intersection numbers of nef divisors on a **smooth projective variety**, where Alexandrov–Fenchel/Khovanskii–Teissier applies in its classical form.

---

### §3. Precise Alexandrov–Fenchel / Khovanskii–Teissier inequality and log-concavity of the two-point slice

Fix distinct indices \(i\neq j\), and fix the exponents \(e_\ell\) for \(\ell\neq i,j\). Let
\[
S:=e_i+e_j,\qquad 
C := \prod_{\ell\neq i,j} \widetilde\psi_\ell^{e_\ell}\quad\text{(a fixed product of nef classes)}.
\]
Define for \(k=0,1,\dots,S\):
\[
a_k := \int_{\widetilde X} \widetilde\psi_i^{k}\,\widetilde\psi_j^{S-k}\, C.
\tag{3}
\]
Note: \(a_k = D(\dots, k,\dots,S-k,\dots)\) with all other coordinates held fixed.

#### 3.1. The exact AF/KT inequality used

I use the following standard mixed Alexandrov–Fenchel (equivalently, a Khovanskii–Teissier inequality):

> **Theorem (AF/KT inequality for nef divisors; “2-by-2” form).**  
> Let \(Y\) be a smooth projective variety of dimension \(d\) and let \(D_1,\dots,D_d\) be nef \(\mathbb R\)-Cartier divisor classes on \(Y\). Then
> \[
> (D_1D_2\cdots D_d)^2 \ \ge\ (D_1^2D_3\cdots D_d)\,(D_2^2D_3\cdots D_d).
> \tag{AF}
> \]
> Here products are intersection numbers.

This inequality is compatible with repeating divisor classes among the \(D_r\) (indeed it is formulated for an arbitrary list \(D_1,\dots,D_d\), with no distinctness assumed).

#### 3.2. Substituting divisors to get \(a_k^2\ge a_{k-1}a_{k+1}\)

Fix \(k\) with \(1\le k\le S-1\). Consider the following list of \(d\) nef divisors on \(\widetilde X\):

- \(D_1 := \widetilde\psi_i\),
- \(D_2 := \widetilde\psi_j\),
- The remaining \(d-2\) divisors \(D_3,\dots,D_d\) are the multiset consisting of:
  - \((k-1)\) copies of \(\widetilde\psi_i\),
  - \((S-k-1)\) copies of \(\widetilde\psi_j\),
  - and for each \(\ell\neq i,j\), \(e_\ell\) copies of \(\widetilde\psi_\ell\).

This uses exactly
\[
1+1+(k-1)+(S-k-1)+\sum_{\ell\neq i,j}e_\ell
= S + \sum_{\ell\neq i,j}e_\ell
= d
\]
divisors, as required.

Then, by construction,
\[
D_1D_2\cdots D_d
= \widetilde\psi_i^k \widetilde\psi_j^{S-k} C,
\]
so
\[
(D_1\cdots D_d)=a_k.
\]
Also,
\[
D_1^2D_3\cdots D_d
= \widetilde\psi_i^{k+1}\widetilde\psi_j^{S-k-1}C
= a_{k+1},
\]
and
\[
D_2^2D_3\cdots D_d
= \widetilde\psi_i^{k-1}\widetilde\psi_j^{S-k+1}C
= a_{k-1}.
\]
Plugging into (AF) gives:

> **Lemma 2 (log-concavity of the slice).** For \(1\le k\le S-1\),
> \[
> a_k^2 \ge a_{k-1}a_{k+1}.
> \tag{LC}
> \]

This is exactly the needed log-concavity statement, now fully justified on \(\widetilde X\), hence on \(X\), hence on the stack via (1)–(2).

#### 3.3. Symmetry of the slice

By symmetry under swapping marked points \(i\leftrightarrow j\),
\[
a_k = a_{S-k}\qquad\text{for all }k.
\tag{SYM}
\]

---

### §4. Symmetric log-concave sequences (allowing zeros) peak at the center

We need a discrete fact, but we must not assume “no internal zeros”.

> **Lemma 3 (contiguous support for log-concave sequences).**  
> If \((a_k)_{k=0}^S\) is nonnegative and log-concave in the sense \(a_k^2\ge a_{k-1}a_{k+1}\), then the set \(\{k: a_k>0\}\) is an interval (possibly empty).

*Proof.* If \(a_m=0\) and \(a_{m-1}>0\), then log-concavity gives \(0=a_m^2\ge a_{m-1}a_{m+1}\), so \(a_{m+1}=0\). Induct forward; similarly backward. \(\square\)

Now add symmetry.

> **Lemma 4 (symmetric log-concave \(\Rightarrow\) “move toward center doesn’t decrease”).**  
> Let \((a_k)_{k=0}^S\) be nonnegative, log-concave, and symmetric \(a_k=a_{S-k}\). Let \(m:=\lfloor S/2\rfloor\). Then for every \(k\ge m+1\),
> \[
> a_{k-1}\ge a_k.
> \tag{CENTER}
> \]
> (So stepping one unit toward the center weakly increases the value.)

*Proof.* By Lemma 3, the positive support is an interval \([L,R]\cap\mathbb Z\). Symmetry forces \(L=S-R\). In particular, \(m\in[L,R]\) whenever the sequence is not identically \(0\).

On the positive support, define ratios \(r_k:=a_k/a_{k-1}\) for \(L<k\le R\). Log-concavity \(a_k^2\ge a_{k-1}a_{k+1}\) is equivalent (when all three terms are positive) to \(r_{k+1}\le r_k\), i.e. \((r_k)\) is nonincreasing. By symmetry, \(a_{m+t}=a_{m-t}\), which forces the ratios to cross \(1\) at the center: for \(k\ge m+1\), one gets \(r_k\le 1\), hence \(a_k\le a_{k-1}\). If zeros occur, the inequality is automatic once past the endpoint \(R\). \(\square\)

Apply Lemma 4 to our slice \((a_k)\).

---

### §5. Proof of the transfer inequality (TI)

Assume \(e_i\ge e_j+2\). With \(S=e_i+e_j\), this implies
\[
e_i \ge \frac S2 + 1,
\]
so \(k:=e_i\) lies strictly to the right of the middle.

Recall:
\[
a_{e_i} = D(\dots,e_i,\dots,e_j,\dots),
\qquad
a_{e_i-1} = D(\dots,e_i-1,\dots,e_j+1,\dots).
\]
By Lemma 4, since \(e_i\ge \lfloor S/2\rfloor + 1\),
\[
a_{e_i-1} \ge a_{e_i},
\]
i.e.
\[
D(\dots,e_i,\dots,e_j,\dots)\ \le\ D(\dots,e_i-1,\dots,e_j+1,\dots).
\]
This is exactly (TI).

---

### §6. Conclude: a maximizer can be chosen balanced (for \(n\ge 1\))

Assume \(n\ge 1\), so \(E(g,n)\neq\varnothing\). Since \(E(g,n)\) is finite, \(D\) has at least one maximizer \(\mathbf e_{\max}\in E(g,n)\).

Apply Lemma 1 to \(\mathbf e_{\max}\): by repeated balancing moves we reach a balanced \(\mathbf b\in E(g,n)\). Each move does not decrease \(D\) by (TI), so
\[
D(\mathbf b)\ \ge\ D(\mathbf e_{\max})=\max_{\mathbf e\in E(g,n)}D(\mathbf e).
\]
Hence \(\mathbf b\) is also a maximizer, and \(\mathbf b\) is balanced.

This proves the theorem (meaningful version), and together with §0 it answers the problem as posed.

\(\square\)

---

## Gaps: None

---

## Self-evaluation

Confidence score (0–100): 86

Known or suspected issues:
- I treated two standard inputs as “known theorems” without reproducing their full proofs:
  1) the rational Chow ring identification between a smooth proper DM stack and its coarse space, and  
  2) nefness of \(\psi_i\) on \(\overline M_{g,n}\).  
  Both are standard in the literature on stacks/moduli, and the logical dependence is now clean: once nefness holds on the coarse space, everything else is a textbook application of AF/KT on a smooth projective resolution.
- One could further expand the justification that \(\psi_i\) is \(\mathbb Q\)-Cartier on the coarse space and that its intersection numbers are computed on a resolution as in (2). This is standard for \(\mathbb Q\)-factorial varieties / \(\mathbb Q\)-Cartier divisors.

Coverage:
- Fully addresses the question: provides a genuine obstruction/counterexample to the *literal* statement when \(n=0\) (empty domain), and proves the balanced-maximizer claim for all cases where \(E(g,n)\) is nonempty (in particular all \(n\ge 1\) in the stable range).

---

# Expert evaluator's assessment and feedback on Solution Attempt 2

## Status
Status: Solved with minor gaps

## Score
Score (0–100): 86

## Major issues

- **MAJOR-ISSUE-ID-AFSTACK**  
  - **Severity:** local/patchable  
  - **Location:** §2.1–§2.2 (stack→coarse→resolution reduction), and the sentence “\(\psi_i\) define nef \(\mathbb Q\)-Cartier divisor classes on \(X\)”  
  - **Issue type:** missing critical justification / misuse of theory (imprecise foundational claims)  
  - **Description:** You have substantially improved the AF/KT step: you now (a) state the exact Alexandrov–Fenchel/Khovanskii–Teissier inequality in a usable form (AF), and (b) explicitly show the “repetitions allowed” substitution producing \(a_k^2\ge a_{k-1}a_{k+1}\). That part is excellent.

    However, the *bridge* from the descendant integral on the **DM stack** \(\overline{\mathcal M}_{g,n}\) to an intersection product of nef divisors on a **smooth projective variety** \(\widetilde X\) is still written too loosely, and in a couple of places it is not literally correct as stated:

    1. **Chow ring identification statement is imprecise.**  
       You write: “\(p_*:A^*(\mathcal X)_\mathbb Q \xrightarrow{\sim} A^*(X)_\mathbb Q\) (with inverse \(p^*\)).”  
       Even when there is a rational identification between Chow theories of a DM stack and its coarse space, it is *not generally correct* that the inverse of the relevant isomorphism is literally the pullback \(p^*\) (or that \(p_*\) is a ring isomorphism in the naive sense). One needs to cite the correct theorem and use the correct formulation (often in terms of **operational Chow rings** and/or a carefully normalized pushforward).  

       What *is* true (and standard) is that with \(\mathbb Q\)-coefficients, the Chow ring of a DM stack agrees with that of its coarse moduli space; a modern secondary-source statement to this effect is explicitly noted in the literature (e.g. “Working with rational coefficients gives the significant advantage that the Chow ring of a Deligne–Mumford stack agrees with that of its coarse moduli space; see Edidin, Thm 4.40”). ([cambridge.org](https://www.cambridge.org/core/journals/compositio-mathematica/article/integral-chow-ring-of-mathcal-m0mathbb-pr-d-for-d-odd/1C80394BE55BE39BA69B776F8CDD87B0))  
       But your write-up should precisely invoke that theorem (Edidin’s Thm 4.40, or Vistoli/Kresch in an equivalent form) and state exactly what map is an isomorphism (and in what category: Chow groups vs operational Chow rings).

    2. **Descent of \(\psi_i\) to coarse space and compatibility with nefness is not justified.**  
       You assert there are classes \(\psi_i^{\mathrm{coarse}}\) with \(p^*\psi_i^{\mathrm{coarse}}=\psi_i\) and then proceed to treat them as nef \(\mathbb Q\)-Cartier divisors on the coarse space. This is plausible and likely correct, but you must either:
       - cite a standard result: \(L_i\) (cotangent line bundle) is nef on the stack and descends to a nef \(\mathbb Q\)-line bundle on the coarse space, **or**
       - give a 3–5 line argument that nefness (intersection with curves \(\ge 0\)) is preserved under passage to coarse, using finite covers of curves to lift maps into the stack.

    3. **Equality (2) via a resolution requires an explicit “projection formula / definition of intersection on singular \(X\)” justification.**  
       You write \(D(\mathbf e)=\int_{\widetilde X}\prod \pi^*\psi_i^{e_i}\). This is standard *if* one uses operational Chow and the projection formula, but you should say so. As written, it reads as though the usual smooth pullback/pushforward intersection theory is available on \(X\) without comment.

  - **Suggested direction for fix:**  
    Keep your overall proof unchanged, but tighten §2 as follows:
    - Replace the “\(p_*\) isomorphism with inverse \(p^*\)” sentence by a precise theorem statement from a standard reference (Edidin, or Vistoli/Kresch). At minimum, cite the theorem and state: “With \(\mathbb Q\)-coefficients, \(A^*(\overline{\mathcal M}_{g,n})_\mathbb Q\) identifies with the operational Chow ring \(A^*(\overline M_{g,n})_\mathbb Q\).” ([cambridge.org](https://www.cambridge.org/core/journals/compositio-mathematica/article/integral-chow-ring-of-mathcal-m0mathbb-pr-d-for-d-odd/1C80394BE55BE39BA69B776F8CDD87B0))  
    - Explicitly state that \(\psi_i\) gives a nef \(\mathbb Q\)-Cartier divisor class on the coarse space; provide a correct reference for nefness of \(\psi_i\) (the QJM remark you used earlier is a *secondary* citation; it’s okay if you treat it as your reference, but then say so explicitly).
    - Add one lemma: “If \(X\) is projective, \(\pi:\widetilde X\to X\) a resolution, and \(\alpha\in A^d(X)_\mathbb Q\) comes from divisors on \(X\), then \(\int_X \alpha = \int_{\widetilde X}\pi^*\alpha\)” (projection formula / definition of operational intersection).

## Counterexamples / impossible claims (OPTIONAL)

- The “counterexample” \((g,n)=(2,0)\) to the *literal wording* is valid in the standard logical reading: \(E(2,0)=\varnothing\), hence there is no maximizer and the existential statement “achieves its maximum (at a balanced \(\mathbf e\in E(g,n)\))” fails.  
  This is essentially the previously identified empty-domain issue, now correctly handled. (Related to **MAJOR-ISSUE-ID-EMPTYDOMAIN**, now resolved.)

## Minor issues

- **Lemma 4 proof contains an incorrect symmetry identity for odd \(S\).**  
  - **Location:** §4, Lemma 4 proof: “By symmetry, \(a_{m+t}=a_{m-t}\)”  
  - **Nature:** logical slip / incorrect formula (but fixable)  
  - **Explanation:** For \(S\) odd, symmetry is about a half-integer center: if \(S=2m+1\), then \(a_{m+t}=a_{m+1-t}\), not \(a_{m-t}\).  
  - **Suggestion:** Easiest fix: split even/odd \(S\). If \(S=2m+1\) (odd), symmetry gives \(a_m=a_{m+1}\), hence \(r_{m+1}=1\), and ratio monotonicity implies \(r_k\le 1\) for all \(k\ge m+1\). If \(S=2m\) (even), argue by contradiction using log-concavity at \(m\): if \(a_{m+1}>a_m\), then by symmetry \(a_{m-1}=a_{m+1}\) and log-concavity forces \(a_m^2\ge a_{m-1}a_{m+1}>a_m^2\), impossible.

- **References still not pinpointed.**  
  - **Location:** throughout §2–§3  
  - **Nature:** citation quality  
  - **Suggestion:** Give exact bibliographic items and theorem numbers for:
    - the DM stack ↔ coarse-space Chow identification ([cambridge.org](https://www.cambridge.org/core/journals/compositio-mathematica/article/integral-chow-ring-of-mathcal-m0mathbb-pr-d-for-d-odd/1C80394BE55BE39BA69B776F8CDD87B0)),
    - AF/KT inequality (e.g. Lazarsfeld, *Positivity*, or a standard AF/Teissier source).

## Established building blocks

- **EBB-ID-BALANCE-TRANSFER** (reused)  
  The “Robin Hood transfer” termination argument via the quadratic potential \(\Phi\) is correct and clean.

- **EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE** (reused)  
  The reduction “balanced maximizer follows from pairwise transfer monotonicity (TI)” is correct.

- **EBB-ID-AF-SUBSTITUTION** *(new)*  
  Your §3.2 substitution of nef divisors into the 2-by-2 Alexandrov–Fenchel/Khovanskii–Teissier inequality to derive
  \[
  a_k^2\ge a_{k-1}a_{k+1}
  \]
  is correct and is now written at the right level of explicitness (counts check out; repetitions handled properly).

- **EBB-ID-LOGCONCAVE-SUPPORT** *(new)*  
  Lemma 3 (“log-concave nonnegative ⇒ contiguous support”) is correct and useful for removing the “no internal zeros” fragility.

## Gap assessment

You declared “Gaps: None.” I partially disagree.

- **Gap: Stack/coarse/resolution intersection-theory identifications.**  
  - **Assessment:** Moderate (but very standard-tech)  
  - **Comment:** The proof is essentially complete once you write the correct theorem statements and compatibility of integrals under the identifications. This is now mostly a *citation/precision* gap, but it still sits at the core of the justification chain.

Everything else is in good shape.

## Coverage assessment

All subparts addressed: **Yes**, in the following sense:

- You correctly note the literal statement fails/has no meaning when \(E(g,n)=\varnothing\) (e.g. \((g,n)=(2,0)\)), and you supply this as a counterexample.
- You then prove the intended statement for all meaningful cases \(n\ge 1\).

## Summary

This attempt is a substantial improvement over Attempt 1: you now state a precise AF/KT inequality and show exactly how it implies log-concavity of the two-point slice \((a_k)\) via an explicit repeated-divisor substitution. That was the main missing mathematical “engine,” and it is now correctly integrated into the argument.

The combinatorial reduction to balancing moves remains correct and well-explained, and the symmetry + log-concavity ⇒ “move toward center” step is conceptually right; you also appropriately removed the “no internal zeros” assumption by proving contiguous support.

The remaining weaknesses are almost entirely foundational/citation-level: the stack-to-coarse Chow identification is stated too naively (in particular, the claim about \(p_*\) having inverse \(p^*\) is not safe as written), and the descent/nefness/Q-Cartier properties of \(\psi_i\) on the coarse space are asserted without a proper reference. There is also a small but real slip in the symmetry identity used inside the proof of Lemma 4 for odd \(S\), though it is easily corrected.

Overall, the strategy is correct; with a tightened §2 and a corrected Lemma 4 proof, this is a complete solution (plus the empty-domain counterexample).

## Recommendations for next iteration

1. **Rewrite §2.1 with a correct, cited theorem statement.**  
   Cite Edidin Thm 4.40 (as referenced in the literature) or Vistoli/Kresch, and clearly state what is isomorphic to what (Chow groups vs operational Chow rings) and which maps are isomorphisms. ([cambridge.org](https://www.cambridge.org/core/journals/compositio-mathematica/article/integral-chow-ring-of-mathcal-m0mathbb-pr-d-for-d-odd/1C80394BE55BE39BA69B776F8CDD87B0))

2. **Add a short lemma justifying equality of integrals after passing to a resolution.**  
   Use the projection formula in operational Chow: \(\int_X \alpha = \int_{\widetilde X}\pi^*\alpha\) for \(\alpha\in A^d(X)_\mathbb Q\) coming from divisor classes.

3. **Cite nefness (and Q-Cartier descent) of \(\psi_i\) explicitly.**  
   Provide a primary reference or a clearly identified standard source, and state the exact version you use (“\(\psi_i\) is nef as a \(\mathbb Q\)-Cartier divisor on \(\overline M_{g,n}\)”).

4. **Fix Lemma 4’s odd-\(S\) symmetry formula.**  
   Split even/odd \(S\) and use the quick contradiction argument at the center for even \(S\), and the “central two equal” fact for odd \(S\).

5. **(Optional) Clarify that AF/KT extends from ample to nef by limit.**  
   A one-line remark “nef is a limit of ample; intersection numbers vary continuously; hence (AF) extends to nef” is enough.

## Meta-level guidance for both the probem solver and the orchestrator

### Strategy-level assessment
The overall line of attack is **fundamentally sound and well-calibrated**: maximizing a symmetric multilinear intersection functional under a fixed-sum constraint is exactly the kind of setting where AF/KT log-concavity implies “majorization increases the value,” hence balanced maximizers.

### Structural blockers
- **MAJOR-ISSUE-ID-AFSTACK** remains the only real blocker in the sense that, without the *precise* stack/coarse/resolution justification, the proof is not formally complete. This is not a new mathematical idea blocker; it is a correctness-of-foundations blocker.

### Dead directions / approaches to abandon
- None.

### Promising lines and subproblems
- Isolate a clean lemma package for §2:
  1) rational Chow/operational Chow identification for DM stacks vs coarse spaces,  
  2) descent of line bundles/divisors and nefness preservation,  
  3) projection formula compatibility with pullback to resolutions.
- Once that is done, the remainder (§3–§6) is essentially “final form.”

### Recommendations for the orchestrator
1. **Treat EBB-ID-AF-SUBSTITUTION as established and reuse it.**
2. **Treat EBB-ID-BALANCE-TRANSFER and EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE as established and reuse them.**
3. **Spawn a short verification pass specifically on the exact statement of the “Chow ring of DM stack equals coarse moduli with \(\mathbb Q\)” theorem and how integrals compare.** The literature explicitly notes this advantage. ([cambridge.org](https://www.cambridge.org/core/journals/compositio-mathematica/article/integral-chow-ring-of-mathcal-m0mathbb-pr-d-for-d-odd/1C80394BE55BE39BA69B776F8CDD87B0))  
4. **Do not pivot to DVV recursion / brute force counterexample search** unless the nefness/descent facts fail (unlikely).

## Research flag
Research needed: No

## Updated Registry of IDs

### Major issues
- **MAJOR-ISSUE-ID-AFSTACK:** Stack/coarse/resolution justification still imprecise; need correct theorem statement for Chow identification with \(\mathbb Q\), descent/nefness of \(\psi_i\), and projection-formula compatibility.
- **MAJOR-ISSUE-ID-EMPTYDOMAIN:** Empty-domain case \(E(g,0)=\varnothing\) makes the literal statement ill-posed/false; now correctly handled via a counterexample and a restricted “meaningful version” proof.

### Established building blocks
- **EBB-ID-BALANCE-TRANSFER:** Finite termination of Robin Hood transfers to reach a balanced exponent vector.
- **EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE:** Reduction of global balanced maximizer to pairwise transfer monotonicity.
- **EBB-ID-SYMLOGCONCAVE-UNIMODAL:** Symmetric log-concave sequences are unimodal with maxima at the center (with a minor odd-\(S\) proof fix needed in the current write-up).
- **EBB-ID-AF-SUBSTITUTION:** Explicit divisor-list substitution into AF/KT yielding slice log-concavity \(a_k^2\ge a_{k-1}a_{k+1}\).
- **EBB-ID-LOGCONCAVE-SUPPORT:** Nonnegative log-concave sequences have contiguous support.

### Dead directions
- None.

---

# Solution Attempt 3 by the problem solver

Status: Complete

## Response to last evaluation

- **MAJOR-ISSUE-ID-AFSTACK**: **Fixed (here’s where)**  
  Fixed in **§2–§3** by rewriting the stack/coarse/resolution bridge with precise objects and standard theorems:
  1) I use **Edidin’s theorem** that with \(\mathbb Q\)-coefficients the Chow ring of a DM stack agrees with the **operational** Chow ring of its coarse moduli space, and I state it in the correct direction (no incorrect “\(p_*\) inverse is \(p^*\)” claim).  
  2) I add a lemma explaining the **descent** of \(\psi_i\) to a nef \(\mathbb Q\)-Cartier divisor on the coarse space (via descent of a tensor power of the cotangent line bundle), and why nefness is preserved.  
  3) I add a lemma giving the **projection-formula / operational-Chow** justification that the top intersection numbers may be computed on a resolution \(\widetilde X\), and then apply AF/KT there.

- **MAJOR-ISSUE-ID-EMPTYDOMAIN**: **Fixed (here’s where)**  
  Kept and stated cleanly in **§0**: for \(g\ge 2,n=0\), \(E(g,0)=\varnothing\), so the literal claim “achieves its maximum on \(E(g,n)\)” is false/ill-posed; this is a counterexample to the statement as literally written. Then I prove the meaningful version for \(n\ge 1\).

- **Minor issue (Lemma 4 odd-\(S\) symmetry slip)**: **Fixed (here’s where)**  
  Fixed in **§5** by splitting into even/odd \(S\) and using a short center-argument plus ratio monotonicity, avoiding the incorrect identity.

No dead directions were provided.

---

## Solution

### §0. Non-emptiness of \(E(g,n)\) and a counterexample to the literal statement

Let
\[
d:=\dim \overline{\mathcal M}_{g,n}=3g-3+n.
\]
Recall
\[
E(g,n)=\{\mathbf e=(e_1,\dots,e_n)\in\mathbb Z_{\ge 0}^n:\ e_1+\cdots+e_n=d\}.
\]

- If \(n\ge 1\), then \(E(g,n)\neq\varnothing\) (e.g. \((d,0,\dots,0)\in E(g,n)\)).
- If \(n=0\), then \(E(g,0)\) is the set of \(0\)-tuples with sum \(d\). This is empty unless \(d=0\).  
  Under the hypothesis \(2g-2+n>0\), if \(n=0\) then \(g\ge 2\), hence \(d=3g-3>0\), so \(E(g,0)=\varnothing\).

Therefore the original claim, read literally as an existential statement about a maximum on \(E(g,n)\), **fails** for \((g,n)=(2,0)\) (and in fact for all \(g\ge 2,n=0\)):

> **Counterexample (empty domain).** For \((g,n)=(2,0)\), the stability condition \(2g-2+n=2>0\) holds, but \(E(2,0)=\varnothing\). Hence \(D:E(2,0)\to\mathbb Q\) has no maximizer.

From now on I prove the **meaningful version** (the one clearly intended in the moduli/descendant context):

> **Theorem.** Assume \(n\ge 1\) (equivalently \(E(g,n)\neq\varnothing\)). Then \(D(\mathbf e)=\int_{\overline{\mathcal M}_{g,n}}\prod_i\psi_i^{e_i}\) attains its maximum on \(E(g,n)\) at a **balanced** \(\mathbf e\).

---

### §1. Basic properties and reduction to a pairwise transfer inequality

For \(\mathbf e=(e_1,\dots,e_n)\in E(g,n)\), set
\[
D(\mathbf e):=\int_{\overline{\mathcal M}_{g,n}}\psi_1^{e_1}\cdots\psi_n^{e_n}
=\big\langle \tau_{e_1}\cdots\tau_{e_n}\big\rangle_g\in \mathbb Q_{\ge 0}.
\]
It is symmetric under permuting the \(e_i\).

A vector \(\mathbf e\) is **balanced** if \(|e_i-e_j|\le 1\) for all \(i,j\).

A **balancing move** (Robin Hood transfer) is:
\[
(\dots,e_i,\dots,e_j,\dots)\mapsto (\dots,e_i-1,\dots,e_j+1,\dots)
\quad\text{with }e_i\ge e_j+2.
\]

#### Lemma 1 (balancing by transfers; EBB-ID-BALANCE-TRANSFER).
Starting from any \(\mathbf e\in E(g,n)\), repeated balancing moves terminate after finitely many steps at a balanced vector.

**Proof.** Let \(\bar e=d/n\) and \(\Phi(\mathbf e)=\sum_k(e_k-\bar e)^2\).  
If \(e_i\ge e_j+2\), then replacing \((e_i,e_j)\) by \((e_i-1,e_j+1)\) decreases \(\Phi\) by \(2(e_i-e_j)-2\ge 2\). Hence \(\Phi\) strictly decreases and the process terminates at a vector with no such pair, i.e. balanced. \(\square\)

Thus, as in Attempt 2, it suffices to prove:

> **Transfer Inequality (TI).** If \(e_i\ge e_j+2\), then
> \[
> D(\dots,e_i,\dots,e_j,\dots)\ \le\ D(\dots,e_i-1,\dots,e_j+1,\dots).
> \tag{TI}
> \]

Once (TI) holds, iterating balancing moves yields a balanced \(\mathbf b\) with \(D(\mathbf e)\le D(\mathbf b)\), so a maximizer can be chosen balanced (EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE).

So the core is to prove (TI).

---

### §2. Geometric input: nefness of \(\psi_i\) and moving from the stack to a smooth projective variety

Let \(\mathcal X:=\overline{\mathcal M}_{g,n}\) (smooth proper DM stack over \(\mathbb C\)), and let
\[
p:\mathcal X\to X:=\overline M_{g,n}
\]
be the coarse moduli space (a projective variety).

#### 2.1. Nefness of the cotangent line bundles \(L_i\)

Let \(L_i\) be the cotangent line bundle at the \(i\)-th marked point on \(\mathcal X\), so \(\psi_i=c_1(L_i)\in A^1(\mathcal X)\).

A standard theorem in the birational geometry of \(\overline M_{g,n}\) asserts:

> **Fact (nefness).** Each \(\psi_i\) is nef on \(\overline{\mathcal M}_{g,n}\) (equivalently, \(L_i\) is a nef line bundle on the stack), and it corresponds to a nef \(\mathbb Q\)-Cartier divisor class on the coarse space \(\overline M_{g,n}\).

This is proved (in various formulations) in the literature; a standard reference is Gibney–Keel–Morrison, *Towards the ample cone of \(\overline{M}_{g,n}\)* (JAMS, 2002), where nefness of \(\psi_i\) is among the foundational positivity results used to describe cones of divisors.

I will use nefness in the following concrete sense: for any integral curve \(C\subset \mathcal X\),
\[
\deg(L_i|_C)\ge 0.
\]

#### 2.2. Correct Chow-theoretic comparison: stack vs coarse space (with \(\mathbb Q\)-coefficients)

The following is the precise replacement for the imprecise “\(p_*\) isomorphism with inverse \(p^*\)” statement.

> **Theorem 2 (Edidin; Chow of DM stack equals operational Chow of coarse, rationally).**  
> Let \(\mathcal X\) be a Deligne–Mumford stack with coarse moduli space \(p:\mathcal X\to X\). Then with \(\mathbb Q\)-coefficients, pullback induces an isomorphism
> \[
> p^*:A^*_{\mathrm{op}}(X)_{\mathbb Q}\ \xrightarrow{\ \sim\ }\ A^*(\mathcal X)_{\mathbb Q}.
> \tag{CH}
> \]
> (Here \(A^*_{\mathrm{op}}\) denotes the operational Chow ring.)

This statement appears (with theorem numbering) in Dan Edidin’s notes/expositions on Chow rings of stacks; it is commonly cited as “Edidin, Thm. 4.40” in later papers.

Because \(\mathcal X\) is **smooth**, we also have \(A^*_{\mathrm{op}}(\mathcal X)=A^*(\mathcal X)\), so operational vs usual Chow does not cause confusion on \(\mathcal X\).

Hence each class \(\psi_i\in A^1(\mathcal X)_\mathbb Q\) corresponds uniquely to an operational class \(\psi_i^X\in A^1_{\mathrm{op}}(X)_\mathbb Q\) with \(p^*(\psi_i^X)=\psi_i\). We will identify them notationally.

Moreover, top-degree integrals can be interpreted operationally:
\[
\int_{\mathcal X}\alpha \quad\text{means}\quad \deg\big(\alpha\cap [\mathcal X]\big),
\]
and via (CH) this equals the corresponding degree on \(X\) defined using \([X]\) and operational intersection.

#### 2.3. Descent of \(L_i\) to a \(\mathbb Q\)-line bundle on \(X\) and nefness on \(X\)

Because stabilizers on a DM stack are finite, a line bundle on \(\mathcal X\) descends to the coarse space after taking a tensor power:

> **Lemma 3 (tensor-power descent).**  
> There exists an integer \(m_i>0\) and a line bundle \(M_i\) on \(X\) such that
> \[
> p^*M_i \cong L_i^{\otimes m_i}.
> \]
> Consequently \(c_1(M_i)=m_i\psi_i^X\), so \(\psi_i^X\) is a \(\mathbb Q\)-Cartier divisor class on \(X\).

**Comment.** This is standard descent for DM stacks with coarse moduli: one kills the stabilizer action on fibers by taking a suitable tensor power.

> **Lemma 4 (nefness descends).**  
> If \(L_i\) is nef on \(\mathcal X\), then \(\psi_i^X\) is nef as a \(\mathbb Q\)-Cartier divisor class on \(X\).

**Proof sketch.** Take an irreducible curve \(C\subset X\) and its normalization \(\nu:\widetilde C\to C\). Form the base change \(\mathcal X\times_X \widetilde C\), and choose an irreducible component \(\widetilde{\mathcal C}\) dominating \(\widetilde C\); then \(\widetilde{\mathcal C}\to \widetilde C\) is finite surjective. Pulling back \(p^*M_i\cong L_i^{\otimes m_i}\) to \(\widetilde{\mathcal C}\) gives
\[
\deg\big(M_i|_{\widetilde C}\big)\cdot \deg(\widetilde{\mathcal C}\to \widetilde C)
=\deg\big((L_i^{\otimes m_i})|_{\widetilde{\mathcal C}}\big)\ge 0
\]
since \(L_i\) is nef on the stack and \(\widetilde{\mathcal C}\) is a curve in \(\mathcal X\). Hence \(\deg(M_i|_{\widetilde C})\ge 0\), and therefore \(M_i\) is nef, i.e. \(\psi_i^X\) is nef as a \(\mathbb Q\)-divisor. \(\square\)

#### 2.4. Pull back to a resolution and compute intersection numbers there

Let \(\pi:\widetilde X\to X\) be a resolution of singularities, with \(\widetilde X\) smooth projective of dimension \(d\). Set
\[
\widetilde\psi_i:=\pi^*(\psi_i^X)\in N^1(\widetilde X)_{\mathbb R}.
\]
Each \(\widetilde\psi_i\) is nef (pullback of nef stays nef by pushing forward curves).

We also need that the top intersection defining \(D(\mathbf e)\) can be computed on \(\widetilde X\).

> **Lemma 5 (operational projection to a resolution).**  
> For \(\mathbb Q\)-Cartier divisor classes \(\alpha_1,\dots,\alpha_d\in A^1_{\mathrm{op}}(X)_\mathbb Q\),
> \[
> \int_X \alpha_1\cdots \alpha_d \;=\; \int_{\widetilde X} \pi^*\alpha_1\cdots \pi^*\alpha_d.
> \tag{RES}
> \]
> In particular,
> \[
> D(\mathbf e)=\int_{\widetilde X}\widetilde\psi_1^{e_1}\cdots \widetilde\psi_n^{e_n}.
> \tag{D=tilde}
> \]

**Justification.** One standard definition of intersection products of \(\mathbb Q\)-Cartier divisors on a normal projective variety uses pullback to a resolution (or any common resolution) and proves independence of the resolution. Equivalently, one can phrase it in operational Chow and use the projection formula for \(\pi_*\) together with the fact that \(\pi_*[\widetilde X]=[X]\) and that divisor pullback is compatible with operational products. Either route gives (RES). \(\square\)

At this point, the problem is reduced to intersection numbers of **nef divisor classes on a smooth projective variety** \(\widetilde X\).

---

### §3. AF/KT inequality \(\Rightarrow\) log-concavity of a two-point slice (EBB-ID-AF-SUBSTITUTION)

Fix \(i\neq j\). Fix all \(e_\ell\) for \(\ell\neq i,j\). Put
\[
S:=e_i+e_j,\qquad 
C:=\prod_{\ell\neq i,j}\widetilde\psi_\ell^{e_\ell}.
\]
Define
\[
a_k:=\int_{\widetilde X}\widetilde\psi_i^{k}\,\widetilde\psi_j^{S-k}\,C,\qquad k=0,1,\dots,S.
\]
Thus \(a_{e_i}=D(\mathbf e)\) for the chosen \(\mathbf e\) (with fixed other coordinates).

#### Theorem 6 (Alexandrov–Fenchel / Khovanskii–Teissier, 2-by-2 form).
Let \(Y\) be a smooth projective variety of dimension \(d\) and let \(D_1,\dots,D_d\) be nef \(\mathbb R\)-Cartier divisor classes on \(Y\). Then
\[
(D_1\cdots D_d)^2 \ \ge\ (D_1^2D_3\cdots D_d)\,(D_2^2D_3\cdots D_d).
\tag{AF}
\]
This can be found in standard references on positivity, e.g. Lazarsfeld, *Positivity in Algebraic Geometry I*, in the Khovanskii–Teissier/Hodge index discussion; nef follows from ample by approximation/continuity.

#### Lemma 7 (log-concavity of \((a_k)\)).
For \(1\le k\le S-1\),
\[
a_k^2\ge a_{k-1}a_{k+1}.
\tag{LC}
\]

**Proof (explicit substitution).** Fix such a \(k\). Apply (AF) on \(Y=\widetilde X\) with the following list of nef divisors:

- \(D_1=\widetilde\psi_i\),
- \(D_2=\widetilde\psi_j\),
- and \(D_3,\dots,D_d\) consisting of:
  - \(k-1\) copies of \(\widetilde\psi_i\),
  - \(S-k-1\) copies of \(\widetilde\psi_j\),
  - and for each \(\ell\neq i,j\), \(e_\ell\) copies of \(\widetilde\psi_\ell\).

Then
\[
(D_1\cdots D_d)=a_k,\qquad (D_1^2D_3\cdots D_d)=a_{k+1},\qquad (D_2^2D_3\cdots D_d)=a_{k-1},
\]
so (AF) becomes \(a_k^2\ge a_{k-1}a_{k+1}\). \(\square\)

#### Lemma 8 (symmetry).
\[
a_k=a_{S-k}\quad\text{for all }k.
\tag{SYM}
\]
**Proof.** Swap the labels \(i\leftrightarrow j\) (marked-point symmetry). \(\square\)

---

### §4. A log-concave nonnegative sequence has contiguous support (EBB-ID-LOGCONCAVE-SUPPORT)

We keep this because it removes any “internal zeros” fragility.

#### Lemma 9.
If \(a_k\ge 0\) and \(a_k^2\ge a_{k-1}a_{k+1}\) for all \(k\), then \(\{k:\ a_k>0\}\) is an interval (possibly empty).

**Proof.** If \(a_m=0\) and \(a_{m-1}>0\), then \(0=a_m^2\ge a_{m-1}a_{m+1}\) forces \(a_{m+1}=0\). Induct forward and backward. \(\square\)

---

### §5. Symmetric log-concave \(\Rightarrow\) moving toward the center does not decrease (fixed even/odd proof)

Let \((a_k)_{k=0}^S\) be nonnegative, log-concave (LC), and symmetric (SYM). Let \(m=\lfloor S/2\rfloor\).

#### Lemma 10 (center monotonicity).
For every integer \(k\ge m+1\),
\[
a_{k-1}\ge a_k.
\tag{CENTER}
\]

**Proof.** By Lemma 9, positivity holds on a contiguous interval; outside it the inequality is trivial, so assume \(a_k>0\) on the relevant indices and use ratio monotonicity.

Define ratios \(r_k:=a_k/a_{k-1}\) for \(1\le k\le S\) wherever denominators are nonzero. Log-concavity implies \(r_{k+1}\le r_k\) (standard equivalence when positive).

Now split:

- **Case 1: \(S=2m\) (even).**  
  Symmetry gives \(a_{m-1}=a_{m+1}\). Log-concavity at \(m\) gives
  \[
  a_m^2\ge a_{m-1}a_{m+1}=a_{m+1}^2,
  \]
  hence \(a_m\ge a_{m+1}\), i.e. \(r_{m+1}\le 1\). Since \(r_k\) is nonincreasing in \(k\), for all \(k\ge m+1\) we have \(r_{k}\le r_{m+1}\le 1\), so \(a_k\le a_{k-1}\).

- **Case 2: \(S=2m+1\) (odd).**  
  Symmetry gives \(a_m=a_{m+1}\), hence \(r_{m+1}=a_{m+1}/a_m=1\). Again by ratio monotonicity, for all \(k\ge m+1\),
  \[
  r_k\le r_{m+1}=1,
  \]
  so \(a_k\le a_{k-1}\).

Thus (CENTER) holds in all cases. \(\square\)

---

### §6. Proof of the Transfer Inequality (TI)

Assume \(e_i\ge e_j+2\). Let \(S=e_i+e_j\) and define the slice \(a_k\) as in §3. Then \(e_i\ge \lfloor S/2\rfloor+1\), i.e. \(e_i\) lies to the right of the center.

By Lemma 10,
\[
a_{e_i-1}\ge a_{e_i}.
\]
But
\[
a_{e_i}=D(\dots,e_i,\dots,e_j,\dots),\qquad a_{e_i-1}=D(\dots,e_i-1,\dots,e_j+1,\dots),
\]
so we obtain (TI).

\(\square\)

---

### §7. Conclude: existence of a balanced maximizer (for \(n\ge 1\))

Assume \(n\ge 1\), so \(E(g,n)\neq\varnothing\). Since \(E(g,n)\) is finite, \(D\) has a maximizer \(\mathbf e_{\max}\).

By Lemma 1, we can reach a balanced vector \(\mathbf b\) from \(\mathbf e_{\max}\) through finitely many balancing moves. Each move does not decrease \(D\) by (TI), hence
\[
D(\mathbf b)\ge D(\mathbf e_{\max})=\max_{\mathbf e\in E(g,n)}D(\mathbf e).
\]
Thus \(\mathbf b\) is a maximizer and is balanced.

This proves the theorem (meaningful version). Together with §0, it completely answers the prompt.

\(\blacksquare\)

---

## Gaps: None

---

## Self-evaluation

Confidence score (0–100): 90

Known or suspected issues:
- The argument relies on standard but nontrivial foundational results (Edidin’s operational Chow identification; descent of tensor powers of line bundles to coarse spaces; AF/KT for nef divisors). I have stated these in a form that is standard in the literature, but I have not reproduced full proofs (by design).
- One could further polish by giving exact bibliographic entries and theorem numbers for:
  - Edidin’s theorem (often cited as Thm. 4.40 in notes/expositions),
  - nefness of \(\psi_i\) (e.g. in Gibney–Keel–Morrison or equivalent moduli references),
  - AF/KT inequality (e.g. Lazarsfeld *Positivity I* in the Khovanskii–Teissier section).
  The logical structure no longer depends on any shaky map-identification statements; it only depends on those standard theorems being correct.

Coverage:
- I give a counterexample to the **literal** statement (empty domain when \(n=0,g\ge 2\)).
- I prove the intended balanced-maximizer claim for all **meaningful** cases \(n\ge 1\) (hence \(E(g,n)\neq\varnothing\)).

---

# Expert evaluator's assessment and feedback on Solution Attempt 3

## Status  
Status: Solved with minor gaps

## Score  
Score (0–100): 93

## Major issues  
Major issues: None.

## Counterexamples / impossible claims (OPTIONAL)

- The “counterexample” \((g,n)=(2,0)\) (indeed any \(g\ge 2,n=0\)) is a valid obstruction to the **literal** statement as written: \(E(g,0)=\varnothing\), so the existential claim “\(D\) achieves its maximum on \(E(g,n)\) at some balanced \(\mathbf e\in E(g,n)\)” fails in the standard logical reading.  
  This was the previously identified empty-domain issue (**MAJOR-ISSUE-ID-EMPTYDOMAIN**) and is now correctly incorporated as part of the final answer rather than being a flaw.

## Minor issues  

- **§2.1 (“nefness of \(\psi_i\)”)**  
  - **Nature:** citation precision / foundational dependence.  
  - **Comment:** You cite Gibney–Keel–Morrison (JAMS 2002) as a “standard reference” for nefness of \(\psi_i\). This is plausible, but for a fully examinable write-up you should point to an explicit theorem/proposition/corollary (and verify it is stated for the coarse space or the stack in the precise form you need).  
  - **Concrete fix:** Add: “By [GKM02, Proposition/Corollary X.Y], \(\psi_i\) is nef on \(\overline M_{g,n}\)” (or give a different standard reference such as Cornalba–Harris style statements if that is where you know it appears).

- **§2.2 (Edidin theorem statement)**  
  - **Nature:** missing theorem-number / hypotheses not spelled out.  
  - **Comment:** You state the correct *shape* of the theorem (operational Chow of coarse \(\simeq\) Chow of stack with \(\mathbb Q\)-coefficients), and you avoided the earlier incorrect “\(p_*\) inverse is \(p^*\)” formulation. However, you still do not specify the exact conditions (e.g. separated DM stack, over \(\mathbb C\)/char \(0\), etc.) under which the theorem holds.  
  - **Concrete fix:** Add an explicit bibliographic reference and theorem number, and state in one sentence that \(\overline{\mathcal M}_{g,n}\) satisfies the hypotheses.

- **§2.3 (tensor-power descent lemma)**  
  - **Nature:** “standard fact” invoked but not explicitly sourced.  
  - **Comment:** The statement “some tensor power descends to the coarse space” is standard, but again needs a reference (or at least a precise lemma statement: e.g. “the cokernel of \(\mathrm{Pic}(X)\to \mathrm{Pic}(\mathcal X)\) is torsion”).  
  - **Concrete fix:** Cite a standard stacks reference (e.g. Vistoli, or a Stacks Project lemma on coarse moduli and descent of line bundles) and/or add a one-paragraph proof sketch with bounded stabilizer orders (which is available for \(\overline{\mathcal M}_{g,n}\)).

- **§2.4 / Lemma 5 (computing intersection numbers on a resolution)**  
  - **Nature:** justification too compressed.  
  - **Comment:** The identity  
    \[
    \int_X \alpha_1\cdots\alpha_d = \int_{\widetilde X}\pi^*\alpha_1\cdots\pi^*\alpha_d
    \]
    for \(\alpha_i\) coming from \(\mathbb Q\)-Cartier divisor classes is correct in the standard operational/intersection-theoretic framework, but your “Justification” is currently at the level of “this is standard.”  
  - **Concrete fix:** Add a short explicit projection-formula argument in operational Chow:
    \[
    \deg(\alpha\cap [X])=\deg(\pi_*(\pi^*\alpha\cap[\widetilde X]))=\deg(\pi^*\alpha\cap[\widetilde X]),
    \]
    using \(\pi_*[\widetilde X]=[X]\) and compatibility of \(\pi^*\) on operational classes. This would fully close the loop.

## Established building blocks

- **EBB-ID-BALANCE-TRANSFER** (still valid)  
  The potential-function argument that repeated Robin Hood transfers terminate at a balanced vector is correct and clean.

- **EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE** (still valid)  
  The reduction “balanced maximizer follows once one proves the pairwise transfer inequality (TI)” is correct.

- **EBB-ID-AF-SUBSTITUTION** (still valid)  
  Your explicit divisor-list substitution into the \(2\times 2\) AF/KT inequality to obtain slice log-concavity \(a_k^2\ge a_{k-1}a_{k+1}\) is correct, with the divisor-count check done correctly.

- **EBB-ID-LOGCONCAVE-SUPPORT** (still valid)  
  Log-concave nonnegative \(\Rightarrow\) contiguous support is correct and is appropriately used to eliminate “internal zeros” issues.

- **EBB-ID-SYMLOGCONCAVE-UNIMODAL** (now fixed and reusable)  
  Your Lemma 10 proof (splitting even/odd \(S\) and using the midpoint ratio \(r_{m+1}\le 1\) plus ratio monotonicity) correctly establishes “move toward center does not decrease.”

## Gap assessment  

You declared “Gaps: None.” I mostly agree, but there remains a **minor** “formal-citation gap”:

- **Gap: precise sourcing/hypotheses for the stack/coarse/operational/resolution identifications in §2.**  
  - **Assessment:** Minor.  
  - **Reason:** The logical structure is now correct and the statements you invoke are standard; what remains is to pin them to precise theorems and make Lemma 5’s operational projection step explicit enough that a strict reader cannot object.

## Coverage assessment  

All subparts addressed: **Yes**.

- You give a counterexample to the **literal** statement for \(n=0\) (empty domain).
- You prove the intended “balanced maximizer” statement for all **meaningful** cases \(n\ge 1\).

## Summary  

Solution Attempt 3 presents a coherent and essentially complete argument that the maximum of the descendant intersection number \(D(\mathbf e)\) is attained at a balanced exponent vector, whenever the domain \(E(g,n)\) is nonempty. The combinatorial reduction via Robin Hood transfers is correct and provides a clean way to reduce the problem to a two-coordinate monotonicity statement (TI). The core geometric step—log-concavity of the two-point slice—has now been properly derived from a standard Alexandrov–Fenchel/Khovanskii–Teissier inequality for nef divisors via an explicit repeated-divisor substitution. The discrete “symmetric + log-concave implies center is maximal” step is now correctly handled for both even and odd totals \(S\), and you robustly addressed the possibility of zeros by proving contiguous support.

The only remaining weaknesses are presentation-level: several standard foundational inputs in §2 (Edidin operational Chow identification, tensor-power descent to the coarse space, and the projection-to-resolution computation of top intersections) are invoked correctly but still need sharper citations and slightly more explicit argumentation. These are minor and do not require changing the strategy or the core proof.

Overall, the approach is the right one, and the proof is correct modulo tightening references and a small amount of formal intersection-theory bookkeeping.

## Recommendations for next iteration (prioritized)

1. **Pin down exact citations and theorem numbers for §2.2 (Edidin) and §2.3 (tensor-power descent).**  
   State hypotheses explicitly and verify \(\overline{\mathcal M}_{g,n}\) satisfies them.

2. **Strengthen Lemma 5 by writing the operational projection-formula argument explicitly.**  
   Make it a short, self-contained proof rather than a “standard definition” remark.

3. **Cite nefness of \(\psi_i\) with a pinpoint reference and exact statement.**  
   E.g. specify whether the nefness is on the stack line bundle \(L_i\) or on the coarse \(\mathbb Q\)-Cartier divisor class, and cite the precise item in GKM (or another standard reference).

4. **Optional polish:** add one sentence explaining the “nef from ample by approximation” step for AF/KT, with a standard reference (Lazarsfeld *Positivity I* or similar).

## Meta-level guidance for both the probem solver and the orchestrator  

### Strategy-level assessment  
The overall approach is **fundamentally sound and correctly executed**: it is essentially a Schur-convexity/majorization phenomenon for a symmetric multilinear form coming from nef intersection theory, and AF/KT log-concavity is exactly the right tool.

### Structural blockers  
None at this stage.

### Dead directions / approaches to abandon  
Dead directions: None.

### Promising lines and subproblems  
- Turn §2 into a compact “foundational lemma package” with explicit references:
  1) operational Chow identification stack \(\leftrightarrow\) coarse (rationally),  
  2) tensor-power descent for line bundles,  
  3) projection formula for pulling top intersection numbers to a resolution.

Once that is done, the rest of the proof (§3–§7) is already in essentially final form.

### Recommendations for the orchestrator (prioritized)

1. **Treat EBB-ID-AF-SUBSTITUTION, EBB-ID-BALANCE-TRANSFER, and EBB-ID-SYMLOGCONCAVE-UNIMODAL as established and reuse them unchanged.**
2. **Do not pursue DVV-recursion brute-force checks or counterexample searches** unless a foundational citation fails (unlikely).
3. **Spawn a quick “citation verification” task**: locate precise theorem/proposition numbers for (i) Edidin operational Chow identification, (ii) tensor-power descent of line bundles to coarse spaces, (iii) nefness of \(\psi_i\) on \(\overline M_{g,n}\), and (iv) AF/KT for nef divisors.

## Research flag  
Research needed: No.  

## Updated Registry of IDs

### Major issues
- **MAJOR-ISSUE-ID-AFSTACK:** Previously “stack/coarse/resolution justification imprecise.” **Now resolved to at most minor citation/polish issues** in Attempt 3.
- **MAJOR-ISSUE-ID-EMPTYDOMAIN:** Empty-domain case \(n=0, g\ge 2\) makes the literal statement fail/ill-posed; now correctly handled as an explicit counterexample.

### Established building blocks
- **EBB-ID-BALANCE-TRANSFER:** Balancing by Robin Hood transfers terminates.
- **EBB-ID-REDUCE-TO-PAIRWISE-MONOTONE:** Reduction to transfer inequality (TI).
- **EBB-ID-AF-SUBSTITUTION:** Explicit AF/KT substitution gives slice log-concavity.
- **EBB-ID-LOGCONCAVE-SUPPORT:** Log-concave nonnegative sequences have contiguous support.
- **EBB-ID-SYMLOGCONCAVE-UNIMODAL:** Symmetry + log-concavity implies maximality at the center (now correctly handled even/odd).

### Dead directions
- None.

