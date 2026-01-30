# TongGeometry: A Critical Assessment of China's Latest AI Geometry Breakthrough

**Report Date:** January 30, 2026  
**Subject:** Evaluation of claims regarding TongGeometry, a neuro-symbolic AI system for olympiad-level geometry
**Author:** Claude Opus 4.5

---

## Executive Summary

On January 26, 2026, researchers from the Beijing Institute for General Artificial Intelligence (BIGAI) and Peking University published a paper in *Nature Machine Intelligence* introducing TongGeometry, an AI system claimed to both solve and propose International Mathematical Olympiad (IMO)-level geometry problems. The system reportedly solved all 30 problems in the IMO-AG-30 benchmark, outperforming the average IMO gold medalist on this specific dataset.

While the research represents genuine technical progress in automated geometry reasoning, this report finds that the headline claims warrant significant qualification. The evaluation methodology has notable limitations including:

- A small (n=30) and potentially biased benchmark that skews toward easier problems
- Absence of machine-verifiable formal proofs in standard systems (Lean/Isabelle)
- Limited independent verification (single expert reviewer)
- **Most critically: No verifiable training cutoff date** — The paper claims IMO 2024 and IMO 2025 problems were "unseen" during training, but provides no timestamps, cryptographic hashes, or third-party verification of when model training was completed. The 5-6 month gaps between these competitions and the paper versions provide ample opportunity for data contamination that the methodology does not rule out.

The problem generation capability is better supported, with evidence that competition-worthy problems were being generated before May 2024 (based on USEMO submission timelines). However, the "temporal holdout" evidence for solving capability generalization is methodologically inadequate. The results are promising but should not be interpreted as demonstrating general superiority over human mathematicians or establishing robust generalization beyond training data without further validation.

---

## 1. Background and Context

### 1.1 The Research Team

TongGeometry was developed by a consortium of Chinese institutions:

- **Beijing Institute for General Artificial Intelligence (BIGAI)** — A government-backed research organization established in 2020, led by Professor Song-Chun Zhu (formerly of UCLA for 28 years). BIGAI pursues what it calls a "small data, big tasks" paradigm for artificial general intelligence.
- **Peking University** — Multiple departments including the School of Psychological and Cognitive Sciences, School of Intelligence Science and Technology, and Institute for Artificial Intelligence.
- **Wuhan Institute for Artificial Intelligence**

The first author is Zhang Chi, a researcher at BIGAI.

### 1.2 Competitive Landscape

TongGeometry enters a rapidly evolving field of AI mathematical reasoning:

| System | Developer | Key Achievement |
|--------|-----------|-----------------|
| AlphaGeometry (2024) | Google DeepMind | 25/30 on IMO-AG-30 benchmark |
| AlphaGeometry2 (2025) | Google DeepMind | 84% solve rate on IMO 2000-2024 geometry |
| DeepSeek Math-V2 | DeepSeek (China) | Gold-level IMO performance (open-sourced) |
| TongGeometry (2026) | BIGAI/Peking U | 30/30 on IMO-AG-30, problem generation |

---

## 2. Technical Architecture

### 2.1 Core Innovation: Dual Capability

TongGeometry's distinguishing feature is its claimed ability to both **solve** and **propose** olympiad-level geometry problems—functioning as what the authors describe as a "coach" rather than merely a "student."

The system operates on the principle that geometry problems emerge when a fact's *construction sequence* (minimum steps to draw the elements) forms a proper subset of its *proof sequence* (minimum steps to prove the fact). This duality enables:

1. **Problem solving**: Identifying auxiliary constructions needed to bridge the gap
2. **Problem generation**: Systematically discovering facts where this gap exists

### 2.2 System Components

**Markovian Framework**  
TongGeometry models geometry as a Markov chain where:
- States represent geometric diagrams constructed through action sequences
- Actions add geometric objects (points, lines, circles)
- State transitions trigger deterministic derivation of new facts

**Neuro-Symbolic Architecture**  
The system employs an actor-critic style approach:
- **Policy model**: A fine-tuned DeepSeek-Coder-1.3B language model suggesting auxiliary constructions
- **Value model**: Estimates remaining proof steps for each candidate path
- **Deductive database**: A symbolic engine deriving facts through rule application

