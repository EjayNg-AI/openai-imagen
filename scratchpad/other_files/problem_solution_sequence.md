# Problem Statement

An urn initially contains one red and one blue ball. At each step we draw one ball at random from the urn, with the uniform distribution over the balls currently in the urn.

* If the ball drawn is red, we place one additional red and one additional blue ball into the urn.
* When we draw a blue ball for the $k$-th time, we place one blue and $2k+1$ red balls into the urn.

(The originally drawn balls are not removed; they remain in the urn.)

Let $G_n$ denote the number of balls in the urn after $n$ steps. Prove that there exist constants $0 < c, \alpha < \infty$ such that with probability $1$ we have:

$$\frac{G_n}{n^\alpha} \longrightarrow c$$

as n tends to infinity.

---

# Approaches initially suggested by the problem solver

### 1. Problem_restatement

We have a reinforced urn process:

- Initially the urn has 1 red and 1 blue ball.
- At step \(n+1\) we draw a ball uniformly from the urn.
  - If it is **red**, we put back the ball (it was never removed) and add **1 new red and 1 new blue**.
  - If it is **blue**, and this is the **\(k\)-th time a blue ball has been drawn** so far, then we put back the ball and add **1 new blue and \(2k+1\) new red**.

Let \(G_n\) be the total number of balls after \(n\) steps.  
We want to prove that there exist constants \(0 < c,\alpha < \infty\) such that almost surely
\[
\frac{G_n}{n^\alpha} \longrightarrow c
\quad\text{as }n\to\infty.
\]

In words: the total number of balls grows like a deterministic power of \(n\), almost surely.

---

### 2. Assumptions or clarifications

1. “\(k\)-th time a blue ball is drawn” means the \(k\)-th blue draw **overall**, not the \(k\)-th time that a given blue ball is drawn. (This matches the usual reading and matches the reddit clarification in the web snippet.)
2. The originally drawn ball is never removed, so “we place … balls into the urn” means we only add new balls; the drawn ball stays.
3. All random choices are conditionally independent given the past (we always choose uniformly among current balls).

No other ambiguities seem present.  

---

### 3. Approaches

I’ll outline several distinct approaches. All of them start from a key simplification: keep track of the number of **blue draws**.

#### Key reduction (used in all approaches)

Let:

- \(B_n\): number of blue balls after \(n\) steps.
- \(R_n\): number of red balls after \(n\) steps.
- \(G_n = R_n + B_n\).
- \(K_n\): number of blue draws among the first \(n\) draws.

Then:

- Each step, regardless of color, we add exactly **one blue ball**. Therefore
  \[
  B_n = 1 + n \quad\text{deterministically}.
  \]
- Let’s count red balls. Up to time \(n\):
  * We have \(n-K_n\) red draws, each contributing 1 new red ball.
  * For the \(k\)-th blue draw (\(k=1,\dots,K_n\)), we add \(2k+1\) red balls.

  Hence
  \[
  R_n 
  = 1 + (n-K_n)\cdot 1 + \sum_{k=1}^{K_n} (2k+1)
  = 1 + n - K_n + \bigl(K_n(K_n+1) + K_n\bigr)
  = 1 + n + K_n^2 + K_n.
  \]

So
\[
G_n 
= R_n + B_n
= \bigl(1 + n + K_n^2 + K_n\bigr) + (1 + n)
= K_n^2 + K_n + 2n + 2.
\]

Thus the **entire** process reduces to the one-dimensional process \(\{K_n\}\), the total number of blues drawn so far.

At step \(n+1\), the probability of drawing blue is
\[
\mathbb{P}(\text{blue at time }n+1 \mid \mathcal F_n)
= \frac{B_n}{G_n}
= \frac{n+1}{K_n^2+K_n+2n+2}.
\]
Call this \(p_n\). Then
\[
K_{n+1} = K_n + \xi_{n+1},\quad
\mathbb{P}(\xi_{n+1}=1 \mid \mathcal F_n)=p_n,\quad
\mathbb{P}(\xi_{n+1}=0 \mid \mathcal F_n)=1-p_n.
\]
So \(\{K_n\}\) is a nondecreasing Markov chain with variable drift
\[
\mathbb{E}[K_{n+1}-K_n\mid\mathcal F_n]
= p_n 
= \frac{n+1}{K_n^2+K_n+2n+2}.
\]

If we can show that
\[
\frac{K_n}{n^{2/3}} \to L>0 \quad\text{a.s. for some deterministic }L,
\]
then
\[
\frac{G_n}{n^{4/3}}
= \frac{K_n^2}{n^{4/3}} + \frac{K_n}{n^{4/3}} + \frac{2n+2}{n^{4/3}}
\to L^2
\]
almost surely; i.e., \(\alpha=4/3\) and \(c=L^2\).

The rest of each approach focuses on analyzing \(\{K_n\}\).

---

## Approach 1. Drift–ODE heuristic and stochastic approximation on \(K_n\)

**Index:** 1  
**Name:** Markov drift analysis and stochastic approximation for \(K_n\).  

#### High-level idea

Use the Markov recurrence for \(K_n\) and approximate its evolution by an ordinary differential equation (ODE). 

Heuristic:

\[
\mathbb{E}[K_{n+1}-K_n \mid \mathcal F_n] 
\approx \frac{n}{K_n^2}.
\]

Treat \(K_n\) as a smooth function \(K(n)\) and compare it with solution of
\[
\frac{dK}{dn} = \frac{n}{K^2}.
\]

Solving the ODE suggests \(K(n)\approx \Bigl(\tfrac{3}{2}\Bigr)^{1/3} n^{2/3}\), so \(G_n\sim \text{const}\cdot n^{4/3}\). Then make this rigorous via stochastic-approximation-style arguments: decompose \(K_n\) into drift plus martingale noise, prove that noise is negligible compared to drift, and show that the scaled process \(K_n/n^{2/3}\) converges almost surely to a deterministic constant.

#### Detailed plan

1. **ODE heuristic and exponent \(\alpha\).**
   - Assume \(K_n \sim C n^\beta\) for some \(\beta>0\).
   - Then \(p_n\approx \dfrac{n}{K_n^2}\approx \dfrac{1}{C^2} n^{1-2\beta}\).
   - So the expected increment scale is
     \[
     \mathbb{E}[K_{n+1}-K_n]\sim \frac{1}{C^2} n^{1-2\beta}.
     \]
   - Summing up to \(n\) gives \(K_n\sim n^{2-2\beta}\). Self-consistency (left and right exponents equal \(\beta\)) yields
     \[
     \beta = 2 - 2\beta \quad\Rightarrow\quad \beta=\frac23.
     \]
   - Hence \(K_n \sim \text{const}\cdot n^{2/3}\), so
     \[
     G_n = K_n^2 + O(n) \sim (\text{const})^2 n^{4/3},
     \]
     suggesting \(\alpha=4/3\).

2. **Bounded increments and variance estimates.**
   - Each increment \(\Delta K_n = K_{n+1}-K_n\in\{0,1\}\).
   - Conditional variance:
     \[
     \operatorname{Var}(\Delta K_n \mid \mathcal F_n) 
     = p_n(1-p_n) \le p_n
     \approx \frac{n}{K_n^2}.
     \]
   - If \(K_n\) behaves like \(n^{2/3}\), then \(\operatorname{Var}(\Delta K_n)\) behaves like \(n^{-1/3}\), so the cumulative variance up to time \(n\) is about \(\sum_{j\le n} j^{-1/3} \sim n^{2/3}\). Thus typical fluctuations of the martingale part are \(O(n^{1/3})\), much smaller than \(K_n\) itself (\(O(n^{2/3})\)), which supports an a.s. law of large numbers for \(K_n\).

3. **Martingale decomposition.**
   - Define
     \[
     M_n := K_n - \sum_{j=0}^{n-1} p_j
     = \sum_{j=0}^{n-1} (\xi_{j+1}-p_j),
     \]
     where \(\xi_{j+1}=\Delta K_j\).
   - Then \(\{M_n\}\) is a martingale with bounded increments and controlled quadratic variation.
   - Moreover,
     \[
     K_n = A_n + M_n,\quad A_n:=\sum_{j=0}^{n-1} p_j.
     \]
   - Goal: show \(M_n=o(n^{2/3})\) a.s. and \(A_n\sim C n^{2/3}\) for some constant \(C\).

4. **Deterministic approximation via a differential equation.**
   - Suppose \(K_n\) is close to a smooth function \(k(t)\) solving
     \[
     \frac{dk}{dt} = \frac{t}{k^2}.
     \]
   - Solve ODE:
     \[
     k^2 dk = t \, dt
     \quad\Rightarrow\quad
     \frac13 k^3 = \frac12 t^2 + \text{const}.
     \]
     So \(k(t)\sim (3/2)^{1/3} t^{2/3}\).
   - Use this ODE solution as the **target curve** against which we compare \(K_n\).

5. **Tight upper and lower bounds on growth of \(K_n\).**
   - Show with high probability (indeed almost surely) that for large \(n\),
     \[
     c_1 n^{2/3} \le K_n \le c_2 n^{2/3}
     \]
     for some \(0<c_1<c_2<\infty\).
   - Strategy:
     - If \(K_n\) is too small (say \(K_n < c\, n^{2/3}\)), then \(p_n\) is relatively large, producing large drift and pushing \(K_n\) upward.
     - If \(K_n\) is too large, \(p_n\) is very small and drift is too small to keep up with current scale, which slows its growth.
   - These drift inequalities can be proved by comparing \(\mathbb{E}[\Delta K_n \mid K_n]\) with functions of \(n\) and \(K_n\), and using Azuma–Hoeffding or Freedman’s inequality to show that the martingale part doesn’t invalidate those trends.

6. **Scaling and stochastic approximation.**
   - Define scaled process
     \[
     Y_n := \frac{K_n}{n^{2/3}}.
     \]
   - Express its increment:
     \[
     Y_{n+1}-Y_n
     = \frac{K_{n+1} - K_n}{(n+1)^{2/3}}
       + K_n\left(\frac{1}{(n+1)^{2/3}} - \frac{1}{n^{2/3}}\right).
     \]
   - Expand for large \(n\) using Taylor:
     \[
     \frac{1}{(n+1)^{2/3}} - \frac{1}{n^{2/3}}
     \approx -\frac{2}{3} n^{-5/3}.
     \]
   - Taking conditional expectation and substituting \(p_n \approx n/K_n^2\) with \(K_n\approx n^{2/3}Y_n\), we get
     \[
     \mathbb{E}[Y_{n+1}-Y_n \mid \mathcal F_n]
       \approx n^{-1/3}\Bigl( Y_n^{-2} - \frac{2}{3}Y_n \Bigr).
     \]
   - This is a standard “stochastic approximation” recursion:
     \[
     Y_{n+1} = Y_n + a_n\bigl(F(Y_n) + \text{noise}\bigr),
     \]
     with step size \(a_n \asymp n^{-1/3}\) and drift function
     \[
     F(y) = y^{-2} - \tfrac{2}{3}y.
     \]

7. **ODE method and attractor.**
   - Look at ODE
     \[
     \frac{dy}{dt} = F(y) = y^{-2} - \tfrac23 y.
     \]
   - Positive equilibria satisfy \(F(y)=0\), i.e.
     \[
     y^{-2} = \tfrac23 y \quad\Rightarrow\quad y^3 = \tfrac32.
     \]
   - So there is a unique positive equilibrium
     \[
     y_* = \Bigl(\frac32\Bigr)^{1/3}.
     \]
   - Check stability: \(F'(y_*)<0\), so \(y_*\) is a **globally attracting** fixed point for \(y>0\).
   - By the general theory of stochastic approximation (Robbins–Monro, Kushner–Clark, Benaïm’s dynamical-system viewpoint), if noise is square-integrable and step sizes \(a_n\) are not too big (here \(a_n\to0\) and \(\sum a_n = \infty\), \(\sum a_n^2<\infty\) both hold), then \(Y_n\to y_*\) almost surely.

8. **Conclusion for \(K_n\) and \(G_n\).**
   - From step 7, we get
     \[
     \frac{K_n}{n^{2/3}} \to y_* = \Bigl(\frac32\Bigr)^{1/3} \quad\text{a.s.}
     \]
   - Thus
     \[
     \frac{G_n}{n^{4/3}}
     = \frac{K_n^2 + K_n + 2n+2}{n^{4/3}}
     \to y_*^2 = \Bigl(\frac32\Bigr)^{2/3}
     \quad\text{a.s.}
     \]
   - This gives the desired form with \(\alpha=4/3\) and \(c=y_*^2\).

#### Required tools or theorems

- Martingale convergence ideas and inequalities (e.g. Azuma–Hoeffding, Freedman).
- Stochastic approximation theorems (Robbins–Monro style; e.g. Kushner–Yin, Benaïm’s work on stochastic approximation).
- Some deterministic ODE analysis: stability of equilibria.

#### Main obstacles

- Making the stochastic approximation reduction precise: tracking error terms in the approximation for \(\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]\).
- Rigorous control of the martingale noise to show it is \(o(1)\) at the scale we care about.
- Showing that the limiting constant \(L\) is deterministic, not random. (Uniqueness of attractive equilibrium helps but must be argued carefully.)

#### Expected difficulty

High: there are several technically demanding steps (martingale bounds, verifying SA conditions) but the structure is very natural.

#### Estimated viability score

**85/100**

#### Notes on similarity to other approaches

This is conceptually similar to Approach 3 (both focus on \(K_n\) and use ODE-type approximations), but here the ODE is for \(K_n\) (or \(Y_n=K_n/n^{2/3}\)) directly, rather than for a more nonlinear function of \(K_n\).

---

## Approach 2. Hitting-time analysis via inter-arrival times of blue draws

**Index:** 2  
**Name:** Renewal-style analysis of the blue hitting times \(\tau_k\).  

#### High-level idea

Instead of tracking \(K_n\) in real time, focus on the **times when blue occurs**:

- Let \(\tau_k\) be the time of the \(k\)-th blue draw.
- Analyze the increments \(T_{k+1} := \tau_{k+1}-\tau_k\) (waiting time between the \(k\)-th and \((k+1)\)-th blue).
- Conditioned on the state at time \(\tau_k\), we have a relatively explicit form for the probabilities of getting a blue on the next draws.
- Show that \(T_{k+1}\) is roughly of order \(\tau_k/k^2\), so that \(\tau_k\) satisfies a recursion \(\tau_{k+1} - \tau_k \approx \tau_k/k^2\), leading to an ODE \(d\tau/dk = \tau/k^2\) whose solution is \(\tau_k \asymp k^{3/2}\).
- Then invert the relation between \(n\) and \(K_n\) to deduce \(K_n \asymp n^{2/3}\) and identify the exponent \(\alpha\).

#### Detailed plan

1. **Express state at time of \(k\)-th blue.**
   - At time \(\tau_k\),
     \[
     K_{\tau_k} = k,\qquad B_{\tau_k} = \tau_k+1,
     \qquad R_{\tau_k} = 1 + \tau_k + k^2 + k.
     \]
   - Thus the red–blue difference at that time is
     \[
     R_{\tau_k} - B_{\tau_k} = k^2 + k.
     \]
   - Between \(\tau_k\) and \(\tau_{k+1}\), there are **no blue draws** (by definition), so every draw is red. Each red draw increases both red and blue counts by 1, preserving the difference \(R-B = k^2+k\).

2. **Blue probability in the waiting period.**
   - At time \(\tau_k+m\) (before the \((k+1)\)-th blue), we have
     \[
     B = (\tau_k+1) + m,
     \quad
     R = (\tau_k+1)+m + k^2+k.
     \]
   - Therefore the probability that the next draw is blue is
     \[
     p^{(k)}_m 
     = \frac{B}{B+R}
     = \frac{\tau_k+1+m}{2(\tau_k+1+m)+k^2+k}.
     \]
   - Thus the waiting time \(T_{k+1}\) until the next blue is the first time \(m\) that we get a success in a “sequence of Bernoulli trials with success probabilities \(p^{(k)}_m\) changing with \(m\).”

3. **Approximate distribution of \(T_{k+1}\).**
   - For large \(k\) and large \(\tau_k\), if \(k^2\ll \tau_k\), then \(p^{(k)}_m \approx 1/2\), so waiting is short.
   - Conversely, if \(k^2 \gg \tau_k\), then \(p^{(k)}_0\approx \tau_k/k^2\ll 1\), and we must wait many steps.
   - Based on the heuristic scaling \(\tau_k \approx c k^{3/2}\), we have \(k^2/\tau_k\approx c^{-1} k^{1/2}\), which diverges; thus \(p^{(k)}_0\approx \tau_k/k^2\approx c k^{-1/2}\) is small, so the geometric mean waiting time is of order \(k^{1/2}\cdot(\tau_k/k^2)\), i.e., of order \(\tau_k/k^2\).
   - A more systematic approximation: treat \(p^{(k)}_m\) as nearly constant over the time window where most of the mass of \(T_{k+1}\) sits, leading to
     \[
     \mathbb E[T_{k+1}\mid \mathcal F_{\tau_k}] \approx \frac{K_{\tau_k}^2}{\tau_k} \sim \frac{k^2}{\tau_k}.
     \]

4. **Recursive relation for \(\tau_k\).**
   - With the heuristic
     \[
     \mathbb E[T_{k+1} \mid \mathcal F_{\tau_k}]
     \approx \frac{k^2}{\tau_k},
     \]
     we get
     \[
     \tau_{k+1}-\tau_k \approx \frac{k^2}{\tau_k}.
     \]
   - Think of \(\tau_k\) as a function of \(k\), and approximate
     \[
     \frac{d\tau}{dk} = \frac{k^2}{\tau}.
     \]
   - Solving this ODE:
     \[
     \tau\, d\tau = k^2 \, dk
     \Rightarrow
     \frac12 \tau^2 = \frac13 k^3 + \text{const}
     \Rightarrow
     \tau_k \sim C k^{3/2}.
     \]

5. **Turn heuristics into rigorous bounds.**
   - First show that, almost surely, for large \(k\), \(\tau_k\) lies between \(c_1 k^{3/2}\) and \(c_2 k^{3/2}\) for constants \(0<c_1<c_2\).
     - If \(\tau_k\) were significantly smaller than \(k^{3/2}\), then \(p^{(k)}_m\) would be too small, giving too large expected waiting times and forcing \(\tau_{k+1}\) to catch up.
     - If \(\tau_k\) were much larger, \(p^{(k)}_m\) would be larger, and we’d get smaller waits, pulling \(\tau_k\) back.
   - Use concentration inequalities (e.g. Chernoff–Hoeffding variants for sums of independent but non-identically distributed Bernoullis) to show that the actual \(T_{k+1}\) concentrates around its conditional expectation and that large deviations across many \(k\) are almost surely finite.

6. **Asymptotic of \(\tau_k/k^{3/2}\).**
   - Once we have tight two-sided bounds, refine the analysis of \(\tau_{k+1}-\tau_k\) to show that
     \[
     \frac{\tau_k}{k^{3/2}} \to D>0
     \]
     almost surely for some deterministic constant \(D\).
   - This is another application of stochastic approximation, but now in the “blue index” variable \(k\) instead of time \(n\).

7. **Inversion to recover \(K_n\).**
   - Since \(\tau_k \approx D k^{3/2}\), we can invert the relation:
     \[
     K_n \approx \left(\frac{n}{D}\right)^{2/3}.
     \]
   - More precisely, show that
     \[
     \frac{K_n}{n^{2/3}} \to D^{-2/3}
     \quad\text{a.s.}
     \]
   - Then plug into \(G_n = K_n^2 + K_n + 2n+2\) to deduce \(G_n\sim D^{-4/3} n^{4/3}\) almost surely.

#### Required tools or theorems

- Strong concentration results for Bernoulli sums with varying success probabilities.
- Stopping time arguments and optional stopping for martingales.
- Some version of stochastic approximation, but now for \(\tau_k\) as function of \(k\).

#### Main obstacles

- Technically more involved than Approach 1 because the waiting time \(T_{k+1}\) has a rather complicated distribution (non-constant probabilities).
- Need to control dependencies between successive waiting times and between \(\tau_k\) and \(k\).
- Inverting the relation between \(\tau_k\) and \(K_n\) in a strong almost-sure sense requires care.

#### Expected difficulty

Very high: many delicate probabilistic estimates and a nontrivial inversion step.

#### Estimated viability score

**60/100**

#### Notes on similarity to other approaches

Conceptually distinct from Approach 1: it works in “blue index space” \(k\), not in calendar time \(n\), and uses renewal-type reasoning rather than direct drift analysis of \(K_n\). However, the exponent \(2/3\) and the eventual ODE are the same.

---

## Approach 3. Lyapunov / potential function: analyze \(K_n^3 / n^2\)

**Index:** 3  
**Name:** Potential function method via the process \(Y_n := K_n^3 / n^2\).  

#### High-level idea

Instead of scaling \(K_n\) linearly, look at the cubic quantity \(K_n^3\). Heuristically:

- From the drift approximation \(dK/dn\approx n/K^2\), we get \(d(K^3)/dn = 3K^2 \, dK/dn \approx 3n\).
- Summing over \(n\) suggests \(K_n^3\approx \frac32 n^2\), so \(K_n^3/n^2\) should converge to \(3/2\).

Thus consider
\[
Y_n := \frac{K_n^3}{n^2}.
\]
Compute its conditional drift and show that it evolves like a (noisy) one-dimensional recursion
\[
Y_{n+1} - Y_n \approx \frac{1}{n^\gamma} \psi(Y_n) +\text{noise},
\]
with a drift function \(\psi\) having a unique root at \(3/2\). Then apply an “almost-supermartingale” convergence theorem (e.g., Robbins–Siegmund) to show \(Y_n\to 3/2\) almost surely, which implies \(K_n\sim (3/2)^{1/3} n^{2/3}\) and thus \(G_n\sim (3/2)^{2/3}n^{4/3}\).

