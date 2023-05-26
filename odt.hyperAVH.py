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
import argparse
import os

# -------- functions --------

# create 'bookmark' node
def bookmarks(search,paragraph):
    for n in tree.iter(search):
        #if n.text == str(paragraph) auor n.xpath("text()") == [str(paragraph)]:
        if ''.join(n.itertext()) == str(paragraph):
            bkm = etree.Element(t+'bookmark')
            bkm.set(t+'name', str(paragraph))
            n.insert(0,bkm)
            logging.debug(str(paragraph))
            logging.debug(etree.tostring(n).decode('utf-8'))
            paragraph += 1
    return paragraph

# create 'hyperlink' node
def hyperlink(number,tail):
    #logging.debug(number)
    link = etree.Element(t+'a')
    link.set(x+'type', "simple")
    link.set(x+'href', "#" + str(number))
    link.set(t+'style-name', "Internet_20_link")
    link.set(t+'visited-style-name', "Visited_20_Internet_20_Link")
    link.text = str(number)
    link.tail = tail
    return link

# -------- args --------

parser = argparse.ArgumentParser(description="hyperAVH - hyperliens pour Aventure dont Vous êtes le Héros - is a tool that automatically adds internal hyperlinks in your gamebook by finding 'turn to' expressions. It works only with Open/LibreOffice documents.")
parser.add_argument("filename", help="the name of your *ODT* file to be processed")
parser.add_argument("--EN", action="store_true", help="find english 'turn to' expressions instead of french ones")
parser.add_argument("--debug", action="store_true", help="turn on DEBUG logging (for developers)", )
args = parser.parse_args()

if args.EN:
    turn_to_regexp = "([Tt]urn[ing]*\s+to\s+)(\d+)"
    remove_links_message = "Please remove existing hyperlinks from document:"
else:
    turn_to_regexp = "([\s\(]au\s+)(\d+)"
    remove_links_message = "Veuillez supprimer les hyperliens existants du document :"

if args.debug:
    logging.basicConfig(level=logging.DEBUG)

filename = args.filename
if filename.startswith('./') or filename.startswith('.\\'):
    filename = filename[2:]

# -------- main --------

# extract archive and parse content.xml
tempdir = tempfile.mkdtemp()
with ZipFile(filename, 'r') as zip:
    zip.extractall(tempdir)
tree = etree.parse(tempdir + '/content.xml')
root = tree.getroot()
nsmap = root.nsmap
t = '{' + nsmap['text'] + '}'
x = '{' + nsmap['xlink'] + '}'

# quit if hyperlinks are already present
links = []
for h in tree.iter(t+'a'):
    links.append(h)
if links:
    print(remove_links_message)
    for h in links:
        print(h.getparent().text + h.text)
    quit()

# create bookmarks into 'heading' nodes, then 'paragraph' nodes
paragraph = 1
search = t + 'h'
paragraph = bookmarks(search, paragraph)
search = t + 'p'
paragraph = bookmarks(search, paragraph)
print(paragraph - 1)

# create turn to's
for p in tree.iter(t+'p'): # noeud "paragraph"
    numbers = []
    txt = ''.join(p.itertext()) # p.xpath("text()"):
    logging.debug(txt)
    for m in re.finditer(turn_to_regexp,txt):
        turn_to = m.group(1)
        number = m.group(2)
        numbers.append(number)

    # update 'p' node if turn_to found
    if numbers:
        # reverse processing
        for number in reversed(numbers):
            logging.debug("RENVOI = "+number)
            # process child elements if needed
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
                        else: # if node contains just the number, replace it by the hyperlink
                            link.tail = c.tail
                            c.getparent().replace(c,link)
            # process on 'p' node text directly if needed
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

# write content.xml and build new ODT
tree.write(tempdir + '/content.xml', xml_declaration = True, standalone = "yes", encoding = 'UTF-8')
if args.debug:
    tree.write('./content.xml', xml_declaration = True, standalone = "yes", encoding = 'UTF-8', pretty_print=True)

output = 'new_' + os.path.basename(filename)
shutil.make_archive(output,'zip',tempdir,'.')
shutil.move(output + '.zip', output)

logging.debug(tempdir)
if not args.debug:
    shutil.rmtree(tempdir)
    