**Key Technical Differences from AlphaGeometry**  
- Integrates algebraic reasoning directly within the deductive database (rather than as a separate component)
- Uses canonical representation to eliminate redundant search paths
- Supports native symmetric problem generation through symmetry maps

### 2.3 Training Data

The system was trained on a massive self-generated dataset:
- **6.7 billion** geometry problems requiring auxiliary constructions
- **4.1 billion** exhibiting geometric symmetry
- Generated through 30 days of parallel search on 10,368 CPU cores
- Guided by statistics from 196 human-created olympiad problems

---

## 3. Claimed Results

**Important Caveat:** The results reported in this section are as claimed by the authors. Section 4 provides critical assessment of these claims, including significant concerns about verification methodology and timeline documentation. Readers should review Section 4.4 (Timeline and Training Cutoff Issues) before accepting claims about "unseen" problems at face value.

### 3.1 Problem Solving Performance

**IMO-AG-30 Benchmark Results:**

| Method | Problems Solved | Notes |
|--------|-----------------|-------|
| Wu's Method | 10/30 | Previous baseline |
| AlphaGeometry (DD+AR) | 25/30 | Google DeepMind (2024) |
| TongGeometry (DD only) | 18/30 | Symbolic engine alone |
| TongGeometry (full) | **30/30** | With neural guidance |
| Average IMO Gold Medalist | 25.9/30 | Human benchmark |

**Computational Efficiency:**  
- TongGeometry: 32 CPU cores + 1 NVIDIA RTX 4090, max 38 minutes per problem
- AlphaGeometry: 246 CPU cores + 4 NVIDIA V100 GPUs for sub-90-minute solving

**Temporal Holdout Validation (Claimed but Unverifiable):**  
The paper claims the system solved IMO 2024 P4 and IMO 2025 P2—problems released after training completion—with solutions verified by a 2024 IMO gold medalist. However, no training cutoff date is specified, no cryptographic verification exists, and the timeline gaps (5-6 months between competitions and paper versions) provide opportunity for contamination. See Section 4.4 for detailed analysis.

### 3.2 Problem Generation

Three problems autonomously generated by TongGeometry were selected for actual competitions:
- One problem: 2024 National High School Mathematics League (Beijing) — the only geometry problem in a Chinese National Team qualifying exam
- Two problems: 2024 US Ersatz Math Olympiad shortlist

**Note on Potential Conflict of Interest:** The USEMO 2024 report indicates the competition was "sponsored by the CoRe Lab, Institute of Artificial Intelligence, Peking University" — the same institution affiliated with TongGeometry's development team. While this does not invalidate the problem selection (problems are evaluated on mathematical merit), it represents a relationship that should be disclosed.

The system also independently rediscovered known geometric lemmas (e.g., nine-point center configurations) and foundational configurations (e.g., mixtilinear incircle), suggesting the search methodology converges toward mathematically meaningful structures.

---

## 4. Critical Assessment

### 4.1 Benchmark Limitations

**Small Sample Size**  
The IMO-AG-30 benchmark contains only 30 problems—statistically insufficient for strong comparative claims. With such a small n, the difference between 25/30 and 30/30 is not necessarily significant.

**Difficulty Selection Bias**  
Independent analysis indicates the benchmark skews toward easier problems:

> "The IMO-30 benchmark predominantly contains problems that are not especially challenging... compared with HAGeo-409, whose average difficulty is 3.47, the IMO-30 benchmark is relatively easy, with an average difficulty of only 2.85."  
> — HAGeo benchmark paper (2024)

IMO problems are graded by difficulty (Problems 1 & 4 are easier; 3 & 6 are hardest). The benchmark's composition may not reflect the full difficulty spectrum.

**Benchmark Staleness**  
The IMO-AG-30 benchmark was created by Google DeepMind for AlphaGeometry evaluation. Using a competitor's benchmark introduces potential issues:
- Problems may have been optimized against by multiple systems
- No contamination detection methodology is described for ensuring training/test separation

### 4.2 Formal Verification Gaps

