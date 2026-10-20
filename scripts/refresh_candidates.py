#!/usr/bin/env python3
"""Find papers by CAUSALab members (current and former) that are new to the
Zotero causalab_* collections, for screening and import.

Roster sources:
  current  scraped from https://hsph.harvard.edu/research/causalab/who-we-are/
           (same regex as the April 2026 build), institutions filtered out
  former   corpus/roster_former.txt (hand-maintained, seeded from Wayback snapshots)

For each name a PubMed author query is run, restricted to records added to
PubMed since --since (Entrez date) and, except for the exhaustive authors
(Hernan, Robins), to causal-inference vocabulary in title or abstract. Common
names are disambiguated after the fact: a record is kept if the matched author
is a core member, or any author lists a Harvard/Boston-area affiliation, or a
core member is a co-author. Everything already in Zotero (by PMID) is dropped.

Outputs (in --out, default: a dated folder in the scratchpad):
  candidates.csv   one row per paper with match reasons, screen flag, abstract
  candidates.ris   import into Zotero, then drag the keepers into the collection
  summary.json

Usage:
    python3 refresh_candidates.py --since 2026/03/01 [--out DIR] [--no-web]
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.environ.get("MIGUEL_CORPUS") or os.path.join(os.path.expanduser("~"), ".claude", "miguel-corpus")
CORPUS = CORPUS_DIR
HOME = os.path.expanduser("~")
ROSTER_URL = "https://hsph.harvard.edu/research/causalab/who-we-are/"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
UA = "MiguelCorpusRefresh/1.0 (Claude Code; local research tool)"

# PubMed "Last Initials" forms for names the default rule gets wrong
NAME_OVERRIDES = {
    "Miguel Hernán": ["Hernan MA"],
    "Jamie Robins": ["Robins JM"],
    "Tyler VanderWeele": ["VanderWeele TJ"],
    "Sonia Hernández-Díaz": ["Hernandez-Diaz S"],
    "José R. Zubizarreta": ["Zubizarreta JR"],
    "Jessica Young": ["Young JG"],
    "Barbra Dickerman": ["Dickerman BA"],
    "Issa Dahabreh": ["Dahabreh IJ"],
    "Sonja Swanson": ["Swanson SA"],
    "Xabier García de Albéniz": ["Garcia-Albeniz X"],
    "Arin Madenci": ["Madenci AL"],
    "Alejandro Szmulewicz": ["Szmulewicz AG"],
    "Katherine/Guilin Li": ["Li G"],
    "Isaac Jacobo Núñez Saavedra": ["Nunez I", "Nunez-Saavedra IJ"],
    "Gonzalo Martínez-Alés": ["Martinez-Ales G"],
    "Antonio Rodriuguez-Miguel": ["Rodriguez-Miguel A"],
    "Ryan O&#039;Dea": ["O'Dea R"],
    "Ryan O'Dea": ["O'Dea R"],
    "Alli LaHood": ["LaHood A"],
    "Meg Buxton": ["Buxton M"],
    "Joe Hakim": ["Hakim J"],
    "Juan Pablo Casas": ["Casas JP"],
    "Kerollos Wanis": ["Wanis KN"],
    "Louisa Smith": ["Smith LH"],
    "Yu-Han Chiu": ["Chiu YH"],
    "Daniela Van Santen": ["van Santen DK"],
    "Emma McGee": ["McGee EE"],
    "Jeremy Brown": ["Brown JP"],
    "Lan Wen": ["Wen L"],
}
EXHAUSTIVE = {"Hernan MA", "Robins JM"}  # no topic filter, as in the April build
AMBIGUOUS_HITS = 50  # more raw hits than this in the window means the name form is not specific enough
CORE_SURNAMES = ["hernan", "robins", "vanderweele", "hernandez-diaz", "dahabreh", "dickerman", "zubizarreta",
                 "swanson", "lodi", "garcia-albeniz", "madenci", "szmulewicz", "chiu", "young jg"]
AFFIL_HINTS = ["harvard", "causalab", "boston", "brigham", "massachusetts general", "beth israel",
               "dana-farber", "va boston", "karolinska", "broad institute", "harvard pilgrim"]
NON_PERSON = ["institut", "office of", "department", "university", "school", "center", "centre", "hospital", "affairs"]
TOPIC_TERMS = ['causal', '"target trial"', 'emulat*', 'confound*', '"g-formula"', '"marginal structural"',
               '"inverse probability"', 'transportab*', 'generalizab*', '"selection bias"', '"competing event*"',
               '"competing risk*"', 'mediat*', '"direct effect*"', '"instrumental variable*"', '"propensity score*"',
               'counterfactual*', 'exchangeability', 'positivity', '"immortal time"', 'interference',
               '"mendelian randomi*"', '"potential outcome*"', '"sensitivity analysis"', '"hazard ratio*"',
               '"structural nested"', '"per-protocol"', '"intention-to-treat"', '"observational"', 'estimand*']
SCREEN_PATTERNS = [r"\bcausal\b", r"target trial", r"trial emulation", r"\bbias\b", r"confound", r"g-formula",
                   r"g-estimation", r"marginal structural", r"inverse probability", r"transportab", r"generalizab",
                   r"selection bias", r"competing event", r"competing risk", r"\bmediat", r"direct effect",
                   r"indirect effect", r"instrumental variable", r"propensity score", r"counterfactual",
                   r"exchangeability", r"positivity", r"identifiab", r"immortal time", r"interference",
                   r"mendelian randomization", r"potential outcome", r"e-value", r"sensitivity analysis",
                   r"hazard ratio", r"emulat", r"structural nested", r"standardi[sz]ation", r"g-method", r"estimand"]

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def http(url, pause=0.35):
    time.sleep(pause)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return resp.read()
        except Exception as e:
            time.sleep(2 ** attempt)
            last = e
    raise SystemExit(f"request failed repeatedly: {url[:120]} ({last})")

def guard(data):
    if b"<!ENTITY" in data:
        raise SystemExit("unexpected ENTITY declaration in response; refusing to parse")
    return data

def current_roster(no_web):
    if no_web:
        return []
    html = http(ROSTER_URL).decode("utf-8", "replace")
    names = re.findall(r'wp-block-hsph-people-list-item__name">([^<]+)</h3>', html)
    out = []
    for raw in names:
        n = " ".join(raw.split()).replace("&#039;", "'")
        if len(n.split()) >= 2 and not any(k in n.lower() for k in NON_PERSON) and n not in out:
            out.append(n)
    return out

def former_roster():
    path = os.path.join(CORPUS, "roster_former.txt")
    if not os.path.exists(path):
        return []
    return [l.strip() for l in open(path) if l.strip() and not l.startswith("#")]

def pubmed_forms(name):
    if name in NAME_OVERRIDES:
        return NAME_OVERRIDES[name]
    clean = strip_accents(name.replace("&#039;", "'"))
    parts = [p for p in re.split(r"\s+", clean) if p and p != "/"]
    if len(parts) < 2:
        return []
    initials = "".join(p[0] for p in parts[:-1] if p[0].isupper())
    return [f"{parts[-1]} {initials}"]

def existing_pmids():
    db = os.path.join(HOME, "Zotero", "zotero.sqlite")
    tmp = tempfile.mkdtemp(); cp = os.path.join(tmp, "z.sqlite"); shutil.copy(db, cp)
    con = sqlite3.connect(cp)
    rows = con.execute("""
        select v.value from collectionItems ci join collections c using(collectionID)
        join itemData id using(itemID) join fields f using(fieldID) join itemDataValues v using(valueID)
        where c.collectionName like 'causalab%' and f.fieldName='archiveLocation' and v.value like 'PMID:%'""").fetchall()
    con.close(); shutil.rmtree(tmp, ignore_errors=True)
    return {r[0].replace("PMID:", "").strip() for r in rows}

def esearch(term):
    q = urllib.parse.urlencode({"db": "pubmed", "retmode": "json", "retmax": 2000, "term": term})
    return json.loads(http(f"{EUTILS}esearch.fcgi?{q}"))["esearchresult"].get("idlist", [])

def efetch(pmids):
    out = {}
    for i in range(0, len(pmids), 150):
        q = urllib.parse.urlencode({"db": "pubmed", "retmode": "xml", "id": ",".join(pmids[i:i + 150])})
        root = ET.fromstring(guard(http(f"{EUTILS}efetch.fcgi?{q}")))
        for art in root.iter("PubmedArticle"):
            pid = art.findtext("./MedlineCitation/PMID")
            a = art.find("./MedlineCitation/Article")
            authors, affils = [], []
            for au in a.findall("./AuthorList/Author"):
                last, fore, init = au.findtext("LastName"), au.findtext("ForeName"), au.findtext("Initials")
                if last:
                    authors.append(f"{last} {init or ''}".strip())
                for af in au.findall("./AffiliationInfo/Affiliation"):
                    affils.append((af.text or "").lower())
            abstract = " ".join("".join(t.itertext()).strip() for t in a.findall("./Abstract/AbstractText"))
            doi = next((x.text for x in art.findall("./PubmedData/ArticleIdList/ArticleId") if x.get("IdType") == "doi"), "")
            year = a.findtext("./Journal/JournalIssue/PubDate/Year") or a.findtext("./ArticleDate/Year") or ""
            out[pid] = {"pmid": pid, "title": "".join(a.find("./ArticleTitle").itertext()).strip() if a.find("./ArticleTitle") is not None else "",
                        "authors": authors, "affils": affils, "journal": a.findtext("./Journal/Title") or "",
                        "year": year, "doi": doi or "", "abstract": re.sub(r"\s+", " ", abstract)}
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026/03/01", help="Entrez date lower bound, YYYY/MM/DD")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-web", action="store_true", help="skip the website roster (former list only)")
    args = ap.parse_args()
    out = args.out or os.path.join(tempfile.gettempdir(), f"causalab_refresh_{dt.date.today()}")
    os.makedirs(out, exist_ok=True)

    cur, former = current_roster(args.no_web), former_roster()
    roster = [(n, "current") for n in cur] + [(n, "former") for n in former if n not in cur]
    have = existing_pmids()
    print(f"roster: {len(cur)} current + {len([r for r in roster if r[1]=='former'])} former | {len(have)} PMIDs already in Zotero")

    topic = " OR ".join(f"{t}[tiab]" for t in TOPIC_TERMS)
    affil = " OR ".join(f"{h}[ad]" for h in ("harvard", "boston", "causalab", "karolinska", "brigham", "massachusetts general"))
    date = f'("{args.since}"[edat] : "3000"[edat])'
    hits = {}  # pmid -> set of (roster name, status, form)
    ambiguous = set()
    for name, status in roster:
        for form in pubmed_forms(name):
            term = f'"{form}"[Author] AND {date}'
            if form not in EXHAUSTIVE:
                term += f" AND ({topic})"
            ids = esearch(term)
            note = ""
            if len(ids) > AMBIGUOUS_HITS:  # a common surname: require a Harvard/Boston-area affiliation in the record itself
                ids = esearch(f"{term} AND ({affil})")
                ambiguous.add(form)
                note = " (common name, affiliation required)"
            for pid in ids:
                hits.setdefault(pid, set()).add((name, status, form))
            print(f"  {name} [{form}]: {len(ids)}{note}")
    new = [p for p in hits if p not in have]
    print(f"{len(hits)} PubMed hits, {len(new)} not in Zotero; fetching details")
    recs = efetch(new)

    rows = []
    for pid, rec in recs.items():
        names = hits[pid]
        auth_l = [a.lower() for a in rec["authors"]]
        core_matched = any(f in EXHAUSTIVE or any(s in f.lower() for s in CORE_SURNAMES) for _, _, f in names)
        core_coauthor = any(any(s in a for s in CORE_SURNAMES) for a in auth_l)
        affil_ok = any(any(h in af for h in AFFIL_HINTS) for af in rec["affils"])
        only_ambiguous = all(f in ambiguous for _, _, f in names)
        # an affiliation alone does not vouch for a common surname; those need a core co-author
        reasons = [r for r, ok in (("core-author", core_matched), ("core-coauthor", core_coauthor),
                                   ("affiliation", affil_ok and not only_ambiguous),
                                   ("affiliation-common-name", affil_ok and only_ambiguous and core_coauthor)) if ok]
        text = f"{rec['title']} {rec['abstract']}".lower()
        screen = any(re.search(p, text) for p in SCREEN_PATTERNS)
        rows.append({**rec, "roster_matches": "; ".join(sorted({n for n, _, _ in names})),
                     "roster_status": "; ".join(sorted({s for _, s, _ in names})),
                     "keep_reasons": "; ".join(reasons), "screen_pass": screen,
                     "n_roster": len({n for n, _, _ in names}), "url": f"https://pubmed.ncbi.nlm.nih.gov/{pid}/"})
    kept = [r for r in rows if r["keep_reasons"]]
    kept.sort(key=lambda r: (-r["n_roster"], not r["screen_pass"], r["year"], r["title"].lower()))
    dropped = len(rows) - len(kept)

    with open(os.path.join(out, "candidates.csv"), "w", newline="") as fh:
        cols = ["pmid", "year", "journal", "title", "authors", "roster_matches", "roster_status", "keep_reasons", "screen_pass", "doi", "url", "abstract"]
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for r in kept:
            w.writerow({**r, "authors": "; ".join(r["authors"])})
    with open(os.path.join(out, "candidates.ris"), "w") as fh:
        for r in kept:
            lines = ["TY  - JOUR"] + [f"AU  - {a}" for a in r["authors"]] + [f"TI  - {r['title']}", f"JO  - {r['journal']}", f"PY  - {r['year']}"]
            if r["doi"]:
                lines.append(f"DO  - {r['doi']}")
            lines += [f"AN  - PMID:{r['pmid']}", f"UR  - {r['url']}", f"AB  - {r['abstract']}"]
            lines += [f"KW  - {n}" for n in r["roster_matches"].split("; ") if n] + ["ER  - ", ""]
            fh.write("\n".join(lines) + "\n")
    summary = {"date": str(dt.date.today()), "since": args.since, "roster_current": cur, "roster_former": former,
               "pubmed_hits": len(hits), "new_to_zotero": len(new), "kept": len(kept), "dropped_ambiguous": dropped,
               "screen_pass": sum(1 for r in kept if r["screen_pass"]), "out": out}
    json.dump(summary, open(os.path.join(out, "summary.json"), "w"), indent=2, ensure_ascii=False)
    print(f"kept {len(kept)} candidates ({summary['screen_pass']} pass the title/abstract screen), dropped {dropped} ambiguous-name hits -> {out}")

if __name__ == "__main__":
    main()
