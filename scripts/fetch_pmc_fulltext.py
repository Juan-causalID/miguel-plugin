#!/usr/bin/env python3
"""Fetch full text from Europe PMC for corpus items that have a PubMed Central
record but no Zotero full-text cache. Writes plain text to corpus/fulltext/<key>.txt
(machine-local, gitignored) and a status table to corpus/pmc_fulltext.tsv.

Europe PMC's REST API is built for programmatic access; this script stays well
under its rate guidance. Standard library only.

Usage:
    python3 fetch_pmc_fulltext.py [--force]
"""
import csv
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.environ.get("MIGUEL_CORPUS") or os.path.join(os.path.expanduser("~"), ".claude", "miguel-corpus")
CORPUS = CORPUS_DIR
ITEMS = os.path.join(CORPUS, "items.tsv")
OUTDIR = os.path.join(CORPUS, "fulltext")
STATUS = os.path.join(CORPUS, "pmc_fulltext.tsv")
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
force = "--force" in sys.argv

with open(ITEMS, newline="") as fh:
    items = list(csv.DictReader(fh, delimiter="\t"))

def get(url):
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read()

def guard(data):
    if b"<!ENTITY" in data:
        raise SystemExit("unexpected ENTITY declaration in response; refusing to parse")
    return data

# 1. PMIDs -> PMCIDs (PubMed knows this mapping; Zotero does not store it)
pmcid = {}
pmids = [r["pmid"] for r in items if r["pmid"]]
for i in range(0, len(pmids), 200):
    q = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(pmids[i:i + 200]), "retmode": "xml"})
    root = ET.fromstring(guard(get(f"{EFETCH}?{q}")))
    for art in root.iter("PubmedArticle"):
        pid = art.findtext("./MedlineCitation/PMID")
        for aid in art.findall("./PubmedData/ArticleIdList/ArticleId"):
            if aid.get("IdType") == "pmc":
                pmcid[pid] = aid.text
    time.sleep(0.4)

# 2. JATS XML -> readable text (section titles, paragraphs, table rows, references)
def local(tag):
    return tag.split("}")[-1]

def flat(el):
    return " ".join("".join(el.itertext()).split())

def walk(el, out):
    tag = local(el.tag)
    if tag == "title":
        t = flat(el)
        if t:
            out.append(f"## {t}")
        return
    if tag in ("p", "mixed-citation", "element-citation", "caption", "label"):
        t = flat(el)
        if t:
            out.append(t)
        return
    if tag == "tr":
        out.append("\t".join(flat(c) for c in el if local(c.tag) in ("td", "th")))
        return
    for child in el:
        walk(child, out)

def jats_to_text(data):
    root = ET.fromstring(data)
    art = root if local(root.tag) == "article" else root.find(".//article")
    if art is None:
        return ""
    meta = art.find(".//front/article-meta")
    out = []
    if meta is not None:
        out.append("# " + flat(meta.find("title-group/article-title")) if meta.find("title-group/article-title") is not None else "")
        authors = []
        for c in meta.findall(".//contrib-group/contrib[@contrib-type='author']"):
            sur, giv = c.findtext("name/surname"), c.findtext("name/given-names")
            if sur:
                authors.append(f"{sur} {giv or ''}".strip())
        jt = art.findtext(".//front/journal-meta/journal-title-group/journal-title") or art.findtext(".//front/journal-meta/journal-title") or ""
        yr = meta.findtext("pub-date/year") or ""
        out.append(f"Authors: {'; '.join(authors)}")
        out.append(f"Journal: {jt} {yr}".strip())
        for ab in meta.findall("abstract"):
            out.append("## Abstract")
            walk(ab, out)
    for part in ("body", "back"):
        node = art.find(part)
        if node is not None:
            walk(node, out)
    return "\n\n".join(o for o in out if o)

# 3. fetch (PMCIDs that failed on a previous run are not retried unless --force)
failed_before = set()
if os.path.exists(STATUS) and not force:
    with open(STATUS, newline="") as fh:
        failed_before = {r["pmcid"] for r in csv.DictReader(fh, delimiter="\t") if r["status"].startswith(("http_", "no_fulltext"))}
os.makedirs(OUTDIR, exist_ok=True)
rows, n_new, n_skip, n_missing = [], 0, 0, 0
for r in items:
    pid, key = r["pmid"], r["key"]
    pc = pmcid.get(pid)
    if not pc:
        continue
    if pc in failed_before:
        rows.append([pid, pc, key, "unavailable_before", 0]); n_missing += 1
        continue
    out_path = os.path.join(OUTDIR, f"{key}.txt")
    has_zotero = r.get("ft_bytes") not in ("", "0", None) and r.get("ft_source", "zotero") == "zotero"
    if has_zotero:
        rows.append([pid, pc, key, "zotero_cache", 0]); n_skip += 1
        continue
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0 and not force:
        rows.append([pid, pc, key, "ok", os.path.getsize(out_path)]); n_skip += 1
        continue
    try:
        text = jats_to_text(guard(get(EPMC.format(pmcid=pc))))
        if len(text) < 2000:  # abstract-only or empty shell, not usable as full text
            rows.append([pid, pc, key, "no_fulltext", len(text)]); n_missing += 1
        else:
            with open(out_path, "w") as fh:
                fh.write(text)
            rows.append([pid, pc, key, "ok", len(text)]); n_new += 1
    except urllib.error.HTTPError as e:
        rows.append([pid, pc, key, f"http_{e.code}", 0]); n_missing += 1
    except Exception as e:  # keep going; the status table records what failed
        rows.append([pid, pc, key, f"error:{type(e).__name__}", 0]); n_missing += 1
    time.sleep(0.3)

with open(STATUS, "w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["pmid", "pmcid", "key", "status", "chars"])
    w.writerows(rows)
print(f"{len(pmcid)} items with a PMCID | {n_new} new full texts | {n_skip} skipped (already had text) | {n_missing} unavailable -> {OUTDIR}")
print("Now rerun build_corpus_index.py so items.tsv points at the new text.")