**No Machine-Verifiable Proofs**  
TongGeometry operates in a proprietary domain-specific language (DSL), not in established formal verification systems like Lean 4 or Isabelle. This means:
- Proofs cannot be independently machine-verified
- The formal system may contain soundness issues

Recent analysis of similar systems has identified this concern:

> "Systems like AlphaGeometry, TongGeometry and SeedGeometry... typically rely on specialized models and operate within geometry-specific formal systems independent of Lean. This isolation prevents integration with other mathematical domains... Additionally, their reliance on graphical verification and unordered formal systems can lead to logical unsoundness and incompleteness."  
> — LeanGeo paper (2025)

**Precedent for Incorrect "Solved" Problems**  
AlphaGeometry's proof for IMO-2020-P1 was later found to be incorrect:

> "We found the proof for IMO-2020-P1 to be incorrect... step 9 of the proof is wrong... This statement is incorrect because it implicitly assumes that M, N, and E are collinear, which is not proven."  
> — HAGeo paper (2024)

This precedent suggests that passing initial review does not guarantee correctness, and TongGeometry's proofs require similar scrutiny.

### 4.3 Verification Methodology

**Limited Expert Review**  
The paper states solutions were verified by "a 2024 IMO gold medallist"—singular. While expert review is valuable, a single reviewer is insufficient for validating 30+ complex proofs, particularly given the precedent of missed errors.

**No Independent Replication**  
At time of writing, no independent research group has replicated TongGeometry's results. While the code is open-sourced (enabling future verification), the claims remain unconfirmed by external parties.

**Resources Available for Independent Verification**  
The authors have made resources available that could enable independent verification:
- GitHub repository: https://github.com/bigai-ai/tong-geometry
- Zenodo archive: https://doi.org/10.5281/zenodo.17646188
- Model checkpoints and training data are reportedly included

**Recommended Verification Steps:**
1. Examine GitHub commit history for timestamps relative to IMO 2024/2025
2. Attempt to reproduce IMO-AG-30 results using published checkpoints
3. Independently verify proofs using the deductive database engine
4. Cross-check generated proofs against known correct solutions

Until such independent verification is conducted, claims should be treated with appropriate skepticism.

### 4.4 Critical Timeline and Training Cutoff Issues

**This represents the most significant methodological concern with the paper.**

#### Reconstructed Timeline

| Date | Event |
|------|-------|
| ~May 2024 | USEMO 2024 problem submission deadline (TongGeometry submitted 6 problems) |
| July 11-22, 2024 | **IMO 2024** (Thailand) — IMO 2024 P4 released; official solutions published |
| October 26-27, 2024 | USEMO 2024 competition held |
| December 14, 2024 | arXiv preprint v1 submitted — mentions IMO 2024 P4, does NOT mention IMO 2025 |
| July 10-20, 2025 | **IMO 2025** (Australia) — IMO 2025 P2 released |
| January 26, 2026 | Nature Machine Intelligence publication — NOW includes both IMO 2024 P4 and IMO 2025 P2 |

#### The Core Problem: No Training Cutoff Date Specified

The Nature paper claims: *"To demonstrate TongGeometry's problem-solving capabilities on contemporary competition problems, we evaluated its performance on IMO 2024 P4 (Fig. 4) and IMO 2025 P2—the geometry problems from the most recent IMO competition. This problem represents a particularly stringent test case since they only came after TongGeometry's training."*

However, **nowhere in the paper is a training completion date specified.** The claim that these problems "only came after TongGeometry's training" is unverifiable.

#### Critical Discrepancy Between Preprint and Publication

The December 2024 arXiv preprint uses notably weaker language about IMO 2024 P4:

> *"Figure 2 shows IMO 2024 P4, the geometry problem in the latest IMO competition, **a relatively new problem without many documented solutions at the time of TongGeometry training**."*

This phrasing is revealing:
1. It admits that solutions to IMO 2024 P4 **existed** at the time of training — just "not many"
2. Official IMO solutions were published in July 2024, immediately after the competition
3. By December 2024 (preprint submission), many solutions would have been documented

The Nature publication (January 2026) strengthens this to "only came after TongGeometry's training" — but provides no additional evidence to support the stronger claim.

