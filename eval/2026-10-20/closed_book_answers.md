# Closed-book answers (written BEFORE opening any full text)

Protocol
- Written 2026-10-20 by the Miguel agent before any full-text cache, PDF, or memory note was opened for these papers.
- What I had seen at this point: the Zotero title, year, and page count of the 149 PDF items (needed to choose papers). I had NOT seen author lists, journals, abstracts (the collection has none), or any body text. I did not open my memory notes.
- Each answer carries a stated confidence (H / M / L). Scoring rule fixed in advance: "confabulated" = wrong AND stated with H or M confidence; "wrong" = wrong with L confidence (a hedged guess); "partial" = core right but a checkable component wrong or missing; "correct" = all checkable components right.
- File hash recorded immediately after writing (see probe_results.md) so the answers cannot be silently revised.

Strata
- FAMOUS: very widely cited, almost certainly heavily represented in pretraining.
- MID: methods papers known to specialists.
- RECENT/OBSCURE: 2025-2026, near or past the pretraining frontier, low citation.

---

## P1. Causal Inference: What If (Hernan and Robins) [FAMOUS] (Zotero key ZNZQPZFC)

Q1.1 In Table 1.1 (Chapter 1), what are Zeus's two potential outcomes, and what are the population causal risks Pr[Y^{a=1}=1] and Pr[Y^{a=0}=1]?
A: Zeus has Y^{a=1}=1 and Y^{a=0}=0 (he dies under transplant, survives without it). Both population risks are 10/20 = 0.5, so the average causal effect is null even though individual effects exist. Confidence: H.

Q1.2 How is Chapter 3 ("Observational studies") organized: which three identifiability conditions, and in which section order?
A: Exchangeability, positivity, consistency. Sections roughly: 3.1 identifiability conditions; 3.2 exchangeability; 3.3 positivity; 3.4 consistency: first, well-defined interventions; 3.5 consistency: second, linking interventions to the data; 3.6 the target trial. Confidence: M for exact section numbering, H for the three conditions.

Q1.3 In Part II (Chapter 12, NHEFS smoking cessation and weight gain), what is the analytic sample size and the IP-weighted estimate of the average causal effect of quitting on weight gain?
A: 1629 cigarette smokers aged 25-74 (1566 uncensored with weight measured in 1982; 403 quitters). IP-weighted (marginal structural model) estimate 3.4 kg (95% CI 2.4 to 4.5). Unadjusted difference about 2.5 kg. Confidence: H.

## P2. A causal framework for classical statistical estimands in failure-time settings with competing events (2020) [FAMOUS] (key SKMN268Y)

Q2.1 Authors and journal?
A: Jessica G. Young, Mats J. Stensrud, Eric J. Tchetgen Tchetgen, Miguel A. Hernan. Statistics in Medicine, 2020 (vol 39, issue 8). Confidence: H.

Q2.2 What data example is used?
A: A randomized trial of diethylstilbestrol (DES, estrogen therapy) versus placebo in men with prostate cancer (Byar and Green data, Veterans Administration Cooperative Urological Research Group), event of interest prostate cancer death, competing event death from other causes. Confidence: H.

Q2.3 Which classical estimand corresponds to the total effect and which to the controlled direct effect?
A: The cause-specific cumulative incidence (subdistribution function / "risk" of the event of interest, competing events treated as events) contrast is a total effect. The "marginal cumulative incidence" (risk under a hypothetical intervention that eliminates the competing event, estimated by treating competing events as censoring with IPCW) contrast is a controlled direct effect. Hazard contrasts (cause-specific and subdistribution hazard ratios) are not causal contrasts even in an RCT, because they condition on survival. Confidence: H.

## P3. Principles of confounder selection (2019) [FAMOUS] (key VCM5AE5T)

Q3.1 Author(s) and journal?
A: Tyler J. VanderWeele (sole author). European Journal of Epidemiology, 2019, 34:211-219. Confidence: H.

Q3.2 State the "modified disjunctive cause criterion" as given in the paper.
A: Control for each covariate that is a cause of the exposure, or of the outcome, or of both; exclude from this set any variable known to be an instrumental variable; and include as a covariate any proxy for an unmeasured variable that is a common cause of both the exposure and the outcome. Confidence: H.

Q3.3 What prior paper does it credit for the (original) disjunctive cause criterion?
A: VanderWeele and Shpitser 2011, "A new criterion for confounder selection", Biometrics. Confidence: H.

## P4. On the definition of a confounder (2013) [MID] (key CDE64B5F)

Q4.1 Authors and journal?
A: Tyler J. VanderWeele and Ilya Shpitser. Annals of Statistics, 2013, 41(1):196-220. Confidence: H.

Q4.2 What definition of "confounder" do they propose?
A: A pre-exposure covariate C is a confounder if it is a member of some minimally sufficient adjustment set: there exists a set X of pre-exposure covariates such that the effect is unconfounded given (X, C) but not given any proper subset of (X, C). Confidence: M.

