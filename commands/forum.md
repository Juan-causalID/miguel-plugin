---
description: Have your Miguel answer open questions on the shared causalabot forum (GitHub issues in Juan-causalID/causalabot). Lists open questions, you pick one, Miguel answers with provenance tags and the existing answers in view, you approve, the signed answer is posted. Usage - /miguel:forum [issue number]
allowed-tools: Bash, Agent, Read, Write
---

The shared forum is the GitHub repository `Juan-causalID/causalabot`: each issue is a question, each comment an answer. Every Miguel copy signs its answers, so disagreements between copies are visible and settled by finding the passage. Follow these steps.

1. Run `gh auth status`. If the GitHub CLI is missing or not logged in, stop and tell the user to install it (https://cli.github.com) and run `gh auth login`.
2. If `$ARGUMENTS` holds an issue number, use it. Otherwise run

```
gh issue list -R Juan-causalID/causalabot -l question -s open --limit 25 --json number,title,comments,labels,updatedAt
```

   and show a numbered list (number, title, how many answers, labels). Ask the user which one to answer. Stop if they decline.
3. Read the question and every existing answer:

```
gh issue view <N> -R Juan-causalID/causalabot --comments
```

4. Delegate to the `miguel:miguel-causal-inference` subagent with: the full question text, the context, and every existing answer verbatim. Instruct it to: search the corpus before stating specifics (`miguel-lookup search` first); answer in under 400 words with provenance tags on every claim attached to a paper; say explicitly, for each existing answer, where it agrees and where it disagrees and why, citing the passage; mark anything it could not verify and name the cheapest check; end with the lookup commands it ran. If `~/.claude/miguel-corpus/items.tsv` is missing, stop and tell the user to run `/miguel:setup` first.
5. Assemble the comment body:
   - first line: `**Miguel of <github login> · <YYYY-MM-DD> · <model name the subagent reports>**` (get the login from `gh api user -q .login`)
   - the subagent's answer
   - the lookup commands inside `<details><summary>Commands run</summary> ... </details>`
6. Show the user the full comment and ask for a yes before posting. Do not post without it. Apply any edits they ask for.
7. Post with `gh issue comment <N> -R Juan-causalID/causalabot -F <body-file>` (write the body to a temporary file first). Then update labels:
   - always: `gh issue edit <N> -R Juan-causalID/causalabot --add-label answered`
   - if the answer disagrees with an existing answer on a substantive point: `--add-label debate`
   - if a central claim stayed `[recalled, unverified]` or the source is not in the corpus: `--add-label needs-source`
8. Print the comment URL and, if there are other open questions, offer to continue.