#### IMO 2025 P2: Added After Preprint

IMO 2025 P2 appears **only** in the Nature paper, not in the December 2024 preprint. This raises critical questions:

1. Was the same frozen model used to solve IMO 2025 P2?
2. Was there retraining between December 2024 and January 2026?
3. When was the IMO 2025 evaluation actually conducted?

The paper provides no information to answer these questions.

#### What the Paper Actually Establishes

The paper provides **verifiable** evidence that problem generation was occurring before May 2024:

> *"Before submission deadlines for the 2024 National High School Mathematics League (Beijing) and 2024 US Ersatz Math Olympiad, we enlisted a 2023 IMO gold medallist and a Chinese National Team student member to evaluate proposal batches during initial search phases."*

Since USEMO 2024 had submissions due around May 2024 and the competition was held in October 2024, this establishes that TongGeometry was generating competition-worthy problems before IMO 2024 occurred.

However, **problem generation capability is separate from problem-solving neural model training.** The workflow is:
1. Run parallel search to generate billions of problems (30 days on 10,368 cores — could have started early 2024)
2. Train neural policy/value models on this data (timing never specified)
3. Evaluate on benchmarks (timing never specified)

The paper conflates these phases, making it impossible to verify when the neural models were frozen relative to the IMO competitions.

#### What Would Establish Credibility

- A cryptographic hash of model weights published **before** IMO 2024/2025
- Third-party attestation of training completion date
- Pre-registered evaluation protocol
- Explicit training data cutoff with verifiable timestamps
- GitHub commit history predating the competitions (the Zenodo archive could potentially provide this)

**None of these safeguards are documented in the paper.**

#### Implications

The 5-6 month gaps between the IMO competitions and the paper versions provide ample opportunity for data contamination:
- IMO 2024 (July 2024) → Preprint (December 2024): 5 months
- IMO 2025 (July 2025) → Publication (January 2026): 6 months

Without verifiable timestamps, the "temporal holdout" claim — which is presented as the strongest evidence for generalization — cannot be independently validated.

### 4.5 Data Contamination Risks (Beyond Timeline Issues)

The paper does not describe systematic contamination detection methodology. Standard concerns include:
- Whether IMO-AG-30 problems or close variants appeared in training data
- Whether the 196 guiding statistics problems overlap with evaluation sets
- The MO-TG-225 benchmark was created by the same team, introducing potential selection bias

The authors' claim that "none of these problems appear in TongGeometry's training dataset" for MO-TG-225 is reassuring but not independently verified.

### 4.6 Framing and Interpretation Issues

**"Outperforms Gold Medalists" Claim**  
The paper carefully qualifies: "Note that we do not claim TongGeometry surpasses an average IMO gold medallist in geometry generally." However, this nuance is lost in media coverage. The comparison is:
- Against a constructed "average gold medalist" metric on historical problems
- Not against actual human competitors under identical conditions
- Limited to problems expressible in the system's DSL (86.8% of IMO geometry)

**Chinese Media Amplification**  
State media coverage has extended claims beyond what the methodology supports:

> "TongGeometry clearly highlights the superiority of original domestic technology in terms of performance."  
> — Xinhua News Agency

Such framing conflates narrow benchmark performance with general capability superiority.

---

## 5. Comparative Analysis

### 5.1 TongGeometry vs. AlphaGeometry

| Dimension | TongGeometry | AlphaGeometry/AG2 |
|-----------|--------------|-------------------|
| IMO-AG-30 performance | 30/30 (claimed) | 25/30 (AG1), higher for AG2 |
| Computational resources | Consumer-grade | Data center scale |
| Problem generation | Yes | No |
| Formal verification | Proprietary DSL | Proprietary DSL |
| Open source | Yes (GitHub/Zenodo) | Partially (AG1 only) |
| Peer review | Nature Machine Intelligence | Nature (AG1) |
| Training cutoff verification | **Not specified** | **Not specified** |
| Independent replication | **Pending** | **Partial** |

