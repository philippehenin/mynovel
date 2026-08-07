# Mon Roman

[![Statut du Manuscrit](https://img.shields.io/badge/manuscrit-en__cours-blue)](#)
[![Nombre de Mots](https://img.shields.io/badge/mots-suivi__actif-green)](#)

Bienvenue dans le dépôt **Mon Roman**. Ce projet contient le manuscrit, le plan détaillé, les fiches de personnages, la documentation de création d'univers (*worldbuilding*) et les scripts d'exportation.

---

## 📖 Synopsis

Dans un monde au bord d'une transformation profonde, une découverte inattendue dévoile des secrets antiques oubliés depuis des siècles. Suivez le périple de héros malgré eux qui doivent naviguer entre périls, mystères et destinée face à l'Ordre du Silence.

---

## 📁 Structure du Dépôt

```text
mynovel/
├── README.md                 # Vue d'ensemble du projet et instructions
├── OUTLINE.md                # Structure du récit, arcs narratifs et actes
├── chapters/                 # Chapitres rédigés en Markdown
│   ├── 01-introduction.md
│   ├── 02-the-awakening.md
│   └── 03-the-crossing.md
├── characters/               # Fiches et arcs de développement des personnages
│   ├── protagonist.md
│   └── antagonist.md
├── worldbuilding/            # Détails du monde, lore et règles de l'univers
│   └── setting.md
├── dist/                     # Manuscrit compilé pour exportation
└── build.sh                  # Script d'assemblage du manuscrit et comptage de mots
```

---

## 🛠️ Instructions de Compilation

### Compiler le Manuscrit & Compter les Mots
Exécutez le script d'assemblage pour regrouper tous les chapitres dans un fichier unique et obtenir les statistiques :

```bash
chmod +x build.sh
./build.sh
```

Le manuscrit complet sera généré dans `dist/manuscript.md`.

---

## 📝 Flux de Travail

- Chaque chapitre est stocké dans `chapters/` avec un préfixe numérique.
- Les profils des personnages résident dans `characters/`.
- Les détails de l'univers sont maintenus dans `worldbuilding/`.
- L'ensemble est suivi et versionné avec Git.

