#!/usr/bin/env python3
"""
Master Release Verification Suite for Philippe Henin Novel Publications
Performs automated structural, typographical, linguistic, and container audits on French & English PDF, EPUB, MOBI, and AZW3 releases.
"""

import sys
import os
import subprocess
import zipfile

DIST_DIR = '/home/philippehenin/Gits/mynovel/dist'
FR_PDF = os.path.join(DIST_DIR, 'Aethelgard_La_Bibliotheque_des_Murmures_Edition_Gare.pdf')
EN_PDF = os.path.join(DIST_DIR, 'Aethelgard_The_Library_of_Whispers_Pocket_Edition.pdf')
FR_EPUB = os.path.join(DIST_DIR, 'Aethelgard_La_Bibliotheque_des_Murmures_Edition_Gare.epub')
EN_EPUB = os.path.join(DIST_DIR, 'Aethelgard_The_Library_of_Whispers_Pocket_Edition.epub')
FR_MOBI = os.path.join(DIST_DIR, 'Aethelgard_La_Bibliotheque_des_Murmures_Edition_Gare.mobi')
EN_MOBI = os.path.join(DIST_DIR, 'Aethelgard_The_Library_of_Whispers_Pocket_Edition.mobi')
FR_AZW3 = os.path.join(DIST_DIR, 'Aethelgard_La_Bibliotheque_des_Murmures_Edition_Gare.azw3')
EN_AZW3 = os.path.join(DIST_DIR, 'Aethelgard_The_Library_of_Whispers_Pocket_Edition.azw3')

def check(condition, desc):
    if condition:
        print(f"  [PASS] {desc}")
        return True
    else:
        print(f"  [FAIL] {desc}")
        return False

def verify_pdf(pdf_path, lang):
    print(f"\n--- Auditing {lang} PDF Publication ({os.path.basename(pdf_path)}) ---")
    all_passed = True
    
    if not check(os.path.exists(pdf_path), "File exists on disk"):
        return False
        
    res = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
    raw_pages = res.stdout.split('\x0c')
    if len(raw_pages) > 1 and not raw_pages[-1].strip():
        raw_pages = raw_pages[:-1]
        
    total_pages = len(raw_pages)
    all_passed &= check(total_pages >= 30, f"Document has solid volume ({total_pages} pages)")
    
    blank_trailing = False
    for p_idx in range(total_pages - 1, -1, -1):
        lines = [l for l in raw_pages[p_idx].split('\n') if l.strip()]
        content_lines = [l for l in lines if not ('PHILIPPE HENIN' in l or 'AETHELGARD' in l or (l.startswith('— ') and l.endswith(' —')))]
        if not content_lines:
            blank_trailing = True
            break
        else:
            break
            
    all_passed &= check(not blank_trailing, "Zero trailing blank pages at end of document")
    
    page2_text = raw_pages[1] if total_pages > 1 else ""
    all_passed &= check("Philippe Henin" in page2_text, "Author 'Philippe Henin' declared on Title Page")
    
    actual_map = {}
    for p_num, p_text in enumerate(raw_pages, 1):
        lines = [l.strip() for l in p_text.split('\n') if l.strip()]
        for ch in range(1, 23):
            ch_kw = f"CHAPITRE {ch}" if lang == 'FR' else f"CHAPTER {ch}"
            if ch_kw in lines:
                if ch not in actual_map:
                    actual_map[ch] = p_num
                    
    all_passed &= check(len(actual_map) == 22, "All 22 chapters present and located")
    
    toc_text = raw_pages[3] if total_pages > 3 else ""
    toc_mismatch = False
    for ch, actual_p in actual_map.items():
        expected_str = f"p. {actual_p}"
        if expected_str not in toc_text:
            print(f"    [MISMATCH] Chapter {ch}: expected '{expected_str}' in TOC text")
            toc_mismatch = True
            
    all_passed &= check(not toc_mismatch, "Table of Contents page numbers 100% match physical page numbers")
    
    raw_asterisks = False
    for p_idx, p_text in enumerate(raw_pages, 1):
        if '*' in p_text:
            raw_asterisks = True
            print(f"    [MARKDOWN LEAK] Page {p_idx} contains raw asterisk")
            break
            
    all_passed &= check(not raw_asterisks, "No raw markdown asterisks in body text")
    
    return all_passed

