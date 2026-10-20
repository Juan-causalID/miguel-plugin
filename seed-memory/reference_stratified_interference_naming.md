---
name: stratified-interference-naming
description: Verified provenance of "stratified interference" (Hudgens & Halloran 2008 Assumption 2) vs "partial interference" (attributed to Sobel 2006), plus documented mis-citation in Buchanan 2021 AJE
metadata:
  type: reference
---

# "Stratified interference" — verified provenance

## Origin (VERIFIED verbatim from JASA PDF)
**Hudgens MG, Halloran ME. "Toward Causal Inference With Interference." J Am Stat Assoc. 2008;103(482):832-842. doi:10.1198/016214508000000292**

Section 4.2.1 is titled "Stratified Interference." Verbatim:

> "Suppose that R^ni, that is, the set of possible treatment programs for group i, can be partitioned into strata such that within strata there is no interference. In particular, we assume:
> **Assumption 2 (Stratified interference).** For k = 1,...,ni − 1, Yij(zi) = Yij(z′i) for all zi, z′i ∈ R^ni_k such that zij = z′ij."

Their own gloss, verbatim:
> "The stratified interference assumption states that the outcome for a child receiving the intervention will be the same when k − 1 schoolmates also receive the intervention, regardless of which particular k − 1 schoolmates receive the intervention. This assumption can be viewed as an intermediate assumption between (i) assuming no interference within a group and (ii) making no assumptions about the nature of interference within a group."

Counting result (verbatim): under Assumption 2 an individual has **ni** potential outcomes for a given zij = z, vs **1** under no interference and **2^(ni−1)** under arbitrary within-group interference.

Note: Assumption 2 is introduced ONLY to get **variance** estimators. Point estimators (Theorems 1-3) need only Assumption 1 (mixed assignment strategies). Verbatim: "Under an additional assumption of stratified interference (Assumption 2), variance estimators of the causal effect estimators are derived that are unbiased under additivity and positively biased otherwise."

## Partial interference — the name is ATTRIBUTED, not self-applied
HH2008 verbatim: "Sobel (2006) called this a partial interference assumption."
Sobel ME. JASA 2006;101(476):1398-1407.
**Key distinction:** partial interference = WHERE interference can occur (within groups, not across). Stratified interference = the FUNCTIONAL FORM of within-group interference (depends on the number/proportion treated, not on which specific others). They are orthogonal, and HH2008 assumes BOTH.

## Halloran & Struchiner (source of direct/indirect/total/overall) — VERIFIED via PubMed
- Halloran ME, Struchiner CJ. "Study designs for dependent happenings." Epidemiology. 1991;2(5):331-338.
- Halloran ME, Struchiner CJ. "Causal inference in infectious diseases." Epidemiology. 1995;6(2):142-151.

## Cleanest verbal restatement in the literature (VERIFIED verbatim)
Imai K, Jiang Z, Malani A. "Causal Inference With Interference and Noncompliance in Two-Stage Randomized Experiments." J Am Stat Assoc. 2021;116(534):632-644. Their **Assumption 6 (Stratified interference)**:
> "Hudgens and Halloran (2008) relied upon the stratified interference assumption that the outcome of one unit depends on the treatment assignment of other units only through the number of those who are assigned to the treatment condition within the same cluster. In other words, what matters is the number of units rather than which units are assigned to the treatment condition."

## DOCUMENTED MIS-CITATION (useful example of loose usage)
Buchanan AL et al. "Disseminated Effects in Agent-Based Models..." Am J Epidemiol. 2021;190(5):939-948 (PMC8096482) **swaps the attributions**: it cites ref 13 = Hudgens & Halloran 2008 for *partial* interference and ref 39 = Sobel 2006 for *stratified* interference. Reference-list numbers verified directly. Historically backwards.

Buchanan also states stratified interference in terms of the **proportion** treated ("their own intervention assignment and the proportion of those randomized to the intervention in their component"), whereas HH2008 states it in terms of the **number** k. Equivalent only when cluster size is fixed.

## Epi-audience terminology signal
Benjamin-Chung J, Arnold BF, Berger D, Luby SP, Miguel E, Colford JM Jr, Hubbard AE. "Spillover effects in epidemiology: parameters, study designs and methodological considerations." Int J Epidemiol. 2018;47(1):332-347. Foregrounds "partial interference"; recommends "spillovers" or "indirect effects" as the terms to use. "Stratified interference" is not the headline term in this epi review — it is a narrower technical assumption.

## Manski's hierarchy — the closest neighbour (VERIFIED verbatim from cemmap draft)
Manski CF. "Identification of treatment response with social interactions." Econometrics Journal. 2013;16(1):S1-S23. Under **Assumption CTR (constant treatment response)**, c_j(t_J) = c_j(s_J) ⟹ y_j(t_J) = y_j(s_J); the level sets C_j are the person's **"effective treatments"**. Then a strict nesting:
1. **interactions within reference groups** ≈ partial interference
2. **Anonymous interactions** (§2.3.1): "the outcome of person j is invariant with respect to permutations of the treatments received by other members of his group." His example: "each child's illness outcome may depend on his own vaccination treatment and on the number of children vaccinated in his school, but not on the identities of the other schoolmates vaccinated." **This is exactly HH's stratified interference.**
3. **Distributional interactions** (§2.3.2): "strengthens an anonymous one by supposing that treatment response is invariant with respect to the size of the reference group *and* to permutations" — outcome varies with own treatment and the **empirical distribution (fraction)** of others' treatments.
4. **Functional interactions** (§2.3.3): depends only on a functional of that distribution (e.g. the mean).

