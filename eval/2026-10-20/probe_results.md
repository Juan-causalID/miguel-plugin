# Closed-book vs open-book probe: results

## Integrity
- Closed-book answers: `closed_book_answers.md`, written before any full text or memory note was opened. SHA-256 `c82672cdbcf4d36e97429369fa81611a5d8844369db93bba9a36343704594c83`, hashed at 2026-10-20 13:02:30 EDT. A read-only copy (`closed_book_answers.locked.md`) still had the same hash after scoring.
- Verification sources: Zotero full-text caches (`~/Zotero/storage/<KEY>/.zotero-ft-cache`) for the body text, and the Zotero DB (read-only copy) for authors, journal, and DOI.
- Scoring rule (fixed in advance):
  - C (correct) = 1: every checkable part is right.
  - P (partial) = 0.5: the core is right, but a checkable part is wrong or missing.
  - W (wrong) = 0: wrong, with a hedged (L) confidence.
  - X (confabulated) = 0: wrong, stated with H or M confidence.
- Parts that cannot be checked in the local corpus are flagged "unverifiable here". They were not counted against the answer.

## Item-level scoring

| # | Paper (stratum) | Question | Conf | Score | Verifying passage (abridged, verbatim) |
|---|---|---|---|---|---|
| 1.1 | What If (FAMOUS) | Zeus potential outcomes, Table 1.1 risks | H | C | "Zeus has Y a=1 = 1 and Y a=0 = 0 because he died when treated but would have survived if untreated"; "Pr[Y a=1 = 1] = 10/20 = 0.5"; "the two counterfactual risks ... are equal to 0.5" |
| 1.2 | What If | Ch 3 structure | M | P | Sections "3.1 Identifiability conditions / 3.2 Exchangeability / 3.3 Positivity / 3.4 Consistency: First, define the counterfactual outcome / 3.5 Consistency: Second, link counterfactuals to the observed data / 3.6 The target trial". Numbering and order were right, but I paraphrased 3.4 as "well-defined interventions" and 3.5 as "linking interventions to the data". |
| 1.3 | What If | NHEFS n, IPW estimate | H | C | "1629 cigarette smokers aged 25-74 years ... Of these, 1566 individuals had their weight measured"; "403/1566"; "point estimate θ̂1 = 3.4"; "conservative 95% confidence interval around θ̂1 was (2.4, 4.5)"; crude "2.5" |
| 2.1 | Young et al 2020 (FAMOUS) | Authors, journal | H | C | Header: "Jessica G. Young, Mats J. Stensrud, Eric J. Tchetgen Tchetgen, and Miguel A. Hernán"; Zotero journal: Statistics in Medicine. Vol 39(8) is unverifiable here because the stored PDF is the arXiv v3 preprint. |
| 2.2 | Young 2020 | Data example | H | C | "a trial that randomly assigned estrogen therapy, Diethylstilbestrol (DES), or placebo to prostate cancer patients ... [Byar and Green, 1980 ...] ... the 125 patients in the high-dose estrogen therapy arm (A = 1) and the 127 patients in the placebo arm". The "VA Cooperative Urological Research Group" detail is unverifiable here. |
| 2.3 | Young 2020 | Estimand mapping | H | C | Table: "risk under elimination of competing events: marginal cumulative incidence, net risk"; "risk without elimination: subdistribution function, cause-specific cumulative incidence"; "contrasts of hazards when competing events exist do not generally have a causal interpretation"; "a controlled direct effect, that coincides with a contrast in estimands historically considered" |
| 3.1 | VanderWeele 2019 (FAMOUS) | Author, journal | H | C | "European Journal of Epidemiology ... Principles of confounder selection, Tyler J. VanderWeele". Vol 34, pp 211-219 is unverifiable here (the PDF header is a placeholder). |
| 3.2 | VanderWeele 2019 | Modified disjunctive cause criterion | H | C (verbatim) | "control for each covariate that is a cause of the exposure, or of the outcome, or of both; exclude from this set any variable known to be an instrumental variable; and include as a covariate any proxy for an unmeasured variable that is a common cause of both the exposure and the outcome" |
| 3.3 | VanderWeele 2019 | Credited source | H | C | "the 'disjunctive cause criterion' [9]"; ref 9 is "VanderWeele TJ, Shpitser I. A new criterion for confounder selection. Biometrics. 2011;67:1406-13." |
| 4.1 | VanderWeele and Shpitser 2013 (MID) | Authors, journal | H | C | "The Annals of Statistics 2013, Vol. 41, No. 1, 196-220 ... By Tyler J. VanderWeele and Ilya Shpitser" |
| 4.2 | VW-S 2013 | Proposed definition | M | C | "a pre-exposure covariate C for which there exists a set of other covariates X such that effect of the exposure on the outcome is unconfounded conditional on (X, C) but such that for no proper subset of (X, C) is the effect ... unconfounded given the subset" |
| 4.3 | VW-S 2013 | Additional concept | M | C | "we propose a variable that helps reduce bias but not eliminate bias be referred to as a 'surrogate confounder.'" |
| 5.1 | Labrecque and Swanson 2018 (MID) | Authors, journal | M | C | "Jeremy Labrecque & Sonja A. Swanson"; "(2018) 5:214-220"; Zotero: Current Epidemiology Reports |
| 5.2 | Labrecque-Swanson | Strategies reviewed | M | P | Table 1 lists over-identification, leveraging positive confounding, negative controls, MR-Egger, "Check in a subgroup where the instrument does not work", IV inequalities, covariate balance and bias component plots, instrument strength across covariates, and always-/never-taker counterfactuals. I got 5 of 9. I named the "Sargan / Hansen J" test where the text says "the Hausman over-identification test". |
| 5.3 | Labrecque-Swanson | Related tool | M | C | "Covariate balance and bias component plots [11•]"; ref 11 is "Jackson JW, Swanson SA ... Epidemiology. 2015 ... Describes bias component plots." |
| 6.1 | Stensrud et al 2021 (MID) | Authors, journal | M | C | "Lifetime Data Analysis (2021) 27:588-631 ... Mats J. Stensrud, Miguel A. Hernán, Eric J Tchetgen Tchetgen, James M. Robins, Vanessa Didelez, Jessica G. Young" |
| 6.2 | Stensrud 2021 | Key generalization | M | P | I named "AY partial isolation" and "AD partial isolation" correctly. But I said separable effects stay "direct/indirect-type". The paper says the opposite: they "can still be meaningfully interpreted as effects of modified treatments, even when they cannot be regarded as direct and indirect effects". Under AY partial isolation the AD separable effects "quantify both direct effects ... and indirect effects". I also left out the main contribution: identification allowing "time-varying common causes of the event of interest, the competing events and loss to follow-up". |
| 6.3 | Stensrud 2021 | Data example | L | W | "7.2 Data example: blood pressure therapy and acute kidney injury ... Systolic Blood Pressure Intervention Trial (SPRINT)". The prostate cancer DES trial is mentioned only as "the running example in Stensrud et al. (2020)". |
| 7.1 | Fu et al 2026 BMJ (RECENT) | Authors, journal | L | P | "Edouard L Fu, Michael O Harhay, Sebastian Schneeweiss, Rishi J Desai, Miguel A Hernán"; "RESEARCH METHODS AND REPORTING ... BMJ 2026;392:e084909". BMJ and Hernán were right; the coauthor "lineage" I guessed was entirely wrong. |
| 7.2 | Fu 2026 | Main argument | M | C | "These design biases can be avoided by synchronising eligibility and treatment assignment at the start of follow-up (time zero)", preventing "immortal time and selection bias" |
| 7.3 | Fu 2026 | Proposed solutions | M | C | "one option is to choose one of those times at random"; "we emulate a sequence of target trials with different starting points"; "design biases can be prevented by repeated use of the same individual through sequential trial emulation or cloning, respectively"; grace-period strategies are given as the example of indistinguishable strategies. (The "first eligible time" option I listed is not mentioned.) |
| 8.1 | Nunez and Matthews 2025 BMJ Med (RECENT) | Authors, journal | L | W | "Núñez I, Matthews AA. BMJMED 2025;4:e001336" |
| 8.2 | Nunez-Matthews | Main argument | M | C | Key messages: "An appropriate negative control outcome, however, must share the same unmeasured determinants of ascertainment as the outcome of interest" |
| 8.3 | Nunez-Matthews | Applied example | L | P | Three examples: surgical masks RCT, "Statins and diabetes" (target trial emulation; more healthcare contact leads to more screening), and a third observational one. COVID vaccine and influenza are used to illustrate NCO choice. My guess was a vague two-option hedge with one overlap. |
| 9.1 | Humphreys et al 2025 (RECENT) | Authors, journal | L | W | "Anna B.C. Humphreys, Anthony A. Matthews, ... Issa J. Dahabreh, Thomas Kahan, Miguel A. Hernán ... Annals of Epidemiology 108 (2025) 56-62" |
| 9.2 | Humphreys 2025 | What is compared | L | P | "the practical implications of using data on prescription versus dispensation as analogues of treatment assignment". My first option was right; the second (grace period) was wrong. |
| 9.3 | Humphreys 2025 | Conclusion | L | W | I claimed estimates are sensitive to the definition. The paper: "Effect estimates did not vary with the choice of prescription or dispensation data ... we found no clear numerical differences in effect estimates". My "prescription as assignment analogue" point does match "with prescription as the analogue of assigned treatment and dispensation as the analogue of received treatment ... arguably the preferred approach". |
| 10.1 | TARGET 2025 (RECENT, HIGH-PROFILE) | Journals, first author | M | C | "Aidan G Cashin, Harrison J Hansford, Miguel A Hernán ... James H McAuley"; "The TARGET Statement is being simultaneously published in The BMJ and JAMA" |
| 10.2 | TARGET | Number of items | M | C | "The 21-item TARGET checklist" |
| 10.3 | TARGET | Organization | M | P | "organized into six sections (abstract, introduction, methods, results, discussion, other information)". I missed "other information". My "typically in a two-column table" claim overstates the text, which says the specification "could be concisely formatted ... in a table ... but are not required to be". |

