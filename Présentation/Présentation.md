---
marp: true
paginate: false
theme: height 
backgroundImage: "background.jpg" # Remplacez par le chemin de votre image d'arrière-plan si nécessaire
---

# **Scan One Piece**

![class:logo](LogoFac.png)


- **Valentin Barthel**  
- **Nathan Dubourg**  
- **Werner Laemlin**

# Introduction
- Plan du jour :
  - Point 1
  - Point 2
  - Point 3

---
# Introduction : Schéma Explicatif
![width:120px](Schema.png)
---
# Introduction : Présentation de l'arborescence

```
├── flaskr
│   ├── add_db.py
│   ├── db.py
│   ├── generate
│   │   └── llm_summary.py
│   ├── init.py
│   ├── scraping
│   │   ├── get_latest_scan.py
│   │   ├── init.py
│   │   ├── working_x_scrap.py
│   │   ├── youtube_api
│   │   │   ├── _error.py
│   │   │   ├── get_link.py
│   │   │   └── init.py
│   │   └── yt_subtitles.py
│   ├── static
│   │   └── op_background.jpg
│   ├── templates
│   │   ├── base.html
│   │   ├── explanation.html
│   │   ├── info.html
│   │   └── theories.html
│   ├── text_routes.py
│   └── text_schema.sql
├── git_tuto.md
├── instance
│   └── flaskr.sqlite
├── README.md
└── requirements.txt
```
---
# Scraping : Script subtitles vidéo youtube de la chaîne Mont Corvo
```
# Script scrap subtitles
```
---
# Scraping : Script Dextero pour obtenir les prochaines dates de sortie
```
# Script scrap date de sortie
```
# DB : SQLite storage
```
# Script architecture DB
```
---
# AI : Llama 3.3-70b (Dextero)
```
# Script scrap Dextero passage au LLM
```
---
# AI : Llama 3.3-70b (Subtitles)
```
# Script scrap Subtitles passage au LLM
```
- > Prompt

---
# AI : Sentiment Analysis (Subtitles)
```
# Script Sentiment Analysis
```
- > Prompt

---
# Flask

---
# HTML

---
# Rendu terminal
- > Link
