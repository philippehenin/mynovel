#!/usr/bin/env bash
set -euo pipefail

DIST_DIR="dist"
OUTPUT_FILE="${DIST_DIR}/manuscript.md"

mkdir -p "${DIST_DIR}"
echo "# Complete Manuscript" > "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"
echo "_Generated on $(date -u)_" >> "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"
echo "---" >> "${OUTPUT_FILE}"
echo "" >> "${OUTPUT_FILE}"

for chapter in chapters/*.md; do
    if [ -f "$chapter" ]; then
        cat "$chapter" >> "${OUTPUT_FILE}"
        echo -e "\n\n---\n" >> "${OUTPUT_FILE}"
    fi
done

WORD_COUNT=$(wc -w < "${OUTPUT_FILE}")
CHAPTER_COUNT=$(ls -1 chapters/*.md 2>/dev/null | wc -l)

echo "=========================================="
echo " Manuscript Compilation Complete!"
echo " Total Chapters Compiled: ${CHAPTER_COUNT}"
echo " Total Word Count:       ${WORD_COUNT}"
echo " Output File:            ${OUTPUT_FILE}"
echo "=========================================="