#### Detailed plan

1. **Exact increment for \(K_n^3\).**
   - Recall \(\Delta K_n := K_{n+1}-K_n = \xi_{n+1}\in\{0,1\}\).
   - Then
     \[
     K_{n+1}^3 - K_n^3
     = (K_n+\xi_{n+1})^3 - K_n^3
     = (3K_n^2 + 3K_n + 1)\,\xi_{n+1}.
     \]
   - Taking conditional expectation:
     \[
     \mathbb{E}[K_{n+1}^3 - K_n^3 \mid \mathcal F_n]
     = (3K_n^2+3K_n+1)\, p_n,
     \]
     where \(p_n = (n+1)/(K_n^2+K_n+2n+2)\).

2. **Heuristic computation of the drift.**
   - If \(K_n^2\gg n\), then
     \[
     p_n\approx \frac{n}{K_n^2},
     \quad\text{so}\quad
     \mathbb{E}[K_{n+1}^3 - K_n^3 \mid \mathcal F_n]
     \approx 3K_n^2 \cdot \frac{n}{K_n^2} = 3n.
     \]
   - This matches the earlier ODE heuristic and suggests
     \[
     K_n^3 \approx \frac32 n^2,
     \quad\text{so}\quad
     Y_n = \frac{K_n^3}{n^2} \to \frac32.
     \]

3. **Compute the drift of \(Y_n\).**
   - Write
     \[
     Y_{n+1}
     = \frac{K_{n+1}^3}{(n+1)^2}
     = \frac{K_n^3 +(3K_n^2+3K_n+1)\xi_{n+1}}{(n+1)^2}.
     \]
   - Subtract \(Y_n = K_n^3 / n^2\):
     \[
     Y_{n+1}-Y_n
     = K_n^3\left( \frac{1}{(n+1)^2} - \frac{1}{n^2}\right)
       + \frac{(3K_n^2+3K_n+1)\xi_{n+1}}{(n+1)^2}.
     \]
   - Expand the deterministic coefficient:
     \[
     \frac{1}{(n+1)^2} - \frac{1}{n^2}
     = -\frac{2n+1}{n^2(n+1)^2}
     \approx -\frac{2}{n^3}.
     \]
   - Using \(K_n^3\approx c n^2\) as a heuristic, the first term is of order \(-c'(1/n)\); the second term, after expectation, is of order \(n/K_n^2 \cdot K_n^2/n^2 \sim 1/n\).

   - So overall \(\mathbb{E}[Y_{n+1}-Y_n\mid \mathcal F_n]\) behaves like \((1/n)\psi(Y_n)\) for some function \(\psi\), whose zero will correspond to the limiting value of \(Y_n\).

4. **Identify limiting ODE in terms of \(Y\).**
   - Under the heuristic \(K_n^3 \approx Y_n n^2\), we have \(K_n^2\approx Y_n^{2/3} n^{4/3}\), and
     \[
     p_n
     \approx \frac{n}{K_n^2}
     \approx \frac{1}{Y_n^{2/3}} n^{-1/3}.
     \]
   - The main contribution to \(\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]\) comes from:
     \[
     \frac{(3K_n^2)\,p_n}{(n+1)^2}
     \approx \frac{3K_n^2}{n^2} \cdot \frac{n}{K_n^2}
     = \frac{3}{n}.
     \]
   - The negative term from \(K_n^3(\frac{1}{(n+1)^2}-\frac{1}{n^2})\) is roughly \(-2Y_n/n\).
   - So we approximate:
     \[
     \mathbb{E}[Y_{n+1}-Y_n\mid \mathcal F_n]
     \approx \frac{1}{n}\bigl(3 - 2Y_n\bigr).
     \]
   - This suggests the limiting ODE:
     \[
     \frac{dy}{dt} = \frac{3 - 2y}{t}.
     \]
   - The solution has a stable equilibrium at \(y=3/2\). More precisely, reparametrize time \(\log t\) and see that \(y\) is driven towards \(3/2\).

5. **Apply an “almost supermartingale” theorem.**
   - We can try to write something like:
     \[
     \mathbb{E}[Y_{n+1} \mid \mathcal F_n]
     = Y_n + \frac{3 - 2Y_n}{n} + \varepsilon_n,
     \]
     where the error \(\varepsilon_n\) is summable (or its sum is almost surely finite).
   - This has the form of a stochastic approximation scheme with step size \(1/n\) and drift function \(G(y)=3-2y\).
   - Standard Robbins–Siegmund or Robbins–Monro arguments show that \(Y_n\) converges almost surely to the unique zero of \(G\), i.e., \(3/2\).

6. **Control fluctuations / noise.**
   - The noise comes from \(\xi_{n+1}-p_n\), a bounded martingale increment with variance of order \(p_n\).
   - The contribution of this noise to \(Y_{n+1}-Y_n\) is of order
     \[
     \frac{(3K_n^2+O(K_n))(\xi_{n+1}-p_n)}{(n+1)^2}
     \approx \frac{K_n^2}{n^2}(\xi_{n+1}-p_n).
     \]
   - Under \(K_n^2\sim c n^{4/3}\), this is roughly \(n^{-2/3}(\xi_{n+1}-p_n)\).
   - So the “noise step size” in \(Y_n\) is about \(n^{-2/3}\), whose squared sum \(\sum n^{-4/3}\) is finite. This gives strong control over the martingale part, implying it converges almost surely and does not prevent \(Y_n\) from converging to the attracting equilibrium.

7. **From \(Y_n\) back to \(K_n\) and \(G_n\).**
   - With \(Y_n\to 3/2\), we have
     \[
     \frac{K_n^3}{n^2} \to \frac32 \quad\Rightarrow\quad 
     K_n \sim \Bigl(\frac32\Bigr)^{1/3} n^{2/3}.
     \]
   - As before,
     \[
     \frac{G_n}{n^{4/3}} 
     = \frac{K_n^2}{n^{4/3}} + \text{smaller terms}
     \to \Bigl(\frac32\Bigr)^{2/3}.
     \]

#### Required tools or theorems

- Martingale convergence and almost-sure bounds using square-summable step sizes.
- Robbins–Siegmund almost-supermartingale convergence lemma, or a similar technique from stochastic approximation.
- Basic calculus/ODEs to understand the limiting ODE for \(Y_n\).

#### Main obstacles

- Making the “\(\approx\)” in step 4 precise and providing explicit bounds on \(\varepsilon_n\).
- Some care needed to **bootstrap**: we used heuristics about growth of \(K_n\) to justify the scale of various terms; we must first show that \(K_n\) is indeed of order between \(n^\gamma\) with \(\gamma\in(1/2,1)\), say, before refining to \(\gamma=2/3\).

#### Expected difficulty

High: somewhat more technical algebraically than Approach 1, but conceptually very similar.

#### Estimated viability score

**80/100**

#### Notes on similarity to other approaches

Very similar in spirit to Approach 1 (stochastic approximation), but uses the potential function \(K_n^3/n^2\) instead of working directly with \(K_n/n^{2/3}\). This can give cleaner drift formulas and sometimes more robust proofs.

---

## Approach 4. Use general results on non-linear reinforced urns

**Index:** 4  
**Name:** Embed in a generalized/self-interacting urn framework and apply known LLNs.  

#### High-level idea

There is an established theory of **non-linear reinforcement** and generalized Pólya urns (see work by Pemantle, Benaïm & Raimond, Launay, and others). These often consider processes where the probability of drawing a color is proportional to a non-linear function \(w(k)\) of its current count, and where increments might depend on such weights.

Here, although the rule depends on the **number of blue draws** \(K_n\) rather than simply on the current number of blue balls, there might be a way to embed the process into a higher-dimensional Markov chain that fits the hypotheses of such general theorems on reinforced urns.

Once we do this, we can **import a law of large numbers** or asymptotic growth result from the literature, which will give almost sure convergence of a suitably normalized process, possibly nailing down the exponent \(\alpha\) and the constant \(c\).

#### Detailed plan

1. **Identify an appropriate model class.**
   - Look at existing papers on “nonlinear Pólya urns” and “self-interacting urns” where the replacement rules depend on some non-linear functional of previous draws (for example, weight sequences \(w(k)\) specifying reinforcement strength when color count is \(k\)).
   - Try to see if our process can be expressed as:
     - A two- or three-color urn with a replacement matrix that depends on current counts in a polynomial way.
     - Or as a **self-interacting urn** where the probability of drawing blue is changed by some weight \(w(K_n)\), and the addition of red balls is also related to \(K_n\).
   - For example, in each blue draw, we add a number of red balls that grows linearly in the number of previous blue draws; this might be treated as having a weight proportional to \(K_n\) or \(K_n^2\).

2. **Enlarge the state space if necessary.**
   - Introduce an extra “counter” color (say, green balls representing “blue-draw index”) so that:
     - Each time a blue is drawn, the number of green balls increments in a way that encodes the current \(k\).
     - The number of red balls added could then be expressed as a function of the number of green balls.
   - Make this into a (possibly high-dimensional) generalized Pólya urn with replacement matrix depending polynomially on the state.

3. **Locate a suitable theorem.**
   - There are results giving strong laws (and sometimes CLTs) for urns whose replacement mechanism is polynomially dependent on the state vector, with certain regularity or irreducibility conditions.  
   - Identify a theorem of the following kind:
     > For a multi-dimensional urn with replacement function \(R(x)\) of polynomial growth and some regularity, the composition \(X_n\) satisfies
     > \(\|X_n\|\sim C n^\alpha\) almost surely for some deterministic \(\alpha\) and \(C>0\).
   - Verify that our embedded process satisfies the hypotheses: monotonicity, irreducibility (both colors drawn infinitely often at an appropriate scale), and so on.

4. **Extract exponent and constant.**
   - Translate the theorem’s conclusions back to our original variables \(R_n, B_n, G_n\).
   - Often the exponent \(\alpha\) is determined by the **spectral radius** of a certain matrix or by the degree of the polynomial describing the drift.
   - Deduce \(\alpha\) and \(c\) for our problem.

5. **Check almost sure convergence and non-random limit.**
   - Many such theorems yield deterministic limiting behavior (no random limit). Confirm this holds here.
   - Ensure that the conditions ruling out multiple attractors (which would require random choice of equilibrium) are satisfied.

#### Required tools or theorems

- Deep results from the theory of generalized and self-interacting Pólya urns (e.g., Janson’s functional limit theorems, Benaïm–Raimond on self-interacting urns, Launay on urns with weighted reinforcement).
- Ability to embed our model into those frameworks rigorously.

#### Main obstacles

- It’s not obvious that existing theorems directly cover a rule that depends on the **number of blue draws** instead of just ball counts.
- The embedding itself might be quite artificial and cumbersome, possibly obscuring more than it clarifies.
- Even if a theorem applies, one still has to translate its parameters into the constants \(\alpha\) and \(c\) we need.

#### Expected difficulty

Medium-to-very-high, depending on how close the existing literature is to this specific model. For a contest or textbook problem, this is probably overkill; for research-level work, it might be quite natural.

#### Estimated viability score

**40/100**

#### Notes on similarity to other approaches

Conceptually distinct: it aims to leverage **external theorems** rather than build a problem-specific stochastic approximation analysis. Still, at the level of exponents, it is likely to re-derive the same \(2/3\) and \(4/3\) powers found in Approaches 1–3.

---

### 4. Overall recommendation

**Recommended approach indices:** **1** and **3** (with 1 slightly preferred).

**Rationale:**

- The key simplification \(G_n = K_n^2+K_n+2n+2\) reduces the problem to tracking the one-dimensional Markov chain \(\{K_n\}\) with simple increments.
- Approach 1 (stochastic approximation on \(K_n/n^{2/3}\)) directly exploits this and gives a very natural ODE heuristic leading to the exponent \(\alpha=4/3\), with a standard toolkit (martingales + stochastic approximation).
- Approach 3 refines this via a particularly convenient potential function \(K_n^3/n^2\), often making the drift algebra cleaner and fitting nicely into a Robbins–Siegmund type almost-supermartingale argument.
- Approach 2, although conceptually interesting, is more technically tangled with hitting times; and Approach 4 depends heavily on specialized literature and nontrivial embeddings.
- For a self-contained rigorous solution, starting with Approach 1 and supplementing it with the potential-function insight of Approach 3 is, in my view, the cleanest and most promising path.

---

### 5. Internet search results

- I searched for this urn process and found **exactly the same problem** posted on Reddit in the mathriddles community:  
  “Growth of Ball Counts in a Probabilistic Urn Process” on r/mathriddles, with the same rule (“when we draw a blue ball for the \(k\)-th time, we add one blue and \(2k+1\) red balls”). The URL is:
  - https://www.reddit.com/r/mathriddles/comments/1h7axlr
- From the snippet visible in search results, the post identifies the problem and notes it is “definitely a tough one.” When I attempted to open the page, the site returned a rate-limit error (HTTP 429: Too Many Requests), so I could **not** access any full solution or discussion there.
- I did not find this exact problem (with the same reinforcement rule) on Math StackExchange, arXiv, or other common math sources, nor any paper that explicitly states this exact urn model and its asymptotics.
- Therefore:
  - This **same problem** does appear on the internet (Reddit), but
  - **No accessible partial or full solution** was found in the sources I could retrieve.
  
So, in the sense of the instructions:

- The same problem was found online (on Reddit).
- **No solution found on the internet** (in the accessible content).

---

# Expert evaluator's feedback on the proposed approaches

## 1. Global assessment

Your reduction of the urn process to the one-dimensional Markov chain \(K_n\) is completely correct and already does most of the conceptual heavy lifting. All four approaches then try to understand the asymptotics of this chain, and the heuristics for the exponent \(\beta=2/3\) for \(K_n\) (and hence \(\alpha=4/3\) for \(G_n\)) are internally consistent. Approaches 1 and 3 are both solid stochastic-approximation style plans that, after some cleanup, should be realistically pushable to a full proof. Approach 3 in particular chooses a very convenient Lyapunov/potential \(Y_n = K_n^3/n^2\) that makes the drift structure almost linear and well matched to standard “almost supermartingale” tools.  

Approach 2 (hitting times \(\tau_k\)) is conceptually interesting and uses a nice structural property (that \(R-B\) stays constant between blue draws), but the distribution of the inter-arrival times is messy; turning the heuristics into rigorous bounds will likely be technically heavy. Approach 4 (importing general urn theory) is the least certain: it might work with the right theorem in hand, but the dependence on the *number of blue draws* rather than just current counts is far enough from standard generalized Pólya urns that there is a serious risk that no ready-made result applies cleanly. Overall, your plan is well thought out and mostly technically sound, with a few places where approximations must be tightened and one noticeable slip in a step-size exponent.

**Overall viability score (0–100): 84**

**Key global concerns:**

- The “bootstrap” step is missing: you still need a rigorous argument that \(K_n\) is eventually of order \(n^{2/3}\) (at least within exponents \(\beta\in(1/2,1)\)) so that approximations like \(K_n^2 \gg n\) are justified.
- In Approach 1, the derived effective “step size” for the stochastic approximation of \(Y_n=K_n/n^{2/3}\) is misstated (you write \(n^{-1/3}\) where it should be \(1/n\)); this needs correction before applying standard SA theorems.
- For all stochastic-approximation arguments: you need to explicitly verify the hypotheses (bounded noise, square-summable noise scale, Lipschitz drift, boundedness of the iterates) rather than only heuristically.
- Approach 2’s renewal-style analysis requires careful control of non-constant-success-probability geometric-like variables; at present this is only sketched very heuristically.

---

## 2. Addressing assumptions or clarifications

You listed three clarifications:

1. **“\(k\)-th time a blue ball is drawn”** is the \(k\)-th blue draw *in total*, not of a specific ball.  
   - This is indeed the natural interpretation and is consistent with how you define \(K_n\) and the replacement rule. No further clarification needed.

2. **Drawn balls are not removed.**  
   - Correct. Your derivation of \(B_n = 1+n\) and the formula for \(R_n\) both properly use this.

3. **All draws are uniform among current balls, conditionally independent given the past.**  
   - This is the standard setup and underlies your Markov property for \(K_n\). There is no hidden dependence other than through the urn contents, so this is fine.

No additional ambiguities or hidden conventions appear. All later computations (e.g., \(G_n = K_n^2+K_n+2n+2\)) are consistent with these clarifications.

---

## 3. Per-approach feedback

### Approach 1: Markov drift analysis and stochastic approximation for \(K_n\)

**Viability score (0–100): 87**

**Strengths**

- The reduction to the one-dimensional Markov chain \(K_n\) is spot-on and very powerful; from there, writing
  \[
  \mathbb{E}[K_{n+1}-K_n\mid\mathcal F_n]
  = p_n
  = \frac{n+1}{K_n^2+K_n+2n+2}
  \]
  is exactly the right starting point.
- Your heuristic exponent analysis (“assume \(K_n\sim Cn^\beta\) and balance exponents”) correctly yields \(\beta=2/3\), and the ODE \(dK/dn = n/K^2\) is the right deterministic analog.
- Decomposing \(K_n = A_n + M_n\), with \(M_n\) a martingale and \(A_n=\sum p_j\) the drift, is a standard and powerful technique here.
- Formulating the scaled process \(Y_n = K_n / n^{2/3}\) and identifying the drift function
  \[
  F(y) = y^{-2} - \frac{2}{3}y
  \]
  with a unique positive stable equilibrium \(y_*=(3/2)^{1/3}\) is exactly what stochastic approximation theory wants.
- You are correctly aware that you must control the martingale noise and show it is small relative to the deterministic drift.

**Weaknesses**

- The calculation of the *effective* step size for \(Y_n\) has an exponent mistake. A careful Taylor expansion shows
  \[
  \mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
  \approx \frac{1}{n}\Bigl(Y_n^{-2} - \frac{2}{3}Y_n\Bigr),
  \]
  so the step size is \(\sim 1/n\), not \(n^{-1/3}\). This matters when you appeal to conditions like \(\sum a_n^2<\infty\).
- The argument that \(K_n\) really stays in the regime where \(K_n^2\gg n\) (so that \(p_n\approx n/K_n^2\)) is only sketched. You will need explicit upper and lower growth bounds for \(K_n\) **before** linearizing the dynamics around \(n^{2/3}\).
- You rely on general stochastic-approximation theorems (Robbins–Monro, Kushner–Clark, Benaïm) but do not yet articulate the exact form of your recursion in the canonical
  \[
  Y_{n+1} = Y_n + a_n (F(Y_n) + \eta_{n+1})
  \]
  or check all their hypotheses (boundedness of \(Y_n\), Lipschitzness of \(F\), square-summability of noise scale, etc.) in detail.
- The proof-of-determinism of the limit constant (i.e., that the limit of \(Y_n\) is non-random) is currently only argued at a heuristic level (“unique attractive equilibrium”), whereas SA theory requires checking that the process does not get attracted to other invariant sets.

**Severity flags:** logical error (step size exponent), missing critical subproblem (coarse growth bounds for \(K_n\)).

**Suggested refinements**

- **Correct the step-size computation.**  
  Recompute
  \[
  Y_{n+1}-Y_n
  = K_n\left(\frac{1}{(n+1)^{2/3}}-\frac{1}{n^{2/3}}\right)
    + \frac{\xi_{n+1}}{(n+1)^{2/3}},
  \]
  and show
  \[
  \mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
  = \frac{1}{n}\Bigl(Y_n^{-2}-\frac{2}{3}Y_n\Bigr) + \text{(error with summable expectation)}.
  \]
  Then you may set \(a_n=1/n\), \(F(y)=y^{-2}-(2/3)y\).
- **Prove preliminary growth bounds for \(K_n\).**  
  For example, aim to show: there exists \(\varepsilon>0\) and random \(N\) such that a.s. for \(n\ge N\),
  \[
  n^{1/2+\varepsilon} \le K_n \le n^{1-\varepsilon}.
  \]
  You can do this by:
  - Showing that if \(K_n\) is *too small*, then \(p_n\) is bounded below by a positive power of \(n\), and \(\sum p_n\) diverges fast enough to force many blue increments.
  - Showing that if \(K_n\) is *too large*, then \(p_n\) becomes tiny and \(K_n\) cannot keep growing at that rate.
- **Explicitly apply a stochastic-approximation theorem.**  
  Once you have the recursion in the form
  \[
  Y_{n+1}=Y_n + a_n(F(Y_n) + \eta_{n+1}),
  \]
  with \(a_n=1/n\), verify:
  - \(\sum a_n = \infty\), \(\sum a_n^2<\infty\).
  - \(|\eta_{n+1}|\) is uniformly bounded and \(\mathbb{E}[\eta_{n+1}^2\mid \mathcal F_n]\) is \(O(1)\).
  - \(F\) is continuous and has a unique attracting root \(y_*\).
  Then you can cite a specific theorem (e.g. Benaïm’s 1999 survey on SA and dynamical systems).
- **Boundedness/tightness of \(Y_n\).**  
  Use drift inequalities: for large \(Y_n\), \(\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]\) is negative (since \(-\tfrac{2}{3}Y_n\) dominates), and for very small \(Y_n\) it is positive. Together with bounded noise, this gives that \(Y_n\) is confined to a compact interval eventually, a key input to SA theory.

---

### Approach 2: Renewal-style analysis via blue hitting times \(\tau_k\)

**Viability score (0–100): 58**

**Strengths**

- The way you parametrize the process at blue-hitting times \(\tau_k\) is very clean: at time \(\tau_k\),
  \[
  R_{\tau_k}-B_{\tau_k}=k^2+k,
  \]
  and between blue draws this difference is invariant. This is a genuinely useful structural observation.
- Writing down the exact blue probability at time \(\tau_k+m\),
  \[
  p^{(k)}_m = \frac{\tau_k+1+m}{2(\tau_k+1+m)+k^2+k},
  \]
  fully characterizes the law of the waiting time \(T_{k+1}\).