**Critical Note on Comparability:** Direct performance comparisons between TongGeometry and AlphaGeometry are complicated by:
- Different domain-specific languages requiring problem translation
- Neither system provides machine-verifiable proofs in standard formal systems
- Both lack explicit training cutoff documentation
- The IMO-AG-30 benchmark was created by DeepMind for AlphaGeometry, potentially favoring that system's design

### 5.2 Acknowledged Limitations

The TongGeometry authors acknowledge several limitations:

1. **Statistical prior dependency**: "By anchoring our generation to this prior, we risk constraining our search to a 'local optimum' defined by known human definitions of 'elegance'... We may be missing classes of valuable configurations that humans have not yet discovered."

2. **Problem coverage**: The system cannot handle geometry involving inequalities, variable numbers of points, or advanced techniques like inversion and projective geometry.

3. **Benchmark specificity**: Results on IMO-AG-30 do not generalize to all geometry or mathematics.

---

## 6. Implications

### 6.1 For AI Research

**Genuine Progress**  
Despite methodological concerns, TongGeometry represents meaningful advancement:
- The dual solve/propose capability is novel and potentially valuable
- Efficiency gains (consumer hardware) democratize access to such systems
- Open-sourcing enables community scrutiny and improvement

**Research Directions**  
The field requires urgent methodological improvements that apply not just to TongGeometry but to AI mathematical reasoning research broadly:
- Larger, difficulty-graded benchmarks with formal holdout procedures
- Integration with established formal verification systems (Lean, Isabelle)
- Standardized contamination detection protocols
- **Mandatory training cutoff documentation** with verifiable timestamps or cryptographic commitments
- **Pre-registration of evaluation protocols** before competitions occur
- Independent replication studies with third-party verification

### 6.2 For Mathematics Education

The authors have deployed TongGeometry in educational applications:

> "In a weekly competition, TongGeometry's proposed problems are meticulously reviewed, edited and refined by experienced IMO coaches who adjust difficulty, enhance pedagogical value and ensure they align with the curriculum."

This represents a potentially valuable application—AI-assisted problem generation for training materials—that is less dependent on the system achieving superhuman problem-solving.

### 6.3 For Geopolitical AI Competition

TongGeometry is framed within China's broader AI development strategy. BIGAI explicitly pursues approaches alternative to Western "big data" paradigms. The paper's publication in a high-impact Western journal, combined with open-sourcing, positions China as a competitive and transparent participant in frontier AI research.

However, the nationalistic framing in Chinese media coverage risks conflating scientific achievement with technological superiority claims that exceed the evidence.

---

## 7. Conclusions

### 7.1 Summary Assessment

| Claim | Assessment |
|-------|------------|
| Solves all IMO-AG-30 problems | **Plausible but requires verification** — Results consistent with incremental progress, but benchmark limitations and verification gaps warrant caution |
| Outperforms gold medalists | **Oversimplified** — True only on a specific, small, potentially easy benchmark; not generalizable |
| Superior to AlphaGeometry | **Partially supported** — Efficiency gains appear genuine; performance comparison complicated by benchmark issues |
| Can propose olympiad-worthy problems | **Validated** — Three problems selected for real competitions provides concrete evidence; timeline supports pre-May 2024 capability |
| Consumer hardware efficiency | **Credible** — Specific claims are verifiable via open-source code |
| IMO 2024/2025 as temporal holdout | **Unverifiable** — No training cutoff date specified; no cryptographic or third-party verification; the strongest generalization claim lacks adequate evidence |

### 7.2 Recommendations

**For researchers citing this work:**
- Qualify claims with benchmark limitations
- Note absence of formal verification
- **Flag the unverifiable training cutoff date as a significant limitation**
- Await independent replication

**For educators/practitioners:**
- Problem generation capability may be more immediately useful than solving
- Treat generated problems as requiring expert review before use
- The pre-May 2024 problem generation timeline is better established than solving claims

**For policymakers/observers:**
- Distinguish between narrow benchmark performance and general capability
- Note that Chinese and Western systems operate at comparable levels
- Recognize that open-sourcing enables global scientific scrutiny
- **Be aware that headline claims about "outperforming humans" lack rigorous temporal controls**

### 7.3 Final Assessment

