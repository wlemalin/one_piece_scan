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
│   ├── add_db.py
│   ├── db.py
│   ├── generate
│   │   └── llm_summary.py
│   ├── __init__.py
│   ├── scraping
│   │   ├── actus_twitter.txt
│   │   ├── actu_x_scraping.py
│   │   ├── get_latest_scan.py
│   │   ├── __init__.py
│   │   ├── is_release_week.py
│   │   ├── release_date.csv
│   │   ├── x_scraping.py
│   │   ├── youtube_api
│   │   │   ├── _error.py
│   │   │   ├── get_link.py
│   │   │   └── __init__.py
│   │   └── yt_subtitles.py
│   ├── static
│   │   └── op_background.jpg
│   ├── templates
│   │   ├── actu.html
│   │   ├── base.html
│   │   ├── explanation.html
│   │   ├── info.html
│   │   ├── release_status.html
│   │   └── theories.html
│   ├── text_routes.py
│   └── text_schema.sql
├── git_tuto.md
├── instance
│   └── flaskr.sqlite
├── Présentation
│   └── Présentation.md
├── README.md
└── requirements.txt
```
---
# Scraping : Script subtitles vidéo youtube de la chaîne Mont Corvo

[get_latest_scan.py](https://github.com/wlemalin/one_piece_scan/blob/main/flaskr/scraping/get_latest_scan.py)

[yt_subtitles.py](https://github.com/wlemalin/one_piece_scan/blob/main/flaskr/scraping/yt_subtitles.py)

---
# Scraping : Script Dextero pour obtenir les prochaines dates de sortie
```
# Script scrap date de sortie
```
# DB : SQLite storage

[add_db.py](https://github.com/wlemalin/one_piece_scan/blob/main/flaskr/add_db.py)

[db.py](https://github.com/wlemalin/one_piece_scan/blob/main/flaskr/db.py)

[text_schema.sql](https://github.com/wlemalin/one_piece_scan/blob/main/flaskr/text_schema.sql)

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
# Flask

---
# HTML

---
# Rendu terminal
- > Link
