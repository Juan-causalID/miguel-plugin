---
name: sequential-trials-vs-ccw
description: Verified decision rule for sequential target trial emulation vs cloning-censoring-weighting (What If 2025 Ch 22.4 + FP 22.5; Fu 2026 BMJ Fig 3; Garcia-Albeniz 2026 head-to-head with assumption contrast and numbers)
metadata:
  type: reference
---

# Sequential trial emulation vs cloning + censoring + weighting (CCW)

Verified 2026-10-20 by grepping corpus full text (lookup.sh). Keys: What If = QGR6CQV5 (2025 corpus copy), Fu 2026 = X46P2G9Z, Garcia-Albeniz 2026 = J9CBLTAF.

## Decision rule (two distinct problems, two distinct fixes)

- **Multiple eligibility times -> sequential trials.** What If Ch 22.4 (page 316 of the 2025 copy): "Strategy c) requires emulating multiple sequential target trials, each of them with a different start of follow-up." Efficiency: "the sequential emulation strategy c) can be more efficient than the previous ones because it uses more of the available data. However, because individuals may be included in multiple target trials, appropriate adjustment of the variance of the effect estimate is required. This can be achieved by bootstrapping the entire analysis."
- **Strategies indistinguishable at time zero -> cloning.** What If Ch 22.4, same section: "Second, let us talk about how to tackle the impossibility of assigning a unique treatment strategy to each individual." CD4 500/350/200 example; "create two exact copies—clones—of each of these individuals in the data and assign each of the two clones to a different strategy. Clones are then censored at the time their data stop being consistent with the arm they were assigned to."
- **Not alternatives; combinable.** What If Ch 22.4: "The cloning + censoring + weighting procedure can be combined with sequential target trial emulation when the eligibility criteria can be met at multiple times." Fu 2026 (line 140 of cache): "When a person has multiple possible times zero and have data compatible with assignment to multiple strategies, sequential trial emulation can be combined with cloning."
- Fu 2026 BMJ Fig 3 decision diagram: "sequential trials are used to handle multiple eligibility times, cloning is used to handle indistinguishable strategies, and inverse probability (IP) weighting is used to adjust for time fixed and time varying confounders". Fu 2026 Key messages: "design biases can be prevented by repeated use of the same individual through sequential trial emulation or cloning, respectively".
- Fu 2026 lists indistinguishable-strategy cases: grace periods, "strategies that compare different treatment durations" and "dynamic strategies that mandate a treatment change when the individual develops some condition".

## Sequential emulation as a substitute for CCW (reformulate the question)

Garcia-Albeniz 2026 (GEMCAD 1401, mAb first vs second line, 8-week grace): two solutions to immortal time from misclassification: "cloning-censoring-weighting (CCW) [12, 13] and changing the causal question to make the treatment strategies distinguishable at time zero" (reformulated as "Initiate mAb concomitantly with first line chemotherapy", then a sequence of 8 weekly trials pooled).

Choice criterion (Discussion): "The preference of one approach vs. another should be based on whether changing the research question is clinically relevant, and on the strength of the identifying assumptions of each approach ... the CCW approach assumed exchangeability over the grace period conditional on baseline and time-varying variables, and the sequential emulation approach assumed baseline exchangeability in each of the 8 cohorts, conditional on baseline variables."

Numbers (abstract): CCW 4-year survival difference (second minus first line) 4.3% (-3.3%; 10.0%), RR 0.95 (0.88; 1.04). Sequential: -2.8% (-7.5%; 1.2%), RR 1.04 (0.98; 1.10). Sensitivity with 1-day intervals (56 trials): -2.3% (-5.9%; 2.5%), RR 1.03 (0.97; 1.09). Biased analysis 6-month RR 0.13 (0.03; 0.28).

Caveat in Garcia-Albeniz: weekly intervals in sequential emulation can themselves introduce immortal time if outcome risk within the interval is non-negligible (only those surviving the baseline week can initiate in that week); they checked with 1-day intervals.

Related: [[whatif-ccw-grace-period]], [[grace-period-estimand-distinction]] (CCW with grace period cannot estimate ITT; FP 22.5).
