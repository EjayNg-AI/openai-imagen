## Possibly helpful URLs and citations

- URLs:
  - https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai
  - https://www.ams.org/journals/proc/2024-152-07/S0002-9939-2024-16738-1/?utm_source=openai
  - https://annals.math.princeton.edu/2020/192-3/p04?utm_source=openai
  - https://www.cambridge.org/core/journals/compositio-mathematica/article/integral-chow-ring-of-mathcal-m0mathbb-pr-d-for-d-odd/1C80394BE55BE39BA69B776F8CDD87B0

- Academic citations:
  - Khovanskii–Teissier/Alexandrov–Fenchel log-concavity for mixed intersections of nef divisors.
  - Hodge–Riemann/Lorentzian-polynomial perspective on volume polynomials.
  - Nefness of \(\psi_i\) (e.g., Gibney–Keel–Morrison 2002, Arakelov/Mumford).
  - Lazarsfeld, *Positivity in Algebraic Geometry* (KT/Hodge index).
  - Edidin (operational Chow isomorphism), Vistoli/Kresch stack–coarse comparisons.

- URLs:
  - https://eudml.org/doc/143716?utm_source=openai
  - https://academic.oup.com/qjmath/article/71/1/247/5709654?utm_source=openai
  - https://arxiv.org/abs/2502.13099?utm_source=openai
  - https://en.wikipedia.org/wiki/Keel%E2%80%93Mori_theorem?utm_source=openai
  - https://ar5iv.org/pdf/2004.02749
  - https://www.ams.org/jag/2012-21-02/S1056-3911-2011-00606-1/?utm_source=openai

- Academic citations:
  - Keel–Mori coarse-moduli theorem.
  - Vistoli’s “Intersection theory on algebraic stacks and on their moduli spaces.”
  - Khovanskii–Teissier/Alexandrov–Fenchel inequality (classical KT sources; Khovanskii preprint).
  - Nefness references for \(\psi_i\) (Cornalba–Harris/Arbarello–Cornalba; Gibney–Keel–Morrison).
  - Positivity of Witten–Kontsevich correlators (Delecroix–Goujard–Zograf–Zorich; Kontsevich ribbon-graph/Strebel framework).
  - DVV/Witten–Kontsevich recursion; Lazarsfeld’s *Positivity in Algebraic Geometry*.

- URLs:
  - https://ar5iv.org/pdf/math/0006208
  - https://mathoverflow.net/questions/204701/do-line-bundles-descend-to-coarse-moduli-spaces-of-artin-stacks-with-finite-iner

- Academic citations:
  - Kresch’s quotient-stack theorem; Edidin on Chow groups of quotient stacks.
  - Gibney–Keel–Morrison “Towards the ample cone of \(\overline M_{g,n}\)” (nefness of \(\psi_i\)).
  - Descent of line bundles to coarse moduli spaces (torsion Picard cokernel).
  - Alexandrov–Fenchel/Khovanskii–Teissier inequality for nef divisors.
  - Hardy–Littlewood–Pólya majorization.
  - Intersection-theory foundations: Vistoli/Kresch/Edidin–Graham/Fulton for stack → coarse → resolution.

---

## Major issues (load-bearing; should be fixed before final write-up)

### 1) Missing explicit, exam-grade citation for **nefness of each \(\psi_i\)**  
- **Location in Attempt 4:**  
  - §4 **Fact 4.1 (nefness of \(\psi_i\))**  
  - Used again in §6.1 (KT inequality requires nefness), and indirectly throughout the transfer inequality argument.
- **Issue:**  
  Attempt 4 states nefness as “standard” but does not provide a **specific** reference (author/title/theorem/section) establishing that **each cotangent line bundle \(L_i\)** (equivalently \(\psi_i=c_1(L_i)\)) is nef on \(\overline{\mathcal M}_{g,n}\) (or on the coarse space).
- **Why it matters:**  
  The KT/Alexandrov–Fenchel step is only valid under the nef hypothesis. A strict reader will not accept “standard” here.
- **How to fix it (recommended patch):**
  1. Replace “one may cite a standard nefness reference” with an explicit citation, e.g. something in the standard birational geometry / nef cone literature on \(\overline M_{g,n}\).
  2. Add one sentence: “Pullback of nef divisors is nef”, to justify nefness on \(\widetilde X\).