def verify_epub(epub_path, lang):
    print(f"\n--- Auditing {lang} EPUB 3 Publication ({os.path.basename(epub_path)}) ---")
    all_passed = True
    
    if not check(os.path.exists(epub_path), "File exists on disk"):
        return False
        
    with zipfile.ZipFile(epub_path, 'r') as epub:
        namelist = epub.namelist()
        
        mimetype_first = (namelist[0] == 'mimetype')
        info = epub.getinfo('mimetype')
        mimetype_stored = (info.compress_type == zipfile.ZIP_STORED)
        
        all_passed &= check(mimetype_first and mimetype_stored, "'mimetype' is uncompressed first entry in archive")
        all_passed &= check('META-INF/container.xml' in namelist, "'META-INF/container.xml' present")
        all_passed &= check('OEBPS/content.opf' in namelist, "'OEBPS/content.opf' present")
        all_passed &= check('OEBPS/toc.xhtml' in namelist, "'OEBPS/toc.xhtml' present")
        all_passed &= check('OEBPS/toc.ncx' in namelist, "'OEBPS/toc.ncx' present")
        all_passed &= check('OEBPS/cover.jpg' in namelist, "Cover image embedded")
        
        opf_data = epub.read('OEBPS/content.opf').decode('utf-8')
        all_passed &= check('Philippe Henin' in opf_data, "Author 'Philippe Henin' in EPUB metadata")
        
    return all_passed

def verify_kindle_file(file_path, lang, fmt_label):
    print(f"\n--- Auditing {lang} Kindle {fmt_label} File ({os.path.basename(file_path)}) ---")
    all_passed = True
    
    if not check(os.path.exists(file_path), "File exists on disk"):
        return False
        
    size_bytes = os.path.getsize(file_path)
    all_passed &= check(size_bytes > 50000, f"Kindle {fmt_label} file compiled with solid size ({size_bytes} bytes)")
    
    with open(file_path, 'rb') as f:
        data = f.read(500)
        has_magic = (b'BOOKMOBI' in data or b'TPBR' in data or b'KF8' in data)
        all_passed &= check(has_magic, f"Valid Kindle {fmt_label} binary magic header")
        
    return all_passed

def main():
    print("=========================================================================")
    print("  PHILIPPE HENIN PUBLICATION RELEASE VERIFICATION SUITE")
    print("=========================================================================")
    
    ok_fr_pdf = verify_pdf(FR_PDF, 'FR')
    ok_en_pdf = verify_pdf(EN_PDF, 'EN')
    ok_fr_epub = verify_epub(FR_EPUB, 'FR')
    ok_en_epub = verify_epub(EN_EPUB, 'EN')
    ok_fr_mobi = verify_kindle_file(FR_MOBI, 'FR', 'MOBI')
    ok_en_mobi = verify_kindle_file(EN_MOBI, 'EN', 'MOBI')
    ok_fr_azw3 = verify_kindle_file(FR_AZW3, 'FR', 'AZW3 (KF8)')
    ok_en_azw3 = verify_kindle_file(EN_AZW3, 'EN', 'AZW3 (KF8)')
    
    print("\n=========================================================================")
    if ok_fr_pdf and ok_en_pdf and ok_fr_epub and ok_en_epub and ok_fr_mobi and ok_en_mobi and ok_fr_azw3 and ok_en_azw3:
        print("  🎉 ALL RELEASE VERIFICATIONS PASSED SUCCESSFULLY! (100% READY)")
        print("=========================================================================")
        sys.exit(0)
    else:
        print("  ❌ RELEASE VERIFICATION FAILED! PLEASE RESOLVE FAILURES ABOVE.")
        print("=========================================================================")
        sys.exit(1)

if __name__ == '__main__':
    main()
