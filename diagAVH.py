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
import graphviz

# -------- functions --------

# -------- args --------

parser = argparse.ArgumentParser(description="creates diagram from your gamebook, based on hyperAVH generated document")
parser.add_argument("filename", help="the name of your *ODT* file to be processed")
parser.add_argument("--debug", action="store_true", help="turn on DEBUG logging (for developers)", )
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)

filename = args.filename
if filename.startswith('./') or filename.startswith('.\\'):
    filename = filename[2:]
diagname = filename.replace('odt','gv')

# -------- main --------

# extract archive and parse content.xml
tempdir = tempfile.mkdtemp()
with ZipFile(filename, 'r') as zip:
    zip.extractall(tempdir)
tree = etree.parse(tempdir + '/content.xml')
root = tree.getroot()
nsmap = root.nsmap
t = '{' + nsmap['text'] + '}'

# quit if hyperlinks or bookmarks are missing or not accurante
lfound=0
bfound=0
for l in tree.iter(t+'a'):
    logging.debug(l.text)
    try:
        if re.match("^\d+$",l.text):
            lfound += 1
    except TypeError:
        print(tempdir)
        quit()
for b in tree.iter(t+'bookmark'):
    if re.match("^\d+$",b.get(t+'name')):
        bfound += 1
if not lfound or not bfound:
    print("No links or bookmarks were found. Please run hyperAVH on your gamebook first.")
    quit()

# init diagram
dot = graphviz.Digraph(comment=diagname)
section = "0"
get_next_text = False
# main loop
for e in tree.iter():
    # search section number
    if e.tag == t + 'bookmark':
        section = e.get(t+'name')
        get_next_text = True
    # create node and include part of text that follows
    if e.text and get_next_text and e.tag == t + 'p':
        logging.debug(section+":"+e.text)
        extract = e.text[0:10]
        gvtext = ''.join(char if idx % 25 or idx == 0 else char+'\n' for idx,
              char in enumerate(extract)) + "..."
        dot.node(section,section+"\n"+gvtext)
        get_next_text = False
    # construct edges between nodes
    if e.tag == t + 'a':
        dot.edge(section,e.text)

# render diagram
dot.format = 'svg'
dot.render(diagname).replace('\\', '/')

# cleanup
shutil.rmtree(tempdir)
quit()
