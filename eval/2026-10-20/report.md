# How a literature-grounded causal inference agent works: an audit of "Miguel" (2026-10-20)

Sources: read-only copy of `~/Zotero/zotero.sqlite`, `~/Zotero/storage/`, `~/.claude/agent-memory/miguel-causal-inference/`. Zotero MCP failed (expired token), so local files only.

## 0. What Miguel is
- Prompt-defined subagent: `~/.claude/agents/miguel-causal-inference.md` (226 lines). Not fine-tuned; same base model as the main session.
- Three parts: persona plus methods checklist (question, target trial, identification assumptions, estimator, sensitivity); a "read the literature first" instruction pointing at a Zotero collection; typed persistent memory.
- Knowledge comes from three layers: pretraining, on-demand retrieval, curated memory.

## A. Access inventory (collection 26, `causalab_selected_plus_miguel_exhaustive`)
- 616 items (615 journal articles, 1 book: What If). DOI 612 (99.4%), PMID 615.
- Abstracts: 0. Notes: 0.
- PDFs: 149 (24.2%), all with a usable full-text index.
- Metadata only: 467 (75.8%).
- Full text: 2,919 pages, about 9.2 MB, roughly 2.3M tokens. What If alone is about 310k tokens.
- Missing PDFs include Hernan and Robins 2016 "Using Big Data", Hernan 2016 "Specifying a target trial", and Tchetgen Tchetgen and VanderWeele on interference. Of 356 Hernan-tagged items, 85 have a PDF.
- Recency: 15% of items and 21% of PDFs are from 2024 or later.
- Sibling collections (DOI overlap; Zotero copies, not links): 26 = 24 (all 371 DOIs) + 241 extra Hernan papers; 104 of 26's DOIs appear in no sibling. 25 (574) is inside 23 (1,438). 22 (493) is the base export. Only 26 has PDFs.
- In practice: load memory index, answer from pretraining by default, and when a claim needs a source or is challenged, query the DB, search the full text, and save the verified quote to memory. "Read everything first" is impossible.

## B. Closed-book vs open-book probe
- Method: 10 papers, 30 questions. Closed-book answers with stated confidence, hashed (SHA-256) before any paper was opened, then graded against full text.

| Stratum | Items | Accuracy (partial = 0.5) | Strict |
|---|---|---|---|
| Famous (What If; Young 2020; VanderWeele 2019) | 9 | 94% | 89% |
| Mid-profile (VanderWeele-Shpitser 2013; Labrecque-Swanson 2018; Stensrud 2021) | 9 | 78% | 67% |
| Recent, low profile (Fu 2026 BMJ; Nunez-Matthews 2025; Humphreys 2025) | 9 | 50% | 33% |
| Recent, high profile (TARGET 2025) | 3 | 83% | 67% |
| All | 30 | 75% | 63% |

- Calibration: high confidence 9/9, medium 86%, low 21%. No confident outright fabrications.
- Bibliographic facts: 5/5 for famous and mid papers, 0/3 fully right for recent low-profile papers.

Takeaways
1. Famous papers are in pretraining nearly verbatim (e.g., What If smoking-cessation numbers 1629/1566/403 and 3.4 kg, 95% CI 2.4 to 4.5). For them, retrieval adds verification, not knowledge.
2. Profile, not date, decides recall: TARGET (Sept 2025) known; Fu et al 2026 and two 2025 papers not.
3. "What is this paper about?" is a misleading test: correct answers on low-profile papers were reconstructible from the title.
4. The real failure mode is a plausible guess at medium confidence (Sargan/Hansen vs Hausman; separable effects as "direct/indirect-type"; DES vs SPRINT example; "sensitive" vs "no clear numerical differences"). This is paraphrase-to-citation drift.
5. Memory holds a past confident error a recall probe would miss: stabilized weights with dynamic regimes (What If Technical Point 21.2: "Hence stabilized weights cannot be used with dynamic strategies").

Limitations: agent wrote its own questions (tilts famous and mid strata upward); n = 30; partial-credit judgement calls; two stored PDFs are preprints.

## C. Memory
- 50 files (292 KB): 44 reference, 2 feedback, 2 project, 1 user, plus index. 36 files contain verbatim quotes (about 187 quote lines).
- Adds: verified quote anchors (What If Ch 21-22, DiD canon, interference); corrected attributions (stratified interference = Hudgens and Halloran 2008 Assumption 2; partial interference = Sobel 2006; Buchanan 2021 AJE swaps them); behaviour rules (`feedback_verified_citations.md`, `feedback_self_correction.md`).
- Guards against paraphrase-to-citation drift, which the probe shows is how the base model fails on mid and low-profile papers.
- Caveats: many verified quotes come from outside the Zotero collection; notes can go stale.

## D. Pipeline for others
1. Curate the collection with a documented inclusion rule.
2. Make it readable: attach PDFs, import abstracts, rebuild the full-text index, check for empty index files (scanned PDFs need OCR).
3. Access route: baseline is a copy of the local DB plus full-text cache files; optional Zotero MCP or Web API (tokens expire) or an exported folder.
4. Agent file: persona; methods checklist; on-demand retrieval rule; verification rule; stated knowledge boundary.
5. Memory: typed notes plus index; seeded citation-verification rule; quotes saved with section and version; optionally in git.
6. Evaluate: blinded, stratified closed-book then open-book probe with hashed answers and confidence labels; report accuracy by stratum and calibration; include nuance questions; re-run after model upgrades.

Pitfalls: metadata-only items; MCP login expiry; context limits; training leakage; title-inferable answers; preprint vs published mismatch; scanned PDFs; stale memory.
