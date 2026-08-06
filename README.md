# My Novel

[![Build Status](https://img.shields.io/badge/manuscript-in__progress-blue)](#)
[![Word Count](https://img.shields.io/badge/word__count-tracking-green)](#)

Welcome to the **My Novel** repository. This project contains the manuscript, outline, character sheets, worldbuilding documentation, and build scripts for writing and exporting the novel.

---

## 📖 Synopsis

In a world standing on the brink of profound transformation, an unexpected discovery uncovers ancient secrets long forgotten. Follow the journey of unexpected heroes who must navigate peril, mystery, and destiny.

---

## 📁 Repository Structure

```text
mynovel/
├── README.md                 # Project overview and instructions
├── OUTLINE.md                # Story structure, plot arc, and act details
├── chapters/                 # Individual chapter drafts in Markdown
│   ├── 01-introduction.md
│   ├── 02-the-awakening.md
│   └── 03-the-crossing.md
├── characters/               # Character profiles and character arcs
│   ├── protagonist.md
│   └── antagonist.md
├── worldbuilding/            # Setting details, lore, and universe notes
│   └── setting.md
├── dist/                     # Compiled manuscript outputs
└── build.sh                  # Manuscript compilation and word count tool
```

---

## 🛠️ Usage & Build Instructions

### Compile Manuscript & Word Count
Run the provided build script to aggregate all chapters into a single file and generate word count stats:

```bash
chmod +x build.sh
./build.sh
```

The compiled draft will be output to `dist/manuscript.md`.

---

## 📝 Writing Workflow

- Each chapter is stored cleanly in `chapters/` with numerical prefixes.
- Character notes belong in `characters/`.
- Lore and universe details are maintained in `worldbuilding/`.
- All changes are version-controlled with Git.
