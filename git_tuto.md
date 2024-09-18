# Fonctions basiques git

## Configurer git la première fois

Après avoir installer git: 

### Configuration du nom et de l'email associés aus commits:
```
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

### Créer un projet local:
```
cd chemin/vers/votre/dossier
git init
```

### Ajouter des fichiers au projets (Local)
```
git add . 
```

Permet d'ajouter les nouveaux dossiers et les nouvelles modifications.
Après git add ., les modifications sont ajoutées dans la 'stagging area' et ne sont pas encore 
ajoutées au projet.

Pour verifier si toutes les modifications ont été ajoutées:

```
git status 
```

Une fois que les modifications ont été ajoutées à la stagging area et une fois que l'on est sur
de vouloir les garder il faut les ajouter sur le répertoire local:

```
git commit -m 'message associé au commit'
```

Ajouter un message est obligatoire sinon le commit ne fonctionne pas. 

### Connecter le projet à GitHub
Pour connecter le dépôt Git local au dépôt GitHub distant, il faut exécuter la commande suivante:

```
git remote add origin https://github.com/VotreNomUtilisateur/NomDuDepot.git 
```

On peut également se connecter au dépot GitHub à l'aide d'une clef ssh (voir doc).

### Ajouter les modifications sur le dépot distant 
Après avoir ajouter les modifications en local (commit), il faut les ajouter sur le dépot distant:
```
git push 
```

Lors du premier push, il faut associer la branche sur laquelle on est au dépot d'une branche distante:
```
git push origin nom_branche
```

Le nom par default de la branche principale est toujours 'main' ou 'master'

Si le nom de la branche n'est pas le même en local que sur GitHub:
```
git push origin nom_branche_locale:nom_branche_distante
```

On peut également lier les deux branches sans avoir à push:
```
git branch --set-upstream-to=origin/NomDeLaBranche
```

Il est cepandant plus pratique d'utiliser les mêmes noms en local que sur le repo distant. 

Pour avoir la liste des associations entre branches locales et distantes vous pouvez utiliser la commande:
```
git branch -vv
```

### Cloner un dépot distant
Pour cloner un dépot distant:
```
git clone https://github.com/VotreNomUtilisateur/NomDuDepot.git
```

Toutes les branches du dépot distant sont automatiquement créees en local. Voir la partie suivante pour 
l'utilisation des branches. 


## Utilisation des branches

### Afficher la liste des branches existantes
Afficher les branches locales:
```
git branch 
```

Pour afficher les branches distantes 
```
git branch -r
```

Pour afficher les branches locales et distantes 
```
git branch -a 
```

### Créer une branche en local
Pour créer une branche en local si elle n'existe pas déjà:
```
git checkout -b NomDeLaBranche
```

Pour créer une branche à partir d'une branche existante:
```
git checkout -b NomDeLaBranche BrancheACopier
```

Cette commande permet de créer une branche et d'aller sur celle-ci.
Si la branche existe déjà:
```
git checkout -B NomDeLaBranche
git checkout -B NomDeLaBranche BrancheACopier
```

Ces commandes permettent de réinitialiser une branche existante et d'aller dessus.
La seconde commande permet de faire pointer la branche a réinitialiser sur une autre 
branche existante. 

Pour changer de branche vers une branche déjà existante:
```
git checkout NomDeLaBranche 
```

La commande git switch peut également permettre de changer de branche ou d'en créer une et 
peut être plus intuitive notemment pour la restauration de fichiers (voir doc git).

### Ajout d'une branche locale au dépot distant

Pour ajouter une branche qui existe uniquement sur le dépot local au dépot distant il suffit 
de suivre les mêmes étapes que pour associer une branche distante à une brache locale: 
```
git push origin nom_branche
```

### Mise à jour d'une branche locale à partir du dépot distant
Ajout test