## Accuracy by stratum (C = 1, P = 0.5)

| Stratum | Papers | Items | C | P | W | X (confab.) | Score | Accuracy |
|---|---|---|---|---|---|---|---|---|
| Famous (What If, Young 2020, VanderWeele 2019) | 3 | 9 | 8 | 1 | 0 | 0 | 8.5/9 | 94% |
| Mid-profile methods (VW-Shpitser 2013, Labrecque-Swanson 2018, Stensrud 2021) | 3 | 9 | 6 | 2 | 1 | 0 | 7/9 | 78% |
| Recent, low profile (Fu 2026, Nunez-Matthews 2025, Humphreys 2025) | 3 | 9 | 3 | 3 | 3 | 0 | 4.5/9 | 50% |
| Recent, high profile (TARGET 2025) | 1 | 3 | 2 | 1 | 0 | 0 | 2.5/3 | 83% |
| **All** | **10** | **30** | **19** | **7** | **4** | **0** | **22.5/30** | **75%** |

## Accuracy by question type

| Question type | Famous + mid | Recent low profile |
|---|---|---|
| Bibliographic (authors, journal) | 5/5 C | 0/3 fully correct (1 P, 2 W) |
| Specific internal detail (table value, data example, verbatim definition, named test, finding) | 9/13 C (3 P, 1 W) | 0/3 C (2 P, 1 W) |
| "Main argument" / generic method content (inferable from title plus domain knowledge: 7.2, 7.3, 8.2) | n/a | 3/3 C |

