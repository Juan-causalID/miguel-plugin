#!/usr/bin/env bash
# List corpus items that still have no full text, as PubMed links with the
# Harvard Library link-out (otool=hulib), so each can be opened over VPN and
# saved to Zotero with the browser connector. Hernan, Robins and VanderWeele
# items are listed first. Output is Markdown.
#
#   needs_pdf.sh > ~/Desktop/miguel_needs_pdf.md
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
CORPUS="${MIGUEL_CORPUS:-$HOME/.claude/miguel-corpus}"
ITEMS="$CORPUS/items.tsv"
echo "# Corpus items without full text ($(date +%F))"
echo
echo "Open each link while connected to the Harvard VPN, click the Harvard Library button, then save the PDF to Zotero with the connector. Rerun build_corpus_index.py afterwards."
echo
for pass in priority rest; do
  if [ "$pass" = priority ]; then echo "## Priority (Hernan, Robins, VanderWeele)"; else echo "## Everything else"; fi
  echo
  awk -F'\t' -v pass="$pass" 'NR>1 && $10 == 0 {
      pri = ($4 ~ /Hern[aá]n|Robins|VanderWeele|Vanderweele/) ? "priority" : "rest"
      if (pri != pass) next
      link = ($7 != "") ? "https://pubmed.ncbi.nlm.nih.gov/" $7 "/?otool=hulib" : (($6 != "") ? "https://doi.org/" $6 : "(no PMID or DOI)")
      printf "- %s %s, *%s*. %s <%s>\n", $3, $4, $5, $12, link }' "$ITEMS" | sort
  echo
done
