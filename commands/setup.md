---
description: Build Miguel's local corpus (item index, PubMed abstracts, Europe PMC full text, search index). Add --seed-memory to copy the shipped methodology notes into Miguel's memory.
allowed-tools: Bash
---

Run Miguel's setup script and show its output to the user:

```
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh" $ARGUMENTS
```

Then summarize in three lines: how many items are indexed, how many have full text (Zotero PDFs vs Europe PMC) and abstracts, and whether a Zotero collection was found. If no Zotero collection was found, say that the corpus currently holds the shipped metadata, PubMed abstracts and Europe PMC texts only, and that joining the "Causal ID" Zotero group (README) adds the PDFs' text after a rerun of this command.
