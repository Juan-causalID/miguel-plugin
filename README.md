# Miguel: a literature-grounded causal inference subagent for Claude Code

Miguel answers causal inference and epidemiology methodology questions grounded in a curated corpus of about 670 papers connected to CAUSALab (Harvard T.H. Chan School of Public Health), plus the Hernán and Robins textbook *Causal Inference: What If*. Every claim it attaches to a paper carries a provenance tag:

```
[verified: Author Year, location]   read in this session, location given
[memory: note-name]                 from a stored verbatim quotation
[recalled, unverified]              pretraining recall, with what would verify it
[synthesis]                         derived from an established framework
```

It is a prompt-defined subagent (not a fine-tuned model) with three layers of knowledge: the base model's recall, on-demand retrieval over the corpus, and a persistent memory of verified quotations. A closed-book probe (`eval/2026-10-20/`) showed why retrieval is mandatory: recall was 94% accurate on famous papers, 78% on mid-profile ones and 50% on recent low-profile ones, and every error was a plausible guess rather than an obvious fabrication.

## Install

```
claude plugin marketplace add Juan-causalID/miguel-plugin
claude plugin install miguel@miguel-plugin
```

Then, in any Claude Code session:

```
/miguel:setup                 builds the local corpus in ~/.claude/miguel-corpus (a few minutes)
/miguel:setup --seed-memory   also copies the shipped methodology notes into Miguel's memory
```

Requirements: Python 3.9 or newer (standard library only), network access to PubMed and Europe PMC. PyMuPDF is optional (used by the quote audit to read PDF editions).

## Getting the full corpus

Out of the box, setup gives you every item's metadata, PubMed abstracts for most, and full text for the papers available through Europe PMC (roughly 60 at the time of writing). The PDFs of the other papers live in the Zotero group library **Causal ID**. Ask the maintainer for an invitation, let Zotero sync the collection `causalab_selected_plus_miguel_exhaustive` (and its PDFs, if group file storage is enabled), then rerun `/miguel:setup`: Zotero's own full-text cache is picked up automatically.

## Using Miguel

Ask Claude Code a methodology question and it will delegate to `miguel:miguel-causal-inference` when appropriate, or address it directly ("ask Miguel whether stabilized weights are valid with dynamic regimes"). Miguel searches the corpus before stating specifics:

```
miguel-lookup search "stabilized weights dynamic strategies"     ranked passages across the whole corpus
miguel-lookup passage QGR6CQV5 801                                one passage in full
miguel-lookup find "Labrecque"                                    items by title, author or year
miguel-lookup grep LK675IK6 "Hausman" 2                           regex inside one paper
miguel-lookup abstract TFJ9JWSC                                   the PubMed abstract
```

The same commands are available as `scripts/lookup.sh` inside the plugin folder.

## What ships, what is built locally

| In the plugin (git) | Built on your machine (`~/.claude/miguel-corpus/`) |
|---|---|
| agent definition, scripts, this README | `fulltext/` texts fetched from Europe PMC |
| `corpus/items.tsv` metadata for 670 items | `search.sqlite` FTS5 index of all passages |
| `corpus/abstracts.tsv` PubMed abstracts | pointers to Zotero's PDF text cache, if present |
| `corpus/roster_former.txt` former CAUSALab members (for the refresh search) | |
| `seed-memory/` methodology notes with verified quotations (opt-in) | Miguel's own memory as it works |
| `eval/` probe protocol, a baseline run, and a survey of related projects | |

No PDFs or full texts are distributed.

## Maintenance scripts

| Script | Purpose |
|---|---|
| `scripts/refresh_candidates.py --since YYYY/MM/DD` | PubMed search for new papers by current and former CAUSALab members not yet in the corpus |
| `scripts/candidates_review.py DIR --keep A,B` | grouped review sheet and a RIS file to import into Zotero |
| `scripts/audit_memory_quotes.py` | checks every attributed quotation in Miguel's memory against the sources on disk |
| `scripts/needs_pdf.sh` | list of items still without full text, as PubMed links |

## Evaluation

`eval/README.md` describes the closed-book vs open-book probe: sealed answers (SHA-256) before any paper is opened, graded against the full text, reported by paper profile and by stated confidence. Rerun it after changing the agent definition or the model. `eval/related_work_2026-10-20.md` surveys comparable systems (PaperQA2, OpenScholar, CiteME, MedRAG and others) and the improvements they suggest.

## Notes

- The agent definition pins `model: fable`; change it in `agents/miguel-causal-inference.md` if your account lacks that model.
- Miguel writes only to its memory folder and the session scratchpad. It never writes to Zotero.
- The corpus was curated from OpenAlex and PubMed searches of CAUSALab authors (April 2026) and refreshed on 2026-10-20.
