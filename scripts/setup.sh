#!/usr/bin/env bash
# Build Miguel's local corpus. Safe to rerun; each step skips what it already has.
#
#   setup.sh                 build/refresh the corpus in $MIGUEL_CORPUS (default ~/.claude/miguel-corpus)
#   setup.sh --seed-memory   also copy the shipped methodology notes into Miguel's memory folder
#
# Needs: python3 (standard library only), network access to PubMed and Europe PMC.
# Zotero is optional: with the "causalab_selected_plus_miguel_exhaustive" collection
# synced locally, PDFs' text is picked up from Zotero's own full-text cache.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
export MIGUEL_CORPUS="${MIGUEL_CORPUS:-$HOME/.claude/miguel-corpus}"
mkdir -p "$MIGUEL_CORPUS"
for f in items.tsv abstracts.tsv roster_former.txt; do
  [ -f "$MIGUEL_CORPUS/$f" ] || cp "$HERE/corpus/$f" "$MIGUEL_CORPUS/$f"
done
echo "corpus directory: $MIGUEL_CORPUS"
echo "[1/5] item index";        python3 "$HERE/scripts/build_corpus_index.py"
echo "[2/5] PubMed abstracts";  python3 "$HERE/scripts/fetch_abstracts.py" | tail -1
echo "[3/5] Europe PMC text";   python3 "$HERE/scripts/fetch_pmc_fulltext.py" | tail -2 | head -1
echo "[4/5] item index again";  python3 "$HERE/scripts/build_corpus_index.py"
echo "[5/5] search index";      python3 "$HERE/scripts/build_search_index.py"

if [ "${1:-}" = "--seed-memory" ]; then
  # Claude Code names a plugin agent's memory folder when the agent first runs; reuse it if it exists
  base="$HOME/.claude/agent-memory"; mkdir -p "$base"
  target="$(ls -d "$base"/*miguel-causal-inference* 2>/dev/null | head -1 || true)"
  target="${target:-$base/miguel-causal-inference}"; mkdir -p "$target"
  n=0
  for f in "$HERE"/seed-memory/reference_*.md; do
    b="$(basename "$f")"
    [ -f "$target/$b" ] && continue
    cp "$f" "$target/$b"; n=$((n+1))
    name="$(sed -n 's/^name: *//p' "$f" | head -1)"; desc="$(sed -n 's/^description: *//p' "$f" | head -1)"
    grep -q "($b)" "$target/MEMORY.md" 2>/dev/null || echo "- [$name]($b) - $desc" >> "$target/MEMORY.md"
  done
  echo "seeded $n memory notes into $target"
fi
echo "done. Try: $HERE/scripts/lookup.sh search \"stabilized weights dynamic strategies\""