**CRITICAL PRECISION POINT:** stratified/anonymous = invariance to *which* others (number treated, group size fixed). Stating it in terms of the **proportion** treated is Manski's *distributional* interaction, which is strictly STRONGER because it also imposes invariance to cluster size. Papers that gloss stratified interference as "depends on the proportion" (Buchanan 2021; Halloran & Hudgens 2016) are being loose whenever cluster sizes vary.

Liu & Hudgens 2014 JASA explicitly equate the two, verbatim: "Assumption (1) has been referred to as `stratified interference' (Hudgens and Halloran 2008) and `anonymous interaction' (Manski 2012)."

## Exposure mappings (VERIFIED verbatim, arXiv:1305.6156v4)
Aronow PM, Samii C. "Estimating average causal effects under general interference, with application to a social network experiment." Ann Appl Stat. 2017;11(4):1912-1947. "We define an exposure mapping as a function that maps an assignment vector and unit-specific traits to an exposure value: f : Ω × Θ → Δ." And explicitly: "The exposure mapping construction is functionally equivalent to the 'effective treatments' function used by Manski (2013)." They recast HH2008 as an exposure mapping where "θi would be unit i's group index."

So the nesting is: **stratified interference = the special case of an exposure mapping / effective treatment whose value is (own treatment, number treated in own cluster).**

Related: Sävje F. "Causal inference with misspecified exposure mappings: separating definitions and assumptions." Biometrika. 2024;111(1):1-15. Sävje F, Aronow PM, Hudgens MG. "Average treatment effects in the presence of unknown interference." Ann Statist. 2021;49(2):673-701 (EATE — what you still estimate if the exposure mapping is wrong). Forastiere L, Airoldi EM, Mealli F. JASA 2021;116(534):901-918 ("neighbourhood interference assumption"). Athey S, Eckles D, Imbens GW. "Exact p-Values for Network Interference." JASA 2018;113(521):230-240.

## BEST single bridge citation (VERIFIED verbatim)
Basse GW, Feller A, Toulis P. "Randomization tests of causal effects under interference." Biometrika. 2019;106(2):487-494. doi:10.1093/biomet/asy072. Links all three vocabularies in one sentence:
> "Second, we make the stratified interference assumption (Hudgens and Halloran, 2008): unit i's potential outcomes only depend on the number of units treated in the household ... rather than the precise identity of the treated unit. Manski (2013) calls this the anonymous interactions assumption. ... These two assumptions can be expressed by the exposure mapping h_i(Z) = (Z_i, W_[i])."

For "special case of an exposure mapping" language, cite Basse/Feller/Toulis 2019 or Bargagli-Stoffi FJ, Tortù C, Forastiere L. Ann Appl Stat. 2025;19(1):28-55 ("...which are special cases of the clustered network interference assumption"). NOT Aronow & Samii: they only say HH is "conceptually similar to" their Conditions 1-2, and "stratified" appears exactly once in their whole paper.

## Composition of the two assumptions (VERIFIED verbatim)
Sävje, Aronow & Hudgens 2021 Ann Statist 49(2):673-701: "The assumption is known as partial interference ... While partial interference allows for some progress on its own, it is often coupled with stratified interference. The additional assumption stipulates that the only relevant aspect of the interference is the proportion of treated units in the groups. The identities of the units are, in other words, inconsequential for the spillover effects."

## Manski's own comment on HH2008 (VERIFIED verbatim)
"...such as Hudgens and Halloran (2008). These authors, and others they cite, assume that the population partitions into a large number of symmetric reference groups, each of finite size."

## The assumption stated as a TESTABLE NULL
Athey S, Eckles D, Imbens GW. JASA 2018;113(521):230-240, **Hypothesis 7 (No Peer Effect Heterogeneity)**: "Y_i(w) = Y_i(w′) for all i, and for all pairs of assignment vectors w, w′ ∈ W such that Σ w_j·G_ij = Σ w′_j·G_ij." Exact randomization test. This is the answer to Liu & Hudgens' open problem ("Methods for assessing the stratified interference assumption are needed in future research"). Also Basse/Feller/Toulis 2019 Biometrika = randomization tests under interference.

