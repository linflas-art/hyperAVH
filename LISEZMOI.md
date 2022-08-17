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
Par défaut, le script renvoit le nombre de paragraphes présents dans l'AVH.
Un fichier avec le préfixe '**new_**' est alors créé dans le répertoire courant. C'est ce fichier qui contient les hyperliens, votre fichier de départ n'a pas été modifié.
