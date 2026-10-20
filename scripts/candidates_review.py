#!/usr/bin/env python3
"""Turn a refresh_candidates.py output folder into a grouped review sheet
(review.md with checkboxes and PubMed links) and, optionally, a filtered RIS.

Groups:
  A  core member is an author, causal vocabulary in title/abstract   (import by default)
  B  core member is an author, no causal vocabulary                  (check: applied or off-topic)
  C  other member, causal vocabulary                                  (check)
  D  other member, no causal vocabulary                               (usually skip)

Usage:
    python3 candidates_review.py DIR                 write DIR/review.md
    python3 candidates_review.py DIR --keep A,C      write DIR/import.ris with those groups
    python3 candidates_review.py DIR --drop 123,456  same, minus listed PMIDs
"""
import argparse
import csv
import os

ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("--keep", default=None, help="comma-separated groups to write to import.ris, e.g. A,C")
ap.add_argument("--drop", default="", help="comma-separated PMIDs to exclude from import.ris")
ap.add_argument("--add", default="", help="comma-separated PMIDs to include in import.ris regardless of group")
args = ap.parse_args()

rows = list(csv.DictReader(open(os.path.join(args.dir, "candidates.csv"), newline="")))
def group(r):
    core = "core-author" in r["keep_reasons"]
    causal = r["screen_pass"] == "True"
    return "A" if core and causal else "B" if core else "C" if causal else "D"
for r in rows:
    r["group"] = group(r)
titles = {"A": "Core member author, causal vocabulary (import by default)",
          "B": "Core member author, no causal vocabulary (applied or off-topic? check)",
          "C": "Other member, causal vocabulary (check)",
          "D": "Other member, no causal vocabulary (usually skip)"}

lines = [f"# CAUSALab refresh candidates ({os.path.basename(args.dir.rstrip('/'))})", "",
         f"{len(rows)} papers not yet in the Zotero causalab collections. Tick to keep; then run "
         f"`candidates_review.py {args.dir} --keep A,C --drop <pmids>` to write import.ris.", ""]
for g in "ABCD":
    sel = sorted((r for r in rows if r["group"] == g), key=lambda r: (r["year"], r["title"].lower()))
    lines += [f"## {g}. {titles[g]} ({len(sel)})", ""]
    for r in sel:
        who = r["roster_matches"]
        lines.append(f"- [ ] **{r['pmid']}** {r['year']} *{r['journal']}*. {r['title']} ({who}) "
                     f"<https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/>")
    lines.append("")
open(os.path.join(args.dir, "review.md"), "w").write("\n".join(lines))
print(f"review.md: " + ", ".join(f"{g}={sum(r['group']==g for r in rows)}" for g in "ABCD"))

if args.keep:
    keep = set(args.keep.split(",")); drop = {p.strip() for p in args.drop.split(",") if p.strip()}
    add = {p.strip() for p in args.add.split(",") if p.strip()}
    chosen = [r for r in rows if (r["group"] in keep or r["pmid"] in add) and r["pmid"] not in drop]
    with open(os.path.join(args.dir, "import.ris"), "w") as fh:
        for r in chosen:
            out = ["TY  - JOUR"] + [f"AU  - {a}" for a in r["authors"].split("; ")] + [
                f"TI  - {r['title']}", f"JO  - {r['journal']}", f"PY  - {r['year']}"]
            if r["doi"]:
                out.append(f"DO  - {r['doi']}")
            out += [f"AN  - PMID:{r['pmid']}", f"UR  - {r['url']}", f"AB  - {r['abstract']}"]
            out += [f"KW  - {n}" for n in r["roster_matches"].split("; ") if n] + ["ER  - ", ""]
            fh.write("\n".join(out) + "\n")
    print(f"import.ris: {len(chosen)} records")