## ATTRIBUTION TRAPS (verified)
- **"anonymous interference" is NOT Manski's phrase.** Manski writes "anonymous interactionS". The named assumption "Anonymous Interference" is Li S & Wager S, Ann Statist. 2022;50(4):2334-2358, Assumption 3, and it is **fraction**-based (= Manski's *distributional* tier, not his anonymous tier). Sussman & Airoldi and others mis-attribute it to Manski.
- **"exchangeable interference" has no established usage** (0 hits across ~50 full texts). Using it would be coining. Nearest real usage: Qu, Xiong, Liu & Imbens, "the fully exchangeable assumption (Hudgens and Halloran (2008) calls this stratified interference)."
- **"symmetric interference" is not a term of art.**
- **Do NOT cite Ogburn & VanderWeele (Statist Sci. 2014;29(4):559-578) for exchangeable interference.** Their taxonomy is about MECHANISM: "direct interference", "interference by contagion" ("a pathway mediated by the outcome of the exposed individual"), "allocational interference". Ward transmission = interference by contagion.
- **Forastiere et al. 2021 "neighbourhood interference" and Leung 2022 are LOCALITY assumptions, not anonymity ones.** Forastiere verbatim: "G_i can be any function of treatment vector in the neighborhood Z_N_i, even the identity function." Do not equate them with stratified interference.

## The exchangeability critique (relevant to wards)
Leung, arXiv:2403.08183 (preprint): "A common assumption in the CRT literature is stratified interference ... However this is restrictive because it presumes units are exchangeable within cluster." Directly applicable: colonized vs non-colonized patients in a ward are NOT exchangeable.

## If the assumption is WRONG, the estimator does not break
Aronow & Samii §8, Condition 7 (Misspecification): the HT estimator "is unbiased for the population mean of what Hudgens and Halloran (2008, p. 834) refer to as the 'individual average potential outcome'". Sävje Biometrika 2024: exposure mappings fill two roles (capturing what is interesting vs encoding causal structure) and only the second requires correct specification. So misspecification shifts the estimand rather than invalidating the estimator.

## Prevalence (Europe PMC full-text counts, 2026-07)
"partial interference" ~493 hits vs "stratified interference" ~31 (29 genuine). Roughly 1/3 as common, but growing (most since 2019). It HAS outcompeted Manski's "anonymous interaction" and Barkley's "clustered interference".

## Who uses the term (VERIFIED verbatim by subagent)
USE it as a named/numbered assumption: Tchetgen Tchetgen & VanderWeele 2012 (SMMR 21(1):55-75, their Assumption 2, then relax it — that relaxation is their headline contribution); Liu & Hudgens 2014 (JASA 109(505):288-301, unnumbered, notes it is also Manski's "anonymous interaction"); Basse & Feller 2018 (JASA 113(521):41-55, Assumption 2, keeps HH's name but renames partial interference "No Interference Across Household"); Imai/Jiang/Malani 2021 (Assumption 6); Rigdon & Hudgens 2015 (Stat Prob Lett 105:130-135); Miles/Petersen/van der Laan 2019 (Biometrics 75(3):768-777); Lee et al 2023 (AoAS 17:2165-2191, Assumption 6); McNealis/Moodie/Dean 2024 (JRSS-C 73:715-734); Kilpatrick/Lee/Hudgens 2024 (Stat Med 43:2853-2868 — introduces **"weak stratified interference"** because plain SI "might be unrealistic in some settings").

DO NOT use it (partial interference only): Perez-Heydrich et al 2014 Biometrics 70(3):731-741 (cholera — zero "stratified" hits); Halloran & Hudgens 2012 IJB; Saul & Hudgens 2017 JSS (inferference package); Papadogeorgou/Mealli/Zigler 2019 Biometrics.

NAME IT ONLY TO DECLINE IT: Baird/Bohren/McIntosh/Özler 2018 REStat 100(5):844-860; Barkley et al 2020 AoAS 14(3):1432-1448 (which instead coins "clustered interference" for partial interference).

## Documented loose/inconsistent usage (beyond Buchanan 2021)
- Chusyd et al, Nature Aging 2022;2:1101-1111 (PMC10099485) glossary **defines "stratified interference" as partial interference** — both halves misassigned.
- VanderWeele/Tchetgen Tchetgen/Halloran 2014 Stat Sci 29(4):687-706 writes "stratified **inference**" (typo) in the very sentence that defines it; typo present in both arXiv and PMC.
- Lee et al 2023 and Bargagli-Stoffi et al 2025 mis-attribute partial interference to HH2008 / stratified interference to Sobel.
- Semantic drift: in the network literature (Lee 2023, McNealis 2024) "stratified interference" now labels an exposure mapping over nearest NEIGHBOURS, treated as synonymous with Forastiere's "neighbourhood interference" — no longer HH's partition-based Assumption 2.

## Related
- Type A (fixed proportion) vs Type B (independent Bernoulli α) allocation parameterizations: VanderWeele TJ, Tchetgen Tchetgen EJ. "Effect partitioning under interference in two-stage randomized vaccine trials." Stat Probab Lett. 2011;81(7):861-869. Relevant because stratified interference sits naturally with Type A (fixed number treated); the α-indexed average potential outcomes Ȳij(z, α) are a DIFFERENT object obtained by averaging over the assignment distribution.
- See [[2sr-interference-assumptions]] and [[2sr-denominator-causal-verdict]].