TongGeometry represents genuine scientific progress in automated geometry reasoning, meriting its publication in a respected journal. The dual capability to solve and propose problems is a meaningful innovation, and the computational efficiency claims appear credible. The problem generation capability is particularly well-supported, with evidence of competition-worthy problems being generated before May 2024.

However, the headline claim of "outperforming IMO gold medalists" requires substantial qualification. The evaluation methodology has significant limitations:

1. **A small and potentially biased benchmark** (30 problems, skewing easier)
2. **Absence of machine-verifiable proofs** in standard formal systems
3. **Limited independent verification** (single expert reviewer)
4. **No systematic contamination detection**
5. **Most critically: No verifiable training cutoff date** — The paper's strongest claim to generalization (solving IMO 2024 P4 and IMO 2025 P2 as "unseen" problems) is unverifiable without timestamps, cryptographic hashes, or third-party attestation of when model training was completed

Previous geometry AI systems have produced proofs that passed initial review but were later found incorrect—a precedent that demands caution. The 5-6 month gaps between the IMO competitions and the paper versions provide ample opportunity for data contamination that the methodology does not rule out.

The appropriate interpretation is that TongGeometry demonstrates strong performance on a narrow benchmark and introduces valuable problem-generation capabilities, but the "temporal holdout" evidence for generalization beyond training data is methodologically inadequate. The research is promising and the open-sourcing commendable, but the extraordinary claims require more rigorous evidence than currently provided.

**The field urgently needs standardized protocols for establishing training cutoff dates in AI evaluation, including pre-registration, cryptographic commitments, and third-party verification.**

---

## References

### Primary Sources

1. Zhang, C. et al. "Proposing and solving olympiad geometry with guided tree search." *Nature Machine Intelligence* 8, 84–95 (2026). https://doi.org/10.1038/s42256-025-01164-x

2. Zhang, C. et al. "Proposing and solving olympiad geometry with guided tree search." arXiv preprint (December 14, 2024). https://arxiv.org/abs/2412.10673 — **Note: This preprint version uses weaker language about IMO 2024 P4 and does not mention IMO 2025 P2**

3. TongGeometry Code Repository (GitHub): https://github.com/bigai-ai/tong-geometry

4. TongGeometry Code and Data Archive (Zenodo): https://doi.org/10.5281/zenodo.17646188

### Comparative Systems

5. Trinh, T.H. et al. "Solving olympiad geometry without human demonstrations." *Nature* 625, 476–482 (2024). https://doi.org/10.1038/s41586-023-06747-5

6. AlphaGeometry Code Repository (GitHub): https://github.com/google-deepmind/alphageometry

7. Chervonyi, Y. et al. "Gold-medalist performance in solving olympiad geometry with AlphaGeometry2." arXiv:2502.03544 (2025). https://arxiv.org/abs/2502.03544

8. Sicca, V. et al. "Newclid: a user-friendly replacement for AlphaGeometry." arXiv:2411.11938 (2024). https://arxiv.org/abs/2411.11938

9. ByteDance Seed-Prover: "Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving." arXiv:2507.23726 (2025). https://arxiv.org/abs/2507.23726 — **Note: Seed-Geometry builds on TongGeometry's approach**

### Critical Analyses and Benchmarks

10. HAGeo Benchmark Analysis: "HAGeo: A Large-scale Hard Geometry Benchmark for Evaluating Theorem Provers." arXiv:2512.00097 (2024). — **Source of benchmark difficulty comparison showing IMO-AG-30 skews easier**

11. LeanGeo: "Formalizing Competitional Geometry problems in Lean." arXiv:2508.14644 (2025). — **Source of critique regarding proprietary DSLs and formal verification gaps**

12. Sinha, S. et al. "Wu's method can boost symbolic AI to rival silver medalists and AlphaGeometry to outperform gold medalists at IMO geometry." arXiv:2404.06405 (2024). https://arxiv.org/abs/2404.06405

### Competition and Benchmark Sources

13. IMO 2024 Official Problems and Solutions. International Mathematical Olympiad (Thailand, July 2024). https://www.imo-official.org/year_info.aspx?year=2024

