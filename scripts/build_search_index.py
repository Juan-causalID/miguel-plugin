#!/usr/bin/env python3
"""Build corpus/search.sqlite: an SQLite FTS5 index of passages from every full
text and abstract listed in corpus/items.tsv, so Miguel can search the whole
corpus for a claim instead of grepping one paper at a time.

Rebuilt from scratch on every run (a few seconds). Standard library only; FTS5
is compiled into macOS's SQLite. The database is machine-local and gitignored.

Usage:
    python3 build_search_index.py
"""
import csv
import datetime as dt
import os
import re
import sqlite3
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.environ.get("MIGUEL_CORPUS") or os.path.join(os.path.expanduser("~"), ".claude", "miguel-corpus")
CORPUS = CORPUS_DIR
ITEMS = os.path.join(CORPUS, "items.tsv")
ABS = os.path.join(CORPUS, "abstracts.tsv")
DB = os.path.join(CORPUS, "search.sqlite")
CHUNK = 1500   # characters per passage, roughly two or three paragraphs
HARD = 3000    # a single paragraph longer than this is split


def passages(text):
    """Group paragraphs into passages of about CHUNK characters."""
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)          # re-join words hyphenated at line ends
    paras = [p.strip() for p in re.split(r"\n\s*\n|\n", text) if p.strip()]
    out, buf = [], ""
    for p in paras:
        pieces = [p[i:i + HARD] for i in range(0, len(p), HARD)] if len(p) > HARD else [p]
        for piece in pieces:
            if buf and len(buf) + len(piece) > CHUNK:
                out.append(buf); buf = ""
            buf = f"{buf}\n{piece}" if buf else piece
    if buf:
        out.append(buf)
    return out


with open(ITEMS, newline="") as fh:
    items = list(csv.DictReader(fh, delimiter="\t"))
abstracts = {}
if os.path.exists(ABS):
    with open(ABS, newline="") as fh:
        abstracts = {r["key"]: r["abstract"] for r in csv.DictReader(fh, delimiter="\t") if r["abstract"]}

if os.path.exists(DB):
    os.remove(DB)
con = sqlite3.connect(DB)
con.execute("""create virtual table passages using fts5(
    key UNINDEXED, year UNINDEXED, author UNINDEXED, title, source UNINDEXED, n UNINDEXED, text,
    tokenize='porter unicode61 remove_diacritics 2')""")
con.execute("create table meta(k text, v text)")

n_docs = n_pass = n_abs = 0
for r in items:
    base = (r["key"], r["year"], r["first_author"], r["title"])
    if r["key"] in abstracts:
        con.execute("insert into passages values (?,?,?,?,?,?,?)", base + ("abstract", 0, abstracts[r["key"]]))
        n_abs += 1
    path = r["ftcache"]
    if path and os.path.exists(path):
        with open(path, errors="replace") as fh:
            text = unicodedata.normalize("NFKC", fh.read())
        for i, p in enumerate(passages(text), start=1):
            con.execute("insert into passages values (?,?,?,?,?,?,?)", base + (r["ft_source"], i, p))
            n_pass += 1
        n_docs += 1
con.execute("insert into meta values ('built', ?)", (dt.datetime.now().isoformat(timespec="seconds"),))
con.execute("insert into meta values ('full_texts', ?)", (n_docs,))
con.execute("insert into meta values ('passages', ?)", (n_pass,))
con.execute("insert into meta values ('abstracts', ?)", (n_abs,))
con.commit(); con.close()
print(f"{n_docs} full texts -> {n_pass} passages, plus {n_abs} abstracts -> {DB} ({os.path.getsize(DB) // 1024} KB)")
