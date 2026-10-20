---
name: recall-boundary-probe
description: Measured where my closed-book recall of papers fails (2026-10-20 probe, 30 items); medium-confidence plausible-prior substitution on mid/low-profile papers; Zotero corpus is 76% metadata-only
metadata:
  type: reference
---

Closed-book probe, 2026-10-20: 10 papers, 30 items, answers hashed before verification against the Zotero ft-cache.
- Famous papers 94%; mid-profile 78%; recent low-profile 50%; TARGET 2025 83%. High-confidence answers 9/9; low-confidence 21%.
- Fame, not date, sets the frontier. TARGET (Sept 2025) was known; Fu et al BMJ 2026 "Starting right", Nunez-Matthews BMJ Med 2025 and Humphreys Ann Epidemiol 2025 were not, beyond their titles.
- Errors were plausible priors at medium confidence:
  - Labrecque-Swanson 2018 names the **Hausman** over-identification test, not Sargan/Hansen.
  - Stensrud et al 2021 (LIDA, generalized separable effects): the data example is **SPRINT** (blood pressure and acute kidney injury), not prostate cancer DES. Under partial isolation, separable effects are "effects of modified treatments", not direct/indirect effects.
  - Humphreys 2025: prescription vs dispensation as assignment found **no clear numerical differences**.

**How to apply:** for any mid- or low-profile paper, grep the full text before stating its data example, named tests or findings. A correct gist from the title is not evidence that I know the paper.

Corpus facts: collection 26 has 616 items, 149 with PDF plus ft-cache, 0 abstracts, so 467 are title-only. Hernan and Robins 2016 "Using Big Data" and Hernan 2016 "Specifying a target trial" are metadata-only. Fallback when the Zotero MCP fails: copy zotero.sqlite, then collectionItems → itemAttachments.key → ~/Zotero/storage/<key>/.zotero-ft-cache. See [[stratified-interference-naming]] for a memory-corrected attribution.

**Verified anchors (2026-10-20, via lookup.sh grep on the ft-cache):**
- Labrecque and Swanson 2018, section "Settings with Multiple Proposed IVs" (p. 218): "the Hausman over-identification test in which all proposed instruments are regressed on the residuals of a regression of the outcome on the exposure. It can identify whether at least one of the proposed instruments used is invalid but cannot identify which [4]. Moreover, it cannot detect which condition is violated among conditions (2), (3), or (4h). Such a test is especially underpowered and may not valid for weak instruments [44]." All multi-IV methods rely on homogeneity (4h).
- Stensrud et al 2021 LIDA: Sect 7.2 "Data example: blood pressure therapy and acute kidney injury" (SPRINT, age >75, AKI vs death; AY separable effect 0.00 at 30 months when aD=1). Abstract: "separable effects can still be meaningfully interpreted as effects of modified treatments, even when they cannot be regarded as direct and indirect effects." Sect 5.2/5.3 define AY and AD partial isolation (condition (6) without (7), and vice versa); the non-isolated component's separable effect then mixes direct and indirect pathways. Prostate cancer DES is only the Appendix A recap of Stensrud 2020.
- Dib et al 2025 PPE (title-only; PubMed abstract): simulation, null effect, 500 datasets of n=10,000, two censoring mechanisms (LTFU, competing events); compares IPW, IV, sibling comparison. Conclusion: bias in all three generally away from the null, same direction, similar size; IV meaningfully more biased under strong treatment-censoring association (up to 2 pp); triangulation across approaches "may lead to invalid interpretations in the presence of selection processes."
