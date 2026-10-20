---
name: Competing events causal framework
description: Key papers and results on total effect vs controlled direct effect in competing events settings, including pregnancy-specific applications
type: reference
---

Key papers in Zotero collection (causalab_selected_plus_miguel_exhaustive):

1. **Young JG, Stensrud MJ, Tchetgen Tchetgen EJ, Hernan MA (2020)**. "A causal framework for classical statistical estimands in failure-time settings with competing events." Statistics in Medicine. DOI: 10.1002/sim.8471
   - Foundational framework paper. Defines total effect and controlled direct effect (under elimination of competing events).
   - Total effect: compare Pr(Y_k^{a=1} = 1) vs Pr(Y_k^{a=0} = 1), where Y_k^a is set to 0 after the competing event.
   - Controlled direct effect: compare risks in a hypothetical world where competing events are eliminated.
   - Total effect identified from cause-specific hazards under standard exchangeability; direct effect requires additional cross-world independence assumption.

2. **Stensrud MJ et al. (2021)**. "A generalized theory of separable effects in competing event settings." Lifetime Data Analysis. DOI: 10.1007/s10985-021-09530-8
   - Extends to separable effects framework as alternative to controlled direct effects.

3. **Chiu YH, Stensrud MJ, Dahabreh IJ, Rinaudo P, Diamond MP, Hsu J, Hernandez-Diaz S, Hernan MA (2020)**. "The Effect of Prenatal Treatments on Offspring Events in the Presence of Competing Events." Epidemiology. DOI: 10.1097/ede.0000000000001222
   - Application to pregnancy: prenatal treatment effect on offspring events with pregnancy loss as competing event.

4. **Brown JP, Hernandez-Diaz S (2025)**. "Ending Pregnancy Ends Risks. Consistent Questions, Estimands, Estimates, and Interpretation in the Presence of Competing Events." Paediatric and Perinatal Epidemiology. DOI: 10.1111/ppe.70076
   - Directly addresses pregnancy as the setting: delivery/pregnancy loss as competing event for outcomes during pregnancy.

Local R implementation: `/Users/jug242/Documents/ClaudeTest/competing_events_analysis.R` (parametric g-formula for both estimands with bootstrap CIs).

## Verified citations (Crossref/PubMed, 2026-08-19)

- **Brown JP, Hernández-Díaz S.** Ending Pregnancy Ends Risks... Paediatr Perinat Epidemiol. **2026;40(2):173-176** (online 2025-09-24). DOI 10.1111/ppe.70076. Brown is FIRST author; drafts often reverse the order.
- **Stensrud MJ, Robins JM, Sarvet A, Tchetgen Tchetgen EJ, Young JG.** Conditional separable effects. JASA. **2023;118(544):2671-2683** (arXiv 2006.15681). For outcomes truncated by death; conditions on survival without cross-world strata.
- **Janvin M, Young JG, Ryalen PC, Stensrud MJ.** Causal inference with recurrent and competing events. Lifetime Data Anal. **2024;30(1):59-118**.
- **Rojas-Saunero LP, Young JG, Didelez V, Ikram MA, Swanson SA.** Considering questions before methods in dementia research... Am J Epidemiol. **2023;192(8):1415-1423**. Rojas-Saunero first, Swanson last.
- **Chen N, McGee EE, Nethery RC, Mucci LA, Dickerman BA.** Guideline-based physical activity and HRQoL among prostate cancer survivors (HPFS target trial emulation). Am J Epidemiol. **2026;195(4):966-974** (PMID 40462309). Truncation-by-death exemplar.
- Stensrud et al. separable effects JASA paper: print 2022;117(537):175-183, but online 2020, preprint arXiv:1901.09472 (2019) — "generalized in Stensrud et al. 2021 (LDA)" reads anachronistic without noting this.

## Recurring corrections for this literature

- **Monotonicity alone does NOT point-identify the survivor average causal effect (SACE)** — it yields bounds/partial identification. Chiba & VanderWeele (AJE 2011;173:745-751) = sensitivity analysis under monotonicity (SACE = survivor contrast minus sensitivity parameter); the canonical large-sample **bounds are Zhang & Rubin (J Educ Behav Stat 2003;28:353-368)**. "Chiba-VanderWeele bounds" is a misattribution.
- **Separable effects identification = dismissible component conditions** (Stensrud 2022 JASA; generalized LDA 2021 allows partial isolation). Fail under unmeasured common causes of the two event types OR isolation violations. Under full isolation, A_D still affects the event of interest THROUGH the competing event — "influences only the competing event" is wrong phrasing.
- For truncation-by-death menus, don't forget **while-alive functionals** (days alive and out of hospital, QoL-days) as a coherent pragmatic option alongside composite/principal stratum/conditional separable effects.
- Excuse-variable device in IPW per-protocol analyses: strategy = "adhere until excusing event, then anything permitted"; post-excuse weight contribution **equals 1 by definition** (P(adherence)=1), not "set to 1" ad hoc; excusing event must be protocol-specified ex ante. Citation candidates: Murray & Hernán CDP papers (Clin Trials 2016; Trials 2018); Hernán & Robins NEJM 2017 discusses toxicity-permitting strategies but verify wording.
