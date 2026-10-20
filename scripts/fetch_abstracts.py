#!/usr/bin/env python3
"""Fetch PubMed abstracts for every PMID in corpus/items.tsv.

Writes corpus/abstracts.tsv (pmid, key, abstract). Standard library only.
Already-fetched PMIDs are skipped unless --force is given. Stays under
NCBI's limit of 3 requests per second for unauthenticated clients.

Usage:
    python3 fetch_abstracts.py [--force]
"""
import csv
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.environ.get("MIGUEL_CORPUS") or os.path.join(os.path.expanduser("~"), ".claude", "miguel-corpus")
ITEMS = os.path.join(CORPUS_DIR, "items.tsv")
OUT = os.path.join(CORPUS_DIR, "abstracts.tsv")
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH = 150
force = "--force" in sys.argv

with open(ITEMS, newline="") as fh:
    items = list(csv.DictReader(fh, delimiter="\t"))
pmid_to_key = {r["pmid"]: r["key"] for r in items if r["pmid"]}

existing = {}
if os.path.exists(OUT) and not force:
    with open(OUT, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            existing[r["pmid"]] = r["abstract"]

todo = [p for p in pmid_to_key if p not in existing]
print(f"{len(pmid_to_key)} PMIDs in corpus, {len(existing)} already fetched, {len(todo)} to fetch")

def fetch(batch):
    q = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(batch), "retmode": "xml", "rettype": "abstract"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(f"{EFETCH}?{q}", timeout=60) as resp:
                return resp.read()
        except Exception as e:  # network hiccup or 429, back off and retry
            wait = 2 ** attempt
            print(f"  retry in {wait}s: {e}")
            time.sleep(wait)
    raise SystemExit("PubMed fetch failed repeatedly")

found = 0
for i in range(0, len(todo), BATCH):
    batch = todo[i:i + BATCH]
    data = fetch(batch)
    if b"<!ENTITY" in data:  # PubMed sends a DOCTYPE but never inline entities; stdlib XML has no expansion guard
        raise SystemExit("unexpected ENTITY declaration in PubMed response; refusing to parse")
    root = ET.fromstring(data)
    for art in root.iter("PubmedArticle"):
        pmid = art.findtext("./MedlineCitation/PMID")
        parts = []
        for at in art.findall("./MedlineCitation/Article/Abstract/AbstractText"):
            text = "".join(at.itertext()).strip()
            label = at.get("Label")
            parts.append(f"{label}: {text}" if label else text)
        existing[pmid] = re.sub(r"\s+", " ", " ".join(parts))
        if parts:
            found += 1
    for p in batch:  # record PMIDs PubMed returned nothing for, so we do not refetch forever
        existing.setdefault(p, "")
    print(f"  batch {i // BATCH + 1}: {len(batch)} requested")
    time.sleep(0.4)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\", lineterminator="\n")
    w.writerow(["pmid", "key", "abstract"])
    for p in sorted(existing, key=lambda x: int(x)):
        w.writerow([p, pmid_to_key.get(p, ""), existing[p]])

n_nonempty = sum(1 for v in existing.values() if v)
print(f"{found} new abstracts this run | {n_nonempty}/{len(existing)} PMIDs with a non-empty abstract -> {OUT}")
