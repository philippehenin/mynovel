#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  BUILDING PHILIPPE HENIN NOVEL PUBLICATIONS (FULL SUITE)"
echo "========================================================"

mkdir -p dist

# 1. Build PDF Master Publications (with Frontispiece Art & Map)
node /tmp/pdfgen/perfect_2pass_toc_verifier.js

# 2. Build EPUB 3 Master Publications (with Frontispiece Art, Map & Drop Caps)
python3 /tmp/pdfgen/build_epub_publications.py

# 3. Build KDP Print Cover Spread PDF (Full Wrap with Spine & Bleed)
python3 /tmp/pdfgen/build_kdp_print_cover.py

# 4. Build Native Amazon Kindle Ebooks (.mobi via KindleGen)
/tmp/kindlegen dist/Aethelgard_La_Bibliotheque_des_Murmures_Edition_Gare.epub -o Aethelgard_La_Bibliotheque_des_Murmures_Edition_Gare.mobi >/dev/null 2>&1 || true
/tmp/kindlegen dist/Aethelgard_The_Library_of_Whispers_Pocket_Edition.epub -o Aethelgard_The_Library_of_Whispers_Pocket_Edition.mobi >/dev/null 2>&1 || true

# 5. Build KF8 AZW3 Kindle Ebooks (.azw3 via Calibre ebook-convert)
ebook-convert dist/Aethelgard_La_Bibliotheque_des_Murmures_Edition_Gare.epub dist/Aethelgard_La_Bibliotheque_des_Murmures_Edition_Gare.azw3 --output-profile kindle >/dev/null 2>&1 || true
ebook-convert dist/Aethelgard_The_Library_of_Whispers_Pocket_Edition.epub dist/Aethelgard_The_Library_of_Whispers_Pocket_Edition.azw3 --output-profile kindle >/dev/null 2>&1 || true

# 6. Run Automated Release Verification Suite
python3 scripts/verify_release.py
