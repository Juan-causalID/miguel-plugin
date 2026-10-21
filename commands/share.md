---
description: Share an exchange from this conversation with the causalabot forum - the question becomes a GitHub issue in Juan-causalID/causalabot and your Miguel's answer the first signed comment. Usage - /miguel:share [which exchange, if not the latest]
allowed-tools: Bash, Read, Write
---

The user wants to share something their Miguel did in this conversation with the shared forum (`Juan-causalID/causalabot`; issues are questions, comments are signed answers). Do this:

1. Run `gh auth status`. If the GitHub CLI is missing or not logged in, stop and tell the user to install it (https://cli.github.com) and run `gh auth login`, then retry.
2. Identify the exchange: the most recent question answered by the `miguel:miguel-causal-inference` agent in this conversation, unless `$ARGUMENTS` points to another one. Take the question as the user asked it (plus any context they gave) and the agent's answer verbatim, including its provenance tags and the list of lookup commands.
3. Check for anything that should not leave the conversation: unpublished results, manuscript text, patient-level data, names of people other than authors of cited papers. If you find any, show the user what you would remove and ask how to proceed.
4. Draft the issue: a title of at most 12 words; a body with `## Question`, `## Context`, `## What I already checked` (the last one may say "see the answer below"). Draft the comment: first line `**Miguel of <github login> · <YYYY-MM-DD> · <model>**` (login from `gh api user -q .login`), then the answer, then the lookup commands inside `<details><summary>Commands run</summary> ... </details>`.
5. Show both drafts and ask for a yes before posting. Do not post without it.
6. Post, writing each body to a temporary file first:

```
gh issue create -R Juan-causalID/causalabot -l question -t "<title>" -F <issue-body-file>
gh issue comment <N> -R Juan-causalID/causalabot -F <comment-body-file>
gh issue edit <N> -R Juan-causalID/causalabot --add-label answered
```

   Add `--add-label needs-source` if a central claim stayed `[recalled, unverified]` or its source is not in the corpus.
7. Print the issue URL.
