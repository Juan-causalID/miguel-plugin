#!/usr/bin/env bash
# Miguel's retrieval helper. Reads corpus/items.tsv, corpus/abstracts.tsv and
# the Zotero full-text cache. Never touches the live Zotero database.
#
#   lookup.sh search "<query>" [-n 10] [--any]       rank passages across the WHOLE corpus (FTS5, BM25)
#   lookup.sh passage <KEY> <N>                      print passage N of an item in full
#   lookup.sh find "<title words | author | year>"   list matching items
#   lookup.sh grep <KEY> "<regex>" [context]         search one item's full text
#   lookup.sh abstract <KEY>                         print the abstract
#   lookup.sh path <KEY>                             print the full-text cache path
#
# KEY is the 8-character Zotero item key printed by `find`.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
CORPUS="${MIGUEL_CORPUS:-$HOME/.claude/miguel-corpus}"
ITEMS="$CORPUS/items.tsv"
ABS="$CORPUS/abstracts.tsv"
[ -f "$ITEMS" ] || { echo "missing $ITEMS; run scripts/build_corpus_index.py" >&2; exit 1; }

cmd="${1:-}"; shift || true
case "$cmd" in
  search)
    python3 "$HERE/scripts/search.py" "$@"
    ;;
  passage)
    python3 "$HERE/scripts/search.py" --show "${1:?key}" "${2:?passage number}"
    ;;
  find)
    q="${1:?pattern}"
    # columns: 1 itemID 2 key 3 year 4 first_author 5 journal 6 doi 7 pmid 8 pdf_key 9 ftcache 10 ft_bytes 11 ft_source 12 title
    awk -F'\t' -v q="$q" 'BEGIN{IGNORECASE=1} NR>1 && ($12 ~ q || $4 ~ q || $3 ~ q || $6 ~ q) {
        ft = ($10 > 0) ? "FULLTEXT:" $11 : "title-only"
        printf "%s | %s %s | %s | %s | %s\n", $2, $3, $4, $5, ft, $12 }' "$ITEMS"
    ;;
  path)
    k="${1:?key}"
    awk -F'\t' -v k="$k" 'NR>1 && $2==k {print $9}' "$ITEMS"
    ;;
  grep)
    k="${1:?key}"; pat="${2:?regex}"; ctx="${3:-2}"
    f="$(awk -F'\t' -v k="$k" 'NR>1 && $2==k {print $9}' "$ITEMS")"
    [ -n "$f" ] && [ -f "$f" ] || { echo "no full text for $k (title-only item); try: lookup.sh abstract $k, then WebFetch the paper" >&2; exit 2; }
    grep -n -i -C "$ctx" -E "$pat" "$f" || { echo "no match for /$pat/ in $k" >&2; exit 3; }
    ;;
  abstract)
    k="${1:?key}"
    [ -f "$ABS" ] || { echo "missing $ABS; run scripts/fetch_abstracts.py" >&2; exit 1; }
    line="$(awk -F'\t' -v k="$k" 'NR>1 && $2==k' "$ABS" | head -1)"
    [ -n "$line" ] || { echo "no PubMed ID recorded for $k" >&2; exit 2; }
    out="$(printf '%s\n' "$line" | cut -f3-)"
    if [ -n "$out" ]; then printf '%s\n' "$out"; else echo "(no abstract on PubMed for $k)"; fi
    ;;
  *)
    sed -n '2,10p' "$0"; exit 1 ;;
esac
