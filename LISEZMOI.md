# hyperAVH
Ajout d'hyperliens au sein d'une AVH (Aventure dont Vous êtes le Héros)
## Prérequis
### Un terminal
- sous Linux, n'importe quel terminal shell fera l'affaire
- sous Windows, utiliser Powershell (Menu Démarrer > Windows Powershell)
### Python (version 3)
- sur n'importe quelle version de Linux récente, python 3 est généralement déjà disponible
- sur Windows 10/11, taper dans Powershell la commande :
```
python
```
Cela va lancer le Microsoft Store et vous proposer d'installer la dernière version de Python. Pour s'assurer que l'installation est terminée et qu'il s'agit bien de python en version 3, taper la commande (V majuscule) :
```
python -V
```
### Lxml
Il s'agit d'une librairie Python qui permet de simplifier le traitement de fichiers XML et HTML.
Pour l'installer, il faut exécuter la commande suivante dans un terminal shell ou Powershell sous Windows :
```
pip install lxml
```
## Utilisation
### AVH au format LibreOffice Writer
- Télécharger le script **odt.hyperAVH.py**.
- Copier votre AVH dans le répertoire où se trouve le script.
- Lancer votre terminal shell ou Powershell et vous placer dans le répertoire du script. Par exemple, si vous êtes sous Windows et que le script est dans vos Téléchargements, il suffit de taper :
```
cd Downloads
```
- Exécuter le script avec comme argument le nom de votre fichier AVH :
```
python odt.hyperAVH.py mon_AVH.odt
```
Par défaut, le script renvoie le nombre de paragraphes présents dans l'AVH.
Un fichier avec le préfixe '**new_**' est alors créé dans le répertoire courant. C'est ce fichier qui contient les hyperliens, votre fichier de départ n'a pas été modifié.

- Si vous souhaitez mélanger vos paragraphes de manière aléatoire :
```
python odt.hyperAVH.py mon_AVH.odt --shuffle
```
Le script renvoie le nouvel ordonnancement de vos paragraphes sous forme d'une liste de numéros. Par défaut, le paragraphe 1 et le dernier restent inchangés. Si l'ordre ne vous convient pas, vous pouvez relancer la commande avec cette option autant de fois que vous le souhaitez.

- Si vous souhaitez mélanger vos paragraphes mais garder certains à leur place d'origine (dans l'exemple, les 1, 156, 287, 342 et 400 ne bougeront pas):
```
python odt.hyperAVH.py mon_AVH.odt --shuffle --keep 1 156 287 342 400
```

# diagAVH
Génération d'un diagramme d'AVH (Aventure dont Vous êtes le Héros) à partir d'un document modifié par hyperAVH
## Prérequis
### Graphviz
Il s'agit d'une librairie Python qui permet de créer des diagrammes.
Pour l'installer, il faut exécuter la commande suivante dans un terminal shell ou Powershell sous Windows :
```
pip install graphviz
```
## Utilisation
### Votre AVH doit avoir des repères/hyperliens générés par hyperAVH
- Exécuter le script avec comme argument le nom de votre fichier AVH :
```
python diagAVH.py mon_AVH.odt
```
On obtient deux fichiers :
- mon_AVH.gv : une simple liste des liens entre les paragraphes de votre AVH
- mon_AVH.gv.svg : le diagramme de votre AVH, que vous pouvez visualiser dans votre navigateur web préféré.
L'option "--text N" ajoute à chaque noeud du diagramme les N premiers caractères du paragraphe concerné.
