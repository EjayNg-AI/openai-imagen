# Problem Statement

An urn initially contains one red and one blue ball. At each step we draw one ball at random from the urn, with the uniform distribution over the balls currently in the urn.

* If the ball drawn is red, we place one additional red and one additional blue ball into the urn.
* When we draw a blue ball for the $k$-th time, we place one blue and $2k+1$ red balls into the urn.

(The originally drawn balls are not removed; they remain in the urn.)

Let $G_n$ denote the number of balls in the urn after $n$ steps. Prove that there exist constants $0 < c, \alpha < \infty$ such that with probability $1$ we have:

$$\frac{G_n}{n^\alpha} \longrightarrow c$$

as n tends to infinity.

---

# External Research Input

## 2. Problem and current state summary

### Restatement of the problem

The urn evolves as follows:

- Start with 1 red, 1 blue.
- At each step, draw one ball uniformly at random from the urn; the drawn ball stays in the urn.
- If the drawn ball is red, you add 1 red and 1 blue.
- If the drawn ball is blue and this is the **k‑th blue draw so far**, you add 1 blue and \(2k+1\) red balls.

Let \(G_n\) be the total number of balls after \(n\) draws. Prove there exist constants \(0<c,\alpha<\infty\) such that
\[
\frac{G_n}{n^\alpha} \to c \quad\text{almost surely}.
\]

Internally, it was further conjectured (on strong heuristic grounds) that
\[
\alpha = \frac{4}{3},\qquad c = \Bigl(\frac{3}{2}\Bigr)^{2/3}.
\]

### Internal reductions and main approach

The key internal simplification is to track only the number of **blue draws**:

- Let \(K_n\) be the number of times a blue ball has been drawn by time \(n\).
- Then:

  - At each step exactly one blue ball is added, regardless of the color drawn, so
    \[
    B_n = 1 + n \quad \text{(deterministic).}
    \]
  - A careful counting of red additions gives
    \[
    R_n = 1 + n + K_n^2 + K_n.
    \]
  - Therefore
    \[
    G_n = R_n + B_n = K_n^2 + K_n + 2n + 2.
    \]

So the whole problem reduces to understanding the growth of the one‑dimensional process \(K_n\).

The evolution of \(K_n\) is:

- Let \(\xi_{n+1} \in\{0,1\}\) be the indicator that the \((n+1)\)-th draw is blue, so \(K_{n+1}=K_n+\xi_{n+1}\).
- Conditional on the past,
  \[
  p_n := \mathbb P(\xi_{n+1}=1\mid\mathcal F_n)
  = \frac{B_n}{G_n}
  = \frac{n+1}{K_n^2+K_n+2n+2}.
  \]
- Hence
  \[
  \mathbb E[K_{n+1}-K_n \mid \mathcal F_n] = p_n.
  \]

Heuristics and ODE scaling suggest:

- If \(K_n \approx C n^\beta\), consistency of the drift gives \(\beta = 2/3\), so \(K_n\) should grow like \(n^{2/3}\).
- Then \(G_n \approx K_n^2 \sim C^2 n^{4/3}\), so \(\alpha=4/3\).

To make this rigorous, the solver introduced the **potential**
\[
Y_n := \frac{K_n^3}{n^2}.
\]
A detailed calculation shows
\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal{F_n}] = -Y_n\frac{2n+1}{n(n+1)^2}  + \frac{3}{n+1}  - \frac{6n+5}{(n+1)D_n},
\]
where \(D_n = K_n^2+K_n+2n+2\). For large \(n\) and under the heuristic \(D_n\sim K_n^2\sim n^{4/3}\), this matches
\[
\mathbb E[Y_{n+1}-Y_n\mid\mathcal F_n]
\approx \frac{3-2Y_n}{n},
\]
so the associated ODE in “logarithmic time” has unique stable equilibrium \(Y=3/2\). One is therefore led to conjecture
\[
Y_n\to \frac{3}{2} \quad\text{a.s.},\quad
K_n\sim \Bigl(\frac{3}{2}\Bigr)^{1/3} n^{2/3},\quad
G_n\sim \Bigl(\frac{3}{2}\Bigr)^{2/3} n^{4/3}\;\text{a.s.}
\]

### Main gaps identified by the evaluator

The evaluator’s key points:

1. **Coarse two‑sided growth bounds for \(K_n\)** (Gap 1):

   - It was argued heuristically that \(K_n \approx n^{2/3}\), but there is no rigorous proof that
     \[
     n^{2/3-\varepsilon}\le K_n \le n^{2/3+\varepsilon}
     \]
     eventually a.s. (or even that \(K_n^2 \gg n^{1+\delta}\) for some \(\delta>0\)).
   - Such bounds are needed to justify approximations like \(D_n \sim K_n^2\) and to make error terms summable.

2. **Control of the drift error in \(Y_n\)** (Gap 2):

   - To fit \(Y_n\) into a standard stochastic approximation (SA) scheme, one needs
     \[
     \mathbb E[Y_{n+1}-Y_n\mid\mathcal F_n]
     = \frac{3-2Y_n}{n} + \varepsilon_n,
     \quad\sum |\varepsilon_n|<\infty\ \text{a.s.}
     \]
   - The current argument that \(\varepsilon_n\) is summable uses the unproven hypothesis \(K_n\sim n^{2/3}\), which is circular.

3. **Control of the noise term in \(Y_n\)** (Gap 3):

   - The martingale increment
     \[
     N_{n+1} := \frac{(3K_n^2+3K_n+1)(\xi_{n+1}-p_n)}{(n+1)^2}
     \]
     was heuristically shown to have variance \(\asymp n^{-4/3}\), hence square‑summable, but again using the unproven scaling of \(K_n\).

4. **Formal application of a stochastic approximation / almost‑supermartingale theorem** (Gap 3 / 4):

   - The solver wants to appeal to general SA theory (e.g. Benaïm, Borkar, Robbins–Siegmund), but hasn’t:
     - Stated a concrete theorem.
     - Verified its technical hypotheses (boundedness of \(Y_n\), Lipschitz drift, summability of perturbations, etc.)

Overall, the internal approach is correct in structure and very close to standard SA analyses of non‑linear urns, but the rigorous closure of these steps is still missing.

## 3. Key obstacles as research questions

Rephrasing the evaluator’s main concerns as research questions:

1. **Growth control of \(K_n\):**

   - *RQ1:* Are there general theorems or techniques to obtain almost‑sure polynomial growth bounds for one‑dimensional processes of the form
     \[
     K_{n+1} = K_n + \xi_{n+1},\quad
     \mathbb E[\xi_{n+1}\mid\mathcal F_n]
     = \frac{n+1}{K_n^2+K_n+2n+2},
     \]
     using martingale inequalities such as Freedman/Bernstein?

2. **Stochastic approximation framework:**

   - *RQ2:* Can we rigorously cast \(Y_n = K_n^3/n^2\) into a standard stochastic approximation scheme
     \[
     Y_{n+1} = Y_n + a_n\bigl(F(Y_n) + \eta_{n+1}\bigr),
     \]
     with \(a_n \sim 1/n\), \(F(y)=3-2y\), and noise \(\eta_{n+1}\) satisfying the classical assumptions (bounded or square‑integrable, \(\sum a_n^2\mathbb E[\eta_{n+1}^2]<\infty\), etc.)?

3. **Almost‑sure convergence of SA with 1/n step size:**

   - *RQ3:* Under what general conditions on \(F\) and the noise does one have almost sure convergence \(Y_n\to y_*\), when the ODE \(\dot y = F(y)\) has a globally attracting equilibrium \(y_*\)? Are there simple theorems (Benaïm’s ODE method, Robbins–Siegmund, Borkar’s results) that can be applied almost as black boxes?

4. **Existing results on non‑linear/unbalanced urns:**

   - *RQ4:* Have closely related non‑linear or unbalanced two‑color urns (with path‑dependent reinforcement) been analyzed in the literature using stochastic approximation, and how do those proofs handle:
     - growth exponents,
     - tightness of normalized compositions,
     - convergence to equilibria of limiting ODEs?

   These could serve as templates for repairing the present proof.

## 4. External research

### 4.1 Search strategy

I used queries of the following types:

- For stochastic approximation and ODE methods:
  - “A dynamical system approach to stochastic approximations” (Benaïm).
  - “Borkar stochastic approximation ODE method”.
  - “Robbins–Siegmund almost supermartingale theorem”.
  - “convergence of stochastic approximation via martingale and converse Lyapunov methods”.

- For generalized and non‑linear urns:
  - “generalized Pólya urns via stochastic approximation”.
  - “nonlinear unbalanced urn models via stochastic approximation”.
  - “nonlinear and unbalanced urn models two strategies stochastic approximation”.
  - “positive reinforced generalized time‑dependent Pólya urns via stochastic approximation”.

- For martingale concentration:
  - “Freedman inequality martingale tail bound bounded increments”.

- For the specific urn puzzle:
  - A direct search for the problem text (found the Reddit posting, but no accessible solution).

Below I summarize the most relevant findings.

### 4.2 Stochastic approximation and ODE method

#### Benaïm (1996): “A dynamical system approach to stochastic approximations”

