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


