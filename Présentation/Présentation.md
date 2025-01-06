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
Structure du dossier 
¦   #Play vs DDQN continu.py
¦   #Play vs DDQN discret.py
¦   1-pong_Qlearning_Discret.py
¦   1.1-pong_Qlearning_Discret_decay.py
¦   1.2-pong_Qlearning_rdm.py
¦   1.5-pong_Qlearning_Continu.py
¦   2-pong_DQN_Discret.py
¦   2.5-pong_DQN_Continu.py
¦   3-pong_DDQN_Discret.py
¦   3.5-pong_DDQN_Continu.py
¦   Fonctions.md
¦   README.md
¦   requirements.txt
¦   
+---.ipynb_checkpoints
¦       pong_DQN_CPU-checkpoint.py
¦       pong_DQN_GPU-checkpoint.py
¦       pong_Qlearning-checkpoint.py
¦       
+---Graphics
¦       1-Q_learning_analysis.py
¦       2-DQN_and_DDQN_discret_analysis.py
¦       Deep Q Learning.png
¦       Deep Q Learning_2.png
¦       Deep Q Learning_3.png
¦       Different_epsilon__min.png
¦       EnvironnementScreen.png
¦       EnvironnementScreenWithCoords.png
¦       EpsilonDecay_MarginEffect_analysis.py
¦       Q_Learning_tabulaire.png
¦       Q_Learning_tabulaire_2.png
¦       SchemaNNPong.png
¦       Space_size.py
¦       taille_espace_etat.png
¦       Évolution de la fonction de perte (Loss) en Continu.png
¦       Évolution de la fonction de perte (Loss) en Discret.png
¦       Évolution des Estimate Value and True Value en Continu.png
¦       Évolution des Estimate Value and True Value en Discret.png
¦       
+---LearningData
¦       1.1_q_learning_decay_log.csv
¦       1.2_q_learning_rdm_log.csv
¦       1.5_q_learning_continuous_log.csv
¦       1_q_learning_log.csv
¦       2.5_pong_dqn_continuous_training_log.csv
¦       2_pong_dqn_discret_training_log.csv
¦       3.5_pong_double_dqn_continuous_training_log.csv
¦       3_pong_double_dqn_discret_training_log.csv
¦       
+---ModelsPTH
¦       2.5_dqn_continuous.pth
¦       2_dqn_discret.pth
¦       3.5_Ddqn_continuous.pth
¦       3_Ddqn_discret.pth
¦       
+---Records
        IA_PONG_usebug.mp4
        IA_PONG_usebugv2.mp4
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