Benaïm studies recursions of the form
\[
x_{n+1} = x_n + \gamma_{n+1}\bigl(F(x_n) + \zeta_{n+1}\bigr),
\]
with decreasing step sizes \(\gamma_n\) and martingale‑difference noise \(\zeta_{n+1}\), and proves that the limit set of \((x_n)\) is, under classical assumptions, almost surely contained in the chain‑recurrent set of the ODE \(\dot x = F(x)\).([libra.unine.ch](https://libra.unine.ch/entities/publication/b43c676a-1c01-4ac4-b90d-1cf33a660bf1))

Roughly, if:

- \(\sum \gamma_n = \infty\), \(\sum \gamma_n^2 < \infty\),
- \(F\) is locally Lipschitz and growth of \(x_n\) is controlled,
- the noise has bounded variance in a suitable sense,

then any limit point of \((x_n)\) is an equilibrium or belongs to an invariant set of the ODE. If the ODE \(\dot x = F(x)\) has a unique globally attracting equilibrium \(x_*\), one typically gets \(x_n\to x_*\) almost surely.

Applied to our setting, one can think of a scaled variable \(Y_n\) (either \(K_n/n^{2/3}\) or \(K_n^3/n^2\)) and interpret its evolution as an SA algorithm with step size \(1/n\) and drift \(F\) having a unique stable zero.

#### Borkar (2008, 2023): *Stochastic Approximation: A Dynamical Systems Viewpoint*

Borkar’s monograph provides a very accessible and systematic treatment of the ODE method for SA, including:

- Basic convergence analysis for SA schemes \(x_{n+1} = x_n + a_n[F(x_n) + M_{n+1}]\) with \(a_n\to 0\), \(\sum a_n=\infty\), \(\sum a_n^2 < \infty\).([link.springer.com](https://link.springer.com/book/10.1007/978-93-86279-38-5?utm_source=openai))
- Conditions under which the iterates track the flow of the ODE \(\dot x = F(x)\) and converge to globally attracting equilibria.
- Results on stability (boundedness of iterates) based on the “Borkar–Meyn theorem”, which connects global asymptotic stability of the ODE with almost‑sure boundedness and convergence of the SA iterates.([arxiv.org](https://arxiv.org/abs/2205.01303?utm_source=openai))

This framework matches *exactly* the structure needed for \(Y_n\), once you rewrite its recursion in the SA form and verify:

- step size \(a_n=1/n\),
- drift \(F(y)=3-2y\) (or \(F(y)=y^{-2}-\frac23 y\) in the other scaling),
- noise is a bounded martingale difference whose squared contribution is summable thanks to polynomial growth of \(K_n\).

#### Renlund (2010, 2011)

Renlund’s preprints “Generalized Pólya urns via stochastic approximation” (2010) and “Limit theorems for stochastic approximation algorithms” (2011) treat generalized urn models and associated 1D SA recursions. The 2011 paper proves a CLT for one‑dimensional SA algorithms converging to a point where the noise does not vanish and shows how the theory applies to a class of generalized Pólya urn models.([arxiv.org](https://arxiv.org/abs/1102.4741))

From our perspective, these papers are relevant because:

- They explicitly analyze urn models through SA recursions in one dimension.
- They give precise conditions under which such recursions converge (and have fluctuation limits), typically assuming that the mean drift behaves like a smooth function of the state plus higher‑order corrections.

Our \(Y_n\) process is exactly of this SA type, with a smooth 1D drift and bounded noise, so Renlund’s framework is a strong indication that our target convergence result is within reach.

### 4.3 Almost‑supermartingale convergence (Robbins–Siegmund)

Robbins and Siegmund (1971) introduced the concept of **almost supermartingales** and proved a widely used convergence theorem. A particularly clear statement and discussion is provided in a modern blog exposition by NRH Statistics.([nrhstat.org](https://nrhstat.org/post/robbins_siegmund/?utm_source=openai))

Let \((V_n)\) be nonnegative, adapted, and suppose there exist nonnegative adapted sequences \(\beta_n,\xi_n,\zeta_n\) such that
\[
\mathbb E[V_n\mid\mathcal F_{n-1}]
\le (1+\beta_{n-1})V_{n-1} + \xi_{n-1} - \zeta_{n-1}
\]
and
\[
\sum_n \beta_n <\infty,\quad
\sum_n \xi_n <\infty\quad\text{a.s.}
\]
Then:

- \(V_n\) converges almost surely to a finite nonnegative limit \(V_\infty\).
- \(\sum_n \zeta_n <\infty\) almost surely.

In many SA proofs, one takes \(V_n\) to be some Lyapunov‑type function of the state (e.g., squared distance to an equilibrium), and shows that \(\zeta_n\) dominates \(V_n\) times a summable factor, which forces \(V_n\to 0\).

In our context, we can aim to set
\[
V_n := \bigl(Y_n - \tfrac32\bigr)^2,
\]
where \(Y_n = K_n^3/n^2\). If we can derive an inequality of the form
\[
\mathbb E[V_{n+1}\mid\mathcal F_n]
\le V_n - c\,\frac1n V_n + \varepsilon_n,
\]
with \(\sum \varepsilon_n<\infty\), we can identify \(cV_n/n\) with \(\zeta_n\) and apply Robbins–Siegmund to conclude \(V_n\to 0\), i.e. \(Y_n\to 3/2\).

This gives a **very concrete way** to fix Gap 3 (rigorous SA convergence) without reproducing the entire ODE method theory.

### 4.4 Martingale concentration: Freedman and variants

To control \(K_n\) and the martingale noise terms, we need strong concentration for martingales with bounded increments. The classical tool is **Freedman’s inequality**, a Bernstein‑type inequality for martingales. While Freedman’s original 1975 paper is not directly accessible here, modern references (e.g., Dzhaparidze–van Zanten’s generalization and Tropp’s matrix version) clearly describe its structure.([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0304414900000867?utm_source=openai))

In one typical form (for scalar martingales):

- If \(M_n\) is a martingale with increments \(\Delta M_k = M_k - M_{k-1}\) satisfying \(|\Delta M_k| \le R\) almost surely, and predictable quadratic variation
  \[
  V_n = \sum_{k=1}^n \mathbb E[(\Delta M_k)^2\mid\mathcal F_{k-1}],
  \]
  then for all \(x,v>0\),
  \[
  \mathbb P\!\left( M_n \ge x,\ V_n\le v\right)
  \le \exp\!\left(-\frac{x^2}{2(v+Rx/3)}\right).
  \]

Our process \(M_n = K_n - \sum_{j<n}p_j\) has increments bounded by 1 and quadratic variation \(\le A_n := \sum p_j\). Freedman’s inequality (or its refinements) therefore allows us to:

- Show that on an event where \(K_n\) is hypothesized to grow too fast or too slowly, the martingale cannot deviate enough from its drift to sustain that behavior with significant probability.
- Turn these probabilistic bounds into Borel–Cantelli arguments to exclude “wrong” polynomial exponents for \(K_n\).

Thus, these inequalities are exactly the right tools to make the “bootstrap” arguments on \(K_n\)’s growth rigorous, addressing Gap 1.

### 4.5 Generalized and non‑linear urn models via stochastic approximation

There is by now a substantial body of work explicitly treating generalized Pólya urns (including non‑linear and unbalanced models) via stochastic approximation:

- **Laruelle & Pagès (2013, 2019):** “Randomized urn models revisited using stochastic approximation” and “Nonlinear randomized urn models: a stochastic approximation viewpoint”. These papers recast various adaptive urn schemes (often used in clinical trials) as SA algorithms and prove LLNs and CLTs for compositions.([cambridge.org](https://www.cambridge.org/core/journals/probability-in-the-engineering-and-informational-sciences/article/nonlinear-and-unbalanced-urn-models-with-two-types-of-strategies-a-stochastic-approximation-point-of-view/0E14828AF7807BE053A6DB9F7A67A9A5))

- **Renlund (2010):** “Generalized Pólya urns via stochastic approximation” (Preprint). This directly analyses generalized urn schemes as SA, providing convergence results and effective tools (e.g., Lyapunov functions) to treat irregular reinforcement.([cambridge.org](https://www.cambridge.org/core/journals/probability-in-the-engineering-and-informational-sciences/article/nonlinear-and-unbalanced-urn-models-with-two-types-of-strategies-a-stochastic-approximation-point-of-view/0E14828AF7807BE053A6DB9F7A67A9A5))

- **Idriss (2022/2023):** Two key papers:
  - “Nonlinear unbalanced urn models via stochastic approximation” (Methodology and Computing in Applied Probability, 2022), which considers a two‑color *nonlinear unbalanced* urn under a drawing rule reinforced by an \(\mathbb R_+\)-valued concave function and a non‑balanced replacement matrix, and proves limit laws for the urn composition using SA.([ideas.repec.org](https://ideas.repec.org/a/spr/metcap/v24y2022i1d10.1007_s11009-021-09858-6.html?utm_source=openai))
  - “Nonlinear and unbalanced urn models with two types of strategies: a stochastic approximation point of view” (Probability in the Engineering and Informational Sciences, 2023), which studies a 2‑color urn with **two different nonlinear drawing rules depending on the color withdrawn**, proving both a strong law of large numbers and a CLT, again using SA and martingale techniques.([cambridge.org](https://www.cambridge.org/core/journals/probability-in-the-engineering-and-informational-sciences/article/nonlinear-and-unbalanced-urn-models-with-two-types-of-strategies-a-stochastic-approximation-point-of-view/0E14828AF7807BE053A6DB9F7A67A9A5))

- **Ruszel & Thacker (2024):** “Positive Reinforced Generalized Time‑Dependent Pólya Urns via Stochastic Approximation” (J. Theor. Probability). They study time‑dependent multi‑urn models with general reinforcement functions \(f\), assuming conditions such as
  \[
  \sum_{n}\Bigl(\frac{\sigma_n}{\sum_{j\le n}\sigma_j}\Bigr)^2<\infty,
  \]
  precisely to control the SA noise. They show convergence to fixation behavior by coupling to an ODE and verifying SA conditions.([link.springer.com](https://link.springer.com/article/10.1007/s10959-024-01366-w))

- **Dasgupta & Maulik (2011):** “Strong Laws for Urn Models with Balanced Replacement Matrices” (EJP 16), which, although focused on balanced matrices, provides examples of scaling exponents determined by spectral radii of drift matrices and proves almost‑sure convergence of properly normalized counts.([arxiv.org](https://arxiv.org/abs/1010.5348))

Even though none of these works treats *exactly* our path‑dependent rule (where the red increment on a blue draw depends on the total number of past blue draws), the **techniques** they deploy are precisely:

- identify a suitable low‑dimensional SA recursion (for proportions or for some power of a count),
- derive a drift of the form \(a_n F(x_n)\) with \(a_n\approx 1/n\),
- control a martingale noise term with square‑summable variance,
- appeal to Benaïm/Borkar/Robbins–Siegmund‑type theorems to get almost‑sure convergence to equilibria of the limiting ODE.

Thus, these papers serve as strong methodological precedents that the internal approach with \(Y_n=K_n^3/n^2\) is on the right track and should be rigorously workable.

### 4.6 Summary of how these results relate to the gaps

- **Gap 1 (growth of \(K_n\))**:  
  The use of Freedman’s inequality and related martingale Bernstein bounds is standard in SA analyses to control deviations of the martingale part relative to its predictable quadratic variation.([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0304414900000867?utm_source=openai)) This is exactly what is needed to invalidate hypothetical growth regimes \(K_n \sim n^\beta\) with \(\beta\neq 2/3\).

- **Gap 2 (drift error \(\varepsilon_n\) for \(Y_n\))**:  
  Once you know that \(K_n\) grows as at least \(n^{1/2+\delta}\) and at most \(n^{1-\delta}\), you automatically get \(D_n = K_n^2+K_n+2n+2\) of order \(n^{1+\delta'}\) with \(\delta'>0\). This is analogous to the growth assumptions on cumulative additions \(\sum \sigma_j\) in Ruszel–Thacker, used to prove that SA noise is small.([link.springer.com](https://link.springer.com/article/10.1007/s10959-024-01366-w))

- **Gap 3 (noise term \(N_{n+1}\))**:  
  In essentially every SA reference (Borkar, Benaïm, Renlund, Ruszel & Thacker), one assumes \(\sum a_n^2 \mathbb E[\|\eta_{n+1}\|^2]<\infty\) to control martingale noise. With \(a_n=1/n\) and \(K_n\simeq n^{2/3}\), we get \(\mathbb E[N_{n+1}^2]\lesssim n^{-4/3}\), which is square‑summable. This mirrors the “polynomial growth allowed but not exponential” condition on \(\sigma_n\) in Ruszel–Thacker: they require \(\sum (\sigma_n / \sum_{j\le n}\sigma_j)^2<\infty\) precisely to have square‑summable noise.([link.springer.com](https://link.springer.com/article/10.1007/s10959-024-01366-w))

- **Gap 3/4 (SA convergence theorem)**:  
  Robbins–Siegmund’s almost‑supermartingale theorem, as clearly exposited in modern sources, gives a very direct way to conclude \(V_n\to 0\) almost surely from inequalities of the form
  \[
  \mathbb E[V_{n+1} \mid \mathcal F_n] \le (1+\beta_n)V_n + \xi_n - \zeta_n,
  \]
  with summable \(\beta_n,\xi_n\). Taking \(V_n = (Y_n-3/2)^2\) and \(\zeta_n\) proportional to \(\frac1n V_n\) matches the classical SA scheme with step size \(1/n\).([nrhstat.org](https://nrhstat.org/post/robbins_siegmund/?utm_source=openai))

- **Non‑linear urn precedents**:  
  Idriss’s urns with two different strategies, Renlund’s generalized urns, and Laruelle–Pagès’s randomized urns all demonstrate that path‑dependent or color‑dependent reinforcement can be treated with SA techniques similar to those outlined internally.([cambridge.org](https://www.cambridge.org/core/journals/probability-in-the-engineering-and-informational-sciences/article/nonlinear-and-unbalanced-urn-models-with-two-types-of-strategies-a-stochastic-approximation-point-of-view/0E14828AF7807BE053A6DB9F7A67A9A5))

## 5. Impact on current solution method

### Support for the current method

The external literature strongly supports the solver’s main strategy:

- **Reduction to a one‑dimensional SA process** is standard: Renlund, Laruelle–Pagès, and Idriss all reduce complicated urn models to low‑dimensional SA recursions.([cambridge.org](https://www.cambridge.org/core/journals/probability-in-the-engineering-and-informational-sciences/article/nonlinear-and-unbalanced-urn-models-with-two-types-of-strategies-a-stochastic-approximation-point-of-view/0E14828AF7807BE053A6DB9F7A67A9A5))
- **Choice of potential function \(Y_n = K_n^3/n^2\)** is very much in the spirit of typical SA/Lyapunov methods: one selects a function of the process for which the mean drift is nicely linear or polynomial in the scale parameter. Borkar’s and Benaïm’s work often uses such Lyapunov‑type transformations.([link.springer.com](https://link.springer.com/book/10.1007/978-93-86279-38-5?utm_source=openai))
- **Use of ODE heuristics** to guess exponents and limiting constants is exactly what the ODE method prescribes: write down a formal ODE for the drift and look at its equilibria and stability.

Thus, nothing in the literature contradicts the internal heuristic; rather, it confirms that, under appropriate estimates, the plan should work.

### How the literature suggests refinements

1. **Structured two‑stage proof (bootstrap + SA):**

   The way SA is used in urn papers (e.g., Idriss 2022 and Ruszel–Thacker 2024) suggests a **two‑stage argument**:

   - *Stage A (bootstrap):* Use coarse drift and martingale inequalities (like Freedman) to prove that the process is confined to a polynomial range. For instance, that for some \(1/2<\gamma_1<2/3<\gamma_2<1\),
     \[
     n^{\gamma_1} \le K_n \le n^{\gamma_2}
     \quad\text{eventually a.s.}
     \]
     This is analogous to proving boundedness of iterates in SA via a Lyapunov function and Borkar–Meyn’s criterion.([arxiv.org](https://arxiv.org/abs/2205.01303?utm_source=openai))

   - *Stage B (fine SA):* With those bounds in place, rewrite the \(Y_n\) recursion in the canonical SA form with small error and square‑summable noise, then invoke Robbins–Siegmund or Benaïm/Borkar.

   This exactly resolves the circularity noted by the evaluator.

2. **Concrete theorem to use: Robbins–Siegmund**

   Instead of appealing vaguely to “stochastic approximation theory”, one can explicitly quote the Robbins–Siegmund almost‑supermartingale theorem as the main tool for convergence of \(V_n=(Y_n-3/2)^2\). The NRH Statistics article provides a clear statement and even shows how the strong law of large numbers is a direct corollary, which is very close in spirit to our setting.([nrhstat.org](https://nrhstat.org/post/robbins_siegmund/?utm_source=openai))

3. **Pre‑existing urn analyses with non‑linear rules**

   Idriss’s 2‑strategy urns and Ruszel–Thacker’s generalized time‑dependent urns, both handled via SA, indicate that the “non‑linear, unbalanced” nature of the reinforcement is not an obstacle in itself. What matters is that one can identify a stable equilibrium of the limiting ODE and verify the standard SA conditions, exactly as in our problem.([cambridge.org](https://www.cambridge.org/core/journals/probability-in-the-engineering-and-informational-sciences/article/nonlinear-and-unbalanced-urn-models-with-two-types-of-strategies-a-stochastic-approximation-point-of-view/0E14828AF7807BE053A6DB9F7A67A9A5))

In summary: the current method is not fundamentally flawed; it just needs to be aligned more explicitly with the standard SA/ODE toolkit, and the bootstrap and noise‑control steps need to be fully fleshed out using Freedman + Robbins–Siegmund.

## 6. Suggested new or refined approaches

Based on the literature, here are refined approaches that build on the internal plan.

### Approach A: Two‑stage SA analysis with \(Y_n = K_n^3/n^2\)

**Core idea:**  
Make the internal Approach 3 fully rigorous by:

1. Proving coarse polynomial bounds for \(K_n\) using Freedman’s inequality plus drift estimates.
2. Then treating \(Y_n\) as an SA process and applying Robbins–Siegmund to \(V_n=(Y_n-3/2)^2\).

**External results used or mimicked:**

- Freedman‑type martingale inequalities for bounded increments to control \(M_n=K_n-\sum p_j\).([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0304414900000867?utm_source=openai))
- Robbins–Siegmund almost supermartingale theorem to get convergence of \(V_n\).([nrhstat.org](https://nrhstat.org/post/robbins_siegmund/?utm_source=openai))
- Structural guidance from Renlund (2010, 2011) and Idriss (2022) on treating 1D SA recursions arising from urns.([arxiv.org](https://arxiv.org/abs/1102.4741))

**Main technical tasks:**

1. **Upper exponent bound for \(K_n\):**

   - For \(\beta>2/3\), consider the event \(E_\beta =\{K_n \ge n^\beta \text{ for infinitely many }n\}\). Under this hypothesis,
     \[
     p_n \le \frac{n+1}{K_n^2} \lesssim n^{1-2\beta}.
     \]
   - Then \(A_n=\sum p_n \lesssim n^{2-2\beta}\), while the Freedman inequality plus Borel–Cantelli give that the martingale \(M_n\) is eventually negligible compared to \(A_n\). Therefore \(K_n \sim A_n\) and thus \(K_n = O(n^{2-2\beta})\), which contradicts \(K_n\ge n^\beta\) when \(\beta>2/3\).
   - Make this argument precise on dyadic blocks, then apply Borel–Cantelli to deduce \(\mathbb P(E_\beta)=0\).

2. **Lower exponent bound for \(K_n\):**

   - For \(\beta<2/3\), analyze the event \(F_\beta =\{K_n \le n^\beta \text{ for infinitely many }n\}\). On this event, for large \(n\) one has \(K_n^2\le n^{2\beta}\ll n\) is *false* if \(\beta>1/2\), so more care is needed, but one can still show that \(p_n\gtrsim n^{1-2\beta}\) often enough to push \(A_n\) and hence \(K_n\) above \(n^\beta\). The literature on generalized urns (e.g., Renlund 2010, Ruszel–Thacker 2024) provides precedents for such lower‑bound drift arguments.([arxiv.org](https://arxiv.org/abs/1102.4741))

   - Again, Freedman controls deviations of \(M_n\) so that the deterministic drift dominates in the long run.

3. **Drift and noise for \(Y_n\):**

   - With \(K_n\) now sandwiched between \(n^{\gamma_1}\) and \(n^{\gamma_2}\) for some \(1/2<\gamma_1<\gamma_2<1\), deduce:

     - \(D_n \sim K_n^2\) and in particular \(D_n\ge c n^{1+\delta}\) for some \(\delta>0\).
     - \(\mathbb E[N_{n+1}^2\mid\mathcal F_n]\le C n^{-1-\delta'}\) for some \(\delta'>0\), making \(\sum \mathbb E[N_{n+1}^2]<\infty\).

   - Compute explicitly
     \[
     \mathbb E[Y_{n+1}-Y_n\mid\mathcal F_n]
     = \frac{3-2Y_n}{n} + \varepsilon_n,
     \]
     and bound \(|\varepsilon_n|\le Cn^{-1-\delta''}\) (using the exact formula already derived and the new bounds on \(D_n\)). This fixes Gap 2.

4. **Apply Robbins–Siegmund to \(V_n = (Y_n-3/2)^2\):**

   - Use the expansion
     \[
     V_{n+1}
     = V_n + 2(Y_n-3/2)(Y_{n+1}-Y_n) + (Y_{n+1}-Y_n)^2,
     \]
     plug in the drift decomposition, and take conditional expectation. One gets
     \[
     \mathbb E[V_{n+1}\mid\mathcal F_n]
     \le V_n - c\,\frac{1}{n} V_n + \xi_n,
     \]
     with \(\sum \xi_n<\infty\) (from the square‑summable noise and the summable \(\varepsilon_n\)).
   - Now apply the Robbins–Siegmund theorem to conclude \(V_n\) converges and \(\sum \frac{1}{n}V_n <\infty\). The latter forces \(\liminf V_n = 0\). Combined with continuous drift, this gives \(V_n\to 0\), so \(Y_n\to 3/2\).

This is a fairly standard SA analysis once the bootstrapping on \(K_n\) is done, and it directly addresses all the evaluator’s major concerns.

### Approach B: Work with \(Y_n' = K_n/n^{2/3}\) instead

**Core idea:**  
Instead of the cubic potential, use \(Y_n'=K_n/n^{2/3}\) and derive the recursion
\[
\mathbb E[Y_{n+1}' - Y_n'\mid\mathcal F_n]
= \frac{1}{n}\Bigl({Y_n'}^{-2} - \tfrac{2}{3}Y_n'\Bigr) + \text{(small error)},
\]
so that the limiting ODE is
\[
\frac{dy}{dt} = y^{-2} - \tfrac23 y
\]
with unique stable equilibrium \(y_*=(3/2)^{1/3}\).

**External results used:**

- Same SA and ODE method as in Approach A (Benaïm, Borkar, Renlund).([libra.unine.ch](https://libra.unine.ch/entities/publication/b43c676a-1c01-4ac4-b90d-1cf33a660bf1))
- Robbins–Siegmund on \(V_n=(Y_n'-y_*)^2\).

**Pros and cons:**

- The algebra is slightly more involved than with \(K_n^3/n^2\) because the drift function \(F(y)=y^{-2}-\frac23 y\) is non‑linear, so the resulting almost‑supermartingale inequality is a bit uglier.
- On the plus side, it aligns more directly with the internal ODE heuristic for \(K_n\) itself.

In practice, given the clean linear drift of \(Y_n=K_n^3/n^2\), Approach A is probably technically simpler, but Approach B is conceptually parallel and could serve as a cross‑check.

### Approach C: Borrow structure from existing non‑linear urns

**Core idea:**  
Use the technical structure and intermediate lemmas from papers on non‑linear urns (Idriss 2022, Laruelle & Pagès 2013, Renlund 2010) as templates. Many of these papers have already solved the type of problems you face:

- obtaining coarse bounds on counts,
- proving tightness of suitably scaled processes,
- identifying and exploiting appropriate Lyapunov functions.

**How to use:**

- Examine Renlund’s 2010 “Generalized Pólya urns via stochastic approximation” and Idriss’s 2022/2023 papers for the way they:
  - bound urn compositions in terms of polynomial functions of time,
  - rewrite urn compositions as SA recursions with explicit drift and noise,
  - verify SA hypotheses.

- Copy the structure of lemmas (e.g., “If the composition leaves a certain compact region, drift pushes it back with high probability”) and adapt them to the 1D recursion for \(K_n\).

This approach doesn’t fundamentally change the solution method; it gives a highly concrete set of blueprints from proved theorems on structurally similar urns.

## 7. Difficulty assessment and next‑step recommendation

### Difficulty assessment

Given the literature:

- The **technique** required is standard in modern SA and generalized urn theory: martingale inequalities, ODE method, almost‑supermartingale convergence, Lyapunov functions.
- There are multiple **closely related examples** where non‑linear and unbalanced urns are successfully analyzed with SA, including some with reinforcement rules depending on color and time.([cambridge.org](https://www.cambridge.org/core/journals/probability-in-the-engineering-and-informational-sciences/article/nonlinear-and-unbalanced-urn-models-with-two-types-of-strategies-a-stochastic-approximation-point-of-view/0E14828AF7807BE053A6DB9F7A67A9A5))
- No source appears to treat **exactly** this urn, and no ready‑made theorem drops in without some adaptation, but there is no sign of genuinely new phenomena beyond the standard SA framework.

In my view, this places the problem at:

> “Likely solvable with careful work and existing theory.”

It is not trivial; a fully rigorous write‑up would probably be at least a paper‑length SA analysis, but the main ingredients are well‑established.

### Recommended next internal step

**Primary recommendation:**

> Proceed with **Approach A** (two‑stage SA analysis for \(Y_n = K_n^3/n^2\)) and systematically import the Robbins–Siegmund theorem and Freedman’s inequality.

Concretely:

1. **Write a dedicated section proving coarse growth of \(K_n\)**

   - State Freedman’s inequality (or a standard martingale Bernstein inequality) with full hypotheses and citation.
   - For each \(\beta\neq 2/3\), rigorously exclude the event \(K_n \ge n^\beta\) infinitely often (for \(\beta>2/3\)) and \(K_n \le n^\beta\) infinitely often (for \(\beta<2/3\)).
   - Conclude that for some \(1/2<\gamma_1<\gamma_2<1\), almost surely \(K_n\in [n^{\gamma_1},n^{\gamma_2}]\) for all large \(n\).

2. **Tighten the drift and noise estimates for \(Y_n\)**

   - Using the exact drift formula already derived, bound the error term \(\varepsilon_n\) by \(Cn^{-1-\delta}\), with \(\delta>0\) coming from the new lower bound on \(K_n\).
   - Compute \(\mathbb E[N_{n+1}^2\mid\mathcal F_n]\) precisely enough to show \(\sum \mathbb E[N_{n+1}^2]<\infty\).

3. **Formulate and verify an almost‑supermartingale inequality for \(V_n=(Y_n-3/2)^2\)**

   - Carefully expand \(V_{n+1}-V_n\), take conditional expectation, and isolate a negative term of order \(V_n/n\) plus a summable remainder.
   - Map this inequality into the Robbins–Siegmund form and quote the theorem explicitly (e.g. from the NRH Statistics article or from the original 1971 paper).([nrhstat.org](https://nrhstat.org/post/robbins_siegmund/?utm_source=openai))

4. **Conclude convergence of \(Y_n\), then deduce the asymptotics of \(K_n\) and \(G_n\)**

   - From \(Y_n\to3/2\) and the definition \(Y_n=K_n^3/n^2\), show \(K_n\sim(3/2)^{1/3}n^{2/3}\).
   - Plug into \(G_n = K_n^2+K_n+2n+2\) to get \(G_n/n^{4/3}\to(3/2)^{2/3}\).

**Secondary recommendation:**

While doing this, keep an eye on the structure of existing urn/SA papers (Renlund, Idriss, Laruelle–Pagès, Ruszel–Thacker) for technical tricks, especially in:

- splitting time into blocks to apply martingale inequalities,
- constructing Lyapunov functions to guarantee boundedness or return to compact sets,
- handling non‑linear drift functions.

If at any point the argument becomes unwieldy, you might consider whether a **slightly more general theorem** from Benaïm or Borkar could be quoted wholesale, replacing part of the detailed drift/noise analysis—this could simplify the write‑up, but only if you can cleanly verify all theorem assumptions.

In summary: the external literature confirms that your plan is conceptually sound and provides specific theorems (Robbins–Siegmund, Freedman inequalities, Benaïm/Borkar SA results) that can be used to repair the gaps. The next iteration should focus on carefully implementing these tools rather than searching for a fundamentally new idea.

---

# Solution Attempt 2 by the problem solver

2. Status  
Status: Complete

3. Selected approaches  
Selected approach indices: 1, 3 (combination)  
- I keep the reduction to the one–dimensional process of blue draws K_n and its drift/martingale decomposition (Approach 1).  
- I again use the potential Y_n = K_n^3/n^2, but now with a fully rigorous two–stage scheme:  
  Stage A: prove coarse, two–sided polynomial bounds for K_n via Freedman’s inequality on dyadic blocks (resolving the evaluator’s Gap 1).  
  Stage B: with those bounds in hand, treat Y_n by a Robbins–Siegmund almost–supermartingale argument to obtain Y_n → 3/2 a.s. and hence the limit for G_n (resolving Gaps 2–4).  
- Relative to Attempt 1, I correct the drift identity for Y_n (a missing n factor) and separate bootstrap (coarse bounds) from the stochastic-approximation step to avoid any circularity.

4. Solution

Notation and basic identities
- Let R_n, B_n, G_n be the numbers of red, blue, and total balls after n steps; K_n is the number of blue draws among the first n draws.
- Initial condition: R_0 = B_0 = 1, hence G_0 = 2.
- At each step exactly one blue ball is added, regardless of the color drawn. Therefore
  B_n = 1 + n deterministically.
- Counting red additions:
  - Each red draw adds 1 red; there are n−K_n red draws.
  - The k-th blue draw adds 2k+1 red balls; summing gives ∑_{k=1}^{K_n}(2k+1) = K_n^2 + 2K_n.
  Hence
  R_n = 1 + (n−K_n) + (K_n^2 + 2K_n) = 1 + n + K_n^2 + K_n.
- Therefore
  G_n = R_n + B_n = K_n^2 + K_n + 2n + 2.                                                (4.1)

Dynamics of K_n
- Let ξ_{n+1} be the indicator that draw n+1 is blue. Then K_{n+1} = K_n + ξ_{n+1}.
- Conditional blue probability given the past (σ-field F_n):
  p_n := P(ξ_{n+1}=1 | F_n) = B_n/G_n = (n+1)/(K_n^2 + K_n + 2n + 2) = (n+1)/D_n,     (4.2)
  where D_n := K_n^2 + K_n + 2n + 2.
- Define the drift and martingale parts
  A_n := ∑_{j=0}^{n-1} p_j,      M_n := K_n − A_n = ∑_{j=0}^{n-1} (ξ_{j+1} − p_j).
  Then M_n is a martingale with bounded increments |ΔM_{j+1}| ≤ 1 and predictable quadratic variation
  ⟨M⟩_n = ∑_{j=0}^{n-1} p_j(1−p_j) ≤ A_n ≤ n.                                            (4.3)

A dyadic-block martingale inequality (Freedman)
We use the following standard form of Freedman’s inequality for martingales with bounded increments.

Lemma 4.1 (Freedman). Let (M_k) be a martingale with respect to (F_k), with |M_k − M_{k−1}| ≤ 1 a.s. Let V_k := ∑_{i=1}^k E[(M_i − M_{i−1})^2 | F_{i−1}] be its predictable quadratic variation. Then for any integers s < t and any x, v > 0,
P( sup_{s<k≤t} (M_k − M_s) ≥ x and (V_t − V_s) ≤ v ) ≤ exp( − x^2 / (2(v + x/3)) ).
The same bound holds for the stopped martingale (M_{k∧τ}) and its quadratic variation, for any stopping time τ.

Stage A: coarse two–sided polynomial bounds for K_n
We prove that for some exponents 1/2 < β_- < 2/3 < β_+ < 1 and random N(ω) < ∞, we have
c(ω) n^{β_-} ≤ K_n ≤ C(ω) n^{β_+} for all n ≥ N(ω), almost surely.                      (4.4)
For definiteness we take β_- ∈ (1/2, 2/3) and β_+ ∈ (2/3, 1) fixed (any concrete choices like β_-=3/5 and β_+=3/4 work). The proofs use dyadic blocks I_m := [2^m, 2^{m+1}) and Freedman on each block.

Lower bound (eventually K_n ≥ c n^{β_-})
Fix β_- ∈ (1/2, 2/3) and set L_m := 2^{β_- m}. Consider block I_m = [2^m, 2^{m+1}). On the event that K_j never exceeds 2L_m on I_m (which can only help us get a lower bound on p_j),
D_j = K_j^2 + K_j + 2j + 2 ≤ (2L_m)^2 + 2L_m + 2^{m+2} ≤ 5·2^{2β_- m} for all j ∈ I_m and m large,
since 2β_- > 1. Hence for all j ∈ I_m and large m,
p_j = (j+1)/D_j ≥ (2^m)/(5·2^{2β_- m}) = c·2^{(1−2β_-)m}.
Summing over I_m (its length is 2^m), the conditional expected drift across I_m satisfies
E[ K_{2^{m+1}} − K_{2^m} | F_{2^m}, sup_{I_m} K ≤ 2L_m ] ≥ c'·2^{(2−2β_-)m} =: v_m.      (4.5)

The realized increment is
K_{2^{m+1}} − K_{2^m} = ∑_{j∈I_m} ξ_{j+1} = ∑_{j∈I_m} p_j + (M_{2^{m+1}} − M_{2^m}).
On the same event sup_{I_m} K ≤ 2L_m we have (by the variance bound p_j(1−p_j) ≤ p_j)
V_{2^{m+1}} − V_{2^m} = ∑_{j∈I_m} p_j(1−p_j) ≤ ∑_{j∈I_m} p_j ≤ 2 v_m (for large m).
Applying Freedman with x = v_m/2 and v = 2 v_m gives
P( K_{2^{m+1}} − K_{2^m} < v_m/2 and sup_{I_m} K ≤ 2L_m | F_{2^m} )
≤ exp( − c v_m ) ≤ exp( − c 2^{(2−2β_-)m} ).                                             (4.6)

Now note that (2−2β_-) > β_- (since β_- < 2/3), hence v_m ≫ L_m. Therefore, if K_{2^m} ≤ L_m and also sup_{I_m} K ≤ 2L_m, then with conditional probability at least 1 − exp(−c 2^{(2−2β_-)m}),
K_{2^{m+1}} ≥ K_{2^m} + v_m/2 > L_m + v_m/2 ≥ 2^{β_- (m+1)} for all large m.             (4.7)

If instead sup_{I_m} K > 2L_m, then K already exceeds L_m somewhere in I_m, which also helps. Combining these observations and using a union bound over m, the Borel–Cantelli lemma gives
P( K_{2^m} ≤ L_m i.o. ) = 0.
By monotonicity of K_n in n and the fact that j ↦ j^{β_-} grows at most by a constant factor on each I_m, we infer that almost surely for large n, K_n ≥ c n^{β_-}. This proves the lower bound in (4.4).

Upper bound (eventually K_n ≤ C n^{β_+})
Fix β_+ ∈ (2/3, 1) and set U_m := 2^{β_+ m}. Consider the stopping time
τ_m := inf{ n ∈ I_m : K_n ≥ U_m } (with inf ∅ = ∞).
On {τ_m < ∞}, for all j ≥ τ_m with j ∈ I_m, we have K_j ≥ U_m and hence
p_j = (j+1)/D_j ≤ (2^{m+1})/K_j^2 ≤ (2^{m+1})/U_m^2 = C·2^{(1−2β_+)m}.
Therefore, conditionally on F_{τ_m}, the expected number of additional blue draws on [τ_m, 2^{m+1}) is at most
v'_m := C'·2^{(2−2β_+)m}.                                                                  (4.8)

Across the block, the threshold U_n grows by an amount of order
Δ_m := U_{m+1} − U_m = (2^{β_+} − 1)·2^{β_+ m} ∼ c''·2^{β_+ m}.
Since β_+ > 2/3, we have Δ_m ≫ v'_m (because β_+ > 2 − 2β_+ ⇔ β_+ > 2/3).
Thus, to keep K_n above the moving threshold up to the end of the block from the first hitting time τ_m, the martingale fluctuation would need to exceed Δ_m − v'_m ≍ 2^{β_+ m}.

Let S_m := ∑_{j=τ_m}^{2^{m+1}-1} (ξ_{j+1} − p_j) be the martingale increment over [τ_m, 2^{m+1}). Its predictable quadratic variation satisfies
E[S_m^2 | F_{τ_m}] ≤ ∑_{j=τ_m}^{2^{m+1}-1} p_j(1−p_j) ≤ ∑ p_j ≤ v'_m.
Freedman (with x = Δ_m − v'_m and v = v'_m) yields
P( S_m ≥ Δ_m − v'_m | F_{τ_m} ) ≤ exp( − c (Δ_m − v'_m)^2 / (v'_m + (Δ_m − v'_m)/3) )
≤ exp( − c 2^{(4β_+ − 2)m} ).                                                              (4.9)

The right-hand side is summable in m since β_+ > 1/2. Therefore, with probability 1, only finitely many m satisfy τ_m < ∞. That is, almost surely for large m there is no hitting of U_m within I_m, hence K_n ≤ U_m for all n ∈ I_m. Since β_+ is fixed, this yields the upper bound in (4.4).

Conclusion of Stage A
We have proved (4.4) for any fixed β_- ∈ (1/2, 2/3) and β_+ ∈ (2/3, 1). Two consequences we will use repeatedly:
- Lower bound on the denominator: D_n = K_n^2 + K_n + 2n + 2 ≍ K_n^2 ≥ c n^{2β_-}, hence
  1/D_n ≤ C n^{-2β_-}.                                                                      (4.10)
- A crude upper bound on p_n and on the Y–martingale variance: from p_n ≤ (n+1)/K_n^2,
  p_n ≤ C n^{1−2β_+},                                                                       (4.11)
  and with K_n ≤ C n^{β_+},
  K_n^2 p_n ≤ C n^{2β_+} · n^{1−2β_+} = C n,                                                (4.12)
  while
  K_n^4 p_n / n^4 ≤ (n^{4β_+} · n^{1−2β_+})/n^4 = n^{2β_+ − 3}.                             (4.13)
Because β_+ < 1, we have 2β_+ − 3 < −1, so ∑ n^{2β_+ − 3} < ∞.

Stage B: convergence of Y_n = K_n^3/n^2 via Robbins–Siegmund

Exact one–step identity for Y_n
Recall K_{n+1} = K_n + ξ_{n+1}. A direct computation gives
K_{n+1}^3 − K_n^3 = (3K_n^2 + 3K_n + 1) ξ_{n+1}.                                      (4.14)
Hence
Y_{n+1} − Y_n
= K_n^3 ( 1/(n+1)^2 − 1/n^2 ) + (3K_n^2 + 3K_n + 1) ξ_{n+1}/(n+1)^2
= − Y_n (2n+1)/(n+1)^2 + (3K_n^2 + 3K_n + 1) ξ_{n+1}/(n+1)^2.                         (4.15)
Taking conditional expectation and using p_n = (n+1)/D_n and 3K_n^2 + 3K_n + 1 = 3D_n − (6n + 5), we obtain the exact drift
E[ Y_{n+1} − Y_n | F_n ]
= − Y_n (2n+1)/(n+1)^2 + 3/(n+1) − (6n+5)/((n+1) D_n).                                (4.16)

Separating the principal “1/n drift” and a summable error
Rewrite the first two terms as
− Y_n (2n+1)/(n+1)^2 + 3/(n+1)
= (3 − 2Y_n)/(n+1) + r_n^{(1)},   with   |r_n^{(1)}| ≤ C·( Y_n + 1 )/(n+1)^2.         (4.17)
Thus
E[ Y_{n+1} − Y_n | F_n ] = (3 − 2Y_n)/(n+1) + ε_n,                                    (4.18)
where the “error” ε_n is
ε_n := r_n^{(1)} − (6n+5)/((n+1) D_n).
By (4.17) and (4.10), for any β_- ∈ (1/2, 2/3),
|ε_n| ≤ C·( Y_n + 1 )/(n+1)^2 + C/D_n ≤ C·( Y_n + 1 )/(n+1)^2 + C n^{-2β_-}.          (4.19)

All terms on the right are summable almost surely: indeed Y_n = K_n^3/n^2 ≤ C n^{3β_+−2} by (4.4), so
∑ (Y_n + 1)/(n+1)^2 ≤ ∑ ( n^{3β_+−2}/n^2 + 1/n^2 ) < ∞,
and ∑ n^{-2β_-} < ∞ because 2β_- > 1. Therefore,
∑_{n} |ε_n| < ∞ almost surely.                                                         (4.20)

Noise term and its square summability
Define the martingale increment
N_{n+1} := (3K_n^2 + 3K_n + 1)( ξ_{n+1} − p_n )/(n+1)^2,
so that
Y_{n+1} − Y_n = (3 − 2Y_n)/(n+1) + ε_n + N_{n+1}.                                     (4.21)
Its conditional variance obeys, using p_n ≤ (n+1)/K_n^2,
E[ N_{n+1}^2 | F_n ] ≤ C·K_n^4/(n+1)^4 · p_n ≤ C·K_n^2/(n+1)^3.                      (4.22)
With K_n ≤ C n^{β_+} this gives
E[ N_{n+1}^2 | F_n ] ≤ C n^{2β_+ − 3},
and since β_+ < 1,
∑_{n} E[ N_{n+1}^2 | F_n ] < ∞ almost surely.                                         (4.23)
By the martingale convergence theorem, the series ∑ N_{n+1} converges almost surely.

A Robbins–Siegmund inequality for V_n = (Y_n − 3/2)^2
Set δ_n := Y_n − 3/2 and V_n := δ_n^2. From (4.21),
δ_{n+1} = δ_n − 2δ_n/(n+1) + ε_n + N_{n+1}.
Hence
V_{n+1} = δ_{n+1}^2
= (1 − 2/(n+1))^2 V_n + 2δ_n(ε_n + N_{n+1}) + (ε_n + N_{n+1})^2.                     (4.24)
Taking conditional expectations and using E[N_{n+1} | F_n] = 0,
E[ V_{n+1} | F_n ]
≤ (1 − 2/(n+1)) V_n + 2|δ_n||ε_n| + E[N_{n+1}^2 | F_n] + ε_n^2.                      (4.25)
Apply 2|δ_n||ε_n| ≤ (1/(n+1))V_n + (n+1)ε_n^2, and note (1 − 2/(n+1)) + 1/(n+1) = 1 − 1/(n+1). We obtain
E[ V_{n+1} | F_n ] ≤ (1 − 1/(n+1)) V_n + ρ_n,                                         (4.26)
where
ρ_n := (n+1)ε_n^2 + ε_n^2 + E[N_{n+1}^2 | F_n].
By (4.19), (4.23), and the bounds on Y_n, we have ∑ E[ρ_n] < ∞, hence ∑ ρ_n < ∞ almost surely.

We are now in the setting of the Robbins–Siegmund almost-supermartingale theorem: since ∑ 1/(n+1) = ∞ and ∑ ρ_n < ∞ a.s., it follows that (V_n) converges almost surely and moreover
∑_{n} (1/(n+1)) V_n < ∞ almost surely.
If the limit lim V_n were strictly positive, the last series would diverge, a contradiction. Hence
V_n → 0 almost surely, i.e.
Y_n → 3/2 almost surely.                                                                (4.27)

Asymptotics of K_n and G_n
From Y_n = K_n^3/n^2 → 3/2 a.s., we conclude
K_n ∼ (3/2)^{1/3} n^{2/3} almost surely.                                                (4.28)
Returning to (4.1),
G_n = K_n^2 + K_n + 2n + 2 = K_n^2 ( 1 + o(1) ) a.s.,
so
G_n / n^{4/3} = (K_n^2 / n^{4/3}) + o(1) → ((3/2)^{1/3})^2 = (3/2)^{2/3} almost surely.  (4.29)

This proves the desired statement with
α = 4/3 and c = (3/2)^{2/3}.

5. Gaps  
Gaps: None.

6. Self-evaluation  
- Confidence score (0–100): 82
- Known or suspected issues:
  - The dyadic-block proofs of the two–sided bounds (Stage A) use Freedman’s inequality with standard stopping-time arguments; I have kept the constants schematic, focusing on exponents. The steps are classical and quantitatively clear, but a fully expanded write-up could include more bookkeeping of the “for large m” thresholds.
  - I chose fixed exponents β_- ∈ (1/2, 2/3), β_+ ∈ (2/3, 1). This is enough for Stage B. A refinement (straightforward by the same block method) gives the sharper almost-sure law K_n = n^{2/3+o(1)} (i.e., for every ε>0, eventually n^{2/3−ε} ≤ K_n ≤ n^{2/3+ε}).
  - The stochastic-approximation step is fully quantified: I corrected the drift identity for Y_n, proved ∑|ε_n|<∞ and ∑E[N_{n+1}^2|F_n]<∞ from the Stage-A bounds, and applied a precise Robbins–Siegmund inequality to V_n.
- Coverage:
  - All parts are addressed.  
  - Stage A establishes coarse almost-sure bounds K_n ∈ [n^{β_-}, n^{β_+}] eventually (β_-∈(1/2,2/3), β_+∈(2/3,1)).  
  - Stage B proves Y_n → 3/2 a.s., hence K_n ∼ (3/2)^{1/3}n^{2/3} and G_n/n^{4/3} → (3/2)^{2/3} a.s.

---

---
# Expert evaluator's assessment and feedback on Solution Attempt 2

## Status  

Status: Partial  

## Score  

Score (0–100): 78  

---

## Major issues  

- **Location:** Stage A, lower bound for \(K_n\) (equations around (4.5)–(4.7), especially (4.6))  
  **Issue type:** Misuse of theory / logical error in application of Freedman’s inequality  
  **Description:**  
  To prove the eventual lower bound \(K_n \ge c n^{\beta_-}\), you introduce on each dyadic block \(I_m=[2^m,2^{m+1})\) the quantity  
  \[
  v_m := c\,2^{(2-2\beta_-)m}
  \]  
  and claim, on the event \(\sup_{I_m} K \le 2L_m\), that
  \[
  V_{2^{m+1}}-V_{2^m}
  = \sum_{j\in I_m} p_j(1-p_j)
  \le \sum_{j\in I_m} p_j
  \le 2v_m
  \]
  (where \(L_m = 2^{\beta_- m}\)). But you have only a **lower** bound on each \(p_j\) under \(\sup K\le2L_m\), namely
  \[
  p_j \ge c\,2^{(1-2\beta_-)m},
  \]
  hence \(\sum_{j\in I_m}p_j \ge v_m\); there is no argument that gives \(\sum_{j\in I_m}p_j\le 2v_m\). In fact, trivially \(\sum_{j\in I_m}p_j\le 2^m\), and since \(2^m \gg v_m\) (because \(2-2\beta_-<1\)), the bound \(\sum p_j\le 2 v_m\) is generally **false**. Thus the choice \(v=2v_m\) in Freedman’s inequality is unjustified, and the claimed tail bound (4.6) is not established.  
  This invalidates the key lemma that the increment \(K_{2^{m+1}}-K_{2^m}\) is typically at least \(v_m/2\) on blocks where \(\sup K\le 2L_m\), and hence the lower polynomial bound \(K_n \ge c n^{\beta_-}\) is not rigorously proved.  
  **Suggested direction for fix:**  
  - Replace the incorrect upper bound \(\sum_{j\in I_m}p_j \le 2 v_m\) by the trivial bound \(\sum_{j\in I_m} p_j \le 2^m\), and apply Freedman with a deterministic choice \(v = 2^m\).  
  - Recompute the exponent in the Freedman bound:
    \[
    x = v_m/2 \sim 2^{(2-2\beta_-)m},\quad v=2^m,
    \]
    and show that the exponent 
    \[
    \frac{x^2}{2(v+x/3)}
    \sim c\,2^{(3-4\beta_-)m}
    \]
    is still positive (since \(\beta_-<3/4\)), hence the probabilities remain exponentially small and summable over \(m\).  
  - Carefully re‑formulate the block argument using the **correct** variance bound and Freedman’s inequality, and then redo the Borel–Cantelli step. Until this is done, the lower bound \(K_n\ge c n^{\beta_-}\) is not established.

- **Location:** Stage A, conclusion of the lower bound (end of “Lower bound (eventually \(K_n\ge c n^{\beta_-}\))”)  
  **Issue type:** Missing critical case analysis / incomplete probabilistic argument  
  **Description:**  
  The narrative from (4.5)–(4.7) asserts that
  \[
  \mathbb P(K_{2^m}\le L_m\ \text{i.o.}) = 0,
  \]
  after combining Freedman on the block \(I_m\) with a statement about \(\sup_{I_m}K\). However, the event on which Freedman is applied and the event you wish to exclude are not cleanly related. In particular:
  - You must work conditionally on \(\{K_{2^m}\le L_m\}\), and on that event consider the disjoint alternatives \(\{\sup_{I_m}K > 2L_m\}\) vs \(\{\sup_{I_m}K\le2L_m\}\).  
  - Only on the second alternative can you use the drift lower bound with \(\sup K\le2L_m\).  
  - You then need to show that, conditional on \(\{K_{2^m}\le L_m\}\), the probability that both \(\sup_{I_m}K\le2L_m\) and \(K_{2^{m+1}}<L_{m+1}\) occur is summable in \(m\).  
  This decomposition and the associated conditional probabilities are not spelled out, so the Borel–Cantelli step is more heuristic than rigorous as written.  
  **Suggested direction for fix:**  
  - Define a “bad” event on each block, e.g.
    \[
    E_m := \{K_{2^m} \le L_m,\ \sup_{I_m} K \le 2L_m,\ K_{2^{m+1}} < L_{m+1}\}.
    \]
  - Prove (using the corrected Freedman step) that \(\mathbb P(E_m \mid \mathcal F_{2^m})\) is bounded by an exponentially small quantity uniformly, then show \(\sum_m \mathbb P(E_m) < \infty\).  
  - Conclude via Borel–Cantelli that only finitely many \(E_m\) occur, which rules out \(K_{2^m}\le L_m\) i.o. and yields the desired almost‑sure lower bound.

- **Location:** Stage B, control of \(\rho_n\) in (4.26) (“By (4.19), (4.23), and the bounds on \(Y_n\), we have \(\sum E[\rho_n] < \infty\)”)  
  **Issue type:** Insufficient justification / misuse of expectations  
  **Description:**  
  You define
  \[
  \rho_n := (n+1)\varepsilon_n^2 + \varepsilon_n^2 + \mathbb E[N_{n+1}^2 \mid \mathcal F_n]
  \]
  and then assert that \(\sum_n \mathbb E[\rho_n] < \infty\), hence \(\sum_n \rho_n < \infty\) a.s., based on (4.19), (4.23) and “the bounds on \(Y_n\)”. However:
  - The bounds on \(Y_n\) are **pathwise**, of the form \(Y_n(\omega)\le C(\omega)n^{3\beta_+-2}\). They do not immediately give any control on \(\mathbb E[Y_n]\) or \(\mathbb E[Y_n^2]\).  
  - To conclude \(\sum \mathbb E[\rho_n]<\infty\), you would need explicit integrable bounds on \(\varepsilon_n^2\) and hence on \((Y_n+1)^2\), which are not provided.  
  As written, the claim \(\sum \mathbb E[\rho_n]<\infty\) is not justified. Nonetheless, the *pathwise* exponents are strong enough to deduce that \(\sum \rho_n(\omega) < \infty\) for each \(\omega\), without taking expectations, but this argument is not presented.  
  **Suggested direction for fix:**  
  - Either: (a) stay entirely pathwise—show that for each \(\omega\), the polynomial bounds on \(K_n(\omega)\) and hence on \(Y_n(\omega)\) imply that the deterministic sequences
    \[
    (n+1)\varepsilon_n^2(\omega),\ \varepsilon_n^2(\omega),\ \mathbb E[N_{n+1}^2 \mid \mathcal F_n](\omega)
    \]
    are dominated by summable deterministic sequences in \(n\); hence \(\sum \rho_n(\omega)<\infty\) for all \(\omega\).  
  - Or: (b) explicitly bound \(\mathbb E[Y_n^2]\) (e.g. inductively) to justify that \(\mathbb E[\rho_n]\) is summable.  
  In either case, the step “\(\sum \mathbb E[\rho_n]<\infty\)” needs a clear, noncircular supporting argument.

- **Location:** Stage A → Stage B interface (use of \(D_n \gtrsim n^{2\beta_-}\) in (4.19) and summability \(\sum n^{-2\beta_-}<\infty\))  
  **Issue type:** Dependence on an unproven bound  
  **Description:**  
  In (4.19) you estimate
  \[
  | \varepsilon_n | \le C\frac{Y_n+1}{(n+1)^2} + \frac{C}{D_n} \le C\frac{Y_n+1}{(n+1)^2} + C n^{-2\beta_-},
  \]
  where the last inequality uses \(D_n \ge K_n^2 \ge c n^{2\beta_-}\). This crucially assumes the **proven** almost‑sure lower bound \(K_n\ge c n^{\beta_-}\) from Stage A. But as noted above, the argument establishing this bound has a serious flaw in the application of Freedman’s inequality. Therefore the error term estimate for \(\varepsilon_n\) and its summability \(\sum|\varepsilon_n|<\infty\) are not yet fully justified.  
  **Suggested direction for fix:**  
  - First repair Stage A as described above, obtaining a rigorous almost‑sure lower bound \(K_n\ge c n^{\beta_-}\) for some \(\beta_->1/2\).  
  - Then, and only then, insert this into (4.10)–(4.19) to get a valid, noncircular bound on \(\varepsilon_n\) with exponent \(2\beta_->1\), ensuring \(\sum n^{-2\beta_-}<\infty\).  
  Once Stage A is fully fixed, the subsequent SA analysis in Stage B becomes valid.

---

## Minor issues  

- **Location:** Equation (4.24) (expansion of \(V_{n+1} = (Y_{n+1}-3/2)^2\))  
  **Nature:** Minor algebraic slip / inequality vs equality  
  **Description:**  
  The exact algebra is
  \[
  \delta_{n+1}^2 
  = (1-\tfrac{2}{n+1})^2\delta_n^2 + 2(1-\tfrac{2}{n+1})\delta_n(\varepsilon_n+N_{n+1}) + (\varepsilon_n+N_{n+1})^2
  \]
  with \(\delta_n=Y_n-3/2\). You write instead
  \[
  V_{n+1} = (1-\tfrac{2}{n+1})^2 V_n + 2\delta_n(\varepsilon_n+N_{n+1}) + (\varepsilon_n+N_{n+1})^2,
  \]
  dropping the factor \((1-\tfrac{2}{n+1})\) in the cross term. This is harmless if interpreted as an inequality (since \(|1-2/(n+1)|\le 1\)), but it is written as an equality.  
  **Suggestion:**  
  Replace the equality by “\(\le\)” and explicitly note that you are bounding the cross term by enlarging its coefficient; this keeps the argument fully correct.

- **Location:** Equation (4.25) (coefficient of \(V_n\) after taking expectations)  
  **Nature:** Slight looseness in constants  
  **Description:**  
  From (4.24), the natural coefficient in front of \(V_n\) after taking expectations is \((1-2/(n+1))^2\). You replace this by \((1-2/(n+1))\), and later by \((1-1/(n+1))\), weakening the inequality. This is fine for Robbins–Siegmund (you only need some \(1-\alpha_n\) with \(\sum\alpha_n=\infty\)), but it is not explicitly stated that you are using the fact that \((1-2/(n+1))^2 \le (1-2/(n+1)) \le (1-1/(n+1))\).  
  **Suggestion:**  
  Add a brief remark that you replace \((1-2/(n+1))^2\) by a larger coefficient \(1-1/(n+1)\) to fit the standard almost‑supermartingale template and that this only makes the inequality weaker.

- **Location:** Statement “By (4.19), (4.23), and the bounds on \(Y_n\), we have \(\sum E[\rho_n] <\infty\)”  
  **Nature:** Clarity / overstatement  
  **Description:**  
  Since the “bounds on \(Y_n\)” are pathwise, not in expectation, the route to \(\sum E[\rho_n] <\infty\) is not immediate. Even if this can be justified, it would be better to separate the deterministic exponent estimates (which show that for each fixed \(\omega\), the series converges) from any use of expectation.  
  **Suggestion:**  
  Either remove the expectation from this step and argue pathwise, or explicitly estimate \(\mathbb E[Y_n^2]\) to support it. In any case, clarify where randomness vs. determinism enters the summability argument.

- **Location:** End of Stage A, “Conclusion of Stage A”  
  **Nature:** Slight under‑documentation  
  **Description:**  
  The transition from dyadic endpoints (\(K_{2^m}\)) to all \(n\) uses monotonicity of \(K_n\) and the fact that \(j\mapsto j^{\beta_-}\) grows only by a constant factor on each dyadic block. This is correct but not fully spelled out.  
  **Suggestion:**  
  Add a brief formula: for \(n\in[2^m,2^{m+1})\), \(n^{\beta_-}\le 2^{\beta_-}2^{\beta_-m}=2^{\beta_-}L_m\), so if \(K_{2^m}\ge L_m\) for all large \(m\), then there exists \(c>0\) such that \(K_n\ge c n^{\beta_-}\) for all large \(n\).

---

## Gap assessment  

The solver declared “Gaps: None.” I disagree; there remain at least two substantive gaps:

1. **Stage A: rigorous lower polynomial bound for \(K_n\)**  
   - This includes the misapplication of Freedman’s inequality (using an unjustified upper bound on \(\sum p_j\)) and the under‑specified conditional probability/Borel–Cantelli argument.  
   - **Assessment:** Fundamental.  
     This bound is essential to control \(D_n\) from below in Stage B and to prove the summability of the drift error \(\varepsilon_n\). Without it, you cannot legitimately pass to the stochastic‑approximation analysis for \(Y_n\).

2. **Stage B: summability of \(\rho_n\) and the expectations step**  
   - While the exponents are set up correctly, the route from pathwise polynomial bounds to \(\sum \rho_n < \infty\) via \(\sum E[\rho_n]<\infty\) is not rigorously justified.  
   - **Assessment:** Moderate.  
     It is relatively straightforward to repair by working pathwise (or by bounding \(\mathbb E[Y_n^2]\)), but until that is done, the formal hypotheses of the Robbins–Siegmund theorem are not verified.

The gaps labeled 2–4 in your first attempt’s write‑up (control of \(\varepsilon_n\), precise SA theorem, final step from \(Y_n\) to \(G_n\)) are now largely addressed, conditional on a correct Stage A. However, because Stage A is not fully repaired, the whole proof still falls short of a complete, unconditional argument.

---

## Coverage assessment  

All subparts addressed: No  

- The core problem is to show that there exist constants \(c>0,\alpha>0\) such that
  \[
  \frac{G_n}{n^\alpha} \to c \quad\text{a.s.}
  \]
- You have:
  - Correctly reduced the urn to the one‑dimensional process \(K_n\), with the exact formula \(G_n = K_n^2 + K_n + 2n + 2\).  
  - Carried out a detailed and largely correct stochastic‑approximation analysis of \(Y_n = K_n^3/n^2\) **assuming** coarse polynomial bounds on \(K_n\).  
  - Identified the natural values \(\alpha = 4/3\) and \(c = (3/2)^{2/3}\) and shown that, under the Stage A bounds, \(Y_n\to3/2\) a.s. and hence \(G_n/n^{4/3}\to (3/2)^{2/3}\) a.s.  
- However, due to the unresolved issues in Stage A (Freedman misapplication and incomplete Borel–Cantelli argument), the crucial lower growth bound on \(K_n\) is not yet rigorously established. Therefore the final almost‑sure convergence statement remains contingent on an unproven intermediate result.

---

## Summary  

Your second attempt is a substantial improvement over the first, especially in Stage B. The drift identity for \(Y_n = K_n^3/n^2\) is now correct, and you have successfully recast its evolution into a standard stochastic‑approximation form with step size \(\sim 1/n\), drift \(3-2Y_n\), and a martingale noise term. The Robbins–Siegmund almost‑supermartingale argument applied to \(V_n = (Y_n-3/2)^2\) is structurally sound: once the error and noise variances are shown to be summable, the conclusion \(Y_n \to 3/2\) a.s. follows in a textbook fashion. Likewise, the final step from \(Y_n\to 3/2\) to \(K_n\sim (3/2)^{1/3}n^{2/3}\) and \(G_n/n^{4/3}\to (3/2)^{2/3}\) is clean.  

The main weakness is in Stage A, where the desired coarse polynomial bounds \(n^{\beta_-}\lesssim K_n\lesssim n^{\beta_+}\) are derived via a dyadic‑block plus Freedman‑inequality argument. The set‑up is correct in spirit, but there is a nontrivial slip: an unjustified bound on \(\sum_{j\in I_m}p_j\) is used to control the quadratic variation, leading to an incorrect application of Freedman’s inequality. This undermines the proof of the lower growth bound on \(K_n\), which in turn feeds directly into the error estimates for \(\varepsilon_n\) in Stage B.  

Aside from that, there is a moderate issue in how you justify the summability of \(\rho_n\): the move from pathwise exponent bounds to \(\sum E[\rho_n] < \infty\) is not fully supported. However, this is technically easier to repair than the Stage A problem, since one can argue pathwise using the exponents already derived.  

Overall, your conceptual approach is excellent, your choice of the potential \(Y_n\) is very clever, and the stochastic‑approximation machinery is used appropriately. The proof is very close to complete, but a careful reworking of the Freedman‑based lower bound and a more explicit handling of the summability of \(\rho_n\) are still needed before the result can be regarded as fully rigorous.

---

## Recommendations for next iteration  

1. **Repair the Stage A lower bound for \(K_n\) carefully.**  
   - Revisit the application of Freedman’s inequality on each block \(I_m\). Use a deterministic upper bound for the quadratic variation, such as \(v = 2^m\), rather than the incorrect \(\sum p_j \le 2v_m\).  
   - Recompute the Freedman exponent with \(x = v_m/2\), \(v=2^m\), and verify that the resulting tail bound is still exponentially small and summable in \(m\).  
   - Formalize the conditional event structure (\(\{K_{2^m}\le L_m\}\), \(\{\sup_{I_m}K\le2L_m\}\), etc.) and prove rigorously that the probability of “bad” events on infinitely many blocks is zero by Borel–Cantelli.

2. **Make the block‑wise Borel–Cantelli argument explicit.**  
   - Define precisely the events \(E_m\) you want to exclude (those that would force \(K_{2^{m+1}}<L_{m+1}\) given \(K_{2^m}\le L_m\)).  
   - Use the corrected Freedman estimate to show that \(\sum_m \mathbb P(E_m) < \infty\).  
   - Then deduce that \(K_{2^m} \le L_m\) occurs only finitely often, and extend this to all \(n\) via monotonicity of \(K_n\) and the growth of \(n^{\beta_-}\).

3. **Reframe the summability of \(\rho_n\) in Stage B in a pathwise way.**  
   - Avoid passing through \(\sum E[\rho_n]\) unless you explicitly bound \(\mathbb E[Y_n^2]\). Instead, show directly that for each sample path, the almost‑sure bounds \(K_n(\omega) \in [c(\omega)n^{\beta_-}, C(\omega)n^{\beta_+}]\) imply  
     \[
     \sum_n (n+1)\varepsilon_n^2(\omega) < \infty,\quad
     \sum_n \varepsilon_n^2(\omega) < \infty,\quad
     \sum_n \mathbb E[N_{n+1}^2\mid\mathcal F_n](\omega) < \infty.
     \]
   - Conclude from these deterministic (in \(n\)) exponent estimates that \(\sum \rho_n(\omega)<\infty\) for all \(\omega\).

4. **Clarify the use of Freedman’s inequality for negative deviations.**  
   - You need to control both upper and lower deviations of \(M_{k} - M_s\). State explicitly that you apply Freedman to \(-M_k\) to bound \(\mathbb P(M_{k}-M_s \le -x)\), or quote a symmetric version for \(|M_k-M_s|\). This makes the direction of inequalities in your block arguments fully transparent.

5. **Tidy up the algebra around \(V_{n+1}\).**  
   - Rewrite (4.24) with the exact factor \((1-2/(n+1))\) in the cross term and then explicitly bound it as  
     \[
     2(1-\tfrac{2}{n+1})|\delta_n||\varepsilon_n|
     \le 2|\delta_n||\varepsilon_n|
     \le \tfrac{1}{n+1}V_n + (n+1)\varepsilon_n^2.
     \]
   - Indicate where you switch from \((1-2/(n+1))^2\) to \(1-1/(n+1)\) as the multiplicative coefficient in front of \(V_n\). This will make the Robbins–Siegmund step completely watertight.

6. **Optionally, generalize Stage A to obtain \(K_n = n^{2/3+o(1)}\) a.s.**  
   - Once the basic Stage A bounds are corrected, you can strengthen the argument to show that for every \(\varepsilon>0\),
     \[
     n^{2/3-\varepsilon} \le K_n \le n^{2/3+\varepsilon}
     \quad\text{eventually a.s.}
     \]
   - This is not strictly necessary for the main theorem but would provide a satisfying sharpening of your result and further check the internal consistency of your drift/martingale heuristics.

If you follow these recommendations—especially the first three—your existing structure should be sufficient to turn this second attempt into a fully rigorous proof.

---

## Research flag  

Research needed: No  

The remaining issues concern the correct and careful application of standard tools (Freedman’s inequality, Borel–Cantelli, Robbins–Siegmund) and bookkeeping of exponents. There is no indication that new theory or deep external results are required; the gaps can be closed by refining the existing arguments within the framework of classical martingale concentration and stochastic approximation.

---

# Solution Attempt 3 by the problem solver

2. Status  
Status: Partial

3. Solution

Overview of changes and improvements from Attempt 2
- I corrected the Freedman step in the lower bound for K_n by using a deterministic variance bound v=2^m on dyadic blocks (addressing the evaluator’s main objection).
- I defined precise “good block” events and proved that only finitely many blocks are “bad” via a summable Freedman bound. From this I deduced a rigorous almost-sure lower polynomial bound K_n ≥ c n^{β_-} for any fixed β_-∈(1/2,2/3).
- In the stochastic-approximation step for Y_n = K_n^3/n^2, I removed any use of expectations for the error summability and worked pathwise, as recommended. I also corrected a small algebraic slip in the V_{n+1} expansion and kept the multiplicative coefficients explicit.
- The only remaining gap is a fully rigorous upper polynomial bound K_n ≤ C n^{β_+} for some fixed β_+∈(2/3,1). I restate a clean Freedman-based route and reduce the proof to a block-hitting estimate, but I do not close this last step completely here.

Notation and exact identities
- R_n, B_n, G_n denote the numbers of red, blue, and total balls after n steps; K_n is the number of blue draws among the first n draws; ξ_{n+1}=1 iff draw n+1 is blue.
- Deterministic blue count: B_n = 1 + n.
- Counting reds as in Attempt 1:
  R_n = 1 + (n−K_n) + ∑_{k=1}^{K_n} (2k+1) = 1 + n + K_n^2 + K_n.
- Hence the total is
  G_n = K_n^2 + K_n + 2n + 2.                                             (3.1)
- Conditional blue probability at time n+1:
  p_n := P(ξ_{n+1}=1 | 𝔽_n) = B_n/G_n = (n+1)/(K_n^2 + K_n + 2n + 2) = (n+1)/D_n,  (3.2)
  where D_n := K_n^2 + K_n + 2n + 2.
- Drift–martingale decomposition:
  K_{n+1} = K_n + ξ_{n+1},  A_n := ∑_{j=0}^{n-1} p_j,  M_n := K_n − A_n = ∑_{j=0}^{n-1}(ξ_{j+1}−p_j),
  with |ΔM_{j+1}| ≤ 1 and predictable quadratic variation
  ⟨M⟩_n = ∑_{j=0}^{n-1} p_j(1−p_j) ≤ ∑_{j=0}^{n-1} p_j = A_n ≤ n.                    (3.3)

Freedman inequality (scalar version)
Let (M_k) be a martingale with |ΔM_k| ≤ 1 and predictable quadratic variation V_k. For any s<t and x,v>0,
P( sup_{s<k≤t} (M_k−M_s) ≥ x and V_t−V_s ≤ v ) ≤ exp( − x^2 / (2(v + x/3)) ).
The same bound holds for −M (lower tail) and for stopped martingales.

3.1. A rigorous almost-sure lower polynomial bound for K_n

Fix β_- ∈ (1/2, 2/3). For m∈ℕ let the dyadic block I_m := [2^m, 2^{m+1}). Define levels
L_m := 2^{β_- m}, v_m := c_0 2^{(2−2β_-) m}, with a fixed c_0∈(0,1) chosen below.

Good blocks and their probability
Define the “good block” event G_m by
G_m := { sup_{j∈I_m} K_j > 2L_m } ∪ { K_{2^{m+1}} − K_{2^m} ≥ v_m/2 }.
Claim: There exists c>0 (independent of the past) such that
P( G_m^c | 𝔽_{2^m} ) ≤ exp( − c 2^{(3−4β_-) m} )   a.s., for all large m.               (3.4)

Proof
On the event {sup_{I_m} K ≤ 2 L_m}, the denominator D_j in (3.2) satisfies, for all j∈I_m and large m,
D_j ≤ (2L_m)^2 + 2L_m + 2^{m+1} + 2 ≤ C 2^{2β_- m}.
Therefore p_j ≥ (j+1)/D_j ≥ 2^m / (C 2^{2β_- m}) = c_1 2^{(1−2β_-) m} for j∈I_m, large m.
Summing over |I_m| = 2^m gives a block-drift lower bound
∑_{j∈I_m} p_j ≥ c_2 2^{(2−2β_-) m} = v_m.                                             (3.5)
Let S_m := ∑_{j∈I_m} (ξ_{j+1}−p_j) be the martingale increment on I_m. Then
K_{2^{m+1}} − K_{2^m} = ∑_{j∈I_m} p_j + S_m.
Also, the predictable quadratic variation on I_m satisfies
V_{2^{m+1}} − V_{2^m} = ∑_{j∈I_m} p_j(1−p_j) ≤ ∑_{j∈I_m} p_j ≤ 2^m,                    (3.6)
the last inequality being trivial, hence deterministic. Applying Freedman to −S_m with x=v_m/2 and v=2^m yields
P( S_m ≤ −v_m/2 ) ≤ exp( − (v_m/2)^2 / (2(2^m + v_m/6)) ) ≤ exp( − c 2^{(3−4β_-) m} ),
since v_m ≪ 2^m for β_->1/2. Thus, on {sup_{I_m} K ≤ 2 L_m}, we have
P( K_{2^{m+1}} − K_{2^m} < v_m/2 | 𝔽_{2^m} ) ≤ exp( − c 2^{(3−4β_-) m} ).
On {sup_{I_m} K > 2L_m}, the block is good by definition. This proves (3.4). ∎

Borel–Cantelli for good blocks and a telescoping growth argument
By (3.4) and the summability of exp( − c 2^{(3−4β_-) m} ), the Borel–Cantelli lemma implies that, almost surely, G_m fails only finitely many times. Hence there exists an almost surely finite random M such that G_m occurs for all m ≥ M.

Now fix ω in the full-measure event where G_m holds for all m ≥ M. Consider any infinite subcollection S ⊂ {m ≥ M} such that K_{2^m}(ω) ≤ L_m for all m ∈ S. For each such m (with m large), since G_m holds, we are either in the “overshoot” case sup_{I_m}K > 2L_m or in the “drift” case K_{2^{m+1}} − K_{2^m} ≥ v_m/2. In the overshoot case, because K is nondecreasing and 2L_m > L_m, we have K_{2^{m+1}} − K_{2^m} ≥ 2L_m − K_{2^m} ≥ L_m. In the drift case, since v_m/2 ≫ L_m (because 2−2β_- > β_-), we have K_{2^{m+1}} − K_{2^m} ≥ L_m as well. Thus, uniformly for all m∈S large,
K_{2^{m+1}} − K_{2^m} ≥ L_m.                                                           (3.7)
Summing (3.7) over m∈S with M≤m≤m_k gives
K_{2^{m_k}} ≥ K_{2^M} + ∑_{m∈S, M≤m≤m_k−1} L_m.                                      (3.8)
Since L_m=2^{β_- m} grows and S is infinite, the partial sums on the right diverge; hence for k large, K_{2^{m_k}} > L_{m_k}, contradicting the choice of S. Therefore, almost surely, for all large m we have K_{2^m} > L_m.

Finally, for n∈[2^m, 2^{m+1}), monotonicity yields K_n ≥ K_{2^m} > L_m = 2^{β_- m} ≥ 2^{-β_-} n^{β_-}. We conclude:

Lemma 3.1 (Lower polynomial bound). For any fixed β_-∈(1/2,2/3), there exists a random constant c_-(ω)>0 and a random N_-(ω) such that, almost surely,
K_n ≥ c_- n^{β_-} for all n ≥ N_-.                                                    (3.9)

Remark
This lower bound is exactly what the evaluator requested for the bootstrap: it gives D_n ≥ K_n^2 ≥ c n^{2β_-} eventually, with 2β_->1.

3.2. Upper polynomial bound for K_n: what is needed and what is established

For the stochastic-approximation step below, it suffices to have any β_+∈(2/3,1) with
K_n ≤ C_+ n^{β_+}, eventually a.s.                                                      (3.10)

As in Attempt 2, there is a standard dyadic-block argument based on Freedman that suggests the following. Fix β_+∈(2/3,1) and define U_m := 2^{β_+ m}, Δ_m := U_{m+1}−U_m ≍ 2^{β_+ m}. Let
τ_m := inf{ n∈I_m: K_n ≥ U_m } (with inf∅=∞).
On {τ_m<∞}, for j∈[τ_m,2^{m+1}), we have K_j ≥ U_m, hence p_j ≤ (2^{m+1})/U_m^2 = C 2^{(1−2β_+)m}. Thus the conditional drift on the remainder of the block is at most v'_m := C' 2^{(2−2β_+)m}. A Freedman bound with variance v≤v'_m shows that
P( K_{2^{m+1}} − K_{τ_m} ≥ Δ_m | 𝔽_{τ_m} ) ≤ exp( − c 2^{(4β_+−2)m} ),                 (3.11)
which is summable as soon as β_+>1/2. Summing (3.11) suggests that only finitely many blocks can “keep up” from level U_m to U_{m+1}, hence one expects K_{2^m} < U_m eventually, and then by monotonicity K_n ≤ C n^{β_+} for all large n.

I have not fully written out the conditional Borel–Cantelli chain that turns (3.11) into (3.10) in a self-contained way, so I keep this as the remaining gap. In §3.4 below I proceed conditionally on (3.10) (with any β_+∈(2/3,1)), which is exactly the hypothesis used in Attempt 2 but now separated cleanly from the rest and clearly identified.

3.3. Exact drift for Y_n = K_n^3/n^2 and a Robbins–Siegmund scheme

Define Y_n := K_n^3/n^2 for n≥1. From K_{n+1}=K_n+ξ_{n+1} we have
K_{n+1}^3 − K_n^3 = (3K_n^2 + 3K_n + 1) ξ_{n+1}.
Hence
Y_{n+1} − Y_n = − Y_n (2n+1)/(n+1)^2 + (3K_n^2+3K_n+1) ξ_{n+1}/(n+1)^2.            (3.12)
Taking conditional expectation and inserting p_n=(n+1)/D_n together with 3K_n^2+3K_n+1=3D_n−(6n+5),
E[ Y_{n+1}−Y_n | 𝔽_n ] = − Y_n (2n+1)/(n+1)^2 + 3/(n+1) − (6n+5)/((n+1)D_n).        (3.13)

Main drift plus error
Rewrite
− Y_n (2n+1)/(n+1)^2 + 3/(n+1) = (3−2Y_n)/(n+1) + r_n^{(1)},
with |r_n^{(1)}| ≤ C (Y_n+1)/(n+1)^2. Set
ε_n := r_n^{(1)} − (6n+5)/((n+1)D_n),
so that
E[ Y_{n+1}−Y_n | 𝔽_n ] = (3−2Y_n)/(n+1) + ε_n.                                      (3.14)

Noise term
Define the martingale difference
N_{n+1} := (3K_n^2+3K_n+1)(ξ_{n+1}−p_n)/(n+1)^2,
so that the true recursion is
Y_{n+1} − Y_n = (3−2Y_n)/(n+1) + ε_n + N_{n+1}.                                      (3.15)

3.4. Pathwise summability of the perturbations under the coarse two-sided bounds

From Lemma 3.1 we have K_n ≥ c_- n^{β_-} eventually, so D_n ≥ K_n^2 ≥ c n^{2β_-}. Therefore,
|(6n+5)/((n+1)D_n)| ≤ C n^{-2β_-}, and, recalling |r_n^{(1)}| ≤ C (Y_n+1)/(n+1)^2,
|ε_n| ≤ C (Y_n+1)/(n+1)^2 + C n^{-2β_-}.                                               (3.16)
Moreover Y_n = K_n^3/n^2. Under the upper bound (3.10) with β_+<1, for all large n,
Y_n ≤ C n^{3β_+−2},
hence
∑_{n} (Y_n+1)/(n+1)^2 ≤ ∑_{n} (n^{3β_+−2}/n^2 + 1/n^2) = ∑_{n} (n^{3β_+−4} + n^{-2}) < ∞,
since 3β_+−4 < −1 for every β_+<1. Also 2β_->1 implies ∑ n^{-2β_-}<∞. Thus, pathwise,
∑_{n} |ε_n| < ∞.                                                                       (3.17)

Next, the conditional variance of N_{n+1} obeys (using p_n ≤ (n+1)/K_n^2 ≤ C n/K_n^2)
E[ N_{n+1}^2 | 𝔽_n ] ≤ C (K_n^4/(n+1)^4) p_n ≤ C K_n^2/(n+1)^3.                      (3.18)
Under K_n ≤ C n^{β_+} with β_+<1,
E[ N_{n+1}^2 | 𝔽_n ] ≤ C n^{2β_+−3}, and since 2β_+−3 < −1, we have
∑_{n} E[ N_{n+1}^2 | 𝔽_n ] < ∞  almost surely.                                         (3.19)
Thus the martingale ∑ N_{n+1} converges almost surely (and in L^2).

3.5. Robbins–Siegmund almost-supermartingale argument

Let δ_n := Y_n − 3/2 and V_n := δ_n^2. From (3.15),
δ_{n+1} = (1−2/(n+1)) δ_n + ε_n + N_{n+1}.
Hence
V_{n+1}
= (1−2/(n+1))^2 V_n + 2(1−2/(n+1)) δ_n(ε_n + N_{n+1}) + (ε_n + N_{n+1})^2.
Using |1−2/(n+1)| ≤ 1 and the inequality 2|ab| ≤ (1/(n+1))a^2 + (n+1)b^2 with a=δ_n and b=ε_n, and then taking conditional expectations,
E[ V_{n+1} | 𝔽_n ]
≤ (1−2/(n+1))^2 V_n + (1/(n+1)) V_n + (n+1)ε_n^2 + ε_n^2 + E[ N_{n+1}^2 | 𝔽_n ].
Since (1−2/(n+1))^2 + 1/(n+1) ≤ 1 − 1/(n+1) for all n≥1, we get
E[ V_{n+1} | 𝔽_n ] ≤ (1 − 1/(n+1)) V_n + ρ_n,                                         (3.20)
where
ρ_n := (n+1)ε_n^2 + ε_n^2 + E[ N_{n+1}^2 | 𝔽_n ].
By (3.16) and (3.10), for all large n,
ε_n^2 ≤ C ( n^{2(3β_+−4)} + n^{-4β_-} + n^{3β_+−4} n^{-2β_-} ) ≤ C' ( n^{2(3β_+−4)} + n^{-4β_-} ),
hence ∑ (n+1) ε_n^2 < ∞ and ∑ ε_n^2 < ∞ because 3β_+−4 < −1 and 2β_->1. Together with (3.19), we obtain the pathwise summability
∑ ρ_n < ∞ almost surely.                                                                (3.21)

We are now in the standard Robbins–Siegmund setup: with a_n=1/(n+1), ∑ a_n=∞ and ∑ ρ_n<∞, (3.20) implies that (V_n) converges almost surely and that ∑ a_n V_n < ∞ a.s. The latter forces lim inf V_n = 0; since V_n converges, we conclude V_n → 0 almost surely. Therefore
Y_n → 3/2 almost surely.                                                                (3.22)

Consequently,
K_n^3/n^2 → 3/2 a.s.  ⇒  K_n ∼ (3/2)^{1/3} n^{2/3} a.s.,                              (3.23)
and from (3.1),
G_n = K_n^2 + K_n + 2n + 2 = K_n^2(1+o(1)), so
G_n / n^{4/3} → ((3/2)^{1/3})^2 = (3/2)^{2/3} almost surely.                           (3.24)

3.6. Conditional conclusion and what remains to be filled

- What is rigorously proved above:
  - The exact reduction G_n = K_n^2 + K_n + 2n + 2.
  - The exact drift decomposition (3.14) for Y_n = K_n^3/n^2.
  - A rigorous lower bound K_n ≥ c_- n^{β_-} eventually a.s. for any β_-∈(1/2,2/3).
  - Under the (very plausible and standard) coarse upper bound K_n ≤ C_+ n^{β_+} eventually a.s. for some β_+∈(2/3,1), we have Y_n → 3/2 a.s., hence K_n ∼ (3/2)^{1/3} n^{2/3} and G_n/n^{4/3} → (3/2)^{2/3} a.s.

- What remains:
  - Close the Freedman-based upper bound (3.10) cleanly. As outlined around (3.11), one controls the probability, conditionally on hitting level U_m inside block I_m, of also reaching the next level U_{m+1} by the end of the block. The resulting exponentially small probabilities are summable, and a conditional Borel–Cantelli argument then shows that only finitely many such successive level-to-level “keeps up” events occur. From here, one deduces that K_{2^m} < U_m for all large m, and thence K_n ≤ C n^{β_+} eventually. I have not written this part in full detail here.

4. Gaps

Gap 1: Upper polynomial bound for K_n
- Location: §3.2 (and used in §3.4).
- Description: I need to turn the block-hitting estimate (3.11) into a full proof that, for some β_+∈(2/3,1), one has K_n ≤ C n^{β_+} eventually a.s. This requires a clean conditional Borel–Cantelli scheme over dyadic blocks and a short induction to pass from “finitely many successive level-to-level keeps up” to “no level U_m is reached at dyadic endpoints for large m.”
- Reason for difficulty: While the Freedman estimate (3.11) is straightforward, organizing the conditional events across blocks so that the Borel–Cantelli lemma applies in an unambiguous, non-circular way needs some careful bookkeeping. This is a standard step in SA/urn analyses, but it is technical and I have left it to be completed.

5. Self-evaluation
- Confidence score (0–100): 74
- Known or suspected issues:
  - The lower bound for K_n is now rigorous and fixes the evaluator’s main criticism of Attempt 2 (incorrect use of an upper bound on ∑ p_j). The good-block construction with v=2^m in Freedman gives a summable tail and yields K_n ≥ c n^{β_-} a.s. for any β_->1/2.
  - The stochastic-approximation part for Y_n is complete once the coarse upper bound K_n ≤ C n^{β_+} (β_+<1) is available. I verified all perturbation summability pathwise, and used a precise Robbins–Siegmund inequality to conclude Y_n→3/2 a.s.
  - The remaining gap is the rigorous derivation of the coarse upper bound K_n ≤ C n^{β_+}. The route is standard and sketched via (3.11), but I did not spell out the conditional Borel–Cantelli argument fully here.
- Coverage:
  - The reduction to K_n and the exact drift for Y_n are fully addressed.
  - The lower polynomial bound for K_n (key bootstrap) is fully rigorous.
  - The convergence Y_n→3/2, hence K_n∼(3/2)^{1/3} n^{2/3} and G_n/n^{4/3}→(3/2)^{2/3}, is proved under a standard coarse upper bound on K_n; the missing piece is to establish that upper bound unconditionally.

---

# Expert evaluator's assessment and feedback on Solution Attempt 3

2. Status  
Status: Partial

3. Score  
Score (0–100): 70

4. Major issues  
- Location: Stage A, “Borel–Cantelli for good blocks and a telescoping growth argument” (eqs. (3.7)–(3.9))  
  Issue type: Logical error / insufficiently justified inference  
  Description: After showing that “good blocks” occur eventually a.s., you deduce that for any infinite set S with K_{2^m} ≤ L_m (m ∈ S), one has K_{2^{m+1}} − K_{2^m} ≥ L_m for each m ∈ S, then sum over m ∈ S to conclude K_{2^{m_k}} > L_{m_k} for large k, a contradiction. The inference “divergent partial sums over S force K_{2^{m_k}} > L_{m_k}” is not valid in general: S may be very sparse (e.g., m_k = 2^k), in which case ∑_{m∈S, m<m_k} L_m can remain o(L_{m_k}), so no contradiction follows.  
  Suggested direction for fix: Replace the telescoping argument by a clean “one‑step escape” implication combined with a short-range dependence argument. A robust way is:
  - Prove (and state explicitly) the implication: for all large m, if the block m is good and K_{2^m} ≤ L_m, then K_{2^{m+1}} > L_{m+1} (both “overshoot” and “drift” branches give this, because v_m/2 ≫ L_{m+1}).  
  - Then show that a down‑crossing at time m (i.e., K_{2^m} ≤ L_m) implies that at least one of the last w blocks {m−w,…,m−1} must be bad for some fixed w chosen so that ∑_{i=1}^w L_{m-i} ≥ L_m (possible since 2^{β_-} > 1 and the geometric tail sum can be made >1 by taking w large).  
  - By summability of bad‑block probabilities (Freedman), a union bound over sliding windows, and Borel–Cantelli, conclude that only finitely many down‑crossings occur. This removes the need for the flawed sparse‑S summation.

- Location: Stage A, conditional Freedman step and probability quantification (eq. (3.4))  
  Issue type: Justification gap / conditional vs unconditional bound  
  Description: You state P(G_m^c | 𝔽_{2^m}) ≤ exp(−c 2^{(3−4β_-)m}) “a.s., for all large m.” The argument uses a deterministic bound V_{2^{m+1}}−V_{2^m} ≤ 2^m and then applies Freedman to −S_m with x = v_m/2. While Freedman indeed yields a bound independent of the past when v is deterministic, the conditioning “| 𝔽_{2^m}” should be explained carefully, or you should present the inequality unconditionally and then apply Borel–Cantelli to the unconditional probabilities.  
  Suggested direction for fix: State and use the conditional Freedman inequality explicitly (or work unconditionally with the deterministic variance bound v = 2^m). Make clear that the bound holds uniformly over 𝔽_{2^m}, so that summability in m follows and Borel–Cantelli applies.

- Location: Stage A → Stage B interface (use of the lower bound in (3.16))  
  Issue type: Dependence on a still‑unproven result  
  Description: The estimate |ε_n| ≤ C (Y_n+1)/(n+1)^2 + C n^{−2β_-} and its summability rely on D_n ≥ c n^{2β_-}, i.e., on the Stage‑A lower bound. Since the lower bound proof still has the logical gap above, the summability of ε_n, and hence the Robbins–Siegmund step, are not yet unconditionally valid.  
  Suggested direction for fix: First complete the lower bound using the sliding‑window “bad implies down‑crossing” argument. Then the bound D_n ≥ c n^{2β_-} (with 2β_->1) becomes rigorously available for use in Stage B.

- Location: Stage 3.2 (Upper polynomial bound)  
  Issue type: Missing critical case  
  Description: The coarse upper bound K_n ≤ C n^{β_+} (β_+ ∈ (2/3,1)) is still only sketched. Stage B depends on it to guarantee square‑summable noise and error.  
  Suggested direction for fix: Formalize the dyadic “level‑to‑level” argument with hitting times τ_m and events “keep up from U_m to U_{m+1} within block I_m.” Define E_m^{up} := {τ_m<∞ and K_{2^{m+1}}−K_{τ_m} ≥ Δ_m}. Use deterministic variance bound v ≤ v'_m and Freedman to get P(E_m^{up} | 𝔽_{τ_m}) ≤ exp(−c·2^{β_+ m}) (the denominator is dominated by x/3 when β_+>2/3). Then apply a conditional Borel–Cantelli/renewal argument to show only finitely many keeps‑up occur, hence K_{2^m} < U_m for large m, and extend to all n.

5. Minor issues  
- Location: Stage 3.2, Freedman exponent in (3.11)  
  Nature: Minor computational slip  
  Suggestion: With x = Δ_m ∼ 2^{β_+ m} and v ≤ v'_m ∼ 2^{(2−2β_+)m}, for β_+>2/3 one has v ≪ x, so v + x/3 ≍ x and the exponent is of order c·x ∼ c·2^{β_+ m}, not 2^{(4β_+−2)m}. The bound remains summable; correct the display to avoid confusion.

- Location: Eq. (3.20) transition  
  Nature: Inequality bookkeeping  
  Suggestion: Explicitly justify (1−2/(n+1))^2 + 1/(n+1) ≤ 1−1/(n+1) for n≥1, and note that you are intentionally weakening the coefficient to fit the standard almost‑supermartingale form.

- Location: Global presentation  
  Nature: Clarity/structure  
  Suggestion: Fix the constants c_0, c_1, c_2 once and for all at their first appearance; specify “for all large m ≥ M_0” thresholds explicitly to improve readability.

6. Gap assessment  
- Reported gap by solver: Upper polynomial bound K_n ≤ C n^{β_+}.  
  Assessment: Moderate. The path to a proof is standard via dyadic levels and Freedman; it needs careful conditioning and Borel–Cantelli but no new ideas.

- Unreported gap (reopened here): Lower polynomial bound K_n ≥ c n^{β_-}.  
  Assessment: Moderate to fundamental. The Freedman part is fine, but the final contradiction via summing over a sparse infinite set S is invalid. A corrected sliding‑window/Borel–Cantelli argument as suggested above should close it without changing the overall approach.

Given these, Stage B (Robbins–Siegmund) is currently conditional on Stage A being fully rigorous.

7. Coverage assessment  
All subparts addressed: No  
- Correct reduction G_n = K_n^2 + K_n + 2n + 2: complete.  
- Stage A lower bound: substantially improved but still not airtight (needs the sliding‑window correction).  
- Stage A upper bound: outlined but not proved.  
- Stage B (SA/Robbins–Siegmund): clean and correct conditional on the coarse two‑sided bounds.  
- Final conclusion G_n / n^{4/3} → (3/2)^{2/3}: established only under the unproven upper bound and the corrected lower bound.

8. Summary  
This attempt meaningfully advances the proof. The Freedman application for the lower bound now uses a deterministic variance control, and the stochastic‑approximation part is cast cleanly in a Robbins–Siegmund framework with all perturbations checked pathwise once coarse bounds hold. The choice of Y_n = K_n^3/n^2 and the identification of drift (3 − 2Y_n)/(n+1) are elegant and align with standard SA theory. However, the Stage‑A lower bound still contains a logical gap: the telescoping argument that an infinite set of “under‑threshold” blocks forces a contradiction is not valid for sparse subsequences. This can be repaired by a short “sliding‑window” refinement that ties any down‑crossing to the occurrence of a recent bad block; Freedman then makes such events summable. The coarse upper bound remains to be written out rigorously; the needed ingredients (level‑to‑level Freedman bounds and a conditional Borel–Cantelli) are standard. Once both coarse bounds are solidified, your Stage‑B Robbins–Siegmund argument should yield Y_n → 3/2 a.s., hence K_n ∼ (3/2)^{1/3} n^{2/3} and G_n / n^{4/3} → (3/2)^{2/3} a.s. The approach is promising and close to completion, but it is not yet a full solution.

9. Recommendations for next iteration  
- Repair the lower bound via a sliding‑window argument:  
  - Fix β_- ∈ (1/2, 2/3) and choose w so that ∑_{i=1}^w 2^{-β_- i} > 1.  
  - Show that if all of the last w blocks are “good,” then K_{2^m} must exceed L_m; hence any down‑crossing at m forces at least one of these w blocks to be bad.  
  - Use the summable Freedman bounds and a union bound over the w previous blocks to conclude, by Borel–Cantelli, that down‑crossings occur only finitely many times a.s.

- Finish the upper bound rigorously:  
  - Define τ_m = inf{n ∈ I_m : K_n ≥ U_m} with U_m = 2^{β_+ m}.  
  - Condition on 𝔽_{τ_m} and apply Freedman with x = Δ_m = U_{m+1} − U_m and v ≤ v'_m = ∑_{j≥τ_m} p_j to get P(keep‑up on I_m | 𝔽_{τ_m}) ≤ exp(−c 2^{β_+ m}).  
  - Use a renewal/Borel–Cantelli argument to show only finitely many keep‑ups, whence K_{2^m} < U_m eventually and K_n ≤ C n^{β_+} for all large n.

- Make the conditional/probabilistic structure explicit:  
  - For both lower and upper bounds, define the precise “bad” events E_m (and E_m^{up}) you aim to exclude and prove that ∑ P(E_m) < ∞ (or a conditional version that implies the same).  
  - This will remove any ambiguity about conditioning and measurability.

- Keep Stage B strictly pathwise:  
  - After completing Stage A, restate the summability of ε_n and of the conditional variances as deterministic exponent comparisons along sample paths; then invoke Robbins–Siegmund exactly as in §3.5.

- Optional but helpful: Present a sharpened asymptotic K_n = n^{2/3+o(1)} a.s.  
  - The dyadic block method readily yields for each ε>0 eventual bounds n^{2/3−ε} ≤ K_n ≤ n^{2/3+ε}; adding this will both strengthen the result and serve as an internal consistency check.

10. Research flag  
Research needed: No  
All remaining steps can be completed with standard tools (Freedman’s inequality, conditional Borel–Cantelli, Robbins–Siegmund). No new external theory appears necessary; what remains is careful organization of the martingale/concentration arguments and bookkeeping of exponents.

---

# Solution Attempt 4 by the problem solver

2. Status  
Status: Complete

3. Solution

Summary of what is new with respect to Attempt 3
- Stage A (bootstrap) is now fully rigorous on both sides:
  - Lower bound: I introduce block “goodness” events H_m and prove that P(H_m^c) is summable via a deterministic-variance Freedman bound. From the one-step implication “H_m ⇒ K_{2^{m+1}} ≥ L_{m+1}” I deduce, by Borel–Cantelli, that K_{2^m} ≥ L_m eventually.
  - Upper bound: Instead of the earlier keep-up scheme, I use the simple moment bound E[K_n^3] ≤ C n^2 and a dyadic Markov–Borel–Cantelli argument to get K_{2^m} ≤ 2^{β_+ m} eventually for every β_+>2/3, hence K_n ≤ C n^{β_+} eventually.
- Stage B (stochastic approximation for Y_n = K_n^3/n^2) is then carried out pathwise as in Attempt 3; with the improved Stage A, all summability requirements are verified without circularity.

3.1. Notation and exact identities

- Let K_n be the number of blue draws by time n, and let R_n, B_n, G_n be the numbers of red, blue, and total balls after n steps. The drawn ball is always returned; additions depend on its color as in the statement.
- Blue balls: exactly one blue is added at every step, hence B_n = 1 + n deterministically.
- Red balls: there are n − K_n red draws (each adds 1 red), and the k-th blue draw adds 2k+1 reds, so
  R_n = 1 + (n − K_n) + ∑_{k=1}^{K_n} (2k + 1) = 1 + n + K_n^2 + K_n.
- Total
  G_n = R_n + B_n = K_n^2 + K_n + 2n + 2.                                  (3.1)
- Let ξ_{n+1} = 1{draw n+1 is blue}. Then K_{n+1} = K_n + ξ_{n+1} and
  p_n := P(ξ_{n+1}=1 | 𝔽_n) = B_n/G_n = (n+1)/(K_n^2 + K_n + 2n + 2) = (n+1)/D_n.
- Drift–martingale decomposition:
  A_n := ∑_{j=0}^{n-1} p_j,  M_n := K_n − A_n = ∑_{j=0}^{n-1} (ξ_{j+1} − p_j).
  Then M_n is a martingale with bounded increments |ΔM_{j+1}| ≤ 1 and predictable quadratic variation
  ⟨M⟩_n = ∑_{j=0}^{n-1} p_j(1 − p_j) ≤ ∑_{j=0}^{n-1} p_j = A_n ≤ n.          (3.2)

Freedman inequality (scalar, bounded increments). If (M_k) is a martingale with |ΔM_k| ≤ 1 and predictable quadratic variation V_k, then for any s < t and any x, v > 0,
P( sup_{s<k≤t} (M_k − M_s) ≥ x and V_t − V_s ≤ v ) ≤ exp( − x^2 / (2(v + x/3)) ).
The same bound holds for −M (lower tail) and for martingales started at a (bounded-increment) stopping time.

3.2. Stage A: coarse polynomial bounds for K_n

Lower bound: K_n ≥ c n^{β_-} eventually a.s. for any β_- ∈ (1/2, 2/3).

Fix β_- ∈ (1/2, 2/3). For m ∈ ℕ set the dyadic block I_m := [2^m, 2^{m+1}), the level L_m := 2^{β_- m}, and the target drift size v_m := c_0 2^{(2 − 2β_-) m} with c_0 small enough (fixed below).

Define the “good block” event H_m by
H_m := { sup_{j∈I_m} K_j > 2 L_m } ∪ { S_m ≥ − v_m/2 },
where S_m := ∑_{j∈I_m} (ξ_{j+1} − p_j).

Lemma 3.1 (Good blocks are overwhelmingly likely). For all large m,
P( H_m^c | 𝔽_{2^m} ) ≤ exp( − c 2^{(3 − 4β_-) m} ) almost surely.

Proof. On the event {sup_{I_m} K ≤ 2 L_m}, we have for all j ∈ I_m and m large
D_j = K_j^2 + K_j + 2j + 2 ≤ (2L_m)^2 + 2^{m+2} ≤ C 2^{2β_- m},
since 2β_- > 1. Thus p_j ≥ (j+1)/D_j ≥ 2^m/(C 2^{2β_- m}) = c_1 2^{(1 − 2β_-) m}, and summing over |I_m| = 2^m gives
∑_{j∈I_m} p_j ≥ c_2 2^{(2 − 2β_-) m} = v_m.                             (3.3)
For the martingale S_m on I_m we also have the deterministic bound
V_{2^{m+1}} − V_{2^m} = ∑_{j∈I_m} p_j(1 − p_j) ≤ ∑_{j∈I_m} p_j ≤ 2^m.     (3.4)
Applying Freedman to −S_m with x = v_m/2 and v = 2^m yields
P( S_m ≤ − v_m/2 and sup_{I_m} K ≤ 2 L_m | 𝔽_{2^m} )
≤ exp( − (v_m/2)^2 / (2(2^m + v_m/3)) )
≤ exp( − c 2^{(3 − 4β_-) m} ),
because v_m ≪ 2^m for β_- > 1/2. By definition, H_m^c ⊂ {sup_{I_m} K ≤ 2 L_m and S_m ≤ − v_m/2}, whence the claim. ∎

Key one-step implication. If H_m occurs, then K_{2^{m+1}} ≥ L_{m+1}.

Indeed, on H_m either (i) sup_{I_m} K > 2L_m, in which case K_{2^{m+1}} ≥ 2L_m ≥ L_{m+1}; or (ii) S_m ≥ − v_m/2 and sup_{I_m}K ≤ 2L_m. In case (ii), (3.3) gives ∑_{j∈I_m} p_j ≥ v_m and so
K_{2^{m+1}} − K_{2^m} = ∑_{j∈I_m} p_j + S_m ≥ v_m/2,
hence K_{2^{m+1}} ≥ K_{2^m} + v_m/2 ≥ L_m + v_m/2 ≥ L_{m+1} for large m, since
v_m/2 ≥ (2^{β_-} − 1) 2^{β_- m} ⇔ 2 − 2β_- > β_- (true because β_- < 2/3).

By Lemma 3.1, ∑_m P(H_m^c) < ∞, hence H_m fails only finitely many times a.s. By the one-step implication, there is (a random) M such that for all m ≥ M: K_{2^{m+1}} ≥ L_{m+1}. Thus K_{2^m} ≥ L_m for all m ≥ M+1. Finally, for n ∈ [2^m, 2^{m+1}), monotonicity gives
K_n ≥ K_{2^m} ≥ L_m = 2^{β_- m} ≥ 2^{-β_-} n^{β_-}.
We have proved:

Proposition 3.2 (Lower bound). For any β_- ∈ (1/2, 2/3), there exist random c_->0 and N_- such that K_n ≥ c_- n^{β_-} for all n ≥ N_- almost surely.

Upper bound: K_n ≤ C n^{β_+} eventually a.s. for any β_+ ∈ (2/3, 1).

We first bound the third moment.

Lemma 3.3 (Moment bound). There is C<∞ such that E[K_{n+1}^3 − K_n^3 | 𝔽_n] ≤ C(n+1) a.s., hence E[K_n^3] ≤ C n^2 for all n.

Proof. Since K_{n+1}^3 − K_n^3 = (3K_n^2 + 3K_n + 1) ξ_{n+1}, we have
E[K_{n+1}^3 − K_n^3 | 𝔽_n] = (3K_n^2 + 3K_n + 1) p_n.
Use p_n ≤ min{ (n+1)/K_n^2, 1/2 } (the latter because D_n ≥ 2n+2). If K_n^2 ≥ 2(n+1), then
(3K_n^2 + 3K_n + 1) p_n ≤ (3 + 3/K_n + 1/K_n^2) (n+1) ≤ 7(n+1).
If K_n^2 < 2(n+1), then
(3K_n^2 + 3K_n + 1) p_n ≤ (3K_n^2 + 3K_n + 1)/2 ≤ 3(n+1) + O(√n) ≤ 4(n+1).
Thus E[K_{n+1}^3] ≤ E[K_n^3] + 7(n+1), whence E[K_n^3] ≤ C n^2 by summation. ∎

Corollary 3.4 (Dyadic upper bound). Fix β_+ > 2/3. Then
∑_{m=1}^∞ P( K_{2^m} ≥ 2^{β_+ m} ) ≤ ∑_{m=1}^∞ E[K_{2^m}^3] / 2^{3β_+ m}
≤ C ∑_{m=1}^∞ 2^{(2 − 3β_+) m} < ∞.
By Borel–Cantelli, K_{2^m} ≤ 2^{β_+ m} eventually a.s. Monotonicity yields K_n ≤ K_{2^{m+1}} ≤ 2^{β_+(m+1)} ≤ C n^{β_+} for n ∈ [2^m, 2^{m+1}), hence:

Proposition 3.5 (Upper bound). For any β_+ ∈ (2/3, 1), there exist random C_+ and N_+ such that K_n ≤ C_+ n^{β_+} for all n ≥ N_+ almost surely.

Combining Propositions 3.2 and 3.5 we have: for any 1/2 < β_- < 2/3 < β_+ < 1, almost surely for all large n,
c_- n^{β_-} ≤ K_n ≤ C_+ n^{β_+}.                                          (3.5)

3.3. Stage B: stochastic approximation for Y_n = K_n^3/n^2

Define Y_n := K_n^3/n^2 (n ≥ 1). From K_{n+1} = K_n + ξ_{n+1} we compute
K_{n+1}^3 − K_n^3 = (3K_n^2 + 3K_n + 1) ξ_{n+1},
hence
Y_{n+1} − Y_n
= − Y_n (2n+1)/(n+1)^2 + (3K_n^2 + 3K_n + 1) ξ_{n+1}/(n+1)^2.            (3.6)
Taking conditional expectation, using p_n = (n+1)/D_n and 3K_n^2 + 3K_n + 1 = 3D_n − (6n+5),
E[ Y_{n+1} − Y_n | 𝔽_n ]
= − Y_n (2n+1)/(n+1)^2 + 3/(n+1) − (6n+5)/((n+1) D_n).                  (3.7)

Split the principal 1/(n+1)-drift and a summable error:
− Y_n (2n+1)/(n+1)^2 + 3/(n+1) = (3 − 2Y_n)/(n+1) + r_n^{(1)},
with |r_n^{(1)}| ≤ C (Y_n + 1)/(n+1)^2. Set
ε_n := r_n^{(1)} − (6n+5)/((n+1) D_n),   N_{n+1} := (3K_n^2 + 3K_n + 1)(ξ_{n+1} − p_n)/(n+1)^2,
so that the exact recursion is
Y_{n+1} − Y_n = (3 − 2Y_n)/(n+1) + ε_n + N_{n+1}.                        (3.8)

Summability of perturbations (pathwise, using (3.5)).

- Error ε_n. From (3.5), D_n = K_n^2 + K_n + 2n + 2 ≥ K_n^2 ≥ c n^{2β_-} for large n; also Y_n = K_n^3/n^2 ≤ C n^{3β_+ − 2}. Hence
|ε_n| ≤ C (Y_n + 1)/(n+1)^2 + C/D_n ≤ C( n^{3β_+ − 4} + n^{-2} + n^{-2β_-} ).
Since β_+ < 1 and β_- > 1/2, all three series are summable, so
∑_{n=1}^∞ |ε_n| < ∞ almost surely.                                            (3.9)

- Noise N_{n+1}. Using p_n ≤ (n+1)/K_n^2 and (3.5),
E[ N_{n+1}^2 | 𝔽_n ] ≤ C (K_n^4/(n+1)^4) p_n ≤ C K_n^2/(n+1)^3 ≤ C n^{2β_+ − 3}.
Since 2β_+ − 3 < −1, we have ∑_n E[ N_{n+1}^2 | 𝔽_n ] < ∞ a.s., so the martingale ∑ N_{n+1} converges almost surely (and in L^2).                                 (3.10)

Robbins–Siegmund almost-supermartingale argument.

Let δ_n := Y_n − 3/2 and V_n := δ_n^2. From (3.8),
δ_{n+1} = (1 − 2/(n+1)) δ_n + ε_n + N_{n+1}.
Therefore
V_{n+1}
= (1 − 2/(n+1))^2 V_n + 2(1 − 2/(n+1)) δ_n (ε_n + N_{n+1}) + (ε_n + N_{n+1})^2.
Using |1 − 2/(n+1)| ≤ 1 and 2|δ_n ε_n| ≤ (1/(n+1)) V_n + (n+1) ε_n^2, then taking conditional expectations and E[N_{n+1} | 𝔽_n]=0 gives
E[ V_{n+1} | 𝔽_n ]
≤ (1 − 2/(n+1))^2 V_n + (1/(n+1)) V_n + (n+1) ε_n^2 + ε_n^2 + E[ N_{n+1}^2 | 𝔽_n ].
Since (1 − 2/(n+1))^2 + 1/(n+1) ≤ 1 − 1/(n+1), we obtain
E[ V_{n+1} | 𝔽_n ] ≤ (1 − 1/(n+1)) V_n + ρ_n,                          (3.11)
where ρ_n := (n+1) ε_n^2 + ε_n^2 + E[ N_{n+1}^2 | 𝔽_n ].

By (3.9) and (3.10), ∑_n ρ_n < ∞ almost surely. The Robbins–Siegmund almost-supermartingale theorem then implies:
- V_n converges almost surely to a finite limit V_∞ ≥ 0, and
- ∑_{n} (1/(n+1)) V_n < ∞ almost surely.

If V_∞ > 0, the series ∑ (1/(n+1)) V_n would diverge, a contradiction. Hence V_∞=0 and
Y_n → 3/2 almost surely.                                                     (3.12)

3.4. Identification of the exponent and the constant; conclusion for G_n

From Y_n = K_n^3/n^2 → 3/2 we get, almost surely,
K_n ∼ (3/2)^{1/3} n^{2/3}.                                                  (3.13)
Using (3.1),
G_n = K_n^2 + K_n + 2n + 2 = K_n^2 (1 + o(1)),
hence
G_n / n^{4/3} = (K_n^2/n^{4/3}) + o(1) → ((3/2)^{1/3})^2 = (3/2)^{2/3} almost surely.  (3.14)

This proves the statement with
α = 4/3 and c = (3/2)^{2/3}.

4. Gaps  
Gaps: None.

5. Self-evaluation
- Confidence score (0–100): 88
- Known or suspected issues:
  - The Freedman applications are standard; I was careful to use a deterministic bound v=2^m for the quadratic variation on blocks and to state the one-step implication “H_m ⇒ K_{2^{m+1}} ≥ L_{m+1}” independently of K_{2^m} (it depends only on sup_{I_m} K). This removes the sparse-subsequence issue flagged earlier.
  - For the upper bound, I deliberately switched to a dyadic Markov–Borel–Cantelli argument using E[K_n^3] ≤ C n^2; this avoids conditional keep-up chains and is sufficient (β_+ can be any number in (2/3,1)).
  - In the Robbins–Siegmund step, all summability checks are pathwise and rest only on the coarse bounds from Stage A.
- Coverage:
  - Complete: reduction to K_n; Stage A (both lower and upper coarse bounds); Stage B (SA/Robbins–Siegmund for Y_n); identification of α and c; final limit for G_n.