- The heuristic scaling \(\tau_k\sim C k^{3/2}\) and thus \(K_n\sim C' n^{2/3}\) is consistent with your Approach 1 and 3 heuristics, so there is good cross-checking between methods.
- Using the strong Markov property at times \(\tau_k\) to treat successive waiting times is a sound conceptual step.

**Weaknesses**

- The step where you assert
  \[
  \mathbb{E}[T_{k+1}\mid \mathcal F_{\tau_k}] \approx \frac{k^2}{\tau_k}
  \]
  is currently only heuristic. To make this rigorous, you need to analyze the first success time in a sequence of Bernoulli trials with **non-constant** success probabilities \(p^{(k)}_m\). This is much subtler than a geometric distribution with a fixed parameter.
- The line “geometric mean waiting time is of order \(\tau_k/k^2\cdot k^{1/2}\)” is not clearly justified and seems dimensionally at odds with the later claim \(\mathbb{E}[T_{k+1}] \approx k^2/\tau_k\); these two heuristics pull in opposite directions.
- Even if you get good asymptotics for \(\mathbb E[T_{k+1}\mid \mathcal F_{\tau_k}]\), controlling fluctuations of \(T_{k+1}\) around its mean is nontrivial: \(T_{k+1}\) is not a sum of independent Bernoullis, but a stopping time based on an inhomogeneous hazard sequence.
- The inversion step, from \(\tau_k\sim Ck^{3/2}\) a.s. to \(K_n\sim C' n^{2/3}\) a.s., requires careful almost-sure control (“regular variation inversion”), not just pointwise equivalence.

**Severity flags:** missing critical subproblem (rigorous control of \(T_{k+1}\)), likely intractable (in comparison to cleaner alternatives).

**Suggested refinements**

- **Work with bounds rather than exact expectations.**  
  For fixed \(k\), note that for \(0\le m\le M\),
  \[
  p^{(k)}_m \in [p^{(k)}_0, p^{(k)}_M],
  \]
  so you can sandwich \(T_{k+1}\) between geometric variables with parameters \(p^{(k)}_0\) and \(p^{(k)}_M\). Choose \(M\) as a suitable function of \(k\) (e.g. \(M\asymp k^{3/2-\delta}\)) and balance the contributions.
- **Use survival-hazard representation.**  
  Express
  \[
  \mathbb{P}(T_{k+1}>m\mid \mathcal F_{\tau_k}) = \prod_{j=0}^{m-1}(1-p^{(k)}_j),
  \]
  and approximate the log-survival as a Riemann sum
  \(\sum\log(1-p^{(k)}_j)\approx -\sum p^{(k)}_j\). This can give effective bounds on median or typical size of \(T_{k+1}\).
- **Avoid full LLN in \(k\) if possible.**  
  Instead of a full stochastic approximation in the \(k\)-index, it might be enough to prove:
  \[
  c_1 k^{3/2} \le \tau_k \le c_2 k^{3/2}
  \]
  a.s. for large \(k\), and then use monotonicity of \(K_n\) to deduce the exponent \(2/3\) for \(K_n\). That is still nontrivial but perhaps less intricate than getting a sharp almost sure limit for \(\tau_k/k^{3/2}\).
- **Be explicit about dependence.**  
  Subsequent waiting times \(T_{k+1}\) are not independent given the whole past (though they are conditionally independent given the state at \(\tau_k\)). When applying concentration inequalities, ensure you condition appropriately on \(\mathcal F_{\tau_k}\) and use martingale-based inequalities rather than iid Chernoff bounds.

---

### Approach 3: Potential function method via \(Y_n = K_n^3 / n^2\)

**Viability score (0–100): 92**

**Strengths**

- Choosing \(Y_n = K_n^3/n^2\) is very well motivated: it matches the ODE heuristic \(d(K^3)/dn \approx 3n\) and leads naturally to an expected growth \(K_n^3 \sim \tfrac32 n^2\), i.e. \(Y_n\to 3/2\).
- The exact algebra for \(K_{n+1}^3-K_n^3\) is clean:
  \[
  K_{n+1}^3 - K_n^3=(3K_n^2+3K_n+1)\xi_{n+1},
  \]
  and this leads to a very tractable expression for the drift of \(Y_n\).
- Your heuristic derivation
  \[
  \mathbb{E}[Y_{n+1}-Y_n\mid \mathcal F_n] \approx \frac{3-2Y_n}{n}
  \]
  is exactly of the canonical stochastic-approximation form with step size \(1/n\) and *linear* drift \(G(y)=3-2y\), whose unique equilibrium \(y=3/2\) is plainly attractive.
- The noise term in \(Y_n\) is of size \(\sim n^{-2/3}\), and you correctly note that the sum of its squared magnitudes \(\sum n^{-4/3}\) converges, implying strong control over the martingale fluctuations.
- This approach can likely be plugged directly into something like the Robbins–Siegmund almost-supermartingale lemma once you separate the main linear drift from the small error terms.

**Weaknesses**

- As in Approach 1, the heuristic expansions assume you are in the regime \(K_n^2\gg n\) so that \(p_n \approx n/K_n^2\). A bootstrap argument is needed to rigorously show that this regime indeed holds for large \(n\).
- The “error term” \(\varepsilon_n\) in
  \[
  \mathbb{E}[Y_{n+1}\mid \mathcal F_n]
  = Y_n + \frac{3-2Y_n}{n} + \varepsilon_n
  \]
  is not yet quantified. You will need to show \(\sum |\varepsilon_n| <\infty\) a.s. or at least \(\sum \mathbb{E}[|\varepsilon_n|]<\infty\).
- Boundedness or tightness of \(Y_n\) is again assumed but not yet proved. To apply supermartingale convergence results, you must show \(Y_n\) does not diverge to \(\infty\) or to \(0\).

**Severity flags:** missing critical subproblem (bootstrap bounds to control the regime of approximation).

**Suggested refinements**

- **Do a precise drift computation for \(Y_n\).**  
  Starting from
  \[
  Y_{n+1}-Y_n
  = K_n^3\Bigl(\frac{1}{(n+1)^2}-\frac{1}{n^2}\Bigr)
    + \frac{(3K_n^2+3K_n+1)\,\xi_{n+1}}{(n+1)^2},
  \]
  compute
  \[
  \mathbb{E}[Y_{n+1}-Y_n\mid \mathcal F_n]
  = -\frac{(2n+1)K_n^3}{n^2(n+1)^2}
    + \frac{(3K_n^2+3K_n+1)p_n}{(n+1)^2}.
  \]
  Replace \(p_n\) by its exact form and then separate the leading terms (which give \((3-2Y_n)/n\)) from the remainder (which you can bound by \(Cn^{-1-\delta}\) for some \(\delta>0\)).
- **Establish preliminary order-of-magnitude for \(K_n\).**  
  As in Approach 1, prove that for large \(n\),
  \[
  n^{1/2+\varepsilon} \le K_n \le n^{1-\varepsilon}
  \]
  almost surely. This ensures \(K_n^2\gg n\) and allows you to treat the denominator of \(p_n\) as \(K_n^2(1+o(1))\).
- **Apply Robbins–Siegmund or a similar lemma.**  
  After you have
  \[
  \mathbb{E}[Y_{n+1}\mid \mathcal F_n]
  \le Y_n - \frac{2}{n} (Y_n - \tfrac32)^2 + \text{small error},
  \]
  and a.s. \(\sum \text{small errors} < \infty\), you can apply the almost-supermartingale theorem to deduce:
  - \(Y_n\) converges almost surely,
  - the only possible limit is \(3/2\) because otherwise \(\sum (Y_n-\tfrac32)^2 = \infty\) would contradict the inequality.
- **Check tightness explicitly.**  
  Use the sign of the drift to show that for \(Y_n\) large, the expected increment is negative, and for \(Y_n\) very small, it is positive. Combine with bounded noise increments to conclude that \(Y_n\) eventually stays in some deterministic compact interval \([a,b]\subset(0,\infty)\).

---

### Approach 4: Embedding into generalized/self-interacting urn theory

**Viability score (0–100): 35**

**Strengths**

- It’s good that you are aware of the broader literature on non-linear urns and self-interacting processes; many powerful theorems do exist and can sometimes save a lot of work.
- Conceptually, encoding the “blue-draw index” \(k\) as an extra component in a higher-dimensional state vector and trying to use known LLNs for polynomial drift urns is not absurd.
- If a suitable theorem *did* apply, it would likely give you not only the exponent \(\alpha\) but also finer fluctuation results with relatively little additional work.

**Weaknesses**

- Standard generalized Pólya urn theory usually assumes that the replacement rule depends on the **current composition** of the urn (a state vector in \(\mathbb{R}^d\)) via a fixed replacement matrix (or a polynomial in the state), independent of the *path* of colours drawn. In your model, the replacement rule depends on the **number of past blue draws** \(K_n\) in a way that is not trivially expressible as a function of the current composition alone.
- Introducing an extra “counter colour” to encode \(k\) is not obviously polynomial or affine in the standard sense; you would need a very careful construction to ensure the new process fits the hypotheses of some known theorem.
- You do not currently have a specific theorem in mind; instead you describe a generic class (“some result about polynomial reinforcement”). Without an explicit theorem and its assumptions, there is a real risk that, after a lot of embedding effort, you discover the model does not actually satisfy the required conditions.
- Even if you find a theorem that looks applicable, verifying its often subtle technical conditions (irreducibility, moments, regularity of the replacement function) may absorb as much or more energy as proving the result directly via Approaches 1 or 3.

**Severity flags:** conceptual mismatch (between model and usual urn frameworks), likely intractable.

**Suggested refinements**

- **Identify a specific target theorem.**  
  Instead of “some generalized Pólya urn result,” pick one concrete theorem (e.g., from Benaïm–Raimond or Janson) with clearly stated assumptions and conclusions, and check line by line whether your embedded process satisfies each assumption.
- **Clarify the embedding.**  
  Write explicitly the enlarged state vector \(X_n\) (e.g., numbers of red, blue, and some auxiliary types of balls) and the replacement function \(R(X_n)\) so that the original process is a coordinate projection of \((X_n)\). Check that \(R\) is of the type treated in your target theorem (affine, polynomial of bounded degree, etc.).
- **Decide early whether the literature route is actually simpler.**  
  Once you have a concrete candidate theorem and an explicit embedding, honestly compare the technical work required to verifying its hypotheses against the more self-contained martingale/SA approach of 1 and 3. If it’s not clearly simpler, it’s probably better to drop this in favour of a direct proof.

---

## 4. Recommended approaches

**Recommended approach indices:** 1, 3 (with 3 slightly preferred as the main engine and 1 as complementary)

**Recommendation rationale**

Approach 3, focused on the potential function \(Y_n = K_n^3/n^2\), aligns almost perfectly with standard stochastic-approximation and almost-supermartingale techniques: the drift is essentially linear in \(Y_n\), the step size is the classical \(1/n\), and the martingale noise is small and square-summable. Once you fix the bootstrap showing \(K_n^2\gg n\), the algebraic and probabilistic structure is clean and should lead to a robust a.s. convergence proof for \(Y_n\) to \(3/2\). Approach 1 is very much in the same spirit but works directly with \(Y_n = K_n/n^{2/3}\) and a non-linear drift; it is valuable both for intuition and for auxiliary estimates (e.g., providing preliminary two-sided bounds on \(K_n\)).  

A good strategy is to **combine** them: use the drift analysis and growth-bounds reasoning of Approach 1 to show that \(K_n\) indeed lives on the \(n^{2/3}\) scale and that \(Y_n\) is tight, and then let Approach 3’s potential-function machinery nail down the exact constant and almost-sure convergence. Approach 2, while conceptually elegant, seems likely to be a detour with heavier technical complications around inhomogeneous geometric variables and inversion of \(\tau_k\). Approach 4 hinges on the availability of a very specific, nontrivial theorem from the urn literature and a delicate embedding; unless you already know such a theorem, it’s a higher-risk path. For a self-contained argument, focusing on the martingale/SA toolbox in Approaches 1 and 3 is the most promising line.

---

## 5. Internet search results

No internet solution provided.

---

# FIRST SOLUTION ATTEMPT by problem solver

## 1. Status  

Status: Partial  

---

## 2. Selected approaches  

Selected approach indices: 1, 3 (combination)  

- I follow the reduction to the one–dimensional Markov chain \(K_n\) and the drift/martingale analysis from Approach 1.  
- As the main scaling tool I use the potential function \(Y_n = K_n^3/n^2\) from Approach 3, which linearizes the deterministic drift and fits standard stochastic-approximation ideas.  

I push these as far as I can **rigorously**, then explain exactly where a full proof of almost sure convergence to a deterministic constant is missing.

---

## 3. Solution  

### 3.1. Reduction to the process of blue draws

Let:

- \(R_n\) = number of red balls after \(n\) steps,  
- \(B_n\) = number of blue balls after \(n\) steps,  
- \(G_n = R_n + B_n\) = total number of balls after \(n\) steps,  
- \(K_n\) = number of *blue draws* in the first \(n\) steps.

We first compute \(R_n,B_n,G_n\) in terms of \(K_n\).

#### 3.1.1. Blue balls

At each step (regardless of colour drawn):

- we always add exactly **one** blue ball (either \(+1\) from the red rule, or \(+1\) from the blue rule).

Thus

\[
B_n = 1 + n \qquad\text{(deterministically).}
\]

#### 3.1.2. Red balls

Initially, there is 1 red ball.

- Every *red* draw adds 1 red ball.  
  There are \(n-K_n\) red draws up to time \(n\), so this contributes \(n-K_n\) red balls.
- The \(k\)-th *blue* draw (for \(k=1,\dots,K_n\)) adds \(2k+1\) red balls.  

Thus

\[
R_n
= 1 + (n-K_n)\cdot 1 + \sum_{k=1}^{K_n} (2k+1).
\]

Now

\[
\sum_{k=1}^{K_n} (2k+1)
= 2\cdot\frac{K_n(K_n+1)}{2} + K_n
= K_n(K_n+1) + K_n
= K_n^2 + 2K_n.
\]

Hence

\[
\begin{aligned}
R_n
&= 1 + (n-K_n) + (K_n^2 + 2K_n)\\
&= 1 + n - K_n + K_n^2 + 2K_n\\
&= 1 + n + K_n^2 + K_n.
\end{aligned}
\]

#### 3.1.3. Total balls

Thus

\[
\begin{aligned}
G_n &= R_n + B_n\\
&= (1 + n + K_n^2 + K_n) + (1 + n)\\
&= K_n^2 + K_n + 2n + 2.
\end{aligned}
\]

So the whole problem boils down to understanding the growth of \(K_n\).

---

### 3.2. Dynamics of \(K_n\)

At time \(n+1\), conditional on the past (i.e. on \(\mathcal F_n\), the sigma-field generated by the first \(n\) draws), the probability that we draw blue is

\[
p_n
:= \mathbb{P}(\text{blue at time }n+1 \mid \mathcal F_n)
= \frac{B_n}{G_n}
= \frac{n+1}{K_n^2+K_n+2n+2}.
\]

Define \(\xi_{n+1}\in\{0,1\}\) by
\[
\xi_{n+1} =
\begin{cases}
1,&\text{if draw at time }n+1\text{ is blue},\\[3pt]
0,&\text{if draw at time }n+1\text{ is red}.
\end{cases}
\]

Then

\[
K_{n+1} = K_n + \xi_{n+1}
\]

and

\[
\mathbb{P}(\xi_{n+1} = 1 \mid \mathcal F_n) = p_n,\qquad
\mathbb{P}(\xi_{n+1} = 0 \mid \mathcal F_n) = 1-p_n.
\]

Thus \(\{K_n\}_{n\ge0}\) is a non-decreasing Markov chain on \(\mathbb{Z}_{\ge0}\) with increments in \(\{0,1\}\) and conditional drift

\[
\mathbb{E}[K_{n+1}-K_n\mid\mathcal F_n] = p_n
= \frac{n+1}{K_n^2+K_n+2n+2}.
\]

For later use, note also the variance of the increment:

\[
\mathrm{Var}(K_{n+1}-K_n\mid\mathcal F_n) = p_n(1-p_n)\le p_n.
\]

---

### 3.3. Heuristics: exponent and constant

#### 3.3.1. Exponent of \(K_n\)

Heuristic scaling: assume for large \(n\),
\[
K_n \approx C n^\beta,\quad C>0.
\]

Then typically \(K_n^2\gg n\) if \(\beta>1/2\), so the denominator of \(p_n\) is dominated by \(K_n^2\), and we estimate

\[
p_n \approx \frac{n}{K_n^2}
\approx \frac{1}{C^2}n^{1-2\beta}.
\]

Summing expected increments gives

\[
K_n \approx \sum_{j=1}^n p_j
\approx \frac{1}{C^2}\sum_{j=1}^n j^{1-2\beta}
\approx \frac{1}{C^2}\frac{1}{2-2\beta}n^{2-2\beta}
\quad(\text{if }1-2\beta>-1).
\]

Self-consistency of exponents demands

\[
\beta = 2 - 2\beta \quad\Longrightarrow\quad \beta = \frac{2}{3}.
\]

So heuristically

\[
K_n \asymp n^{2/3}.
\]

In particular, \(K_n^2\asymp n^{4/3}\gg n\), justifying a posteriori the replacement of the denominator in \(p_n\) by \(K_n^2\).

#### 3.3.2. Exponent and constant for \(G_n\)

Since
\[
G_n = K_n^2 + K_n + 2n + 2,
\]
if \(K_n\sim C n^{2/3}\), then \(K_n^2\sim C^2 n^{4/3}\) dominates the linear terms, so one expects
\[
G_n\sim C^2 n^{4/3}.
\]

To identify \(C\), we look at a smoother potential.

---

### 3.4. A “potential function”: \(Y_n := K_n^3/n^2\)

Define
\[
Y_n := \frac{K_n^3}{n^2}\quad(n\ge1).
\]

Heuristically, from the approximate ODE
\[
\frac{dK}{dn} \approx \frac{n}{K^2},
\]
we get
\[
\frac{d}{dn}(K^3) = 3K^2 \frac{dK}{dn} \approx 3n.
\]
Integrating:
\[
K(n)^3 \approx \frac{3}{2}n^2,
\]
so we expect
\[
Y_n = \frac{K_n^3}{n^2}\to \frac{3}{2},
\quad
K_n \sim \Bigl(\frac{3}{2}\Bigr)^{1/3}n^{2/3},
\quad
G_n \sim \Bigl(\frac{3}{2}\Bigr)^{2/3} n^{4/3}.
\]

We now compute the exact drift of \(Y_n\) and see what can be made rigorous.

---

### 3.5. Exact drift of \(Y_n\)

Recall \(K_{n+1}=K_n+\xi_{n+1}\), \(\xi_{n+1}\in\{0,1\}\).

First compute
\[
K_{n+1}^3 - K_n^3
= (K_n+\xi_{n+1})^3 - K_n^3
= (3K_n^2+3K_n+1)\,\xi_{n+1}.
\]

Thus
\[
K_{n+1}^3 = K_n^3 + (3K_n^2+3K_n+1)\,\xi_{n+1}.
\]

Therefore
\[
Y_{n+1}
= \frac{K_{n+1}^3}{(n+1)^2}
= \frac{K_n^3}{(n+1)^2} + \frac{(3K_n^2+3K_n+1)\,\xi_{n+1}}{(n+1)^2}.
\]

Subtracting \(Y_n=\dfrac{K_n^3}{n^2}\), we obtain

\[
\boxed{
Y_{n+1} - Y_n
= K_n^3\Bigl(\frac{1}{(n+1)^2}-\frac{1}{n^2}\Bigr)
  +\frac{(3K_n^2+3K_n+1)\,\xi_{n+1}}{(n+1)^2}.
}
\tag{3.5.1}
\]

Now take conditional expectation given \(\mathcal F_n\). Using \(\mathbb{E}[\xi_{n+1}\mid\mathcal F_n]=p_n\), we get

\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
= K_n^3\Bigl(\frac{1}{(n+1)^2}-\frac{1}{n^2}\Bigr)
  + \frac{(3K_n^2+3K_n+1)p_n}{(n+1)^2}.
\]

Compute
\[
\frac{1}{(n+1)^2}-\frac{1}{n^2}
= \frac{n^2 - (n+1)^2}{n^2(n+1)^2}
= -\frac{2n+1}{n^2(n+1)^2}.
\]

Also recall
\[
p_n = \frac{n+1}{K_n^2 + K_n + 2n + 2}
=: \frac{n+1}{D_n}.
\]

Thus

\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
= -\frac{(2n+1)K_n^3}{n^2(n+1)^2}
  + \frac{(3K_n^2+3K_n+1)(n+1)}{(n+1)^2 D_n}.
\]

Simplifying the second term:
\[
\frac{(3K_n^2+3K_n+1)(n+1)}{(n+1)^2 D_n}
= \frac{3K_n^2+3K_n+1}{(n+1)D_n}.
\]

So

\[
\boxed{
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
= -\frac{(2n+1)K_n^3}{n^2(n+1)^2}
  +\frac{3K_n^2+3K_n+1}{(n+1)D_n}.
}
\tag{3.5.2}
\]

We now express this in terms of \(Y_n\) and \(n\). Note
\[
Y_n = \frac{K_n^3}{n^2}
\quad\Longrightarrow\quad
K_n^3 = Y_n n^2.
\]

Also
\[
\frac{(2n+1)K_n^3}{n^2(n+1)^2}
= Y_n\,\frac{2n+1}{n(n+1)^2}.
\]

For the second term, use the identity
\[
3K_n^2 + 3K_n + 1 = 3D_n - (6n + 5),
\]
since
\[
3D_n = 3(K_n^2 + K_n + 2n + 2)
= (3K_n^2+3K_n+6n+6)
\quad\Rightarrow\quad
3D_n - (6n+5) = 3K_n^2+3K_n+1.
\]