- **Reference suggestions (what to cite / look for):**
  - A very standard place to anchor “\(\psi\) is nef” in the \(\overline M_{g,n}\) nef-cone literature is **Gibney–Keel–Morrison**, *Towards the ample cone of \(\overline M_{g,n}\)* (JAMS 2002). In the arXiv HTML rendering, they explicitly remark that “\(\psi\) is nef” when contrasting \(\psi\) with boundary divisors. ([ar5iv.org](https://ar5iv.org/pdf/math/0006208))  
    **Action item:** verify in the published version / PDF the exact statement: is it “\(\psi_i\) is nef” for all \(i\), or their symmetric \(\psi\)-combination? If it is only the symmetric class, you still need a source that states nefness for each \(i\).
  - If GKM only states nefness for a symmetric \(\psi\), then you should look for a reference that states explicitly:  
    > “Each \(L_i\) (cotangent line bundle) is nef on \(\overline{\mathcal M}_{g,n}\).”  
    Typical “right kinds” of sources: standard moduli-of-curves references (Arbarello–Cornalba / Harris–Morrison style) or a paper explicitly proving nefness of tautological line bundles on \(\overline M_{g,n}\).  
    **Search terms to locate a precise theorem:** “cotangent line bundle \(L_i\) nef \(\overline{M}_{g,n}\)”, “\(\psi_i\) nef divisor \(\overline{\mathcal M}_{g,n}\)”.

---

### 2) Positivity lemma is conceptually right but still citation-light (“Kontsevich ribbon graph positivity”)  
- **Location in Attempt 4:**  
  - §5 **Lemma 5.1 (strict positivity for \(n>0\))**, justification paragraph.
  - Used in §6.2 (positivity \(a_k>0\)) and §7 (unimodality lemma requires positivity).
- **Issue:**  
  The argument says (paraphrasing) “Kontsevich expresses correlators as sums/integrals of positive contributions over ribbon-graph cells; hence \(D(\mathbf e)>0\)”. This is plausible, but without a precise theorem/section/formula it remains non-exam-grade.
- **Why it matters:**  
  Positivity is the **key** hypothesis that prevents internal zeros and justifies the discrete unimodality step; this was the big blocker in Attempt 1. You don’t want the fix to be “folklore”.
- **How to fix it (two good options):**
  **Option A (cleanest for an exam):** Revert to a modern theorem that explicitly gives a **positive lower bound** for every correlator, hence strict positivity immediately.
  - E.g. Delecroix–Goujard–Zograf–Zorich (*Uniform Lower Bound for Intersection Numbers of \(\psi\)-Classes*, SIGMA 2020; also on arXiv). ([sigma-journal.com](https://sigma-journal.com/2020/086/?utm_source=openai))  
  Then add 1–2 sentences explicitly: “Their bound is a strictly positive expression for every stable \((g,n)\) and every ordered partition \((e_1,\dots,e_n)\) of \(3g-3+n\); hence \(D(\mathbf e)>0\).”
  
  **Option B (primary-source style):** Keep Kontsevich/ribbon graphs, but cite the exact place and extract the positivity in 2–4 lines.
  - You’d want to cite *Kontsevich, “Intersection theory on the moduli space of curves and the matrix Airy function”* and point to the explicit ribbon-graph/Feynman expansion formula for correlators (or to an expository source that states the “sum over ribbon graphs with positive weights” formula).
- **What to cite / what to look for:**
  - If you want a **single definitive citation**, DGZZ is ideal because it is literally a “uniform lower bound” paper, and lower bound \(\Rightarrow\) positivity is immediate. ([sigma-journal.com](https://sigma-journal.com/2020/086/?utm_source=openai))  
  - If you prefer Kontsevich/Mirzakhani volume interpretations, look for a theorem explicitly stating: “intersection numbers are coefficients of a volume polynomial / sum over ribbon graphs with positive weights,” then conclude coefficients \(>0\).

---

## Minor issues (polish / citation granularity / small technical clarifications)

### 3) Vistoli/Fulton “bridge lemmas” are structurally correct but need **pinpoint citations**  
- **Location in Attempt 4:**  
  - §3 Lemma 3.1 (tensor-power descent of \(L_i\))  
  - §3 Lemma 3.2 (degree comparison \(\deg_{\mathcal X}(p^*\alpha)=\deg_X(\alpha)\))  
  - §3 Lemma 3.3 (operational Chow + projection formula through resolution)
- **Issue:**  
  The bridge is now well-designed, but it still cites “Vistoli proves…” without theorem/proposition identifiers, and it references Fulton operational Chow without a pinpoint.
- **Why it matters:**  
  This is the only place where a strict reader might say “OK, but *where exactly*?” The evaluator explicitly asked for theorem/section numbers.
- **How to fix it:**
  - For each lemma, add one parenthetical like:  
    “(See Vistoli, Invent. Math. 97 (1989), §… Proposition …)” and  
    “(See Fulton, *Intersection Theory*, §… on operational Chow rings and projection formula).”
  - Alternatively (often acceptable), cite the **Stacks Project literature guide** summary of what Vistoli proves, then cite Vistoli itself for full details.
- **Reference suggestions:**
  - The Stacks Project explicitly summarizes Vistoli’s result that for a DM stack with a moduli space morphism, the induced pushforward on Chow groups is an isomorphism (with \(\mathbb Q\)-coefficients). ([stacks.math.columbia.edu](https://stacks.math.columbia.edu/tag/03B6?utm_source=openai))  
  This is not a replacement for citing Vistoli in a research write-up, but it’s a good “navigation beacon” and helps justify the claimed package.

---

### 4) KT inequality citation should specify the **exact form** used (and ideally theorem number)  
- **Location in Attempt 4:**  
  - §6.1 (“A standard reference is Lazarsfeld…”)
- **Issue:**  
  The write-up says KT gives log-concavity but doesn’t pin down the exact theorem/corollary used.
- **How to fix it:**
  - State explicitly the “\(2\times2\)” Teissier inequality you use (or the standard log-concavity consequence) and cite a theorem number.
  - In Lazarsfeld, the relevant part is in **Positivity I, §1.6** (Hodge-type inequalities / Khovanskii–Teissier). A PDF excerpt indicates this appears as Theorem 1.6.1 (“Generalized inequality of Hodge type”). ([scribd.com](https://www.scribd.com/document/705024715/Lazarsfeld-Positivity-in-Algebraic-Geometry-I?utm_source=openai))  
- **What kind of reference to look for:**
  - Lazarsfeld *Positivity I*, §1.6 (or Teissier’s original papers, or Khovanskii). The important thing is: **nef divisors \(\Rightarrow\) log-concavity of mixed intersection sequences**.

---

### 5) Minor technical clarity: construction of the curve \(\mathcal C \subset \mathcal X\) mapping generically finitely to \(C \subset X\)  
- **Location in Attempt 4:**  
  - §4 Lemma 4.2(1) (nefness passes to coarse space): “Choose an integral curve \(\mathcal C\subset\mathcal X\) mapping generically finitely onto \(C\).”
- **Issue:**  
  This is standard but a strict reader might want one concrete sentence of construction.
- **How to fix it:**
  - Add: “Take an irreducible component of the normalization of \(\mathcal X\times_X C\) dominating \(C\).”
  - Then note that degrees/intersection numbers scale correctly by the generic degree of \(\mathcal C\to C\).

---

### 6) Optional robustness: clarify the base field / resolution step assumptions  
- **Location:**  
  - §3 (resolution \(\widetilde X \to X\))
- **Issue:**  
  The proof implicitly assumes you are over a field where resolution exists (typically \(\mathbb C\), which is standard for Witten–Kontsevich intersection theory).
- **How to fix it:**
  - Add one sentence: “Work over \(\mathbb C\)” (or characteristic \(0\)) so resolution exists.
  - Or cite a standard resolution theorem in char 0.

---

### 7) Optional enhancement: “uniqueness/equality cases” are not required but could be mentioned cleanly  
- **Location:**  
  - Not a gap; just an optional note near §8.
- **Issue:**  
  The proof gives existence of extrema locations, not uniqueness; this is fine, but you could add a short remark: uniqueness would require analyzing equality cases in KT.
- **How to fix it:**
  - Add 2–3 lines: “Strictness and uniqueness reduce to equality cases in Khovanskii–Teissier (numerical proportionality conditions), which are subtle here.”

---

## Quick checklist (what to change in Attempt 4)

1. **§4 Fact 4.1:** add an explicit citation for nefness of **each \(\psi_i\)** (not just a generic “\(\psi\)”).  
2. **§5 Lemma 5.1:** replace the “Kontsevich positivity” paragraph with either:
   - a precise ribbon-graph formula citation, or  
   - a modern explicit lower-bound theorem citation (DGZZ is a strong candidate). ([sigma-journal.com](https://sigma-journal.com/2020/086/?utm_source=openai))  
3. **§3 Lemmas 3.1–3.3:** add theorem/proposition numbers in Vistoli + Fulton operational Chow references (or cite Stacks Project summary as navigation). ([stacks.math.columbia.edu](https://stacks.math.columbia.edu/tag/03B6?utm_source=openai))  
4. **§6.1:** cite KT log-concavity with theorem number (e.g. Lazarsfeld §1.6; Theorem 1.6.1 appears as the “global Hodge-type inequality”). ([scribd.com](https://www.scribd.com/document/705024715/Lazarsfeld-Positivity-in-Algebraic-Geometry-I?utm_source=openai))  
5. **§4.2:** add one construction line for \(\mathcal C\to C\) via normalization of \(\mathcal X\times_X C\).

