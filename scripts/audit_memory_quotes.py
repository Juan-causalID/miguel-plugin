#!/usr/bin/env python3
"""Audit the quotations in Miguel's memory notes against the sources on disk.

Every quoted string of at least MIN_WORDS words in the memory directory is
normalized (case, accents, punctuation, line-end hyphenation) and searched in:
  * every full text and abstract in corpus/items.tsv
  * every What If PDF found under ~/Documents and in the Zotero copy (text via PyMuPDF)
A quote is "found" on an exact normalized match, "near" when at least NEAR of
its 5-word shingles occur in one source (edition drift or light paraphrase),
otherwise "not found" (wrong, or from a source that is not on disk).

Usage:
    python3 audit_memory_quotes.py [--mem DIR] [--out report.md]
"""
import argparse
import csv
import datetime as dt
import glob
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.environ.get("MIGUEL_CORPUS") or os.path.join(os.path.expanduser("~"), ".claude", "miguel-corpus")
CORPUS = CORPUS_DIR
HOME = os.path.expanduser("~")
MIN_WORDS, NEAR = 6, 0.6

ap = argparse.ArgumentParser()
ap.add_argument("--mem", default=os.path.join(HOME, ".claude", "agent-memory", "miguel-causal-inference"))
ap.add_argument("--out", default=None)
args = ap.parse_args()


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)   # re-join hyphenated line breaks
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# ---- sources
sources = {}  # label -> normalized text
with open(os.path.join(CORPUS, "items.tsv"), newline="") as fh:
    items = list(csv.DictReader(fh, delimiter="\t"))
for r in items:
    if r["ftcache"] and os.path.exists(r["ftcache"]):
        with open(r["ftcache"], errors="replace") as fh:
            sources[f"{r['key']} {r['year']} {r['first_author']}: {r['title'][:60]}"] = norm(fh.read())
abs_path = os.path.join(CORPUS, "abstracts.tsv")
if os.path.exists(abs_path):
    with open(abs_path, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["abstract"]:
                sources[f"{r['key']} abstract"] = norm(r["abstract"])
try:
    import fitz
    pdfs = sorted(set(glob.glob(os.path.join(HOME, "Documents", "**", "hernanrobins_WhatIf_*.pdf"), recursive=True)))
    for p in pdfs:
        label = "What If " + re.search(r"WhatIf_([^.]+)", p).group(1)
        if label not in sources:
            sources[label] = norm("\n".join(page.get_text() for page in fitz.open(p)))
except ImportError:
    print("PyMuPDF not installed; What If editions under ~/Documents not checked")

# ---- quotes
QUOTE = re.compile(r"[“\"]([^”\"\n]{20,}?)[”\"]")
# a quote counts as attributed to a source when a citation-like marker sits within 200 characters of it
ATTRIB = re.compile(r"\b(19|20)\d{2}\b|What If|Technical Point|Fine Point|\bTP ?\d|\bFP ?\d|\bCh(apter)? ?\d|\bSect(ion)?\.? ?\d|\bp\. ?\d|et al", re.I)
notes = sorted(glob.glob(os.path.join(args.mem, "**", "*.md"), recursive=True))
results, unattributed = [], 0
for path in notes:
    if os.path.basename(path) in ("MEMORY.md", "INDEX.md"):
        continue
    text = open(path, errors="replace").read()
    for m in QUOTE.finditer(text):
        q = m.group(1).strip()
        nq = norm(q)
        if len(nq.split()) < MIN_WORDS:
            continue
        if not ATTRIB.search(text[max(0, m.start() - 200):m.end() + 200]):
            unattributed += 1   # a label, the user's words, or manuscript text under review; not a citation
            continue
        status, where = "not found", ""
        # is the cited source even on disk? look for "Surname ... 2016" style markers near the quote
        ctx = text[max(0, m.start() - 200):m.end() + 200]
        cited = {(a.lower(), y) for a, y in re.findall(r"([A-Z][\w'’-]+)(?:,? et al\.?| and [A-Z][\w'’-]+|,? & [A-Z][\w'’-]+)?,? \(?((?:19|20)\d{2})", ctx)}
        on_disk = any((a in r["first_author"].lower() or r["first_author"].lower().split()[-1] in a) and r["year"] == y
                      for a, y in cited for r in items if r["ftcache"]) if cited else True
        hits = [lab for lab, src in sources.items() if nq in src]
        if hits:
            status, where = "found", "; ".join(hits[:4])
        else:
            words = nq.split()
            shingles = [" ".join(words[i:i + 5]) for i in range(0, max(1, len(words) - 4))]
            best, best_lab = 0.0, ""
            for lab, src in sources.items():
                frac = sum(1 for s in shingles if s in src) / len(shingles)
                if frac > best:
                    best, best_lab = frac, lab
            if best >= NEAR:
                status, where = "near", f"{best_lab} ({best:.0%} of 5-word shingles)"
            elif not on_disk and not any("what if" in c for c in ctx.lower().split("\n")):
                status, where = "source not in corpus", ", ".join(f"{a} {y}" for a, y in sorted(cited))
        results.append((os.path.relpath(path, args.mem), q, status, where))

# ---- report
counts = {s: sum(1 for r in results if r[2] == s) for s in ("found", "near", "not found", "source not in corpus")}
out = args.out or os.path.join(os.getcwd(), f"quote_audit_{dt.date.today()}.md")
lines = [f"# Memory quote audit ({dt.date.today()})", "",
         f"{len(results)} attributed quotations of {MIN_WORDS}+ words in {len(notes)} notes, checked against {len(sources)} sources "
         f"(full texts, abstracts, What If editions on disk). {unattributed} further quoted phrases had no citation marker nearby and were skipped.", "",
         f"- found: {counts['found']}", f"- near (edition drift or paraphrase): {counts['near']}",
         f"- not found although the cited source is on disk (check these first): {counts['not found']}",
         f"- source not in corpus (cannot be verified locally): {counts['source not in corpus']}", ""]
for status in ("not found", "near", "source not in corpus", "found"):
    sel = [r for r in results if r[2] == status]
    if not sel:
        continue
    lines += [f"## {status} ({len(sel)})", ""]
    for note, q, _, where in sel:
        lines.append(f"- `{note}`: “{q[:140]}{'…' if len(q) > 140 else ''}”" + (f"  →  {where}" if where else ""))
    lines.append("")
open(out, "w").write("\n".join(lines))
print(f"{len(results)} quotes: {counts['found']} found, {counts['near']} near, {counts['not found']} not found -> {out}")