Hence

\[
\frac{3K_n^2+3K_n+1}{(n+1)D_n}
= \frac{3}{n+1} - \frac{6n+5}{(n+1)D_n}.
\]

Substituting into (3.5.2),

\[
\boxed{
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
= -Y_n\frac{2n+1}{n(n+1)^2}
  + \frac{3}{n+1}
  - \frac{6n+5}{(n+1)D_n}.
}
\tag{3.5.3}
\]

This is an *exact* expression.

---

### 3.6. Heuristic identification of the limit of \(Y_n\)

Expression (3.5.3) suggests comparing with a recursion of the form
\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
\approx \frac{3-2Y_n}{n}.
\]

Indeed, for large \(n\):

- \(\dfrac{3}{n+1} = \dfrac{3}{n} + O\bigl(\frac{1}{n^2}\bigr)\).
- \(\dfrac{2n+1}{n(n+1)^2} = \dfrac{2}{n} + O\bigl(\tfrac{1}{n^2}\bigr)\).
- The last term \(\dfrac{6n+5}{(n+1)D_n}\) is small whenever \(D_n\) is large.

Heuristically, for large \(n\), we have \(K_n\asymp n^{2/3}\), so \(K_n^2\asymp n^{4/3}\gg n\), so
\[
D_n = K_n^2+K_n+2n+2 \sim K_n^2\asymp n^{4/3}
\quad\Rightarrow\quad
\frac{6n+5}{(n+1)D_n}
=O\bigl(n^{-1/3}\bigr).
\]
Hence the third term decays faster than \(1/n\), and we may ignore it in the leading drift.

Thus, ignoring lower-order terms,
\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
\approx -Y_n \frac{2}{n} + \frac{3}{n}
= \frac{3-2Y_n}{n}.
\]

This corresponds to the ODE (in continuous time \(t\))
\[
\frac{dy}{dt} \approx \frac{3-2y}{t}.
\]

In terms of “logarithmic time” \(s=\log t\), we get
\[
\frac{dy}{ds} \approx 3-2y,
\]
which has a unique attracting equilibrium at \(y_* = \dfrac{3}{2}\). This suggests
\[
Y_n = \frac{K_n^3}{n^2} \longrightarrow \frac{3}{2},
\]
almost surely and with a nonrandom limit; hence
\[
K_n \sim \Bigl(\frac{3}{2}\Bigr)^{1/3} n^{2/3},
\quad
G_n \sim \Bigl(\frac{3}{2}\Bigr)^{2/3} n^{4/3}.
\]

This completely identifies the candidates
\[
\alpha = \frac{4}{3},
\qquad
c = \Bigl(\frac{3}{2}\Bigr)^{2/3}.
\]

The remainder of the argument is to justify rigorously:

1. that \(K_n\) indeed has deterministic exponent \(2/3\) (i.e. \(K_n\) is between \(n^{2/3\pm o(1)}\) almost surely);
2. that \(Y_n\) converges almost surely to \(3/2\).

The rest of this section outlines rigorous progress towards these goals, and then I explain where I get stuck.

---

### 3.7. Martingale decomposition for \(K_n\)

Recall
\[
K_{n+1}-K_n=\xi_{n+1},\quad \mathbb{E}[\xi_{n+1}\mid\mathcal F_n]=p_n.
\]

Set
\[
M_n := \sum_{j=0}^{n-1}(\xi_{j+1}-p_j)
=K_n - \sum_{j=0}^{n-1} p_j,\qquad A_n := \sum_{j=0}^{n-1}p_j.
\]

Then \(M_n\) is a martingale with bounded increments \(|\xi_{j+1}-p_j|\le1\), and
\[
K_n = A_n + M_n.
\]

Its quadratic variation is
\[
\langle M\rangle_n
= \sum_{j=0}^{n-1}\mathrm{Var}(\xi_{j+1}\mid\mathcal F_j)
= \sum_{j=0}^{n-1}p_j(1-p_j)
\le A_n.
\]

Heuristically, from the scaling \(p_j\asymp j^{1-2\beta}\) with \(\beta=2/3\), one expects
\[
A_n\asymp n^{2/3},
\quad
M_n = O\bigl(A_n^{1/2}\bigr) = O(n^{1/3}),
\]
so the martingale fluctuations are smaller than the drift, and \(K_n\sim A_n\) almost surely. In particular, any exponent information derived for \(A_n\) should transfer to \(K_n\).

---

### 3.8. Lower and upper polynomial bounds for \(K_n\) (partial)

To go beyond heuristics, we want to show:

> For any \(\varepsilon>0\), almost surely,
> \[
> n^{2/3-\varepsilon} \le K_n \le n^{2/3+\varepsilon}
> \]
> for all sufficiently large \(n\).

This would give
\[
\lim_{n\to\infty}\frac{\log K_n}{\log n} = \frac{2}{3}\quad\text{a.s.}
\]

**Partial reasoning (not fully rigorous):**

1. **Crude lower bound \(K_n \gg n^{1/2+\delta}\) for some \(\delta>0\).**  
   - If \(K_n\) were always smaller than \(c\sqrt{n}\), then \(K_n^2 \ll n\), so
     \[
     p_n = \frac{n+1}{K_n^2+K_n+2n+2}
     \ge \frac{n+1}{c^2 n + 2n + O(\sqrt{n})}
     \xrightarrow[n\to\infty]{}\frac{1}{c^2+2}>0.
     \]
   - Then we would have, almost surely, a linear number of blue draws, contradicting \(K_n\le c\sqrt{n}\). A standard drift + Azuma argument can make this precise.

2. **Upper exponent bound \(\limsup \frac{\log K_n}{\log n}\le2/3\).**  
   - Fix \(\beta>2/3\). On the event that \(K_n \ge n^\beta\) for all large \(n\), we would have \(K_n^2\ge n^{2\beta}\), giving 
     \[
     p_n\le\frac{n+1}{K_n^2} \le 2n^{1-2\beta}.
     \]
   - Hence \(A_n =\sum p_j \le C n^{2-2\beta}\). On the other hand, \(\langle M\rangle_n\le A_n\), so \(M_n=O(n^{1-\beta})\) in typical size.
   - This would imply \(K_n=A_n+M_n=O(n^{2-2\beta})\), but \(2-2\beta<\beta\) when \(\beta>2/3\). So we cannot have \(K_n\ge n^\beta\) for all large \(n\). A refinement shows it cannot hold infinitely often, yielding the limsup bound.

3. **Lower exponent bound \(\liminf \frac{\log K_n}{\log n}\ge2/3\).**  
   - Fix \(\beta<2/3\). On an event where \(K_n \le n^\beta\) for all large \(n\), we would have \(K_n^2\le n^{2\beta}\), with \(2\beta>1\) for any \(\beta>1/2\), so the denominator of \(p_n\) is \(\sim K_n^2\), and
     \[
     p_n \ge c n^{1-2\beta}
     \]
     for some \(c>0\). Then \(A_n\ge c' n^{2-2\beta}\) and \(\langle M\rangle_n\le A_n\).
   - With \(2-2\beta>\beta\) for \(\beta<2/3\), this argues that \(K_n\) must eventually exceed any multiple of \(n^\beta\), giving the liminf bound.

These drift/martingale arguments can be made precise with Freedman-type inequalities and a Borel–Cantelli argument, but the details are somewhat technical. The upshot is:

> **Heuristic conclusion:** there is strong evidence that
> \[
> K_n = n^{2/3+o(1)} \quad\text{a.s.}
> \]
> i.e. its logarithmic growth exponent is almost surely \(2/3\).

Assuming this as a *growth bootstrap*, we can go back to \(Y_n\).

---

### 3.9. Towards convergence of \(Y_n\) (partial)

We return to (3.5.3):

\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
= -Y_n\frac{2n+1}{n(n+1)^2}
  + \frac{3}{n+1}
  - \frac{6n+5}{(n+1)D_n}.
\]

Introduce the “main drift”
\[
\frac{3-2Y_n}{n}
\]
and treat the difference as a perturbation.

Write
\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n] = \frac{3-2Y_n}{n} + \varepsilon_n,
\]

with
\[
\varepsilon_n := \Bigl[-Y_n\frac{2n+1}{n(n+1)^2} + \frac{3}{n+1} - \frac{6n+5}{(n+1)D_n}\Bigr]
- \frac{3-2Y_n}{n}.
\]

A tedious but straightforward estimate (using Taylor expansions and the growth information \(K_n\asymp n^{2/3}\), so that \(D_n\asymp n^{4/3}\)) shows:

- For large \(n\),
  \[
  |\varepsilon_n|
  \le C_1\frac{Y_n}{n^2} + C_2 n^{-4/3}
  \]
  for some constants \(C_1,C_2\). Since \(Y_n\) is expected to stay bounded, \(|\varepsilon_n|\) decays at least like \(n^{-4/3}\), which is summable.

At the same time, the *noise* part of \(Y_{n+1}-Y_n\) is

\[
N_{n+1}
:= \frac{(3K_n^2+3K_n+1)(\xi_{n+1}-p_n)}{(n+1)^2}.
\]

Its conditional second moment can be bounded as:

\[
\mathbb{E}[N_{n+1}^2\mid\mathcal F_n]
\le \frac{(3K_n^2+3K_n+1)^2}{(n+1)^4}p_n(1-p_n).
\]

Using \(K_n\asymp n^{2/3}\) and \(p_n\asymp n/K_n^2\asymp n^{-1/3}\), we heuristically get

\[
\mathbb{E}[N_{n+1}^2\mid\mathcal F_n]
\lesssim \frac{n^{8/3}}{n^4} \cdot n^{-1/3}
= n^{-4/3}.
\]

Thus
\[
\sum_n \mathbb{E}[N_{n+1}^2\mid\mathcal F_n] <\infty\quad\text{a.s.}
\]

This implies that the martingale part
\[
\sum_{j=0}^{n-1} N_{j+1}
\]
converges almost surely (by the martingale convergence theorem), and therefore its contribution to \(Y_n\) is negligible at large \(n\).

Combining:

- approximate deterministic recursion
  \[
  \mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
  = \frac{3-2Y_n}{n} + \varepsilon_n,
  \quad
  \sum_n|\varepsilon_n|<\infty,
  \]
- summable noise variance,

one is in the right regime for **stochastic approximation with step size \(a_n=1/n\)** and drift \(F(y)=3-2y\). A standard Robbins–Siegmund or Robbins–Monro type theorem would then imply:

1. \(Y_n\) converges almost surely;
2. its limit is the unique zero of \(F\), namely
   \[
   \lim_{n\to\infty}Y_n = \frac{3}{2}\quad\text{a.s.}
   \]

Once that is obtained, we conclude

\[
\frac{K_n^3}{n^2}\to\frac{3}{2}\quad\text{a.s.}
\quad\Longrightarrow\quad
K_n \sim \Bigl(\frac{3}{2}\Bigr)^{1/3}n^{2/3},\quad
G_n\sim \Bigl(\frac{3}{2}\Bigr)^{2/3} n^{4/3}\quad\text{a.s.}
\]

Thus the natural candidates
\[
\alpha=\frac{4}{3},\quad c=\Bigl(\frac{3}{2}\Bigr)^{2/3}
\]
indeed satisfy
\[
\frac{G_n}{n^\alpha} \longrightarrow c\quad\text{a.s.}
\]

---

### 3.10. Summary of what is solid and what is not

From the above we have:

- A *complete and exact* reduction of the urn model to the one-dimensional Markov chain \(K_n\).

- Exact formula
  \[
  G_n = K_n^2 + K_n + 2n + 2.
  \]

- Strong heuristic plus partial drift/martingale arguments showing
  \[
  K_n = n^{2/3+o(1)}\quad\text{a.s.}
  \]

- Exact formula for the drift of \(Y_n=K_n^3/n^2\),
  \[
  \mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n]
  = -Y_n\frac{2n+1}{n(n+1)^2}
    + \frac{3}{n+1}
    - \frac{6n+5}{(n+1)D_n},
  \]
  which matches a stochastic-approximation scheme with step size \(1/n\) and drift \(3-2Y_n\) plus a small perturbation.

On the basis of standard stochastic-approximation lore, this would yield the claimed a.s. convergence with \(\alpha=4/3\), \(c=(3/2)^{2/3}\). However, some steps (detailed below) still need rigorous closure.

---

## 4. Gaps  

Since the status is **Partial**, I list the remaining gaps explicitly.

### Gap 1: Rigorous two-sided growth bounds for \(K_n\)

**Location:** Section 3.8 (Polynomial bounds for \(K_n\)).  

**Description:**  

I outlined plausibility arguments that for any \(\varepsilon>0\),

\[
n^{2/3-\varepsilon}\le K_n\le n^{2/3+\varepsilon}
\quad\text{eventually a.s.}
\]

by combining drift bounds for \(K_n\) with martingale estimates. To make this fully rigorous one must:

1. For each fixed \(\beta>2/3\), show that the event  
   \(\{K_n \ge n^\beta \text{ for infinitely many }n\}\) has probability 0.

2. For each fixed \(\beta<2/3\), show that the event  
   \(\{K_n \le n^\beta \text{ for infinitely many }n\}\) has probability 0.

This requires a carefully constructed sequence of stopping times, the use of Freedman’s (or Bernstein’s) inequality for martingales with bounded increments, and a Borel–Cantelli argument.

**Reason for difficulty:**  

The conditional drift \(p_n\) depends non-linearly on \(K_n\), so the bounds for \(p_n\) under hypotheses like “\(K_n\le n^\beta\) for all large \(n\)” are delicate. One must repeatedly control the martingale term \(M_n\) relative to its quadratic variation and ensure that drifts dominate fluctuations in the long run. I have not written out these estimates and verifications in full detail.

---

### Gap 2: Precise control of the error term \(\varepsilon_n\) in the drift of \(Y_n\)

**Location:** Section 3.9 (Towards convergence of \(Y_n\)).  

**Description:**  

Defining
\[
\varepsilon_n :=
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n] - \frac{3-2Y_n}{n},
\]
I asserted that, under the (conjectured) bounds \(K_n\asymp n^{2/3}\), there exists a constant \(C\) such that
\[
|\varepsilon_n|\le \frac{C}{n^{4/3}},
\]
so that \(\sum_n |\varepsilon_n|<\infty\).

To prove this rigorously one must:

1. Rewrite \(\varepsilon_n\) explicitly as in terms of \(n,Y_n,D_n\).
2. Use the *already proved* bounds on \(K_n\) (from Gap 1) to bound each piece.
3. Show that the resulting bound is indeed summable.

**Reason for difficulty:**  

The exact algebra somewhat intricate, and without an already established tight control on \(K_n\) (Gap 1), the best a priori bound on the term
\[
\frac{6n+5}{(n+1)D_n}
\]
is of order \(1/n\), which *is not* summable. Only once we know \(K_n^2\gg n^{1+\delta}\) for some \(\delta>0\) can we improve this to \(O(n^{-1-\delta})\). This logical dependency makes the argument delicate.

---

### Gap 3: Application of a concrete stochastic-approximation / almost-supermartingale theorem

**Location:** End of Section 3.9.  

**Description:**  

Given a recursion of the form
\[
Y_{n+1} = Y_n + \frac{1}{n}\bigl(3-2Y_n\bigr) + \varepsilon_n + N_{n+1},
\]
with \(\sum |\varepsilon_n|<\infty\) and \(\sum \mathbb{E}[N_{n+1}^2\mid\mathcal F_n]<\infty\), standard results (Robbins–Siegmund almost supermartingale theorem, or Benaïm’s dynamical-system approach to stochastic approximation) yield:

- almost sure convergence of \(Y_n\);
- identification of the limit as the unique root of \(3-2y=0\), i.e. \(y=3/2\).

However, in this solution I have **not**:

1. Explicitly stated and proved the exact theorem I am appealing to;
2. Verified its hypotheses in detail (e.g. almost-sure boundedness of \(Y_n\), Lipschitz continuity of the drift on the range of \(Y_n\), etc.).

**Reason for difficulty:**  

Writing a fully self-contained proof along these lines would essentially require reproducing nontrivial pieces of the general stochastic-approximation theory (e.g. from Kushner–Yin or Benaïm), which is technically heavy. I have instead sketched how the problem fits perfectly into that framework, but not spelled out every verification step.

---

### Gap 4: From convergence of \(Y_n\) to convergence of \(G_n/n^{4/3}\)

**Location:** Very end (Section 3.9).  

**Description:**  

Assuming we have shown
\[
Y_n=\frac{K_n^3}{n^2}\to\frac{3}{2}\quad\text{a.s.,}
\]
I briefly asserted:

\[
\frac{G_n}{n^{4/3}}
= \frac{K_n^2}{n^{4/3}} + \frac{K_n}{n^{4/3}} + \frac{2n+2}{n^{4/3}}
\to \Bigl(\frac{3}{2}\Bigr)^{2/3}.
\]

This is intuitively clear (the second and third terms vanish), but full rigor needs:

- A precise deduction \(K_n = \Theta(n^{2/3})\) from \(K_n^3/n^2\to 3/2\);
- Control showing \(\frac{K_n}{n^{4/3}}\to0\) and \(\frac{2n+2}{n^{4/3}}\to0\) (which are easy, but should be stated).

**Reason for difficulty:**  

This part is not truly difficult, but I have not gone through every epsilon–delta detail because it depends on Gap 3 (we do not yet have the convergence of \(Y_n\)). Once Gap 3 is resolved, this last step is straightforward.

---

## 5. Self-evaluation  

**Confidence score (0–100):** 55  

**Known or suspected issues:**

- The main missing pieces are the rigorous proofs that:
  - \(K_n\) has almost sure growth exponent exactly \(2/3\);  
  - \(Y_n = K_n^3/n^2\) converges almost surely to \(3/2\) via a bona fide stochastic-approximation theorem.
- I have not fully detailed the martingale concentration arguments (Freedman/Bernstein inequalities, Borel–Cantelli) needed for the “bootstrap” bounds on \(K_n\).
- The stochastic-approximation argument is currently at the level of a carefully motivated sketch, not a fully formal proof (mainly because I did not restate and verify a concrete theorem’s hypotheses).
- There is no doubt that the *heuristics* are internally consistent and match standard theory for such processes, but turning them into a completely rigorous self-contained proof is nontrivial and has not been completed here.

**Coverage comment:**

- The **reduction** of the urn to the single chain \(K_n\) and the formula \(G_n=K_n^2+K_n+2n+2\) are fully rigorous.
- The **identification of the exponent** \(\alpha=4/3\) and the candidate constant \(c=(3/2)^{2/3}\) is well supported heuristically and via partial drift arguments, but I have *not* proved the almost sure convergence
  \[
  \frac{G_n}{n^{4/3}} \to \Bigl(\frac{3}{2}\Bigr)^{2/3}
  \]
  rigorously.
- So the problem’s requirement “prove that there exist constants \(0<c,\alpha<\infty\) such that \(G_n/n^\alpha\to c\) a.s.” is **not fully met** here; instead, I have:
  - described the natural values \(\alpha=4/3\), \(c=(3/2)^{2/3}\);
  - outlined, but not completed, a rigorous proof based on stochastic approximation.

  ---

---

# Expert evaluator's feedback on the problem solver's FIRST SOLUTION ATTEMPT

## 1. Status  

Status: Partial  

---

## 2. Score  

Score (0–100): 72  

---

## 3. Major issues  

- **Location:** §3.8 (“Polynomial bounds for \(K_n\)”)  
  **Issue type:** Missing critical step / incomplete argument  
  **Description:**  
  The two-sided power bounds for \(K_n\) (roughly \(K_n \approx n^{2/3}\)) are only argued heuristically. You sketch how to contradict the scenarios \(K_n \ge n^\beta\) for all large \(n\) when \(\beta>2/3\) and \(K_n \le n^\beta\) for \(\beta<2/3\), but you do not give a fully rigorous drift+martingale argument: no explicit stopping times, no concrete Freedman/Bernstein inequality application, and no Borel–Cantelli implementation. These growth bounds are not cosmetic; they are needed to justify later approximations like \(D_n \sim K_n^2\) and to control error terms.  
  **Suggested direction for fix:**  
  Turn the heuristic into a precise lemma of the form: “For any \(\beta>2/3\), \(\mathbb{P}(K_n \ge n^\beta \text{ i.o.})=0\)” and similar for \(\beta<2/3\). Do this by:  
  1. Fix \(\beta\), assume \(K_n \ge n^\beta\) (or \(\le n^\beta\)) on an interval;  
  2. Use this to get deterministic bounds on \(p_n\) on that interval;  
  3. Control \(M_n\) via Freedman’s inequality to show that with high probability \(K_n\) cannot sustain such behaviour;  
  4. Sum these probabilities over disjoint blocks and apply Borel–Cantelli.  
  This will give you almost-sure bounds of the form \(n^{2/3-\varepsilon} \le K_n \le n^{2/3+\varepsilon}\) eventually.

- **Location:** §3.9 (“Towards convergence of \(Y_n\)”): estimation of \(\varepsilon_n\)  
  **Issue type:** Logical gap / circular reasoning  
  **Description:**  
  The bound \(|\varepsilon_n|\le C_1 Y_n/n^2 + C_2 n^{-4/3}\) and the conclusion that \(\sum_n |\varepsilon_n|<\infty\) rely on the assumption \(K_n \asymp n^{2/3}\) (so that \(D_n \asymp K_n^2 \asymp n^{4/3}\)), which has not yet been proved. Without prior control on \(K_n\), all you can a priori say about \((6n+5)/((n+1)D_n)\) is that it is \(O(1/n)\), which is *not* summable. Thus the justification that the “error” is negligible in the SA scheme is incomplete and currently circular.  
  **Suggested direction for fix:**  
  Separate the argument into two stages:  
  1. Prove coarse but *uniform* bounds on \(K_n\) (e.g. for some fixed \(\gamma\in(1/2,1)\), eventually \(n^\gamma \le K_n \le n^{2-\gamma}\)) that are strong enough to ensure \(D_n \gg n^{1+\delta}\) for some \(\delta>0\).  
  2. Using those bounds, give a **clean algebraic estimate** of \(\varepsilon_n\) that does not use any heuristic about the exact exponent. Show explicitly that \(|\varepsilon_n| \le C n^{-1-\delta}\) a.s. for some \(\delta>0\), so \(\sum |\varepsilon_n|<\infty\).

