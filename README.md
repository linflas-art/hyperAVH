# hyperAVH
Adds inner hyperlinks in your gamebook
## Prerequisites
### A terminal
- on Linux, any terminal shell will do the job
- on Windows, use Powershell (Start > Windows Powershell)
### Python (version 3)
- on any recent Linux distribution, python 3 is already installed
- on Windows 10/11, type in Powershell:
```
python
```
This launchs Microsoft Store and asks you to install the last Python version. To be sure Python version 3 (mandatory) is installed, type below command:
```
python -V
```
### Lxml
It's a Python library which simplifies XML and HTML processing.
To install it, run below command in a shell or Powershell on Windows :
```
pip install lxml
```
## How to use
### Gamebook must be saved in LibreOffice Writer format
- Download script **odt.hyperAVH.py**.
- Copy your gamebook file in the folder where you downloaded the script.
- Run a shell terminal or Powershell and changedir to right location. For example, if you use Windows and the script is located in your Downloads directory, type :
```
cd Downloads
```
- Run the script with below options :
```
python odt.hyperAVH.py --EN my_gamebook.odt
```
By default, the script outputs the number of sections in your gamebook when it has completed.
A file prefixed with '**new_**' has been created in the same directory. That new file contains your gamebook with hyperlinks, your original file has not been modified.

- To randomly shuffle paragraphs :
```
python odt.hyperAVH.py --EN my_gamebook.odt --shuffle
```
The script returns the new range of your paragraphs as a table of numbers. By default, 1 and last paragraphs remain unchanged. If you're not satisfied with the order, you can re-run the command with this option as many times as you require.

- If you want to shuffle your paragraphs but keep some of them in their original place (in the example, 1, 156, 287, 342 and 400 will be kept):
```
python odt.hyperAVH.py --EN my_gamebook.odt --shuffle --keep 156 287 342
```

- If you use a different syntax than the usual "turn to" for your references, for example if you put a ↪ before them (as in "Fight (↪ 12)? Or flee (↪ 23)?"), this is covered through the `--prefix` parameter:
```
python odt.hyperAVH.py mon_AVH.odt --prefix="↪"
```
Said prefixes can technically be a [regular expression](https://en.wikipedia.org/wiki/Regular_expression). If you use one though, we'll take for granted that you know what you're doing and can handle relevant issues on your own.

## Technical documentation (only relevant if you plan to change the code of the script)
### Running tests
```
python -m unittest discover avh
```

# diagAVH
Generate a visual diagram from a gamebook previously processed by hyperAVH.
## Prerequisites
### Graphviz
It's a Python Library for creating graphic diagrams.
To install it, run below command in a shell or Powershell on Windows :
```
pip install graphviz
```
## How to use
### Your gamebook must have bookmarks and hyperlinks generated by hyperAVH
- Run the script with below options :
```
python diagAVH.py my_gamebook.odt
```
You get two files :
- **my_gamebook.gv** : a simple list of all linked sections in the gamebook.
- **my_gamebook.gv.svg** : the graphic diagram of your gamebook, that you can view in your preferred web browser.
The option "--text N" adds to each node of the diagram the first N characters of the section text.