## Calibration (stated confidence vs outcome)

| Confidence | Items | Score | Accuracy |
|---|---|---|---|
| H | 9 | 9/9 | 100% |
| M | 14 | 12/14 | 86% (10 C, 4 P) |
| L | 7 | 1.5/7 | 21% (0 C, 3 P, 4 W) |

## Interpretation
1. **Famous papers are memorized from pretraining, down to verbatim level.** The modified disjunctive cause criterion and the VanderWeele-Shpitser definition came back near-verbatim. What If table values and the NHEFS numbers (1629, 1566, 403, 3.4, 2.4 to 4.5) were exact. This knowledge exists without retrieval, so it cannot be credited to the Zotero pipeline.
2. **Recall degrades with fame, not only with date.** TARGET (Sept 2025) was known because it was heavily publicized. Fu et al (BMJ, Jan 2026) and two 2025 papers were not, even though all are inside or near the pretraining window. For low-profile papers, the base model knows the genre, not the paper.
3. **The "correct" recent-paper answers are title inference, not knowledge.** All 3 correct low-profile answers were main-argument or generic-method questions that a domain expert could reconstruct from the title. A probe that only asks "what is this paper about?" will make an ungrounded agent look grounded.
4. **The dangerous errors are plausible priors stated at medium confidence:**
   - Hausman vs Sargan/Hansen (5.2).
   - "Direct/indirect-type" vs "modified treatments" (6.2): a substantive misreading of the paper's own framing.
   - Reusing the DES example for the 2021 paper (6.3).
   - "Estimates are sensitive" (9.3): the paper found the opposite.

   Each one is what a paper of that kind would typically say, so the error is hard to spot.
5. **No outright confabulations were observed, and stated confidence was well calibrated.** But the test was easy on this dimension, because I wrote the questions myself (see Limitations). My memory notes record a real high-confidence error: I claimed stabilized IP weights are valid for dynamic regimes. What If Technical Point 21.2 says "Hence stabilized weights cannot be used with dynamic strategies" (verified in the What If cache during this audit). This kind of nuance error (a real rule applied to the wrong sub-case) is exactly what a bibliographic probe does not catch.

## Limitations of this probe (state them on the slide)
- **Question-selection bias.** I wrote the questions. Even without peeking, I chose questions I expected to answer, which tilts the famous and mid strata upward. A fairer design: a separate agent (or Juan) writes Q&A pairs from the full text. Miguel answers closed-book; a third party grades.
- **Small n.** 10 papers and 30 items. The stratum estimates are illustrative, not precise.
- **Partial-credit judgement calls:**
  - 1.2: paraphrased section titles.
  - 8.3 and 9.2: hedged multi-option guesses.

  Strict all-or-nothing grading gives 19/30 = 63% overall: 89% famous, 67% mid, 33% recent low profile, 67% TARGET.
- **Version mismatch.** Two stored PDFs are not the version of record (Young 2020 and VanderWeele-Shpitser 2013 are arXiv versions). Volume, issue, and page claims sometimes could not be verified locally.