14. IMO 2025 Official Problems and Solutions. International Mathematical Olympiad (Australia, July 2025). https://www.imo-official.org/year_info.aspx?year=2025

15. US Ersatz Math Olympiad (USEMO) 2024 Results and Solutions. Evan Chen. https://web.evanchen.cc/usemo.html — **Note: TongGeometry problems made shortlist; competition held October 26-27, 2024**

16. USEMO 2024 Report (PDF). https://web.evanchen.cc/exams/report-usemo-2024.pdf — **Confirms USEMO 2024 was sponsored by "CoRe Lab, Institute of Artificial Intelligence, Peking University"**

### Institutional Sources

17. Beijing Institute for General Artificial Intelligence (BIGAI) GitHub Organization: https://github.com/bigai-ai

18. BIGAI Official Website: https://www.bigai.ai/

### Media Coverage (Cited for Framing Analysis)

19. Xinhua News Agency. "China Focus: Chinese researchers score breakthrough in general artificial intelligence logical reasoning." January 27, 2026. https://english.news.cn/20260127/26a2c05ece9f493fbcb90525ce0201f0/c.html

20. China Daily Asia. "Chinese researchers score breakthrough in general AI logical reasoning." January 28, 2026. https://www.chinadailyasia.com/hk/article/627883

21. Guangming Online. "Chinese researchers score breakthrough in general artificial intelligence logical reasoning." January 28-29, 2026. https://en.gmw.cn/2026-01/28/content_38563295.htm

### Background Technical References

22. Chou, S.-C., Gao, X.-S. & Zhang, J.-Z. "A deductive database approach to automated geometry theorem proving and discovering." *J. Autom. Reason.* 25, 219–246 (2000).

23. Guo, D. et al. "DeepSeek-Coder: when the large language model meets programming." arXiv:2401.14196 (2024). https://arxiv.org/abs/2401.14196 — **Base model fine-tuned for TongGeometry**

24. Chen, E. *Euclidean Geometry in Mathematical Olympiads* (American Mathematical Society, 2021). — **Standard reference for olympiad geometry techniques**

25. Chen, E. "A guessing game: mixtilinear incircles." https://web.evanchen.cc/handouts/Mixt-GeoGuessr/Mixt-GeoGuessr.pdf — **Configuration rediscovered by TongGeometry**

---

## Appendix: Key Quotes from Primary Sources

### From Nature Paper (January 2026)

> "To demonstrate TongGeometry's problem-solving capabilities on contemporary competition problems, we evaluated its performance on IMO 2024 P4 (Fig. 4) and IMO 2025 P2—the geometry problems from the most recent IMO competition. **This problem represents a particularly stringent test case since they only came after TongGeometry's training.**"

> "Note that **we do not claim TongGeometry surpasses an average IMO gold medallist in geometry generally.**"

### From arXiv Preprint (December 2024)

> "Figure 2 shows IMO 2024 P4, the geometry problem in the latest IMO competition, **a relatively new problem without many documented solutions at the time of TongGeometry training**."

**Critical Observation:** The preprint acknowledges solutions existed; the Nature paper claims the problem came "after" training. No additional evidence supports this stronger claim.

### From LeanGeo Paper (2025)

> "Systems like AlphaGeometry, TongGeometry and SeedGeometry... typically rely on specialized models and operate within geometry-specific formal systems independent of Lean. This isolation prevents integration with other mathematical domains... Additionally, **their reliance on graphical verification and unordered formal systems can lead to logical unsoundness and incompleteness.**"

### From HAGeo Paper (2024)

> "The IMO-30 benchmark predominantly contains problems that are not especially challenging... compared with HAGeo-409, whose average difficulty is 3.47, **the IMO-30 benchmark is relatively easy, with an average difficulty of only 2.85.**"

> "We found the proof for IMO-2020-P1 to be incorrect... **step 9 of the proof is wrong**... This statement is incorrect because it implicitly assumes that M, N, and E are collinear, which is not proven."

---

*This report was prepared for informational purposes and represents an independent assessment based on publicly available sources. The author has no affiliation with BIGAI, Peking University, Google DeepMind, or any competing research group.*

*Last updated: January 30, 2026*
