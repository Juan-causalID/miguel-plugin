---
name: DiD methodology references with verified content
description: Verified verbatim claims from key DiD and identification papers used in the HPV-sPTB project; safe to cite directly in this form
type: reference
---

All quotes below were verified against the actual paper text in this session. Do not add quotation marks to claims not in this file unless re-verified.

## Hernan 2016, "Does water kill?" Annals of Epidemiology 26(10):674-680
- "The interpretation of counterfactual contrasts requires a relatively unambiguous definition of the meaning of a=1 and a=0, a requirement referred by some of us as 'well-defined interventions'."
- "when there are multiple versions of a and different versions lead to different outcomes, causal effects are not well-defined."
- The paper does NOT argue policy interventions are easier per se; it argues for "feasible interventions that can be actually implemented" so that effects could in principle be checked by a randomized experiment.

## Hernan and VanderWeele 2011, "Compound Treatments and Transportability of Causal Inference," Epidemiology 22(3):368-377
- Consistency for simple treatments: "Yi=Yia when Ai = a for all a and i."
- For compound treatments: "Yi=Yir,a(r) when Ri=r and Ai(r)=a(r)."
- "The average causal effect of the compound treatment R depends on the distribution of versions A(r) of treatment R in the study population."
- "In the absence of consistency, one would not know which counterfactual contrast is being estimated by the data."

## Wing, Simon, Bello-Gomez 2018, Annu Rev Public Health 39:453-469
- Full text was paywalled in this session; only the abstract and PubMed record were verifiable. Cite for the general orientation of DiD in public health policy research and the recommendation that researchers take an active design approach with sensitivity analyses validating parallel trends. Do NOT use direct quotes you have not personally verified against the article.

## Roth, Sant'Anna, Bilinski, Poe 2023, J Econometrics 235(2):2218-2244
Verified directly from the arXiv full text.
- Parallel Trends (Assumption 1): E[Y_{i,2}(0) - Y_{i,1}(0) | D_i = 1] = E[Y_{i,2}(0) - Y_{i,1}(0) | D_i = 0].
- "It has therefore become common practice to check, both visually and using statistical tests, whether there exist pre-existing differences in trends ('pre-trends') as a test of the plausibility of the parallel trends assumption."
- "even if pre-trends are exactly parallel, this need not guarantee that the post-treatment parallel trends assumption is satisfied" (bar-mitzvah/height example).
- Pre-trends tests have known low power and pre-test selection problems (Section 4.4).
- TWFE static specification under heterogeneous effects: beta_post is "a potentially non-convex weighted average ... where the weights ω_s sum to 1 but may be negative." Hence "all of the τ_s could be positive and yet the coefficient β_post may be negative."
- Recommend against dynamic TWFE in staggered settings; use Callaway and Sant'Anna (2021), Sun and Abraham (2021), de Chaisemartin and D'Haultfoeuille (2020), or Borusyak et al.

## Callaway and Sant'Anna 2021, J Econometrics 225(2):200-230
Verified from arxiv 1803.09015 PDF.
- Target parameter: ATT(g,t) = E[Y_t(g) - Y_t(0) | G_g = 1].
- Assumption 4 (Conditional parallel trends, never-treated comparison): E[Y_t(0) - Y_{t-1}(0) | X, G_g = 1] = E[Y_t(0) - Y_{t-1}(0) | X, C = 1].
- Assumption 5 is the not-yet-treated analog.
- Identification of ATT(g,t) under Assumptions 1-3 plus 4 or 5.
- Aggregation schemes (event-study, group, calendar) are positively-weighted averages of ATT(g,t).

## Goodman-Bacon 2021, J Econometrics 225(2):254-277
Verified directly from NBER w25018 PDF.
- "any two-way fixed effects DD estimator is a weighted average of all possible two-group/two-period DD estimators in the data" (decomposition theorem, Theorem 1).
- Some 2x2 comparisons use already-treated units as the "control"; "negative weights occur when already-treated units act as controls, changes in their treatment effects over time get subtracted from the DD estimate. This negative weighting only arises when [treatment effects vary over time]."

## de Chaisemartin and D'Haultfoeuille 2020, AER 110(9):2964-2996
Verified from NBER w25904 PDF.
- "if the treatment is binary, beta_fe identifies a weighted sum of the treatment effect in each group"; weights "sum to one but may be negative."
- "Negative weights arise because beta_fe is a weighted average of several DIDs ... [in some] DIDs, both groups are treated, and the average treatment effect of the comparison group is canceled out by the DID, hence the negative weights."
- Around 50% of weights were negative in their re-analysis of Enikolopov et al. 2011.

## Lipsitch, Tchetgen Tchetgen, Cohen 2010, Epidemiology 21(3):383-388
Verified from PMC full text.
- NEGATIVE controls only: a 2026-08-26 full-text check (PMC3053408) found NO mention of positive controls anywhere in the paper. Do not cite Lipsitch 2010 as the source for "positive control outcome" or benchmark-endpoint logic; if used for that logic, frame it explicitly as an extension by analogy of the negative-control reasoning, or cite it only for control-outcome bias detection.
- "The essential purpose of a negative control is to reproduce a condition that cannot involve the hypothesized causal mechanism, but is very likely to involve the same sources of bias that may have been present in the original association."
- "Ideally, a negative control outcome (N) should be an outcome such that the set of common causes of exposure A and outcome Y should be as identical as possible to the set of common causes of A and N."

## Imbens and Angrist 1994, Econometrica 62(2):467-475
Verified from the PDF.
- LATE = E[Y_i(1) - Y_i(0) | D_i(z) - D_i(w)], the effect "for those who can be induced to change participation status by a change in the instrument."
- Condition 2 (Monotonicity): "For all z, w, either D_i(z) >= D_i(w) for all i, or D_i(z) <= D_i(w) for all i."
- Theorem 1: under Conditions 1 (independence/exclusion) and 2 (monotonicity), LATE is identified.

## Angrist and Krueger 2001, JEP 15(4):69-85
Verified from the PDF.
- "A natural experiment can be studied without application of instrumental variables methods; in this case, reduced form estimates would be presented" (footnote 7).
- "Concerns about weak instruments can be mitigated most simply by looking at the reduced form equation, that is, the ordinary least squares regression of the dependent variable of interest on the instruments and exogenous variables. These estimates are unbiased, even if the instruments are weak."
- "Most importantly, if the reduced form estimates are not significantly different from zero, the presumption should be that the effect of interest is either absent or the instruments are too weak to detect it."
