You are an expert solver of challenging math problems.

Write out detailed solutions to the math problems posed.

---

Let $\mathbb{T} = \mathbb{R}/\mathbb{Z}$ be the circle. Does there exist a homeomorphism

$$\varphi : \mathbb{T} \to \mathbb{T}$$

such that $\varphi$ is *singular* (that is, its derivative is $0$ almost everywhere) but the map

$$f : \mathbb{T} \to \mathbb{T},\quad f(x) = \varphi^{-1}(2 \cdot \varphi(x)),$$

is absolutely continuous?

---

Yes.

A concrete way to do it is to choose an absolutely continuous **“skewed doubling map”** \(f\) (piecewise linear, hence absolutely continuous) and then take \(\varphi\) to be the (unique up to the trivial centralizer) topological conjugacy sending \(f\) to the usual doubling map. For \(p\neq \tfrac12\) this conjugacy is a classical **singular increasing homeomorphism** (its derivative is \(0\) a.e.).

Below is a fully explicit construction and verification.

---

## 1) Work on \([0,1]\) and pass to \(\mathbb T=\mathbb R/\mathbb Z\)

Identify \(\mathbb T\) with \([0,1)\) modulo \(1\).  
Let \(D:\mathbb T\to\mathbb T\) be the doubling map
\[
D(y)=2y \pmod 1.
\]

Fix a parameter
\[
p\in(0,1),\qquad p\neq \tfrac12.
\]

Define a degree–\(2\) circle map \(f_p:\mathbb T\to\mathbb T\) by giving a lift \(F_p:\mathbb R\to\mathbb R\) with \(F_p(x+1)=F_p(x)+2\). On \([0,1]\) set
\[
F_p(x)=
\begin{cases}
\dfrac{x}{p}, & 0\le x\le p,\\[6pt]
1+\dfrac{x-p}{1-p}, & p\le x\le 1.
\end{cases}
\]
Then define \(f_p(x)=F_p(x)\pmod 1\).

### Why \(f_p\) is absolutely continuous
The lift \(F_p\) is piecewise linear on \([0,1]\), hence Lipschitz, hence absolutely continuous. Therefore \(f_p\) is absolutely continuous on \(\mathbb T\) (in the standard sense: it has an absolutely continuous lift).

So if we can produce a **singular** circle homeomorphism \(\varphi\) with
\[
f_p=\varphi^{-1}\circ D\circ \varphi,
\]
we are done (then the map \(f\) in your question is exactly \(f_p\), absolutely continuous).

---

## 2) Construct the conjugacy \(\varphi\) explicitly from itineraries

Let the “Markov partition” for \(f_p\) be
\[
I_0=[0,p),\qquad I_1=[p,1).
\]
For \(x\in[0,1)\) define its itinerary (binary digit sequence)
\[
\varepsilon_n(x)=
\begin{cases}
0,& f_p^{n-1}(x)\in I_0,\\
1,& f_p^{n-1}(x)\in I_1,
\end{cases}
\qquad n=1,2,3,\dots
\]

Now define
\[
\varphi(x)=\sum_{n=1}^\infty \frac{\varepsilon_n(x)}{2^n}\in[0,1].
\]
Interpret the right side as the binary number whose digits are \(\varepsilon_1(x)\varepsilon_2(x)\varepsilon_3(x)\dots\).

There is the usual issue that dyadic rationals have two binary expansions (ending in all \(0\)’s or all \(1\)’s). One can choose a consistent convention (e.g. always take the expansion not ending in all \(1\)’s) and define \(\varphi\) on the corresponding countable set of boundary points accordingly. This gives a well-defined continuous, strictly increasing map \([0,1]\to[0,1]\) with \(\varphi(0)=0\), \(\varphi(1)=1\); hence a homeomorphism of the circle \(\mathbb T\).

### Verify the conjugacy equation
Observe that applying \(f_p\) shifts the itinerary:
\[
\varepsilon_n(f_p(x))=\varepsilon_{n+1}(x).
\]
Therefore
\[
\varphi(f_p(x))
=\sum_{n=1}^\infty \frac{\varepsilon_n(f_p(x))}{2^n}
=\sum_{n=1}^\infty \frac{\varepsilon_{n+1}(x)}{2^n}
=2\sum_{n=1}^\infty \frac{\varepsilon_{n+1}(x)}{2^{n+1}}
\equiv 2\varphi(x)\pmod 1.
\]
But \(2\varphi(x)\pmod 1\) is exactly \(D(\varphi(x))\). Thus
\[
\boxed{\ \varphi\circ f_p = D\circ \varphi\ }.
\]
Equivalently,
\[
\boxed{\ f_p=\varphi^{-1}\circ D\circ\varphi\ }.
\]

So \(f\) in your question, defined by \(f(x)=\varphi^{-1}(2\varphi(x))\), is exactly this absolutely continuous map \(f_p\).

