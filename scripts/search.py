#!/usr/bin/env python3
"""Search the whole corpus (corpus/search.sqlite, built by build_search_index.py).

Usage:
    search.py "<query>" [-n 10] [--any] [--key KEY]     ranked passages, BM25
    search.py --show KEY N                              print passage N of item KEY in full

Query syntax: words are ANDed (stemmed, accent-insensitive); "quoted phrases"
match in order; trailing * is a prefix (confound*). --any ORs the terms instead.
Each hit prints: KEY | year author | source p.N | title, then a snippet with
the matches in [brackets]. Follow up with `lookup.sh grep KEY "<regex>"` or
`search.py --show KEY N` to read the passage before quoting it.
"""
import argparse
import os
import re
import shlex
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.environ.get("MIGUEL_CORPUS") or os.path.join(os.path.expanduser("~"), ".claude", "miguel-corpus")
DB = os.path.join(CORPUS_DIR, "search.sqlite")

ap = argparse.ArgumentParser()
ap.add_argument("query", nargs="?")
ap.add_argument("-n", type=int, default=10)
ap.add_argument("--any", action="store_true", help="OR the terms instead of AND")
ap.add_argument("--key", help="restrict to one item key")
ap.add_argument("--show", nargs=2, metavar=("KEY", "N"), help="print one passage in full")
args = ap.parse_args()

if not os.path.exists(DB):
    sys.exit(f"missing {DB}; run scripts/build_search_index.py")
con = sqlite3.connect(DB)

if args.show:
    key, n = args.show
    row = con.execute("select title, source, text from passages where key=? and n=?", (key, int(n))).fetchone()
    if not row:
        sys.exit(f"no passage {n} for {key}")
    print(f"{key} | {row[1]} p.{n} | {row[0]}\n\n{row[2]}")
    sys.exit(0)

if not args.query:
    ap.print_help(); sys.exit(1)

def fts_term(tok):
    if re.fullmatch(r"[\w]+\*?", tok):
        return tok
    return '"' + tok.replace('"', '""') + '"'   # phrase, or a token with punctuation

terms = [fts_term(t) for t in shlex.split(args.query)]
match = (" OR " if args.any else " ").join(terms)
sql = """select key, year, author, title, source, n,
                snippet(passages, 6, '[', ']', ' … ', 28), bm25(passages, 0, 0, 0, 2.0, 0, 0, 1.0) as score
         from passages where passages match ?"""
params = [match]
if args.key:
    sql += " and key=?"; params.append(args.key)
sql += " order by score limit ?"; params.append(args.n)
try:
    rows = con.execute(sql, params).fetchall()
except sqlite3.OperationalError as e:
    sys.exit(f"query error: {e}\n(quote phrases, avoid stray punctuation)")
if not rows:
    print("no matches"); sys.exit(0)
for key, year, author, title, source, n, snip, score in rows:
    loc = "abstract" if source == "abstract" else f"{source} p.{n}"
    print(f"{key} | {year} {author} | {loc} | {title}")
    print("    " + re.sub(r"\s+", " ", snip))
