---
name: IV methodology references with verified content
description: Verified verbatim claims from the Hernan-Robins What If textbook Chapter 16 and other IV papers used in the HPV-sPTB project; safe to cite directly in this form
type: reference
---

All quotes below were verified against the actual paper or textbook text in this session.
Do not add quotation marks to claims not in this file unless re-verified.

## Hernan and Robins, "Causal Inference: What If" (Chapman and Hall/CRC, 2025; chapter 16, "Instrumental Variable Estimation")

Verified directly from the local PDF
(/Users/jug242/Documents/What if book/hernanrobins_WhatIf_21nov25.pdf, pages 217-225).

The three instrumental conditions (Section 16.1):
- "(i) Z is associated with A"
- "(ii) Z does not affect Y except through its potential effect on A"
- "(iii) Z and Y do not share causes"

Formal restatement (Technical Point 16.1):
- Condition (i) is the relevance condition: "non-null association between Z and A, or Z⊥⊥A does not hold." (The book uses the independence symbol; earlier versions of this note spelled it out as "Z independent of A".) [verified 2026-10-20: What If 2025 edition, Zotero copy, Technical Point 16.1]
- Condition (ii) is the exclusion restriction: "no direct effect of Z on Y." Individual-level form: Y^{z,a}_i = Y^{z',a}_i = Y^a_i for all z, z', all a, all individuals i.
- Condition (iii) is marginal exchangeability: Y^{a,z} independent of Z for all a, z.

Why three conditions are not enough (Section 16.3):
- "The three instrumental conditions (i)-(iii) are insufficient to ensure that the IV estimand is the average causal effect of treatment A on Y. A fourth condition, effect homogeneity (iv), is needed."
- Constant-effect homogeneity is "scientifically implausible for most treatments and outcomes, and impossible for dichotomous outcomes."

The fourth identifying condition under monotonicity (Section 16.4):
- Monotonicity holds when A^{z=1} >= A^{z=0} for all individuals.
- Under (i)-(iii) plus monotonicity (iv), "the usual IV estimand equals the average causal effect of treatment in the compliers, that is E[Y^{a=1} - Y^{a=0} | A^{z=1}=1, A^{z=0}=0]."
- "The 'compliers average causal effect' (CACE) is a local average treatment effect (LATE) in a subpopulation, not the global average causal effect in the entire population."

On observational settings:
- "However, monotonicity is harder to justify for some instruments proposed in observational studies." Example given: physician preference, where some patients are deniers under one physician but compliers under another. Cited to Swanson and Hernan 2014 and Swanson et al 2015b.

Surrogate-instrument warning (proof block in Section 16.4):
- "the interpretation of the IV estimand as the effect in the compliers is questionable in many applications of IV methods to observational data in which Z is at best a surrogate for U_Z."

ITT decomposition under monotonicity (proof block):
- The intention-to-treat effect can be written as a weighted average of the ITT in the four principal strata. Under condition (ii), ITT in always-takers and never-takers is zero. Under monotonicity, defiers do not exist. Hence
  E[Y^{z=1} - Y^{z=0}] = E[Y^{z=1} - Y^{z=0} | compliers] * Pr(compliers).
- And in compliers, the effect of Z on Y equals the effect of A on Y. So the IV ratio gives the LATE.

## Imbens and Angrist 1994, Econometrica 62(2):467-475
(Already verified in reference_did_methodology.md.) Theorem 1: under independence/exclusion plus monotonicity, the LATE is identified as E[Y_i(1) - Y_i(0) | D_i(z) - D_i(w) = 1].

## Angrist and Krueger 2001, JEP 15(4):69-85
(Already verified in reference_did_methodology.md.) The reduced form is unbiased under random assignment of Z, even with weak first stage.

## What is NOT directly verified in this session
- Hernan and Robins 2006 (Epidemiology 17:360-372): only the abstract and PubMed indexed terms accessible; full paper paywalled. The What If chapter 16 IS the canonical exposition in the Hernan-Robins corpus and explicitly cites the 2006 paper for the surrogate-instrument result (Section 16.4 proof block: "Hernan and Robins (2006b) proved that the average causal effect in the compliers (defined according to UZ) is also identified by the usual IV estimator"). Treat the 2006 paper as the foundational citation but anchor specific quotes to the What If textbook unless the 2006 paper is opened directly in a future session.
- Angrist, Imbens, Rubin 1996 JASA: not directly accessible (paywall and 403 from JASA host). The four-assumption framing (SUTVA, random assignment of instrument, exclusion restriction, monotonicity) is a well-known synthesis of this paper and the Imbens-Angrist 1994 framework. When citing AIR 1996, do not put quote marks on claims; cite for the general framework.
- Swanson and Hernan 2013 (Epidemiology 24:370-374): not directly accessible. Cite for the recommendation to report all four IV assumptions explicitly, but do not quote.
- Swanson et al 2018 JASA: not directly accessible. Cite for partial-identification / bounds approaches under weakening of monotonicity.
- Bound, Jaeger, Baker 1995 JASA: PDF returned in binary form. The weak-instrument amplification result is well-established; cite for the general orientation. For a verbatim anchor use What If instead: "Second, weak instruments amplify bias due to violations of conditions (ii) and (iii). A proposed instrument Z which is weakly associated with treatment A yields a small denominator of the IV estimator." [verified 2026-10-20: What If 2025 edition, Zotero copy ZNZQPZFC, Section 16.5 "The three instrumental conditions revisited", p. 221; also present verbatim in the 26apr24, 2jan25 and 21nov25 files]
- Baiocchi, Cheng, Small 2014 Statistics in Medicine: not directly accessible. Cite as a methodologic review.
- Hernan and Robins 2016 AmJEpidemiol (target trial): not directly accessible in this session, but the target-trial framework is well-established in the corpus and I have prior verified material on the seven protocol components from other Hernan papers (Hernan and Robins 2016 IS the seminal cite for this).

## How to apply
- For IV in the HPV-sPTB project, the safest verbatim citations are What If chapter 16 (for the three conditions, monotonicity, and LATE) and Imbens-Angrist 1994 (for the LATE theorem).
- When invoking exclusion restriction, monotonicity, or random-assignment-of-instrument, attach to What If chapter 16 plus AIR 1996 / Imbens-Angrist 1994 by name only.
- When discussing exclusion-restriction sensitivity in the presence of side channels (e.g., screening behavior, sex-ed curriculum), Swanson-Hernan 2013 is the right reporting citation; Swanson et al 2018 is the right citation for bounds when monotonicity is in doubt.

> Edition note (added 2026-10-20): What If quotes in this file were recorded without an edition stamp. Canonical copy for re-verification: the Zotero collection PDF (`~/Zotero/storage/ZNZQPZFC/`, 2025 edition); newest local file is `~/Documents/What if book/hernanrobins_WhatIf_21nov25.pdf`. Technical Point and Fine Point numbering can shift between editions. Re-check the quote and stamp the edition before reusing it.
