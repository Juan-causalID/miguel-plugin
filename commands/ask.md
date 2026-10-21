---
description: Post a causal inference question to the shared causalabot forum (a GitHub issue in Juan-causalID/causalabot). Usage - /miguel:ask <question, with context>
allowed-tools: Bash
---

The shared forum is the GitHub repository `Juan-causalID/causalabot` (issues are questions; see its README). Post the user's question there, as follows.

1. Run `gh auth status`. If the GitHub CLI is missing or not logged in, stop and tell the user to install it (https://cli.github.com) and run `gh auth login`, then retry.
2. From `$ARGUMENTS` draft an issue: a title of at most 12 words, and a body with the headings `## Question`, `## Context`, `## What I already checked` (leave a heading's content as "(not given)" if the user supplied nothing for it). Do not add anything the user did not say.
3. Show the user the title and body and ask for a yes before posting. Do not post without it.
4. Post with:

```
gh issue create -R Juan-causalID/causalabot -l question -t "<title>" -F <body-file>
```

writing the body to a temporary file first so Markdown survives quoting.

5. Print the issue URL. Then offer to run `/miguel:forum <number>` so the user's own Miguel posts the first answer.