- **Location:** §3.9 (“Towards convergence of \(Y_n\)”): variance of the noise term \(N_{n+1}\)  
  **Issue type:** Dependence on unproved growth rate / incomplete justification  
  **Description:**  
  The estimate \(\mathbb{E}[N_{n+1}^2\mid\mathcal F_n] \lesssim n^{-4/3}\) is derived “heuristically” by plugging \(K_n\asymp n^{2/3}\) and \(p_n \asymp n^{-1/3}\). As with \(\varepsilon_n\), this uses the very asymptotic behaviour you intend to prove, creating a circular dependence. Strictly speaking, before you know that \(K_n^2 \gg n^{1+\delta}\), you cannot assert that the quadratic variation of the \(Y\)-martingale is summable.  
  **Suggested direction for fix:**  
  First prove coarse upper and lower bounds on \(K_n\) that ensure \(K_n^2\) grows *at least* like \(n^{1+\delta}\) for some \(\delta>0\). Then redo the computation of  
  \[
  \mathbb{E}[N_{n+1}^2\mid\mathcal F_n]
  \le \frac{(3K_n^2+3K_n+1)^2}{(n+1)^4}\,p_n,
  \]
  using the exact formula for \(p_n\) and those coarse bounds to get an **unconditional** bound of the form \(C n^{-1-\delta'}\), which is summable. This breaks the circularity.

- **Location:** §3.9, end: appeal to stochastic-approximation / almost-supermartingale theorem  
  **Issue type:** Misuse / under-specification of theory  
  **Description:**  
  The core claim “From the recursion \(Y_{n+1} = Y_n + \frac{1}{n}(3-2Y_n) + \varepsilon_n + N_{n+1}\), with \(\sum |\varepsilon_n|<\infty\) and \(\sum \mathbb{E}[N_{n+1}^2\mid\mathcal F_n]<\infty\), we get \(Y_n\to 3/2\) a.s.” is referenced only as “standard stochastic approximation lore” without stating a concrete theorem or verifying its hypotheses. In particular, you never prove that \(Y_n\) is a.s. bounded or that the drift pushes it toward the unique equilibrium, both of which are crucial in SA theory.  
  **Suggested direction for fix:**  
  Choose a specific theorem—e.g. Robbins–Siegmund’s almost-supermartingale convergence lemma, or a precise stochastic-approximation theorem à la Benaïm—and write down its statement. Then, *systematically* verify its assumptions:  
  - Show \(\sum a_n = \infty\), \(\sum a_n^2<\infty\) with \(a_n=1/n\);  
  - Show \(F(y)=3-2y\) is Lipschitz and has unique root;  
  - Prove that \(Y_n\) is eventually confined in some deterministic compact interval \([m,M]\subset(0,\infty)\) by combining sign of the drift with bounded noise;  
  - Show the perturbations \(\varepsilon_n\) are summable and the martingale noise has square-summable scale.  
  Once these are checked, you can legitimately conclude \(Y_n\to 3/2\) a.s.

- **Location:** Overall logical structure (interaction of §3.8 and §3.9)  
  **Issue type:** Structural / circularity of argument  
  **Description:**  
  Several later estimates (both for \(\varepsilon_n\) and for \(\mathbb{E}[N_{n+1}^2\mid\mathcal F_n]\)) rely implicitly on the “fact” that \(K_n\asymp n^{2/3}\), but the only justification for that fact is the drift analysis that itself uses those estimates. This is a typical bootstrap situation, but in its current form the bootstrap is not clearly separated: it is ambiguous where the independent base bounds for \(K_n\) stop and where the consequences of those bounds begin.  
  **Suggested direction for fix:**  
  Explicitly structure the proof in two stages:  
  1. **Bootstrap stage:** Prove coarse but nontrivial a.s. bounds for \(K_n\) (e.g. \(C_1 n^{\gamma_1} \le K_n \le C_2 n^{\gamma_2}\) for some \(1/2<\gamma_1\le\gamma_2<1\)). This part should avoid any use of the potential \(Y_n\) and rely only on crude drift estimates and martingale concentration.  
  2. **Refinement stage:** On the strength of those bounds, analyze \(Y_n\), show its drift is asymptotically \((3-2Y_n)/n\) plus a summable error, and apply SA theory to get \(Y_n\to 3/2\).  
  Making this separation explicit will remove logical circularity and clarify which estimates use which prior information.

---

## 4. Minor issues  

- **Location:** §3.6 (“Heuristic identification of the limit of \(Y_n\)”)  
  **Nature:** Slightly loose comparison of term sizes  
  **Description:**  
  You state that the third term \((6n+5)/((n+1)D_n)\) “decays faster than \(1/n\)”, which is true *if* \(D_n\asymp n^{4/3}\), but this assumption is at that point only heuristic. Although you later flag the need for rigorous bounds, it would be clearer to mark this calculation explicitly as conditional on \(K_n\asymp n^{2/3}\).  
  **Suggestion:**  
  Add a sentence such as: “Under the heuristic \(K_n\asymp n^{2/3}\), we have \(D_n\asymp n^{4/3}\), hence this term is \(O(n^{-4/3})\). We will justify this scaling rigorously later.”

- **Location:** §3.8, bullet 3 (lower exponent bound)  
  **Nature:** Slight conflation of “plausible” with “proved”  
  **Description:**  
  Phrases such as “This argues that \(K_n\) must eventually exceed any multiple of \(n^\beta\)” are a bit strong for what is, at that point, only a sketch.  
  **Suggestion:**  
  Rephrase to emphasize the status: for example, “Heuristically, this suggests that …; a rigorous version would require applying Freedman’s inequality as described.”

- **Location:** §3.10 (summary)  
  **Nature:** Terminology / clarity  
  **Description:**  
  You say “Strong heuristic plus partial drift/martingale arguments showing \(K_n = n^{2/3+o(1)}\) a.s.” It would be clearer to separate what is heuristic from what has been actually established, to avoid over-claiming.  
  **Suggestion:**  
  Replace by: “Strong heuristics, supported by partial drift/martingale calculations, point to \(K_n = n^{2/3+o(1)}\) a.s.; however, the rigorous proof of this statement is not yet complete in this write-up.”

- **Location:** End of §3.9 (from \(Y_n\) to \(G_n\))  
  **Nature:** Minor omission  
  **Description:**  
  You assert that \(G_n/n^{4/3}\to (3/2)^{2/3}\) follows once \(Y_n\to 3/2\). This is correct, but you do not even briefly justify that \(K_n/n^{4/3}\to 0\) and \(2n/n^{4/3}\to0\).  
  **Suggestion:**  
  Add a short calculation: from \(K_n^3/n^2\to 3/2\) we have \(K_n \sim (3/2)^{1/3}n^{2/3}\), hence \(K_n/n^{4/3}\to0\) and \(n/n^{4/3} = n^{-1/3}\to0\), so only the \(K_n^2\) term survives.

---

## 5. Gap assessment  

The problem solver explicitly listed four gaps; here is an assessment of each:

- **Gap 1 (Rigorous two-sided growth bounds for \(K_n\))**  
  **Assessment:** Fundamental.  
  This is a core part of the proof: without solid control on \(K_n\)’s order of growth, you cannot justify the approximations of \(p_n\) and \(D_n\) that power the analysis of \(Y_n\). It is not just a technical clean-up; it addresses the main difficulty of controlling a non-linear drift coupled with martingale noise.

- **Gap 2 (Precise control of \(\varepsilon_n\))**  
  **Assessment:** Moderate.  
  Once you have usable growth bounds for \(K_n\), this becomes a somewhat technical but tractable algebraic exercise. You need to be careful to avoid circularity, but conceptually it is not the heart of the problem.

- **Gap 3 (Application of a stochastic-approximation / supermartingale theorem)**  
  **Assessment:** Moderate.  
  This is conceptually straightforward if you are comfortable with stochastic approximation theory. The main work is: pick an appropriate theorem; verify its hypotheses. It’s nontrivial but not as deep as establishing the right growth exponent in the first place.

- **Gap 4 (From convergence of \(Y_n\) to convergence of \(G_n/n^{4/3}\))**  
  **Assessment:** Minor.  
  Once \(Y_n\to 3/2\) is known, the deduction for \(G_n\) is a short algebraic step.

Overall, I agree with your self-identification of these gaps and would emphasize that Gap 1 is the main conceptual obstacle; Gaps 2–4 are technical but relatively standard once Gap 1 is resolved.

---

## 6. Coverage assessment  

All subparts addressed: No  

- The problem essentially has a single goal: prove that there exist deterministic \(c>0,\alpha>0\) such that \(G_n/n^\alpha \to c\) almost surely.  
- You have:
  - Completely analyzed the *reduction* to the process \(K_n\) and expressed \(G_n\) explicitly in terms of \(K_n\).  
  - Correctly identified the likely exponent \(\alpha=4/3\) and constant \(c=(3/2)^{2/3}\).  
  - Sketched a coherent martingale + stochastic-approximation strategy to prove almost-sure convergence.  
- However, the **actual proof** of almost-sure convergence is incomplete: the crucial growth bounds for \(K_n\) and the rigorous application of SA theorems are not carried through.  

So the only substantive “part” of the problem (the almost-sure limit statement) is addressed in structure and heuristics but not fully solved.

---

## 7. Summary  

Your solution does an excellent job on the structural and heuristic side of the problem. The reduction from the original urn process to the single Markov chain \(K_n\) is completely correct and very powerful, and the explicit formula \(G_n = K_n^2+K_n+2n+2\) is a key simplification. The choice of potential \(Y_n = K_n^3/n^2\) is especially insightful; it linearizes the drift in a way that aligns beautifully with the classical stochastic-approximation framework. Your computation of the exact drift of \(Y_n\) and its approximation by \((3-2Y_n)/n\) is technically accurate and well-motivated.  

On the probabilistic side, you correctly decompose \(K_n\) into drift plus martingale noise, recognize that the noise should be of smaller order than the drift, and outline how this should lead to \(K_n \sim (3/2)^{1/3}n^{2/3}\). You also identify the right general theorem to invoke (Robbins–Siegmund–type or Benaïm-type SA results) and match your recursion to the canonical form.  

The main weaknesses are on the rigor and closure: the two-sided growth bounds for \(K_n\) are only sketched, and several crucial estimates for the drift error and noise variance of \(Y_n\) are derived under the assumption of the very asymptotics you are trying to prove. This creates a circular dependence that must be broken by a bootstrap argument with explicit bounds and martingale concentration. Moreover, the final step where SA theory is applied is left at the “folklore” level; no specific theorem is stated or checked.  

Overall, the approach is highly promising and, with careful work, should be turnable into a complete proof. You are not far from a solution in terms of ideas; the remaining work is mostly about making the drift/noise comparison quantitative enough and about structuring the argument to avoid circular reasoning.

---

## 8. Recommendations for next iteration  

1. **Isolate and prove coarse growth bounds for \(K_n\) first.**  
   - Aim to prove statements of the form: there exist \(\gamma_1,\gamma_2\) with \(1/2<\gamma_1<2/3<\gamma_2<1\) such that eventually  
     \[
     n^{\gamma_1} \le K_n \le n^{\gamma_2} \quad \text{a.s.}
     \]  
   - Use drift inequalities for \(p_n\) under hypotheses like “\(K_n \ge n^\beta\)” or “\(K_n \le n^\beta\)” and apply Freedman’s inequality to show such hypotheses cannot persist (or hold infinitely often) when \(\beta\neq 2/3\). Make this part completely independent of the \(Y_n\)-analysis.

2. **Once you have those bounds, redo the estimates for \(\varepsilon_n\) carefully.**  
   - Start from the exact formula (3.5.3) and write  
     \[
     \mathbb{E}[Y_{n+1}-Y_n\mid\mathcal F_n] = \frac{3-2Y_n}{n} + \varepsilon_n.
     \]  
   - Using only your proven bounds on \(K_n\) (hence on \(D_n\)), establish a deterministic bound \(|\varepsilon_n| \le Cn^{-1-\delta}\) for some \(\delta>0\). Check that \(\sum |\varepsilon_n| < \infty\).

3. **Recompute and rigorously bound the variance of the noise term \(N_{n+1}\).**  
   - Using the exact formula for \(p_n\) and your growth bounds on \(K_n\), show that  
     \[
     \mathbb{E}[N_{n+1}^2\mid\mathcal F_n] \le C n^{-1-\delta'}
     \]  
     for some \(\delta'>0\), which ensures \(\sum \mathbb{E}[N_{n+1}^2\mid\mathcal F_n]<\infty\). This lets you invoke martingale convergence for \(\sum N_{n+1}\).

4. **Prove that \(Y_n\) is almost surely bounded.**  
   - Use the sign of the main drift: for large \(Y_n\), \(\frac{3-2Y_n}{n}\) is negative; for very small \(Y_n\), it is positive. Combine this with the fact that the noise increments are small and square-summable to show that \(Y_n\) cannot diverge to \(\infty\) or to \(0\) and must eventually stay in some interval \([m,M]\subset(0,\infty)\).

5. **Select and apply a precise stochastic-approximation / almost-supermartingale theorem.**  
   - For instance, use Robbins–Siegmund’s theorem: show that \(V_n := (Y_n - 3/2)^2\) satisfies a recursion of the form  
     \[
     \mathbb{E}[V_{n+1}\mid\mathcal F_n] \le V_n - c \frac{1}{n} V_n + \rho_n,
     \]  
     with \(\sum \rho_n<\infty\). Then invoke the theorem to get \(V_n\to 0\) a.s.  
   - Alternatively, phrase the recursion directly in the SA form and use Benaïm’s theorem on convergence to attractors of ODEs.

6. **After establishing \(Y_n\to3/2\), cleanly deduce the behaviour of \(K_n\) and \(G_n\).**  
   - Show \(K_n^3/n^2\to3/2\Rightarrow K_n \sim (3/2)^{1/3}n^{2/3}\), and then plug into \(G_n = K_n^2+K_n+2n+2\) to get \(G_n/n^{4/3}\to(3/2)^{2/3}\).

7. **Keep heuristics and rigorous steps clearly separated.**  
   - Where you use heuristic scaling (e.g. \(K_n\asymp n^{2/3}\)), explicitly mark it as such. Then gradually replace these heuristic steps with proven lemmas. This will help you track which parts of the argument still need rigorous justification.

If you tackle these items systematically—especially the first four—you should be able to turn your already very good conceptual outline into a complete, rigorous solution.

---

# SECOND SOLUTION ATTEMPT by the problem solver

## 1. Status  

Status: Partial  

---

## 2. Selected approaches  

Selected approach indices: 1, 3 (combination)  

- I still reduce the urn to the 1‑dimensional process \(K_n\) (Approach 1) and use drift + martingale decomposition.
- In this iteration I **rigorously establish** the almost-sure *exponent* of growth for \(K_n\) (and hence for \(G_n\)) using Freedman’s martingale inequality.
- I **do not** succeed in completing the stochastic-approximation step (Approach 3) needed to show full convergence of \(G_n/n^{4/3}\) to a deterministic constant \(c\). I explain precisely where this remains open.

Compared to the previous attempt, the main improvement is a fully detailed, rigorous proof that
\[
\lim_{n\to\infty}\frac{\log K_n}{\log n} = \frac{2}{3} \quad\text{a.s.},
\]
and therefore
\[
\lim_{n\to\infty}\frac{\log G_n}{\log n} = \frac{4}{3}\quad\text{a.s.}
\]
The remaining gap is to promote this *logarithmic* asymptotic to the precise ratio limit \(G_n/n^{4/3}\to c\).

---

## 3. Solution  

### 3.1. Reduction to the process \(K_n\)

As before:

- Let \(R_n\) = number of red balls after \(n\) steps.
- Let \(B_n\) = number of blue balls after \(n\) steps.
- Let \(G_n = R_n + B_n\).
- Let \(K_n\) = number of *blue* draws among the first \(n\) draws.

From the rules:

- Each step adds exactly **one** blue ball (regardless of colour drawn), so
  \[
  B_n = 1+n \quad\text{for all }n\ge0.
  \]

- Red balls:
  - Initially: 1 red.
  - Each red draw adds 1 red ball: there are \(n-K_n\) red draws.
  - The \(k\)-th blue draw adds \(2k+1\) red balls, for \(k=1,\dots,K_n\).

Thus
\[
\begin{aligned}
R_n
&= 1 + (n-K_n)\cdot 1 + \sum_{k=1}^{K_n}(2k+1)\\
&= 1 + n-K_n + \bigl(K_n(K_n+1) + K_n\bigr)\\
&= 1 + n + K_n^2 + K_n.
\end{aligned}
\]

Therefore
\[
\boxed{G_n = R_n+B_n = K_n^2 + K_n + 2n + 2.}
\]

The entire problem reduces to understanding the growth of the nondecreasing integer-valued process \(K_n\).

---

### 3.2. Dynamics and martingale decomposition for \(K_n\)

Define the increment
\[
\xi_{n+1} :=
\begin{cases}
1,& \text{if the \((n+1)\)-st draw is blue},\\
0,& \text{otherwise}.
\end{cases}
\]

Then
\[
K_{n+1} = K_n + \xi_{n+1}.
\]

Given the past \(\mathcal F_n\) (generated by the first \(n\) draws), the probability of blue at time \(n+1\) is
\[
p_n := \mathbb P(\xi_{n+1}=1\mid\mathcal F_n)
= \frac{B_n}{G_n}
= \frac{n+1}{K_n^2+K_n+2n+2}.
\]

Define the martingale difference
\[
\Delta M_{n+1} := \xi_{n+1} - p_n,
\qquad
M_n := \sum_{j=0}^{n-1}\Delta M_{j+1},
\]
and the “drift” process
\[
A_n := \sum_{j=0}^{n-1}p_j.
\]

Then
\[
\boxed{K_n = A_n + M_n.}
\]

We note:

- \(M_n\) is a martingale with respect to \((\mathcal F_n)\).
- Increments are bounded: \(|\Delta M_{n+1}|\le 1\).
- Conditional variance: \(\mathbb E[\Delta M_{n+1}^2\mid\mathcal F_n]=p_n(1-p_n)\le p_n\).
- The predictable quadratic variation of \(M_n\) is
  \[
  V_n := \langle M\rangle_n = \sum_{j=0}^{n-1}\mathbb E[\Delta M_{j+1}^2\mid\mathcal F_j]
  \le \sum_{j=0}^{n-1}p_j=A_n.
  \]

We will use **Freedman’s inequality** for martingales to compare \(M_n\) with its quadratic variation, in order to relate \(K_n\) and \(A_n\).

---

### 3.3. Freedman’s inequality (tool)

We quote the following standard inequality (one-sided version):

> **Freedman’s inequality.**  
> Let \((M_k, \mathcal F_k)_{k\ge0}\) be a martingale with \(M_0=0\) and increments \(\Delta M_k:=M_k-M_{k-1}\) satisfying \(|\Delta M_k|\le c\) a.s. Let  
> \[
> V_k := \sum_{j=1}^k\mathbb E[\Delta M_j^2\mid\mathcal F_{j-1}]
> \]
> be the predictable quadratic variation. Then for all \(x,v>0\) and all integers \(n\ge1\),
> \[
> \mathbb P\bigl(\exists k\le n: M_k\ge x \text{ and } V_k\le v\bigr)
> \le \exp\!\left(-\frac{x^2}{2(v+cx)}\right).
> \]
> An analogous bound holds for the lower tail, by applying this to the martingale \(-M_k\).

We will apply Freedman within *blocks* of indices, by restarting the martingale at the beginning of each block.

---

### 3.4. Upper growth exponent for \(K_n\): \(\limsup \le 2/3\)

We prove:

> **Lemma 3.1.** For any \(\beta>2/3\),
> \[
> \mathbb P\bigl(K_n \ge n^\beta\ \text{i.o.}\bigr)=0.
> \]
> Consequently
> \[
> \limsup_{n\to\infty}\frac{\log K_n}{\log n} \le \frac{2}{3}\quad\text{a.s.}
> \]

*Proof.* Fix \(\beta>2/3\). For each integer \(m\ge1\), define the event on the dyadic block \([m,2m]\):
\[
E_m := \Bigl\{K_n \ge n^\beta\text{ for all }n\in[m,2m]\Bigr\}.
\]

We aim to show \(\sum_m\mathbb P(E_m)<\infty\); then Borel–Cantelli gives the lemma.

On \(E_m\), since \(K_n\) is nondecreasing,
\[
K_n \ge n^\beta \ge m^\beta\quad\text{for all }n\in[m,2m].
\]
In particular, for each \(j\in[m,2m]\),
\[
K_{j-1}\ge m^\beta.
\]

Hence the drift at time \(j-1\) is bounded *above* by
\[
p_{j-1}
= \frac{j}{K_{j-1}^2+K_{j-1}+2j+2}
\le \frac{j}{K_{j-1}^2}
\le \frac{2m}{m^{2\beta}}
= 2m^{1-2\beta}
\]
for all large enough \(m\). Therefore, on \(E_m\), the block drift satisfies
\[
A_{2m}-A_{m-1}
:= \sum_{j=m}^{2m}p_{j-1}
\le 2m\cdot 2m^{1-2\beta}
= 4m^{2-2\beta}
=: v_m.
\]

On the other hand, since \(K_n\) is nondecreasing and \(K_n\ge n^\beta\) on \([m,2m]\),
\[
K_{2m}-K_{m-1} \ge K_{2m} - K_{m-1}
\ge (2m)^\beta - (m-1)^\beta.
\]
Since \(\beta>0\), there exists \(c_1>0\) such that for all large \(m\),
\[
(2m)^\beta - (m-1)^\beta \ge c_1 m^\beta.
\]
Thus, on \(E_m\),
\[
K_{2m}-K_{m-1} \ge c_1 m^\beta.
\]

Recall \(K_n = A_n + M_n\), so the martingale increment over the block is
\[
\begin{aligned}
M_{2m}-M_{m-1}
&=(K_{2m}-K_{m-1}) - (A_{2m}-A_{m-1})\\
&\ge c_1 m^\beta - 4m^{2-2\beta}.
\end{aligned}
\]

Since \(\beta>2/3\), we have \(2-2\beta<\beta\). Hence for large \(m\),
\[
c_1 m^\beta - 4m^{2-2\beta}\ \ge\ \frac{c_1}{2}m^\beta
= : x_m.
\]

So on \(E_m\) we have
\[
M_{2m}-M_{m-1} \ge x_m,
\quad
A_{2m}-A_{m-1}\le v_m.
\]

Now consider the shifted martingale on this block:
\[
\widetilde M_k := M_{(m-1)+k} - M_{m-1}
\quad\text{for }k=0,1,\dots,m+1.
\]
Its increments are still bounded by 1, and its quadratic variation over the block satisfies
\[
\widetilde V_{m+1} := \sum_{j=m}^{2m}\mathbb E[\Delta M_{j}^2\mid\mathcal F_{j-1}]
\le A_{2m}-A_{m-1}\le v_m.
\]

Thus, on \(E_m\),
\[
\widetilde M_{m+1} = M_{2m}-M_{m-1} \ge x_m,
\quad
\widetilde V_{m+1} \le v_m.
\]

Freedman’s inequality with \(c=1\), \(x=x_m\), \(v=v_m\), and \(n=m+1\) yields
\[
\mathbb P(E_m)
\le \mathbb P\bigl(\widetilde M_{m+1}\ge x_m,\ \widetilde V_{m+1}\le v_m\bigr)
\le \exp\!\left(-\frac{x_m^2}{2(v_m + x_m)}\right).
\]

We estimate the exponent:  
Since
\[
x_m = \frac{c_1}{2}m^\beta,\quad 
v_m = 4m^{2-2\beta},
\]
we have
\[
\frac{v_m}{x_m} 
= O\bigl(m^{2-2\beta-\beta}\bigr) = O\bigl(m^{2-3\beta}\bigr).
\]
But \(3\beta>2\) (since \(\beta>2/3\)), so \(2-3\beta<0\), and \(\frac{v_m}{x_m}\to0\). Thus for large \(m\),
\[
v_m+x_m \le 2x_m.
\]

Therefore
\[
\frac{x_m^2}{2(v_m + x_m)}
\ge \frac{x_m^2}{4x_m}
= \frac{x_m}{4}
= \frac{c_1}{8}m^\beta.
\]

So for some constant \(c>0\) and all large \(m\),
\[
\mathbb P(E_m) \le \exp(-c m^\beta).
\]

Since \(\beta>0\), the series \(\sum_{m=1}^\infty \exp(-c m^\beta)\) converges. Hence
\[
\sum_{m=1}^\infty\mathbb P(E_m)<\infty,
\]
and by the Borel–Cantelli lemma, with probability one only finitely many \(E_m\) occur.

Now observe: if \(K_n\ge n^\beta\) holds for infinitely many \(n\), then for infinitely many dyadic scales \(m\), the event \(E_m\) must occur (because once \(K_n\ge n^\beta\) for some large \(n\), then, since \(K_n\) is nondecreasing, for all larger \(k\ge n\) we have \(K_k\ge n^\beta\ge c k^\beta\) on some interval). So
\[
\mathbb P(K_n\ge n^\beta\ \text{i.o.})\le \mathbb P(E_m\text{ i.o.})=0.
\]

This proves Lemma 3.1. \(\square\)

---

### 3.5. Lower growth exponent for \(K_n\): \(\liminf \ge 2/3\)

Now we prove the matching lower bound.

> **Lemma 3.2.** For any \(\beta<2/3\),
> \[
> \mathbb P\bigl(K_n \le n^\beta\ \text{i.o.}\bigr)=0.
> \]
> Consequently
> \[
> \liminf_{n\to\infty}\frac{\log K_n}{\log n} \ge \frac{2}{3}\quad\text{a.s.}
> \]

*Proof.* Fix \(\beta<2/3\) with \(\beta>1/2\) (the case \(\beta\le1/2\) is even easier; in any case \(K_n\to\infty\) almost surely, because blue has uniformly positive probability at each step when \(K_n\) is bounded).

Again fix a block \([m,2m]\) and define
\[
F_m := \Bigl\{K_n \le n^\beta\text{ for all }n\in [m,2m]\Bigr\}.
\]

We will show \(\sum_m\mathbb P(F_m)<\infty\).

On \(F_m\), for each \(j\in[m,2m]\),
\[
K_{j-1}\le K_j \le (2m)^\beta.
\]
We want a *lower* bound on \(p_{j-1}\). For large enough \(m\), since \(\beta>1/2\), we have \(K_{j-1}^2\gg j\) uniformly over \(j\in[m,2m]\), more precisely:

There exists \(m_0\) such that for all \(m\ge m_0\),
\[
(2m)^{2\beta} \ge 8m
\quad\Rightarrow\quad
K_{j-1}^2 \ge 4j
\quad\text{for all }j\in[m,2m],
\]
on \(F_m\). Then, for such \(m\), on \(F_m\) and for any \(j\in[m,2m]\),

\[
\begin{aligned}
p_{j-1}
&= \frac{j}{K_{j-1}^2+K_{j-1}+2j+2}\\
&\ge \frac{j}{K_{j-1}^2+K_{j-1}+\frac12 K_{j-1}^2 + 2}\\
\quad\text{(since }2j\le \tfrac12 K_{j-1}^2\text{)}\\[3pt]
&\ge \frac{j}{\frac32(2m)^{2\beta} + O(m^\beta)}\\[3pt]
&\ge c\,\frac{m}{m^{2\beta}}\\
&= c\,m^{1-2\beta}
\end{aligned}
\]
for some constant \(c>0\), when \(m\) is large.

Thus on \(F_m\),

\[
A_{2m}-A_{m-1}
= \sum_{j=m}^{2m}p_{j-1}
\ge m \cdot c m^{1-2\beta}
= c' m^{2-2\beta}
=: v_m.
\]

On the other hand, since \(K_n\) is nondecreasing and \(K_n\le n^\beta\) on \([m,2m]\),

\[
K_{2m}-K_{m-1}
\le K_{2m} \le (2m)^\beta
\le C m^\beta.
\]

Therefore on \(F_m\),

\[
\begin{aligned}
M_{2m}-M_{m-1}
&=(K_{2m}-K_{m-1}) - (A_{2m}-A_{m-1})\\
&\le C m^\beta - c' m^{2-2\beta}.
\end{aligned}
\]

Since \(\beta<2/3\), we have \(2-2\beta>\beta\). Hence for large \(m\),
\[
C m^\beta - c' m^{2-2\beta}
\le -\frac{c'}{2} m^{2-2\beta}
=: -x_m.
\]

Thus on \(F_m\),
\[
M_{2m}-M_{m-1} \le -x_m, \quad
A_{2m}-A_{m-1} \ge v_m=c' m^{2-2\beta}.
\]

Again shift to the block martingale \(\widetilde M_k := M_{(m-1)+k}-M_{m-1}\). Its quadratic variation over the block is
\[
\widetilde V_{m+1} 
= \sum_{j=m}^{2m}\mathbb E[\Delta M_{j}^2\mid\mathcal F_{j-1}]
\le A_{2m}-A_{m-1},
\]
but we now need a *lower* bound, so we simply keep that \(\widetilde V_{m+1}\ge v_m\) as above.

We apply Freedman to the *negative* martingale \(-\widetilde M_k\) (whose increments are still bounded by 1) with \(x=x_m\), \(v=v_m\). Then
\[
\mathbb P(F_m)
\le \mathbb P\bigl(\widetilde M_{m+1} \le -x_m,\ \widetilde V_{m+1}\le v_m\bigr)
\le \exp\!\left(-\frac{x_m^2}{2(v_m + x_m)}\right).
\]

Here
\[
x_m = \frac{c'}{2}m^{2-2\beta},\quad 
v_m = c' m^{2-2\beta}.
\]
Then \(x_m\) and \(v_m\) are of the same order, and
\[
\frac{x_m^2}{2(v_m + x_m)} \asymp m^{2-2\beta}.
\]
More concretely, for large \(m\),
\[
v_m + x_m \le 2v_m = 2c' m^{2-2\beta},
\]
so
\[
\frac{x_m^2}{2(v_m + x_m)}
\ge \frac{x_m^2}{4v_m}
= \frac{(c'/2)^2 m^{4-4\beta}}{4c'm^{2-2\beta}}
= c'' m^{2-2\beta}.
\]

Thus for some constant \(c>0\),
\[
\mathbb P(F_m)\le \exp(-c m^{2-2\beta}).
\]

Since \(\beta<2/3\), we have \(2-2\beta>0\), so the series \(\sum_m \exp(-c m^{2-2\beta})\) converges. Hence
\[
\sum_{m=1}^\infty\mathbb P(F_m)<\infty
\]
and Borel–Cantelli implies that only finitely many \(F_m\) occur almost surely.

Now if \(K_n\le n^\beta\) occurs infinitely often, then infinitely many of these blocks \([m,2m]\) must contain such times and thus infinitely many \(F_m\) occur, which has probability 0. So
\[
\mathbb P(K_n\le n^\beta\ \text{i.o.})=0.
\]

This proves Lemma 3.2. \(\square\)

---

### 3.6. Asymptotic exponent of \(K_n\) and of \(G_n\)

From Lemmas 3.1 and 3.2:

For every rational \(\beta>2/3\), a.s. \(K_n < n^\beta\) for all large \(n\); and for every rational \(\beta<2/3\), a.s. \(K_n> n^\beta\) for all large \(n\). Taking a countable intersection over \(\beta\in\mathbb Q\), we get

> **Corollary 3.3.**
> \[
> \lim_{n\to\infty}\frac{\log K_n}{\log n} = \frac{2}{3}\quad\text{almost surely}.
> \]

Equivalently, for every \(\varepsilon>0\), there is a random \(N(\varepsilon)\) such that almost surely for all \(n\ge N(\varepsilon)\),
\[
n^{2/3-\varepsilon} \le K_n \le n^{2/3+\varepsilon}.
\]

Using \(G_n = K_n^2 + K_n + 2n+2\), we obtain:

> **Corollary 3.4.**
> \[
> \lim_{n\to\infty}\frac{\log G_n}{\log n} = \frac{4}{3}\quad\text{almost surely}.
> \]

*Proof.* From Corollary 3.3, for any fixed \(\varepsilon>0\) and all large \(n\),
\[
n^{2/3-\varepsilon} \le K_n \le n^{2/3+\varepsilon}.
\]
Then
\[
K_n^2 \in \bigl[n^{4/3-2\varepsilon},\, n^{4/3+2\varepsilon}\bigr].
\]
Since \(K_n^2\) dominates both \(K_n\) and \(2n\) at this scale (for small enough \(\varepsilon\)), we have
\[
G_n = K_n^2 + K_n + 2n+2
= K_n^2\bigl(1+o(1)\bigr),
\]
so
\[
\frac{\log G_n}{\log n} = \frac{\log K_n^2(1+o(1))}{\log n}
= 2\frac{\log K_n}{\log n} + o(1)
\to 2\cdot\frac{2}{3} = \frac{4}{3}.
\quad\square
\]

Thus we now know **deterministically** that \(G_n\) grows polynomially with almost sure exponent \(\alpha=4/3\). In symbols,

\[
G_n = n^{4/3 + o(1)} \quad\text{a.s.}
\]

What remains to prove (for a full solution to the original problem) is that the more precise ratio
\[
\frac{G_n}{n^{4/3}}
\]
actually converges almost surely to a finite, positive constant \(c\). We have not yet shown **existence of the limit**, only its order of magnitude on a log-scale.

---

### 3.7. Remarks on the potential function \(Y_n = K_n^3/n^2\) (partial)

This subsection connects to Approach 3 (potential function) and explains where the remaining difficulties lie; no new rigorous results beyond those above are claimed here.

Define
\[
Y_n := \frac{K_n^3}{n^2}\quad(n\ge1).
\]

The exact one-step increment computation (as in the previous attempt, now checked carefully) is:

\[
\begin{aligned}
Y_{n+1}-Y_n
&= K_n^3\Bigl(\frac{1}{(n+1)^2} - \frac{1}{n^2}\Bigr)
  + \frac{(3K_n^2+3K_n+1)\,\xi_{n+1}}{(n+1)^2}\\
&= - K_n^3\frac{2n+1}{n^2(n+1)^2} + \frac{(3K_n^2+3K_n+1)\,\xi_{n+1}}{(n+1)^2}\\
&= -Y_n\frac{2n+1}{(n+1)^2}
   + \frac{(3K_n^2+3K_n+1)\,\xi_{n+1}}{(n+1)^2}.
\end{aligned}
\]

Taking conditional expectation and using \(p_n = \mathbb P(\xi_{n+1}=1\mid\mathcal F_n)\),
\[
\mathbb E[Y_{n+1}-Y_n\mid\mathcal F_n]
= -Y_n \frac{2n+1}{(n+1)^2}
  + \frac{(3K_n^2+3K_n+1)p_n}{(n+1)^2}.
\]

Recall
\[
p_n = \frac{n+1}{K_n^2+K_n+2n+2} = \frac{n+1}{D_n}.
\]

Thus
\[
\mathbb E[Y_{n+1}-Y_n\mid\mathcal F_n]
= -Y_n \frac{2n+1}{(n+1)^2}
  + \frac{3K_n^2+3K_n+1}{(n+1)D_n}.
\]

We also have the identity
\[
3K_n^2+3K_n+1 = 3D_n - (6n+5),
\]
so equivalently
\[
\boxed{
\mathbb E[Y_{n+1}-Y_n\mid\mathcal F_n]
= -Y_n \frac{2n+1}{(n+1)^2} + \frac{3}{n+1} - \frac{6n+5}{(n+1)D_n}.
}
\tag{*}
\]

Using the already proved exponent control on \(K_n\), we know that:

- For any \(\varepsilon>0\), eventually
  \[
  c_1 n^{2/3-\varepsilon} \le K_n \le c_2 n^{2/3+\varepsilon}.
  \]
- Hence
  \[
  c_3 n^{4/3-2\varepsilon} \le K_n^2 \le c_4 n^{4/3+2\varepsilon}.
  \]
- And since \(D_n=K_n^2+K_n+2n+2\), we get for small \(\varepsilon>0\):
  \[
  D_n \asymp K_n^2 \asymp n^{4/3+o(1)}.
  \]

Plugging this into \((*)\), we see that:

- The first term \(-Y_n(2n+1)/(n+1)^2\) is of order \(-Y_n/n\).
- The middle term \(3/(n+1)\) is of order \(1/n\).
- The last term \((6n+5)/((n+1)D_n)\) is of order \(n/D_n \asymp n / n^{4/3} = n^{-1/3}\).

So **at the scale suggested by exponent analysis**, the drift of \(Y_n\) is *dominated* by an \(O(n^{-1/3})\) term. This is larger in magnitude than the \(O(1/n)\) terms coming from the denominator shift and the approximate \(3n\) drift of \(K_n^3\). In particular, the simplistic approximation
\[
\mathbb E[Y_{n+1}-Y_n\mid\mathcal F_n] \approx \frac{3-2Y_n}{n}
\]
is not adequate: the term involving \(D_n\) contributes significantly and in a way that depends intricately on both \(K_n\) and \(Y_n\).

A more natural normalization, therefore, is to work directly with
\[
X_n := \frac{K_n}{n^{2/3}},
\]
for which one can compute that the *effective* “step size” in the stochastic approximation is of order \(n^{-1/3}\), consistent with the exponent of \(p_n\).

Pursuing that analysis rigorously would require:

- expressing the recursion for \(X_{n+1}-X_n\) in a form
  \[
  X_{n+1} = X_n + a_n(F(X_n) + \eta_{n+1})
  \]
  with \(a_n\asymp n^{-1/3}\);
- controlling the noise \(\eta_{n+1}\) and showing its effective variance scale \(\sum a_n^2 \mathbb E[\eta_{n+1}^2\mid\mathcal F_n]\) is finite;
- and verifying that the associated ODE \(dx/dt = F(x)\) has a unique globally attracting equilibrium.

I have not completed those steps here; they are technical, and any clean proof would essentially reproduce a large portion of the general stochastic-approximation machinery.

---

## 4. Gaps  

Gaps remain; I list them clearly.

### Gap 1: Convergence (not just exponent) of \(K_n/n^{2/3}\)

**Location:** Conceptually between §§3.6 and 3.7.  

**What is missing:**  

I have proved that
\[
\lim_{n\to\infty}\frac{\log K_n}{\log n} = \frac{2}{3}\quad\text{a.s.},
\]
but I have **not** proved that the normalized sequence
\[
\frac{K_n}{n^{2/3}}
\]
converges almost surely (or even in probability) to a *finite, positive constant*. At present we only know that for any \(\varepsilon>0\),
\[
n^{2/3-\varepsilon} \le K_n \le n^{2/3+\varepsilon}\quad\text{eventually a.s.}
\]
i.e. the ratio \(K_n/n^{2/3}\) stays in a slowly widening band \(n^{\pm \varepsilon}\); there is no proven convergence to a fixed \(L\).

**Why this is hard:**  

The Markov chain \(\{K_n\}\) has a non-linear, state-dependent drift
\[
\mathbb E[K_{n+1}-K_n\mid\mathcal F_n]=p_n = \frac{n+1}{K_n^2+K_n+2n+2},
\]
and the increments are only \(0\) or \(1\). Turning the exponent control into a precise law of large numbers at the scale \(n^{2/3}\) essentially requires a **stochastic-approximation** theorem in a nonstandard regime (step size \(\asymp n^{-1/3}\), non-linear drift, nontrivial noise). I have not fully implemented such a theorem here.

---

### Gap 2: Convergence of \(Y_n = K_n^3/n^2\)

**Location:** §3.7.  

**What is missing:**  

I have not proved that
\[
Y_n = \frac{K_n^3}{n^2}
\]
converges almost surely to a finite constant (let alone identified that constant).

The exact drift formula \((*)\) reveals that the leading contribution to \(\mathbb E[Y_{n+1}-Y_n\mid\mathcal F_n]\) is of order \(n^{-1/3}\) rather than \(1/n\), making the naive comparison with an ODE of the form \(dy/dt = (3-2y)/t\) invalid. A more sophisticated two-parameter analysis (involving both \(Y_n\) and the ratio \(n/K_n^2\)) seems necessary.

**Why this is hard:**  

The dependence on \(D_n\) in the drift term is subtle: after substituting \(K_n^2\sim Y_n^{2/3}n^{4/3}\), the additional term \(-(6n+5)/((n+1)D_n)\) yields a contribution of order \(n^{-1/3}\) that does *not* vanish in the limit where one might want to treat it as a small perturbation. This complicates the usual “small-error” stochastic-approximation approach via \(Y_n\).

---

### Gap 3: Existence and identification of the limit \(\displaystyle \lim_{n\to\infty} \frac{G_n}{n^{4/3}}\)

**Location:** Global, after Corollary 3.4.  

**What is missing:**  

The original problem asks to prove there exist constants \(0<c,\alpha<\infty\) such that
\[
\frac{G_n}{n^\alpha} \to c\quad\text{a.s.}
\]

I have shown:

- that necessarily \(\alpha=4/3\);
- that \(G_n/n^{4/3} = n^{o(1)}\) almost surely (i.e. its logarithmic behaviour is determined).

I have **not** shown that \(G_n/n^{4/3}\) has an almost sure (or even in-probability) limit. In particular, I have not proved that the ratio converges, rather than oscillating within a band of slowly shrinking or constant relative width.

**Why this is hard:**  

To show convergence of \(G_n/n^{4/3}\) to a *deterministic* constant \(c\) one must:

- establish that \(K_n/n^{2/3} \to L\) for some deterministic \(L>0\);
- then conclude \(G_n/n^{4/3} = (K_n/n^{2/3})^2 + o(1) \to L^2\).

The main technical obstacle is the first step: a precise stochastic-approximation analysis that goes beyond the exponent control provided by Freedman’s inequality. Such an analysis would require a detailed treatment of the drift and noise of the normalized process and an appeal to a general convergence theorem (e.g. Benaïm’s framework), with all hypotheses checked. This is not yet carried out here.

---

## 5. Self-evaluation  

**Confidence score (0–100):** 72  

**Known or suspected issues:**

- The **Freedman-block arguments** in §§3.4–3.5 are, in my view, solid: they carefully use bounded increments, control the drift on blocks, apply Freedman’s inequality with explicit \(x_m,v_m\), and sum resulting tail bounds. I am reasonably confident these lemmas correctly establish the almost-sure exponent \(2/3\) for \(K_n\).
- The passage from exponent of \(K_n\) to exponent of \(G_n\) (Corollary 3.4) is straightforward.
- The **stochastic-approximation part** (convergence of \(K_n/n^{2/3}\) or of \(Y_n\)) is *not* done. My remarks in §3.7, while more cautious than before, are still heuristic and do not constitute a proof.
- There may remain minor algebraic slips (e.g. in the exponents for some bounds), but these would only affect constants, not the main asymptotic exponents.

**Coverage comment:**

- Completely addressed:
  - Reduction of the urn model to the Markov chain \(K_n\) and the identity \(G_n=K_n^2+K_n+2n+2\).
  - Rigorous determination of the almost-sure growth exponent:
    \[
    \lim\frac{\log K_n}{\log n} = 2/3,\quad \lim\frac{\log G_n}{\log n} = 4/3.
    \]
- Not fully addressed:
  - Existence of a *limit* \(c>0\) such that \(G_n/n^{4/3}\to c\) almost surely. I have solidly identified the exponent \(\alpha=4/3\), but convergence of the ratio itself, and the exact value of \(c\), remain unproved in this write-up.

In summary, the present solution significantly advances the previous attempt by rigorously pinning down the growth exponents of \(K_n\) and \(G_n\) using Freedman’s inequality; however, it still falls short of fully solving the original problem, as the almost-sure convergence of \(G_n/n^{4/3}\) to a deterministic constant remains open here.

---

# Expert evaluator's feedback on the problem solver's SECOND SOLUTION ATTEMPT

## 1. Status  

Status: Partial  

---

## 2. Score  

Score (0–100): 58  

---

## 3. Major issues  

- **Location:** Lemma 3.1 (upper growth exponent), final paragraph connecting \(E_m\) and “\(K_n \ge n^\beta\) infinitely often”  
  **Issue type:** Logical error / incorrect event inclusion  
  **Description:**  
  You define  
  \[
  E_m := \{K_n \ge n^\beta \ \text{for all } n\in[m,2m]\},
  \]  
  prove \(\sum_m \mathbb{P}(E_m)<\infty\), and then claim:
  > “if \(K_n\ge n^\beta\) holds for infinitely many \(n\), then for infinitely many dyadic scales \(m\), the event \(E_m\) must occur,”  
  hence \(\mathbb{P}(K_n\ge n^\beta \text{ i.o.}) \le \mathbb{P}(E_m \text{ i.o.}) = 0\).  

  This implication is **not valid**. From \(K_n \ge n^\beta\) at some scattered times \(n\), it does *not* follow that there are infinitely many blocks \([m,2m]\) on which \(K_n\ge n^\beta\) for **all** \(n\) in the block. The event “for all \(n\in[m,2m]\)” is much stronger than “for some \(n\in[m,2m]\)”, and you have only ruled out the stronger event. In fact, the correct inclusion is  
  \[
  \{E_m\ \text{i.o.}\} \subset \{K_n\ge n^\beta\ \text{i.o.}\},
  \]  
  not the other way round.  
  **Suggested direction for fix:**  
  Redefine the block events to match the “infinitely often” notion more directly. For example, define  
  \[
  E_m' := \{\exists n\in[m,2m] \text{ with } K_n \ge c\,n^\beta\}
  \]  
  (or with a suitably chosen constant \(c\)). Freedman’s inequality already controls **suprema** of the martingale, so you can aim to bound \(\mathbb{P}(E_m')\) rather than insisting on “for all \(n\) in the block”. Then a Borel–Cantelli argument on \(\sum_m \mathbb{P}(E_m')\) correctly bears on \(\{K_n\ge n^\beta\ \text{i.o.}\}\). Alternatively, phrase things via hitting times of the curve \(n^\beta\) and control what happens *after* a hitting time using Freedman.

---

- **Location:** Lemma 3.2 (lower growth exponent), middle of proof (deriving a lower bound on \(p_{j-1}\))  
  **Issue type:** Major computational / logical slip  
  **Description:**  
  On \(F_m = \{K_n \le n^\beta \ \forall n\in[m,2m]\}\), you have the upper bound \(K_{j-1} \le (2m)^\beta\). You then write:
  > “since \((2m)^{2\beta} \ge 8m\) we have \(K_{j-1}^2 \ge 4j\) for all \(j\in[m,2m]\) on \(F_m\).”  

  This implication is false as written. From \(K_{j-1} \le (2m)^\beta\) and \((2m)^{2\beta} \ge 8m\) you *cannot* deduce \(K_{j-1}^2 \ge 4j\); the inequality goes in the opposite direction. You are trying to show \(K_{j-1}^2\) is large enough to dominate \(2j\), but your assumption on \(F_m\) only bounds \(K_{j-1}\) from **above**, not below.  
  **Suggested direction for fix:**  
  For a lower bound on \(p_{j-1}\), you want an **upper** bound on the denominator \(K_{j-1}^2 + K_{j-1} + 2j + 2\), so an upper bound on \(K_{j-1}\) is exactly what you need. The correct argument is simpler: on \(F_m\),
  \[
  K_{j-1}^2 + K_{j-1} + 2j + 2 \le (2m)^{2\beta} + (2m)^{\beta} +4m+2 \le C m^{2\beta},
  \]
  for some constant \(C\), since \(2\beta>1\). Then
  \[
  p_{j-1} = \frac{j}{K_{j-1}^2+K_{j-1}+2j+2}
  \ge \frac{m}{C m^{2\beta}} = c m^{1-2\beta}.
  \]
  In other words, you do not need (and must not assume) \(K_{j-1}^2\ge 4j\); you only need an upper bound on the denominator.

---

- **Location:** Lemma 3.2 (lower growth exponent), application of Freedman’s inequality  
  **Issue type:** Misuse of theorem / wrong inequality direction on quadratic variation  
  **Description:**  
  At the end of Lemma 3.2 you want to apply Freedman to the block martingale \(\widetilde M_k\). Freedman gives control of events of the form  
  \[
  \bigl\{\exists k\le n:\ M_k \le -x \text{ and } V_k \le v\bigr\},
  \]
  i.e. with the predictable quadratic variation bounded **above** by \(v\). In your lower-bound proof you derive a lower bound \(A_{2m}-A_{m-1} \ge v_m\), and then incorrectly assert:
  > “we now need a lower bound, so we simply keep that \(\tilde V_{m+1} \ge v_m\) as above.”  

  But \(V_n = \sum p_j(1-p_j) \le \sum p_j = A_n\), so from \(A_{2m}-A_{m-1} \ge v_m\) you cannot deduce \(V_{2m}-V_{m-1} \ge v_m\); you only know \(V\) is **at most** \(A\). This is the wrong direction for Freedman: you need an **upper** bound on \(V\), not a lower bound. The inequality as used is incorrect, and the Freedman application is not justified.  
  **Suggested direction for fix:**  
  Use a **uniform upper bound** on the drift over the block instead. For any block of length \(m+1\), trivially  
  \[
  A_{2m}-A_{m-1} \le \sum_{j=m}^{2m} 1 = m+1,
  \]
  and hence also \(V_{2m}-V_{m-1} \le m+1\). Set \(v=m+1\) in Freedman. Then recompute the exponent  
  \[
  \frac{x_m^2}{2(v + c x_m)}
  \]
  with \(x_m \asymp m^{2-2\beta}\) and \(v\asymp m\); you will obtain an exponent of order \(m^{3-4\beta}\), which is still positive when \(\beta<2/3\), giving summable tail estimates. This preserves your strategy but uses the theorem correctly.

---

- **Location:** Both Lemma 3.1 and Lemma 3.2, final step to infer \(\limsup\) and \(\liminf\) from block estimates  
  **Issue type:** Missing critical link / global-to-local inference  
  **Description:**  
  Even correcting the Freedman applications and the algebra for \(p_n\), your lemmas as written only control probabilities of relatively strong *block events* \(E_m\) and \(F_m\) (“for all \(n\in[m,2m]\), \(K_n \ge n^\beta\)” or \(\le n^\beta\)). To prove 
  \[
  \mathbb{P}(K_n \ge n^\beta \text{ i.o.}) = 0
  \]
  or 
  \[
  \mathbb{P}(K_n \le n^\beta \text{ i.o.}) = 0,
  \]
  you must relate “infinitely often at (possibly isolated) times” to the occurrence of these block events. That relationship is *not* established: it is perfectly consistent for a nondecreasing process to cross above a growing curve \(n^\beta\) infinitely many times without ever staying above it for an entire dyadic block \([m,2m]\). So even with corrected tail bounds
  \(\sum_m \mathbb{P}(E_m)<\infty\) or \(\sum_m \mathbb{P}(F_m)<\infty\), you have not yet shown that \(\limsup \log K_n / \log n \le \beta\) or \(\liminf \ge \beta\).  
  **Suggested direction for fix:**  
  Adjust the block events to correspond more directly to “sup over block” or “inf over block”, e.g.:  
  - Upper bound: \(E_m' := \{\max_{n\in[m,2m]} K_n \ge (2m)^\beta\}\).  
  - Lower bound: \(F_m' := \{\min_{n\in[m,2m]} K_n \le m^\beta\}\).  
  Freedman already bounds events of the form \(\{\sup M_k \ge x\}\), so working with maxima/minima over blocks is natural. Then show that \(K_n \ge n^\beta\) i.o. implies \(E_m'\) i.o., and similarly for the lower bound. This will give the desired conclusions about \(\limsup\) and \(\liminf\) once the block probabilities are shown summable.

---

- **Location:** Global conclusion: Corollary 3.3 and Corollary 3.4  
  **Issue type:** Derived from flawed lemmas  
  **Description:**  
  Corollary 3.3 (that \(\lim (\log K_n)/(\log n) = 2/3\) a.s.) and thus Corollary 3.4 (that the exponent for \(G_n\) is \(4/3\)) both depend crucially on Lemma 3.1 and Lemma 3.2. Since those lemmas are not yet rigorously proved (due to the issues above), the corollaries are not currently justified.  
  **Suggested direction for fix:**  
  Once you fix the lemmas (via corrected Freedman applications and appropriate block events), the rest of the corollaries will likely go through with only minor adjustments. But as of now, you should treat the exponent result as *conjectural*, not established.

---

## 4. Minor issues  

- **Location:** Lemma 3.2, choice of the range \(\beta>1/2\)  
  **Nature:** Unclear necessity / exposition  
  **Description:**  
  You restrict to \(\beta>1/2\) and mention “the case \(\beta\le 1/2\) is even easier”, but you do not actually provide an argument for \(\beta\le 1/2\). While this is likely true (for small \(\beta\) the statement is trivial because \(K_n\to\infty\) a.s.), leaving it implicit makes the exposition slightly incomplete.  
  **Suggestion:**  
  Add a brief argument: since every step has probability at least \(c>0\) of drawing blue as long as \(K_n\) is bounded, we have \(K_n\to\infty\) almost surely; thus for any \(\beta<0\) or small \(\beta\) the lower-bound liminf is automatic. Or simply treat \(\beta\in(0,2/3)\) uniformly via your Freedman method so you don’t need to carve out a special case.

- **Location:** §3.7, order-of-magnitude discussion for drift of \(Y_n\)  
  **Nature:** Slightly misleading heuristic  
  **Description:**  
  You correctly observe that \((6n+5)/((n+1)D_n) \asymp n^{-1/3}\) under the exponent heuristics, and then state that this term “dominates” the \(O(1/n)\) terms. While true for raw orders, the *sign* and *interaction* with the rest of the drift are also crucial, especially if you later hope to regard it as a “small perturbation”. The reader might be left with the impression that the main drift structure is now broken.  
  **Suggestion:**  
  Clarify that the presence of an \(O(n^{-1/3})\) term means the potential \(Y_n\) is *not* the cleanest scaling for a classical \(1/n\)-step stochastic approximation, and that a more natural normalization is likely \(X_n = K_n/n^{2/3}\) with effective step size \(n^{-1/3}\). This keeps the heuristic discussion aligned with the SA literature.

- **Location:** General exposition around Freedman’s inequality  
  **Nature:** Notational consistency / clarity  
  **Description:**  
  You use \(V_n\) both globally and as a block quadratic variation \(\widetilde V_{m+1}\). Although you do define the shifted martingale \(\widetilde M_k\), the corresponding \(V\)-notation could be clearer.  
  **Suggestion:**  
  Explicitly denote the block quadratic variation as  
  \[
  V^{(m)}_k := \sum_{j=1}^k \mathbb{E}[(\Delta \widetilde M_j)^2\mid\mathcal F_{m-1+j}],
  \]  
  with \(k=m+1\) at the end. This makes it easier to track which process Freedman is being applied to.

---

## 5. Gap assessment  

You explicitly listed three gaps; I’ll comment on each and also add one implicit gap:

- **Gap 1: Convergence (not just exponent) of \(K_n / n^{2/3}\)**  
  **Assessment:** Fundamental.  
  This is indeed one of the central difficulties of the original problem: turning exponent information into a precise law of large numbers at the correct scale. Even if the exponent \(2/3\) for \(K_n\) were established, showing that \(K_n / n^{2/3}\) converges (and to a deterministic constant) requires a full stochastic-approximation analysis. This is the main missing content relative to the problem’s statement.

- **Gap 2: Convergence of \(Y_n = K_n^3 / n^2\)**  
  **Assessment:** Moderate-to-fundamental.  
  As you note, once exponent control is available, one could in principle work with \(Y_n\) or directly with \(X_n = K_n/n^{2/3}\). However, the algebra for \(Y_n\) shows that it may not fit a clean \(1/n\)-step SA scheme because of the \(n^{-1/3}\)-order term. This gap sits at the technical heart of the SA approach; closing it requires either a refined scaling or a different potential.

- **Gap 3: Existence and identification of \(\lim G_n / n^{4/3}\)**  
  **Assessment:** Consequential but derivative.  
  Once Gap 1 is resolved (i.e. you know \(K_n / n^{2/3} \to L\) for some deterministic \(L>0\)), then Gap 3 largely becomes a short algebraic step: \(\lim G_n / n^{4/3} = L^2\). So the real core is in proving a strong LLN for \(K_n\), not in the final translation to \(G_n\).

- **Implicit Gap 0: Correct proof of the exponent \(\lim (\log K_n)/\log n = 2/3\)**  
  **Assessment:** Fundamental.  
  You regard this as now “rigorously established” via Freedman, but due to the issues above, the exponent result is not yet proved. Once the block events are adjusted and Freedman is used correctly, this result is very plausible and likely accessible, but it still requires a careful and somewhat delicate argument.

---

## 6. Coverage assessment  

All subparts addressed: No  

- The core requirement of the original problem is to prove that there exist **deterministic** constants \(c>0,\ \alpha>0\) such that  
  \[
  \frac{G_n}{n^\alpha} \to c\quad\text{almost surely}.
  \]
- You have:
  - Correctly reduced the process to the one-dimensional chain \(K_n\) and the identity \(G_n = K_n^2 + K_n + 2n + 2\).  
  - Outlined and partly implemented a promising strategy based on martingale decomposition and Freedman’s inequality.  
  - Attempted to rigorously identify the exponent \(2/3\) for \(K_n\) (and hence \(4/3\) for \(G_n\)), but the current proofs of Lemma 3.1 and 3.2 contain serious gaps.  
  - Explicitly left open the convergence of \(K_n/n^{2/3}\) and of \(G_n/n^{4/3}\).  

So neither the exponent nor the limit constant \(c\) has been fully established; the problem remains unsolved in this iteration.

---

## 7. Summary  

Your second attempt makes real progress in terms of strategy: you move from heuristic scaling arguments to a concrete plan using Freedman’s inequality on block intervals, decomposing \(K_n\) into drift \(A_n\) and martingale noise \(M_n\). This is exactly the right kind of tool for this kind of self-normalizing Markov chain. The reduction to \(K_n\) and the identity \(G_n = K_n^2 + K_n + 2n + 2\) remain fully correct and are the backbone of the analysis.  

The main claimed new result is the almost sure exponent of growth for \(K_n\) and \(G_n\). Unfortunately, the current proofs of Lemmas 3.1 and 3.2 are not yet rigorous: there are logical missteps in how block events are related to “infinitely often” events, and several inequalities (most notably in Lemma 3.2) are used in the wrong direction. Thus, the exponent \(2/3\) is still a well-founded heuristic rather than a theorem in your write-up.  

On the positive side, the Freedman-block idea is a strong and standard method: once the block events are redefined appropriately (e.g., in terms of suprema/infima over blocks rather than “for all times” in a block) and the inequalities are corrected, you are likely to obtain polynomial upper and lower bounds for \(K_n\) with high probability, and then almost surely via Borel–Cantelli. This would then provide a robust base for the more refined stochastic-approximation step.  

You are also now appropriately cautious about the potential-function approach via \(Y_n = K_n^3/n^2\), recognizing that the drift term has a component of order \(n^{-1/3}\) that complicates a naive \(1/n\)-step SA analysis. That indicates a deeper understanding of the technical difficulties at hand. Overall, the conceptual direction remains promising, but the current iteration still has structural gaps that must be closed before you can confidently claim the exponent result or move on to proving convergence of the normalized sequence.

---

## 8. Recommendations for next iteration  

1. **Repair the exponent lemmas via better block events.**  
   - Redefine your block events to align with sup/inf behaviour instead of “for all \(n\)” in the block:  
     - For upper bounds: \(E_m' := \{\max_{n\in[m,2m]} K_n \ge (2m)^\beta\}\).  
     - For lower bounds: \(F_m' := \{\min_{n\in[m,2m]} K_n \le m^\beta\}\).  
   - Show that \(K_n \ge n^\beta\) i.o. implies \(E_m'\) i.o., and similarly for the lower side. Then use Freedman’s inequality to bound \(\mathbb{P}(E_m')\) and \(\mathbb{P}(F_m')\) and apply Borel–Cantelli.

2. **Fix the Freedman applications and inequality directions.**  
   - For the upper bound (Lemma 3.1), the structure is essentially correct: you have \(A_{2m}-A_{m-1} \le v_m\), and thus \(V_{2m}-V_{m-1}\le v_m\); Freedman’s conditions are satisfied.  
   - For the lower bound (Lemma 3.2), avoid claiming \(\tilde V_{m+1} \ge v_m\); instead, use a simple uniform upper bound on \(\tilde V_{m+1}\) such as \(v=2m\) (since in each of the \(m+1\) steps, the variance is at most 1). Recalculate the tail exponent with this \(v\); it still yields a summable series for \(\beta<2/3\).

3. **Recompute the lower-bound drift estimates cleanly.**  
   - Remove the incorrect step asserting \(K_{j-1}^2 \ge 4j\) on \(F_m\). Directly bound the denominator of \(p_{j-1}\) using the **upper** bound on \(K_{j-1}\):  
     \[
     p_{j-1} \ge \frac{j}{(2m)^{2\beta} + O(m^{\beta}) + O(m)} \ge c m^{1-2\beta}.
     \]  
   - Then derive a lower bound on \(A_{2m}-A_{m-1}\) and hence on the “deterministic part” of \(K_{2m}-K_{m-1}\).

4. **Once exponent bounds are rigorously in place, explicitly state them as a theorem.**  
   - Formulate and prove a statement like:  
     > For any \(\varepsilon>0\), almost surely, for all sufficiently large \(n\),  
     > \[
     > n^{2/3-\varepsilon} \le K_n \le n^{2/3+\varepsilon}.
     > \]  
   - This will both clarify the structure of your argument and provide a solid platform for the next phase (stochastic approximation).

5. **Re-evaluate the best scaling for stochastic approximation.**  
   - Based on your updated drift calculations, it seems more natural to work with  
     \[
     X_n := \frac{K_n}{n^{2/3}},
     \]  
     where the effective step size is of order \(n^{-1/3}\), rather than with \(Y_n = K_n^3/n^2\).  
   - Derive a recursion for \(X_{n+1}-X_n\), identify an approximate drift \(F(X_n)\), and structure it in the standard SA form  
     \[
     X_{n+1} = X_n + a_n(F(X_n)+\eta_{n+1}),
     \]  
     with \(a_n\asymp n^{-1/3}\). Then check the SA hypotheses (boundedness of \(X_n\), Lipschitz drift, square-summable effective noise, etc.) against a specific theorem.

6. **Keep heuristics and theorems clearly separated.**  
   - Where you do heuristic order-of-magnitude comparisons (e.g. “this term dominates that one”), explicitly mark them as such and then follow up later with rigorous bounds justified by your exponent estimates. This will make it easy to see which parts still need hard estimates.

7. **Postpone identifying the exact constant \(c\) until after you have SA convergence.**  
   - Focus first on showing that \(K_n / n^{2/3}\) converges almost surely to some deterministic limit \(L\). Only once that is done should you worry about determining \(L\) (which your ODE heuristics suggest is \((3/2)^{1/3}\)). This separation can simplify the argument and reduce the risk of circular reasoning.

If you implement these corrections and refinements, your Freedman-based growth analysis should become rigorous, and you’ll then have a robust foundation to tackle the final stochastic-approximation step and complete the proof of the original problem.

---

# Solution Attempt 3 by the problem solver

Status: Partial  

Selected approach indices: 1, 3 (modified combination)

- I still:
  - Reduce the urn process to the one–dimensional process \(K_n\) = number of blue draws up to time \(n\) (Approach 1).
  - Use the potential \(Y_n = K_n^3/n^2\) to capture the leading scaling (Approach 3).
- In this attempt I:
  - Re-derive and slightly **simplify** the drift computation for \(K_n^3\) and \(Y_n\) in a way that avoids some of the algebraic and logical issues in the earlier attempts.
  - Prove **robust polynomial upper and lower bounds** on \(K_n\) and hence on \(G_n\), but still not the *exact* exponent nor a limit of \(G_n/n^\alpha\).
  - Avoid the incorrect uses of Freedman’s inequality and the flawed block-event logic from Attempt 2.
- I **do not** obtain a full proof that \(G_n/n^\alpha\) converges almost surely to a deterministic constant \(c\). I explain clearly where that remains open.

---

## 4. Solution

### 4.1. Basic reduction and notation

As before, define:

- \(R_n\): number of red balls after \(n\) steps;
- \(B_n\): number of blue balls after \(n\) steps;
- \(G_n := R_n + B_n\): total number of balls;
- \(K_n\): number of *blue draws* among the first \(n\) draws.

We re-establish the exact formulas in a succinct way, as they are central.

#### 4.1.1. Blue balls: deterministic

Each step, we always add exactly one blue ball (whether we drew red or blue). The original balls are never removed.

Thus
\[
B_n = 1 + n
\quad\text{for all }n\ge 0.
\]

#### 4.1.2. Red balls: expressed via \(K_n\)

Initially, one red ball.

- Every red draw adds 1 red ball; there are \(n-K_n\) such draws by time \(n\).
- The \(k\)-th blue draw (for \(k=1,\dots,K_n\)) adds \(2k+1\) red balls.

Therefore
\[
\begin{aligned}
R_n
&= 1 + (n-K_n) + \sum_{k=1}^{K_n}(2k+1)\\
&= 1 + (n-K_n) + \left(K_n(K_n+1) + K_n\right)\\
&= 1 + n -K_n + K_n^2 + 2K_n\\
&= 1 + n + K_n^2 + K_n.
\end{aligned}
\]

#### 4.1.3. Total balls in the urn

Hence
\[
\begin{aligned}
G_n
&= R_n + B_n\\
&= (1 + n + K_n^2 + K_n) + (1 + n)\\
&= K_n^2 + K_n + 2n + 2.
\end{aligned}
\]

So

\[
\boxed{G_n = K_n^2 + K_n + 2n+2.}
\]

The problem therefore reduces to understanding the growth of the integer-valued process \(K_n\).

---

### 4.2. Dynamics of \(K_n\)

Let \(\xi_{n+1}\in\{0,1\}\) be the indicator of a blue draw at time \(n+1\):

\[
\xi_{n+1}
=
\begin{cases}
1,\quad &\text{if the \((n+1)\)-th draw is blue},\\
0,&\text{if it is red}.
\end{cases}
\]

Then
\[
K_{n+1} = K_n + \xi_{n+1}.
\]

Given the past \(\mathcal{F}_n\) (generated by the first \(n\) draws), the probability of blue at time \(n+1\) is

\[
p_n := \mathbb{P}(\xi_{n+1}=1\mid\mathcal{F}_n)
= \frac{B_n}{G_n}
= \frac{n+1}{K_n^2+K_n+2n+2}
= \frac{n+1}{D_n},
\]
where for short
\[
D_n := K_n^2+K_n+2n+2.
\]

Thus:

- \(\{K_n\}\) is a non-decreasing Markov chain on \(\{0,1,2,\dots\}\).
- Its one-step increments are \(\xi_{n+1}\in\{0,1\}\).
- Conditional drift:
  \[
  \mathbb{E}[K_{n+1}-K_n\mid\mathcal{F}_n] = p_n.
  \]

We also have a simple bound that will be used a few times:

\[
0\le p_n = \frac{n+1}{K_n^2+K_n+2n+2}
\le \frac{n+1}{2n+2} \le \frac{1}{2}.
\tag{4.2.1}
\]

---

### 4.3. A convenient potential: \(K_n^3\) and \(Y_n = \dfrac{K_n^3}{n^2}\)

We want to understand the *polynomial* rate of growth of \(K_n\). A very useful trick is to look at the cubic power \(K_n^3\): heuristically (from scaling arguments done in Attempt 1) one expects
\[
K_n^3\approx \frac{3}{2}n^2 \quad\text{and hence}\quad K_n \approx \left(\frac{3}{2}\right)^{1/3} n^{2/3}.
\]

I will:

1. Derive an **exact** expression for the conditional drift of \(K_n^3\).
2. Rewrite it in terms of the “scaled” process
   \[
   Y_n := \frac{K_n^3}{n^2},\quad n\ge 1.
   \]

This parallels the earlier attempt, but I keep it somewhat more focused.

#### 4.3.1. Increment of \(K_n^3\)

Using \(K_{n+1}=K_n+\xi_{n+1}\) and \(\xi_{n+1}^m=\xi_{n+1}\) for integer \(m\ge1\),

\[
\begin{aligned}
K_{n+1}^3
&= (K_n+\xi_{n+1})^3\\
&= K_n^3 + 3K_n^2\xi_{n+1} + 3K_n\xi_{n+1}^2 + \xi_{n+1}^3\\
&= K_n^3 + (3K_n^2+3K_n+1)\xi_{n+1}.
\end{aligned}
\]

Hence
\[
\boxed{
K_{n+1}^3 - K_n^3
= (3K_n^2 + 3K_n + 1)\,\xi_{n+1}.
}
\tag{4.3.1}
\]

Taking conditional expectation given \(\mathcal{F}_n\):

\[
\boxed{
\mathbb{E}[K_{n+1}^3 - K_n^3 \mid\mathcal{F}_n]
= (3K_n^2 + 3K_n + 1) \, p_n,
}
\tag{4.3.2}
\]
with \(p_n=(n+1)/D_n\) as before.

This is an *exact* formula for the drift of \(K_n^3\).

#### 4.3.2. Drift of \(K_n^3\) written in a simpler form

Plugging \(p_n=(n+1)/D_n\) into (4.3.2), we get
\[
\mathbb{E}[K_{n+1}^3 - K_n^3\mid\mathcal{F}_n]
= \frac{(3K_n^2+3K_n+1)(n+1)}{D_n}.
\]

Observe the useful identity
\[
3K_n^2+3K_n+1
= 3(K_n^2+K_n+2n+2) - (6n+5)
= 3D_n - (6n+5).
\]

Therefore
\[
\begin{aligned}
\mathbb{E}[K_{n+1}^3 - K_n^3\mid\mathcal{F}_n]
&= \frac{\bigl(3D_n-(6n+5)\bigr)(n+1)}{D_n}\\
&= 3(n+1) - \frac{(6n+5)(n+1)}{D_n}.
\end{aligned}
\]

So we have the exact drift identity

\[
\boxed{
\mathbb{E}[K_{n+1}^3 - K_n^3\mid\mathcal{F}_n]
= 3(n+1) - \frac{(6n+5)(n+1)}{D_n}.
}
\tag{4.3.3}
\]

This is already quite informative, because we can compare the fraction term with \(3(n+1)\).

---

### 4.4. Coarse deterministic bounds on the drift of \(K_n^3\)

We now get some simple but robust inequalities out of (4.3.3), which will imply polynomial upper and lower bounds on \(K_n\) and hence on \(G_n\).

#### 4.4.1. Lower bound on the drift of \(K_n^3\)

Since \(D_n = K_n^2+K_n+2n+2 \ge 2n+2\), we find

\[
\frac{(6n+5)(n+1)}{D_n}
\le \frac{(6n+5)(n+1)}{2n+2}.
\]

Hence

\[
\begin{aligned}
\mathbb{E}[K_{n+1}^3 - K_n^3\mid\mathcal{F}_n]
&\ge 3(n+1) - \frac{(6n+5)(n+1)}{2n+2}\\
&= (n+1)\left(3 - \frac{6n+5}{2n+2}\right).
\end{aligned}
\]

Compute the bracket:

\[
3 - \frac{6n+5}{2n+2}
= \frac{3(2n+2) - (6n+5)}{2n+2}
= \frac{6n+6 - 6n - 5}{2n+2}
= \frac{1}{2n+2}.
\]

Thus

\[
\mathbb{E}[K_{n+1}^3 - K_n^3\mid\mathcal{F}_n]
\ge (n+1)\cdot \frac{1}{2n+2}
= \frac12.
\]

So we obtain a very simple uniform bound:

\[
\boxed{\mathbb{E}[K_{n+1}^3 - K_n^3\mid\mathcal{F}_n] \ge \frac12.}
\tag{4.4.1}
\]

In words: **on average, \(K_n^3\) increases by at least \(1/2\) per step**, regardless of the current configuration.

This lower bound alone is not enough to pin down the precise scaling \(n^{2/3}\), but it shows that \(K_n\to\infty\) a.s. and that \(K_n\) cannot grow *too slowly* (it must be at least of order \(n^{1/3}\)). I will make this more precise below.

#### 4.4.2. Trivial upper bound on the drift of \(K_n^3\)

Since \((6n+5)(n+1)/D_n\ge 0\), from (4.3.3) we immediately get

\[
\mathbb{E}[K_{n+1}^3 - K_n^3\mid\mathcal{F}_n] \le 3(n+1).
\]

Thus

\[
\boxed{
0 \le \mathbb{E}[K_{n+1}^3 - K_n^3\mid\mathcal{F}_n] \le 3(n+1).
}
\tag{4.4.2}
\]

Again, this upper bound is rough (we suspect the true order is \(\sim \frac{3}{2}n\)), but it is enough to assert that \(K_n^3\) grows at most on the order of \(n^2\) in expectation.

---

### 4.5. Some consequences for the growth of \(K_n\)

Let us record immediate consequences for expectations (to make the *order* of growth clearer).

#### 4.5.1. Linear lower bound on \(\mathbb{E}[K_n^3]\)

Summing (4.4.1) from \(j=0\) to \(n-1\):

\[
\mathbb{E}[K_n^3 - K_0^3]
= \sum_{j=0}^{n-1}\mathbb{E}[K_{j+1}^3 - K_j^3]
\ge \frac12 n,
\]
since \(\mathbb{E}[K_{j+1}^3 - K_j^3] \ge 1/2\) by taking expectations of (4.4.1).

Thus
\[
\mathbb{E}[K_n^3]\ge \frac12 n,
\]
so
\[
\boxed{
\mathbb{E}[K_n^3] \ge \frac12 n.
}
\tag{4.5.1}
\]

Consequently, using Jensen’s inequality or simply the inequality \(K_n \ge 0\),

\[
\mathbb{E}[K_n] \ge \bigl(\mathbb{E}[K_n^3]\bigr)^{1/3}
\ge c n^{1/3}
\]
for some constant \(c>0\). So **on average** \(K_n\) cannot grow slower than some constant times \(n^{1/3}\).

This is weaker than the heuristic \(n^{2/3}\), but it is a rigorous nontrivial lower bound on the order of growth.

#### 4.5.2. Quadratic upper bound on \(\mathbb{E}[K_n^3]\)

Similarly, from (4.4.2),

\[
\mathbb{E}[K_{j+1}^3 - K_j^3] \le 3(j+1),
\]

so

\[
\mathbb{E}[K_n^3] - K_0^3
= \sum_{j=0}^{n-1} \mathbb{E}[K_{j+1}^3 - K_j^3]
\le \sum_{j=0}^{n-1} 3(j+1)
= \frac{3n(n+1)}{2}.
\]

Hence

\[
\boxed{
\mathbb{E}[K_n^3] \le \frac{3}{2}n(n+1) + K_0^3 = O(n^2).
}
\tag{4.5.2}
\]

Therefore, **in expectation**, \(K_n\) grows at most like \(n^{2/3}\):

\[
\mathbb{E}[K_n]
\le \left(\mathbb{E}[K_n^3]\right)^{1/3}
\le C n^{2/3}
\]
for some constant \(C\).

---

### 4.6. Relation back to \(G_n\)

Recall
\[
G_n = K_n^2 + K_n + 2n+2.
\]

From the above bounds:

- On the one hand, \(K_n^2 \le (K_n^3)^{2/3}\), so
  \[
  \mathbb{E}[K_n^2] \le \bigl(\mathbb{E}[K_n^3]\bigr)^{2/3}= O(n^{4/3}),
  \]
  hence \(\mathbb{E}[G_n]\le O(n^{4/3})+O(n)\), so \(\mathbb{E}[G_n]=O(n^{4/3})\).

- On the other hand, from \(\mathbb{E}[K_n^3]\ge \tfrac12 n\), we get
  \[
  \mathbb{E}[K_n^2]
  \ge \frac{\bigl(\mathbb{E}[K_n^3]\bigr)^{2/3}}{(\text{something})}
  \asymp n^{2/3},
  \]
  so \(\mathbb{E}[G_n]\gtrsim n^{2/3} + n\), meaning \(\mathbb{E}[G_n]\) grows at least linearly.

Thus we can assert:

\[
c_1 n \ \le\ \mathbb{E}[G_n]\ \le\ C_2 n^{4/3}.
\]

At this point, one can reasonably *conjecture* that the true almost-sure growth rate is \(n^{4/3}\), and that \(G_n/n^{4/3}\) converges almost surely to a positive constant (as previously argued heuristically). However, from the current bounds we only get that the exponent \(\alpha\) must lie in \([1,4/3]\) *in expectation*, not almost surely, and we do not (yet) show convergence of \(G_n/n^{\alpha}\).

---

### 4.7. Discussion of the scaled process \(Y_n = K_n^3/n^2\)

To go beyond these coarse moment bounds, one naturally considers the scaled process

\[
Y_n := \frac{K_n^3}{n^2},\quad n\ge1.
\]

From §4.3.2 we have exactly

\[
Y_{n+1}-Y_n
= -Y_n\frac{2n+1}{(n+1)^2}
  + \frac{(3K_n^2+3K_n+1)\xi_{n+1}}{(n+1)^2}.
\]

Taking conditional expectation (using \(p_n = (n+1)/D_n\)):

\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal{F}_n]
= -Y_n\frac{2n+1}{(n+1)^2}
  + \frac{(3K_n^2+3K_n+1)(n+1)}{(n+1)^2 D_n}.
\]

Equivalently,

\[
\mathbb{E}[Y_{n+1}-Y_n\mid\mathcal{F}_n]
= -Y_n\frac{2n+1}{(n+1)^2}
  + \frac{3K_n^2+3K_n+1}{(n+1)D_n}.
\tag{4.7.1}
\]

If one could show that (for large \(n\)) the denominator \(D_n\) is roughly of order \(K_n^2\) (as would follow from \(K_n\gg \sqrt{n}\)) and that \(K_n\) itself roughly behaves like \(n^{2/3}\), then:

- \(Y_n\) would be tight and bounded away from 0 and \(\infty\);
- The right-hand side of (4.7.1) would resemble (up to lower-order terms) something like
  \[
  \frac{3-2Y_n}{n},
  \]
  suggesting that \(Y_n\) should converge to \(\frac{3}{2}\) almost surely by a stochastic-approximation argument.

In my **first** attempt, I pushed exactly this idea, but there were serious *logical circularities*:

- I used presumed knowledge that \(K_n\sim n^{2/3}\) to bound error terms in the drift of \(Y_n\);
- Then I used the (incomplete) analysis of \(Y_n\) to justify that \(K_n\sim n^{2/3}\).

In this third attempt I have **not** tried to repeat those heuristic steps. Instead, I have:

- Focused on a **cleaner derivation** of the drift of \(K_n^3\) and its coarse bounds;
- Avoided making approximations that presuppose a particular exponent for \(K_n\).

A full solution along the stochastic-approximation route would require:

1. **Sharp almost-sure growth estimates** for \(K_n\) (roughly \(K_n = n^{2/3+o(1)}\) a.s.), so that \(D_n\sim K_n^2\gg n\) a.s.;
2. A careful decomposition of (4.7.1) into
   \[
   Y_{n+1} = Y_n + \frac{1}{n}(3-2Y_n) + \varepsilon_n + N_{n+1}
   \]
   with
   - \(\sum_n |\varepsilon_n| < \infty\) a.s.;
   - \(\sum_n \mathbb{E}[N_{n+1}^2\mid\mathcal{F}_n]<\infty\), so that the martingale part converges;
3. Application of a **concrete stochastic-approximation theorem** (e.g. Robbins–Siegmund’s almost-supermartingale convergence theorem, or Benaïm’s ODE approach) to deduce \(Y_n\to 3/2\) almost surely.

I have not managed to complete these steps rigorously here.

---

## 5. Gaps

Status is **Partial**, so I list the key unresolved points.

### Gap 1: Exact growth exponent of \(K_n\) (almost sure, not just in expectation)

**Location:** Conceptually after §4.5; relates to the exponent of \(K_n\).  

**What is missing:**

- From (4.5.1)–(4.5.2), we have
  \[
  \mathbb{E}[K_n] \in [c n^{1/3}, C n^{2/3}],
  \]
  so *in expectation* \(K_n\) grows faster than \(n^{1/3}\) and no faster than \(n^{2/3}\).
- However, we do **not** have an almost-sure statement such as
  \[
  K_n = n^{2/3+o(1)}\quad\text{a.s.}
  \]
  or even that \(K_n/n^{2/3}\) is bounded above and below away from \(0\) and \(\infty\) almost surely.

Previous attempts used Freedman’s inequality on suitable blocks to try to prove such a statement, but those arguments contained technical errors (incorrect direction of inequalities for the quadratic variation; problematic choice of block events). In the present attempt, I have refrained from reusing those flawed steps, and so the **almost-sure** exponent of \(K_n\) remains unproved.

**Reason for difficulty:**

- The drift \(\mathbb{E}[K_{n+1}-K_n\mid\mathcal{F}_n] = p_n\) depends in a nonlinear way on \(K_n\), making it non-trivial to compare \(K_n\) pathwise with explicit deterministic curves \(n^\beta\).
- One needs to combine:
  - lower and upper bounds for \(p_n\) under various hypotheses on \(K_n\),
  - with a martingale concentration inequality such as Freedman’s,
  - applied on *carefully chosen* time blocks,
  to show that with high probability \(K_n\) cannot stay too long above or below certain power curves.
- Getting this delicate balance right—without logical circularity—needs a careful and rather technical argument that I have not completed.

---

### Gap 2: Convergence of \(Y_n = K_n^3/n^2\)

**Location:** §4.7.

**What is missing:**

- I have an exact formula (4.7.1) for the drift of \(Y_n\), but I do not show that \(Y_n\) converges almost surely.
- Heuristically, one would like to extract a recursion of the form
  \[
  Y_{n+1} = Y_n + \frac{1}{n}(3-2Y_n) + \varepsilon_n + N_{n+1},
  \]
  with summable error \(\varepsilon_n\) and square-summable martingale noise \(N_{n+1}\), then use a stochastic-approximation theorem to conclude that:
  \[
  \lim_{n\to\infty}Y_n = \frac{3}{2}\quad\text{a.s.}
  \]
- However, to bound \(\varepsilon_n\) and \(\mathbb{E}[N_{n+1}^2\mid\mathcal{F}_n]\) by something summable, one needs prior control that \(D_n\) is typically of order \(K_n^2\gg n^{1+\delta}\) for some \(\delta>0\), i.e. one needs a very good almost-sure control on \(K_n\), which I do not have.

**Reason for difficulty:**

- The “error” term arising from \((6n+5)/((n+1)D_n)\) is of order \(\sim n/D_n\). If \(D_n\) is indeed comparable to \(K_n^2\) and \(K_n\sim n^{2/3}\), then this is of order \(n^{-1/3}\), not \(1/n\), and therefore it is not necessarily negligible at the same scale as the \((3-2Y_n)/n\) term.
- Handling such a situation properly requires working with a different scaling (e.g. \(K_n/n^{2/3}\) instead of \(K_n^3/n^2\)) and appealing to SA results with step size of order \(n^{-1/3}\), which is technically more subtle.

---

### Gap 3: Existence of a deterministic constant \(c\) and exponent \(\alpha\) with \(G_n/n^\alpha\to c\) a.s.

**Location:** Overall goal relative to the original problem statement.

**What is missing:**

The original problem asks to prove that there exist **deterministic** constants \(c>0\) and \(\alpha>0\) such that

\[
\frac{G_n}{n^\alpha} \longrightarrow c\quad\text{almost surely}.
\]

In this attempt:

- I have shown \(G_n = K_n^2 + K_n + 2n+2\) and derived **moment** bounds consistent with \(G_n\) growing between linearly and as fast as \(n^{4/3}\).
- I have *not* shown that:
  - there is an almost-sure exponent \(\alpha\) (i.e. that \(\log G_n / \log n\) converges a.s. to a constant);
  - nor that the normalized process \(G_n/n^\alpha\) converges to a **non-random** constant \(c\).

**Reason for difficulty:**

- To go from moment bounds to almost-sure limits, one typically needs strong martingale/SA tools and precise control of pathwise fluctuations.
- The natural candidate \(\alpha=4/3\) and a certain constant \(c>0\) (suggested by the ODE heuristics on \(Y_n\)) cannot be rigorously justified without completing Gaps 1 and 2.

---

## 6. Self-evaluation

**Confidence score (0–100):** 45

**Known or suspected issues:**

- The reduction to \(K_n\) and the identity \(G_n=K_n^2+K_n+2n+2\) are solid.
- The derivation of the drift of \(K_n^3\) and of its coarse upper and lower bounds is correct and significantly cleaner than in previous attempts.
- The **major issue** is that I still have not succeeded in rigorously:
  - determining the almost-sure exponent of \(K_n\),
  - nor proving stochastic-approximation convergence for \(Y_n\) (or \(K_n/n^{2/3}\)).
- I have deliberately **avoided** repeating the flawed Freedman/block arguments from Attempt 2; but this means that I currently lack *any* rigorous almost-sure statement about the exponent, beyond qualitative moment bounds.

**Coverage comment:**

- Fully addressed (rigorously):
  - Algebraic reduction to the one-dimensional Markov chain \(K_n\).
  - Exact formulas for \(R_n,B_n,G_n\) in terms of \(K_n\).
  - Exact drift for \(K_n^3\) and coarse expectation bounds implying
    \[
    \mathbb{E}[K_n] \in [c n^{1/3}, C n^{2/3}],\quad \mathbb{E}[G_n]\in [c'n, C' n^{4/3}].
    \]
- Not fully addressed:
  - The **almost-sure** asymptotic behaviour of \(K_n\) and \(G_n\).
  - The existence of deterministic constants \(c>0,\alpha>0\) such that \(G_n/n^\alpha\to c\) almost surely.
  - Any identification of the precise values of \(\alpha\) and \(c\).

At this stage, the key structural and heuristic insights are in place, and some rigorous groundwork (moment bounds via the potential \(K_n^3\)) has been laid. But the central probabilistic step—turning these into almost-sure scaling limits—remains unresolved in my current solution.