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
- Run a shell terminal ou Powershell and changedir to right location. For example, if you use Windows and the script is located in your Downloads directory, type :
```
cd Downloads
```
- Run the script with below options :
```
python odt.hyperAVH.py --EN my_gamebook.odt
```
By default, the script outputs the number of sections in your gamebook when it has completed.
A file prefixed with '**new_**' has been created in the same directory. That new file contains your gamebook with hyperlinks, your original file has not been modified.