What remains is to show that \(\varphi\) is **singular**, i.e. \(\varphi'(x)=0\) for Lebesgue-a.e. \(x\).

---

## 3) Show \(\varphi'(x)=0\) for Lebesgue-a.e. \(x\)

### (a) Cylinder intervals and their lengths
Fix \(x\) not on the boundary of any cylinder (this excludes a countable set).  
For each \(n\), let \(C_n(x)\) be the length-\(n\) cylinder interval of points having the same first \(n\) itinerary digits as \(x\):
\[
C_n(x)=\{y:\varepsilon_1(y)=\varepsilon_1(x),\dots,\varepsilon_n(y)=\varepsilon_n(x)\}.
\]
For this piecewise linear full-branch map, each inverse branch scales lengths by a fixed factor: if you follow digit \(0\) you scale by \(p\), and if you follow digit \(1\) you scale by \(1-p\). Hence
\[
|C_n(x)| = p^{k_n(x)}(1-p)^{n-k_n(x)},
\]
where \(k_n(x)\) is the number of zeros among \(\varepsilon_1(x),\dots,\varepsilon_n(x)\).

Meanwhile, by construction, \(\varphi\) maps \(C_n(x)\) onto the dyadic interval of length \(2^{-n}\) corresponding to that binary word, so
\[
|\varphi(C_n(x))| = 2^{-n}.
\]

### (b) Derivative as a limit of ratios
Since \(\varphi\) is increasing, at points of differentiability one can compute the derivative by shrinking nested intervals:
\[
\varphi'(x) = \lim_{n\to\infty}\frac{|\varphi(C_n(x))|}{|C_n(x)|}
= \lim_{n\to\infty}\frac{2^{-n}}{p^{k_n(x)}(1-p)^{n-k_n(x)}}.
\]

So it suffices to understand the asymptotics of \(k_n(x)\) for Lebesgue-a.e. \(x\).

### (c) Under Lebesgue measure, itinerary digits are i.i.d. with bias \(p\)
Because the \(n\)-cylinder lengths are exactly
\[
|C_n|=p^{\#0}(1-p)^{\#1},
\]
the Lebesgue measure of the set of points with a given length-\(n\) word \(w\) equals \(p^{\#0(w)}(1-p)^{\#1(w)}\). This is exactly the Bernoulli product law with parameter \(p\): under Lebesgue, the digits \(\varepsilon_n(x)\) behave like independent draws with
\[
\mathbb P(\varepsilon_n=0)=p,\qquad \mathbb P(\varepsilon_n=1)=1-p.
\]
Hence by the strong law of large numbers,
\[
\frac{k_n(x)}{n}\longrightarrow p
\quad\text{for Lebesgue-a.e. }x.
\]

### (d) Conclude \(\varphi'(x)=0\) a.e.
Take such an \(x\). Then asymptotically
\[
p^{k_n(x)}(1-p)^{n-k_n(x)}
\approx \bigl(p^p(1-p)^{1-p}\bigr)^n,
\]
so
\[
\frac{2^{-n}}{p^{k_n(x)}(1-p)^{n-k_n(x)}}
\approx
\left(\frac{1}{2\,p^p(1-p)^{1-p}}\right)^n.
\]
Now use the strict entropy inequality: for \(p\neq \tfrac12\),
\[
p^p(1-p)^{1-p}>\tfrac12.
\]
(Equivalently, \(-p\log p -(1-p)\log(1-p) < \log 2\), i.e. the binary entropy is maximized at \(p=\tfrac12\).)

Therefore
\[
\frac{1}{2\,p^p(1-p)^{1-p}}<1,
\]
and the ratio tends to \(0\). Hence
\[
\boxed{\ \varphi'(x)=0\ \text{for Lebesgue-a.e. }x\ }.
\]
So \(\varphi\) is singular.

---

## 4) Put it together

- \(\varphi:\mathbb T\to\mathbb T\) is a homeomorphism and is singular (\(\varphi'=0\) a.e.).
- The map
  \[
  f(x)=\varphi^{-1}(2\varphi(x))
  \]
  equals \(f_p\), whose lift \(F_p\) is piecewise linear, hence absolutely continuous.

Therefore, **such a \(\varphi\) exists**.

---

## 5) A succinct explicit choice

Take, for instance, \(p=\tfrac13\). Then \(f=f_{1/3}\) has lift
\[
F(x)=
\begin{cases}
3x, & 0\le x\le \tfrac13,\\[4pt]
1+\tfrac32(x-\tfrac13), & \tfrac13\le x\le 1,
\end{cases}
\]
extended by \(F(x+1)=F(x)+2\). This is absolutely continuous.

Let \(\varphi(x)\) be the binary number whose digits record whether successive iterates of \(x\) under \(f\) fall in \([0,\tfrac13)\) or \([\tfrac13,1)\). Then \(\varphi\) is a singular homeomorphism and satisfies \(f=\varphi^{-1}\circ D\circ\varphi\).

---

If you want, I can also rewrite the construction directly on \(\mathbb T\) with lifts and show continuity at the identified points \(0\sim 1\) and at the break point \(p\), but the essential idea is exactly the skewed doubling map and its (singular) itinerary conjugacy to the standard doubling map.