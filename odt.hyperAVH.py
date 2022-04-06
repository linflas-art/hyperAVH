#!/usr/bin/python3
# coding: utf-8
from lxml import etree
from zipfile import ZipFile
from os.path import basename
import tempfile
import shutil
import re
import copy
import sys
import logging

try:
    filename = sys.argv[1]
except IndexError:
    print("Usage: " + sys.argv[0] + " [fichier ODT]")
    quit()

try:
    opt = sys.argv[2]
    if opt == "--debug":
        logging.basicConfig(level=logging.DEBUG)
except IndexError:
    pass
    
# extraction et parsing du document.xml
tempdir = tempfile.mkdtemp()
with ZipFile(filename, 'r') as zip:
    zip.extractall(tempdir)
tree = etree.parse(tempdir + '/content.xml')
root = tree.getroot()
nsmap = root.nsmap
t = '{' + nsmap['text'] + '}'
x = '{' + nsmap['xlink'] + '}'

# on quitte s'il y a déjà des hyperliens
links = []
for h in tree.iter(t+'a'):
    links.append(h)
if links:
    print('Supprimez les liens existants :')
    for h in links:
        print(h.getparent().text + h.text)
    quit()

# fonction de création de noeuds de type "bookmark"
def bookmarks(search,paragraph):
    for n in tree.iter(search):
        #if n.text == str(paragraph) or n.xpath("text()") == [str(paragraph)]:
        if ''.join(n.itertext()) == str(paragraph):
            bkm = etree.Element(t+'bookmark')
            bkm.set(t+'name', str(paragraph))
            n.insert(0,bkm)
            logging.debug(str(paragraph))
            logging.debug(etree.tostring(n).decode('utf-8'))
            paragraph += 1
    return paragraph

# fonction de création d'un noeud de type "hyperlink"
def hyperlink (number,tail):
    link = etree.Element(t+'a')
    link.set(x+'type', "simple")
    link.set(x+'href', "#" + str(number))
    link.set(t+'style-name', "Internet_20_link")
    link.set(t+'visited-style-name', "Visited_20_Internet_20_Link")
    link.text = str(number)
    link.tail = tail
    return link

# Création des signets dans les noeuds "heading", puis les "paragraph"
paragraph = 1
search = t + 'h'
paragraph = bookmarks(search, paragraph)
search = t + 'p'
paragraph = bookmarks(search, paragraph)
print(paragraph - 1)

# Création des renvois
for p in tree.iter(t+'p'): # noeud "paragraph"
    numbers = []
    txt = ''.join(p.itertext()) # p.xpath("text()"):
    logging.debug(txt)
    for m in re.finditer("([\s\(]au\s+)(\d+)",txt):
        au_ = m.group(1)
        number = m.group(2)
        numbers.append(number)

    # on modifie le noeud "p" s'il y a renvoi
    if numbers:
        # on commence par la fin
        for number in reversed(numbers):
            logging.debug("RENVOI = "+number)
            # traitement sur les sous-elements s'il y a lieu
            for c in p.findall('.//'):
                #logging.debug(c)
                #logging.debug("c = " + etree.tostring(c).decode('utf-8'))
                if c.tail:
                    logging.debug("cTAIL = "+c.tail)
                    if number in c.tail:
                        logging.debug("cTAIL! = "+c.tail)
                        i = c.getparent().index(c)
                        m = re.match("(.*)" + number + "(.*)",c.tail)
                        before = m.group(1)
                        after = m.group(2)
                        link = hyperlink(number,after) 
                        c.getparent().insert(i+1,link)
                        c.tail = before
                if c.text:
                    logging.debug("cTEXT = "+c.text)
                    if number in c.text:
                        logging.debug("cTEXT! = "+c.text)
                        m = re.match("(.*)" + number + "(.*)",c.text)
                        before = m.group(1)
                        after = m.group(2)
                        link = hyperlink(number,after)
                        if before or after:
                            c.insert(0,link)
                            c.text = before
                        else: # si le node ne contient que le numero, on le remplace par l'hyperlien
                            link.tail = c.tail
                            c.getparent().replace(c,link)
            # traitement directement sur le texte du noeud "p" s'il y a lieu
            if p.text:
                logging.debug("pTEXT = "+p.text)
                if number in p.text:
                    logging.debug("pTEXT! = "+p.text)
                    m = re.match("(.*)" + number + "(.*)",p.text)
                    before = m.group(1)
                    after = m.group(2)
                    link = hyperlink(number,after)
                    p.insert(0,link)
                    p.text = before
        
        logging.debug("p = " + etree.tostring(p).decode('utf-8'))

# écriture de content.xml et création du nouvel ODT
tree.write(tempdir + '/content.xml', xml_declaration = True, standalone = "yes", encoding = 'UTF-8')
#if opt == "--debug":
#    tree.write('./content.xml', xml_declaration = True, standalone = "yes", encoding = 'UTF-8', pretty_print=True)
shutil.make_archive('new_' + filename,'zip',tempdir,'.')
shutil.move('new_' + filename + '.zip', 'new_' + filename)
shutil.rmtree(tempdir)
