#!/usr/bin/env python3
"""Build or refresh <corpus>/items.tsv, the index Miguel's helpers read.

With Zotero installed (~/Zotero/zotero.sqlite) and the collection present, the
index is rebuilt from the database (a temporary copy, never the live file;
subcollections included). Without Zotero, or if the collection is absent, the
shipped items.tsv is kept and its full-text columns are re-pointed at whatever
text exists locally (Europe PMC texts fetched by fetch_pmc_fulltext.py).

Usage:
    python3 build_corpus_index.py [collection_name[,collection_name...]]
Environment:
    MIGUEL_CORPUS      data directory (default ~/.claude/miguel-corpus)
    MIGUEL_COLLECTION  default collection name(s)

Columns (tab separated): itemID, key, year, first_author, journal, doi, pmid,
pdf_key, ftcache, ft_bytes, ft_source, title. ft_source is "zotero" (cache of
an attached PDF), "europepmc" (text under <corpus>/fulltext/) or "none".
"""
import csv
import os
import re
import shutil
import sqlite3
import sys
import tempfile

HOME = os.path.expanduser("~")
ZOTERO = os.path.join(HOME, "Zotero")
CORPUS_DIR = os.environ.get("MIGUEL_CORPUS") or os.path.join(HOME, ".claude", "miguel-corpus")
OUT = os.path.join(CORPUS_DIR, "items.tsv")
FULLTEXT = os.path.join(CORPUS_DIR, "fulltext")
COLL = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MIGUEL_COLLECTION", "causalab_selected_plus_miguel_exhaustive")
HEADER = ["itemID", "key", "year", "first_author", "journal", "doi", "pmid", "pdf_key", "ftcache", "ft_bytes", "ft_source", "title"]


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


def local_text(key, pdf_key=""):
    """Best full text on this machine for an item: Zotero's cache, else Europe PMC text."""
    if pdf_key:
        ft = os.path.join(ZOTERO, "storage", pdf_key, ".zotero-ft-cache")
        if os.path.exists(ft) and os.path.getsize(ft) > 0:
            return ft, os.path.getsize(ft), "zotero"
    ft = os.path.join(FULLTEXT, f"{key}.txt")
    if os.path.exists(ft) and os.path.getsize(ft) > 0:
        return ft, os.path.getsize(ft), "europepmc"
    return "", 0, "none"


def write(rows, note):
    os.makedirs(CORPUS_DIR, exist_ok=True)
    rows.sort(key=lambda r: (r[2], r[3], r[11]))
    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\", lineterminator="\n")
        w.writerow(HEADER); w.writerows(rows)
    n_zot = sum(1 for r in rows if r[10] == "zotero"); n_epmc = sum(1 for r in rows if r[10] == "europepmc")
    print(f"{len(rows)} items | full text: {n_zot} Zotero + {n_epmc} Europe PMC = {n_zot + n_epmc} | "
          f"{sum(1 for r in rows if r[6])} with PMID | {note} -> {OUT}")


def relocalize(note):
    if not os.path.exists(OUT):
        sys.exit(f"no {OUT} and no Zotero collection to build it from; run the plugin's setup first")
    with open(OUT, newline="") as fh:
        rows = []
        for r in csv.DictReader(fh, delimiter="\t"):
            ft, nb, src = local_text(r["key"], r.get("pdf_key", ""))
            rows.append([r["itemID"], r["key"], r["year"], r["first_author"], r["journal"], r["doi"], r["pmid"],
                         r.get("pdf_key", ""), ft, nb, src, r["title"]])
    write(rows, note)


db_path = os.path.join(ZOTERO, "zotero.sqlite")
if not os.path.exists(db_path):
    relocalize("no Zotero on this machine; shipped index re-pointed at local text")
    sys.exit(0)

tmp = tempfile.mkdtemp()
db = os.path.join(tmp, "z.sqlite")
shutil.copy(db_path, db)
for suffix in ("-wal", "-journal"):  # recent writes may still sit in the journal
    if os.path.exists(db_path + suffix):
        shutil.copy(db_path + suffix, db + suffix)
con = sqlite3.connect(db)

names = [n.strip() for n in COLL.split(",") if n.strip()]
colls = [r[0] for r in con.execute(f"select collectionID from collections where collectionName in ({','.join('?' * len(names))})", names)]
if not colls:
    con.close(); shutil.rmtree(tmp, ignore_errors=True)
    relocalize(f"Zotero found but no collection named {COLL}; shipped index re-pointed at local text")
    sys.exit(0)
frontier, seen = list(colls), set(colls)  # include subcollections
while frontier:
    kids = [r[0] for r in con.execute(f"select collectionID from collections where parentCollectionID in ({','.join('?' * len(frontier))})", frontier)]
    frontier = [k for k in kids if k not in seen]; seen.update(frontier)
colls = sorted(seen)
item_ids = sorted({r[0] for r in con.execute(f"select itemID from collectionItems where collectionID in ({','.join('?' * len(colls))})", colls)})
ph = ",".join("?" * len(item_ids))

fields = {}
for item_id, name, value in con.execute(
    f"select id.itemID, fl.fieldName, v.value from itemData id join fields fl using(fieldID) "
    f"join itemDataValues v using(valueID) where id.itemID in ({ph})", item_ids):
    fields.setdefault(item_id, {})[name] = value
keys = dict(con.execute(f"select itemID, key from items where itemID in ({ph})", item_ids))
first_author = {}
for item_id, last in con.execute(
    f"select ic.itemID, cr.lastName from itemCreators ic join creators cr using(creatorID) "
    f"where ic.itemID in ({ph}) order by ic.orderIndex desc", item_ids):
    first_author[item_id] = last
pdf_key = {}
for parent, key in con.execute(
    f"select ia.parentItemID, i.key from itemAttachments ia join items i on i.itemID=ia.itemID "
    f"where ia.parentItemID in ({ph}) and ia.contentType='application/pdf'", item_ids):
    pdf_key.setdefault(parent, key)
con.close(); shutil.rmtree(tmp, ignore_errors=True)

rows = []
for item_id in item_ids:
    f = fields.get(item_id, {})
    pmid = (re.search(r"PMID:\s*(\d+)", (f.get("archiveLocation") or "") + " " + (f.get("extra") or ""))
            or re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", f.get("url") or ""))
    pk = pdf_key.get(item_id, "")
    ft, nb, src = local_text(keys[item_id], pk)
    rows.append([item_id, keys[item_id], (f.get("date") or "")[:4], first_author.get(item_id, ""),
                 clean(f.get("publicationTitle")), f.get("DOI", ""), pmid.group(1) if pmid else "",
                 pk, ft, nb, src, clean(f.get("title"))])
write(rows, f"from Zotero collection(s) {COLL}")