Q4.3 What additional named concept(s) do they introduce for variables that are not confounders but whose adjustment helps?
A: "Surrogate confounder" (a variable that is a proxy for a confounder, e.g., on a path from the confounder). Possibly also "confounding" defined separately from "confounder" (a confounder's absence does not imply no confounding). Confidence: M for "surrogate confounder".

## P5. Understanding the Assumptions Underlying Instrumental Variable Analyses: a Brief Review of Falsification Strategies and Related Tools (2018) [MID] (key SFA4NKUC)

Q5.1 Authors and journal?
A: Jeremy A. Labrecque and Sonja A. Swanson. Current Epidemiology Reports, 2018. Confidence: M.

Q5.2 Which falsification strategies are reviewed?
A: (i) the instrumental inequalities (Balke-Pearl / Pearl) for binary/discrete treatment; (ii) covariate balance across levels of the proposed instrument; (iii) over-identification tests with multiple instruments (Sargan / Hansen J); (iv) negative control outcomes or populations, including subgroups in which the instrument should not affect treatment ("zero first stage") so an IV-outcome association there signals exclusion or exchangeability violations. Confidence: M.

Q5.3 Which "related tool" for judging covariate imbalance across instrument levels, relative to imbalance across treatment levels, is discussed?
A: The bias component plot (Jackson and Swanson 2015, Epidemiology). Confidence: M.

## P6. A generalized theory of separable effects in competing event settings (2021) [MID] (key CVPIX76A)

Q6.1 Authors and journal?
A: Mats J. Stensrud, Miguel A. Hernan, Eric J. Tchetgen Tchetgen, James M. Robins, Vanessa Didelez, Jessica G. Young. Lifetime Data Analysis, 2021 (vol 27). Confidence: M.

Q6.2 What is the key generalization relative to the earlier separable effects paper (Stensrud et al., JASA)?
A: The earlier work assumed treatment decomposes into components A_Y and A_D, each affecting only one event (full isolation). The generalized theory relaxes this: components may affect both events through different pathways, with "partial isolation" conditions (A_Y partial isolation and A_D partial isolation), allowing separable effects to be interpreted as direct/indirect-type effects under weaker assumptions; the identification formula is shown to hold under these conditions. Confidence: M.

Q6.3 What data example is used?
A: The same prostate cancer DES trial as Young et al 2020 (estrogen therapy with a component affecting cardiovascular death). Confidence: L.

## P7. Starting right: aligning eligibility and treatment assignment at time zero when emulating a target trial (2026) [RECENT/OBSCURE] (key DFFK4VU6)

Q7.1 Authors and journal?
A: Guess: Miguel A. Hernan with coauthors (possibly Sauer, Hernandez-Diaz, Platt, Shrier lineage); journal possibly BMJ or Annals of Internal Medicine (research methods format). Confidence: L.

Q7.2 What is the main argument?
A: Time zero must coincide with the moment eligibility is met and treatment is assigned (and follow-up starts). Misalignment produces avoidable biases: eligibility determined using post-assignment information, or assignment determined after eligibility/follow-up begins, creates immortal time bias and selection bias (prevalent users). Confidence: M (generic; the title nearly implies this).

Q7.3 What solutions are proposed when an individual meets eligibility at multiple times or treatment strategies are not distinguishable at time zero?
A: Emulating a sequence of nested trials (one per eligible time, e.g., each month), or choosing one eligible time (e.g., first or random); and cloning with censoring and IP weighting (clone-censor-weight) when strategies are indistinguishable at time zero (e.g., grace periods). Confidence: M.

## P8. Detection bias and the role of negative control outcomes (2025) [RECENT/OBSCURE] (key CGA3RHYB)

Q8.1 Authors and journal?
A: Guess: an epidemiology methods commentary, possibly in American Journal of Epidemiology or Epidemiology; authors unknown (possibly involving Lipsitch or Tchetgen Tchetgen lineage on negative controls). Confidence: L.

Q8.2 What is the main argument?
A: Negative control outcomes can detect detection bias (differential outcome ascertainment by exposure group, e.g., more medical contact among the exposed) only if the negative control outcome shares the same detection mechanism as the outcome of interest; an NCO that does not share the ascertainment process can be null even when detection bias is present, so NCO choice should be driven by the bias structure (U-comparability / shared detection pathway). Confidence: M.

Q8.3 Applied example?
A: Guess: vaccine effectiveness or a drug safety example where healthcare-seeking or testing intensity differs by exposure. Confidence: L.

## P9. The definition of treatment assignment in observational emulations of target trials: an empirical examination (2025) [RECENT/OBSCURE] (key 7X49WYUR)

Q9.1 Authors and journal?
A: Guess: an applied group associated with the CAUSALab / target trial literature; journal possibly American Journal of Epidemiology or Epidemiology. Confidence: L.

Q9.2 What is compared?
A: Alternative operational definitions of treatment assignment (for example, prescription versus dispensing/fill date, or initiation within a grace period versus at a single date) and how the choice changes effect estimates in an emulated trial. Confidence: L.

Q9.3 Conclusion?
A: Estimates are sensitive to the assignment definition; the definition should mirror what would be assigned in the target trial (e.g., prescription as the analog of randomized assignment for an intention-to-treat analog), and should be prespecified. Confidence: L.

## P10. Transparent reporting of observational studies emulating a target trial: the TARGET Statement (2025) [RECENT/HIGH-PROFILE] (key XNNN9V76)

Q10.1 Journal(s) and first author?
A: Published simultaneously in JAMA and BMJ (2025); first author Aidan G. Cashin; senior/key authors include Harrison J. Hansford, Miguel A. Hernan, James H. McAuley. Confidence: M.

Q10.2 How many checklist items?
A: 21 items. Confidence: M.

Q10.3 How are the checklist items organized?
A: Sections roughly following a paper (title/abstract, introduction, methods, results, discussion), with the methods requiring specification of the target trial protocol components (eligibility, treatment strategies, assignment, follow-up/time zero, outcomes, causal contrasts, analysis plan) and how each is emulated, typically in a two-column table. Confidence: M.
