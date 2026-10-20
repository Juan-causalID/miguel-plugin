# Miguel probe: closed-book vs open-book

A regression test for how much Miguel knows from recall versus retrieval. Run it after editing the agent definition, after a model upgrade, or after a large change to the corpus. Each run gets its own dated folder.

## Protocol

1. **Questions.** 30 questions over about 10 papers that have full text, stratified by profile: famous, mid-profile, recent low-profile. Each paper gets three questions: one bibliographic (authors, journal, year), one specific (named test, data example, numeric result, numbered assumption), one nuance (a claim the paper qualifies or rejects). Write them from the full text, not from memory. `questions_template.md` has the format. Questions written by someone other than the agent remove the self-selection bias noted in the 2026-10-20 run.
2. **Closed book.** Give Miguel the questions with the instruction: answer every question without opening any file, state a confidence (high, medium, low) for each, and save the answers to `closed_book_answers.md`. Hash the file (`shasum -a 256`) before step 3.
3. **Open book.** Miguel then opens the full text for each paper (`scripts/lookup.sh grep`), grades each answer as correct, partial, wrong, or confabulated (confident but false), and quotes the verifying passage into `probe_results.md`.
4. **Report.** Accuracy by stratum (partial = 0.5, plus a strict column), calibration by confidence level, count of confabulations, and the list of medium-confidence errors. Compare with the previous run.

## Runs

| Date | Model | Questions by | Famous | Mid | Recent low-profile | Overall | Notes |
|---|---|---|---|---|---|---|---|
| 2026-10-20 | Opus 5.5 (inherited) | Miguel (self-written) | 94% | 78% | 50% | 75% (strict 63%) | Baseline, pre-retrieval-rule. 0 confabulations. |
