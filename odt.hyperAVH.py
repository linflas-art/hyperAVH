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
import random
import array

# -------- functions --------

# better display for debug
def show(node):
    xmlns = ' xmlns:\S+'
    return re.sub(xmlns,'',etree.tostring(node).decode('utf-8'))

# create 'bookmark' node
def bookmarks(search,paragraph):
    for n in tree.iter(search):
        if ''.join(n.itertext()).strip() == str(paragraph):
            bkm = etree.Element(t+'bookmark')
            bkm.set(t+'name', str(paragraph))
            n.insert(0,bkm)
            logging.debug(str(paragraph))
            logging.debug(show(n))
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

# isolate link from text element
def isolate_link(number,text):
    m = re.search("(.*\D+)" + number + "(\D+.*)",text)
    try:
        before = m.group(1)
        after = m.group(2)
        logging.debug("BEFORE "+ before)
        logging.debug("AFTER "+ after)
        return before, after
    except AttributeError:
        m = re.search("(.*)" + number + "(.*)",text)
        before = m.group(1)
        after = m.group(2)
        logging.debug("BEFORE "+ before)
        logging.debug("AFTER "+ after)
        if re.search("\d$",before) or re.search("^\d",after): # skip when number is substring of another number
            logging.debug("SKIP " + number)
            return "SKIP", "SKIP"
        else:
            return before, after
            
def default_locale_prefix(locale):
    if locale == 'en':
        return "([Tt]urn[ing]*\s+to)"
    if locale == 'fr':
        return "([\s\(]au)"
    raise ValueError(f'Unsupported locale: "{locale}"')

def prefix(kwargs):
    if "prefix" in kwargs and kwargs["prefix"]:
        return kwargs["prefix"]
    if "locale" in kwargs and kwargs["locale"]:
        return default_locale_prefix(kwargs["locale"])
    raise ValueError('Please provide a locale or an explicit prefix')

def find_numbers(sentence, **kwargs):
    numbers = []
    regexp = prefix(kwargs) + "\s*(\d+)"
    for m in re.finditer(regexp, sentence):
        number = m.group(m.lastindex)
        numbers.append(number)
    return numbers

# https://docs.python.org/3/library/__main__.html
if __name__ == '__main__':

    # -------- args --------

    parser = argparse.ArgumentParser(description="hyperAVH - hyperliens pour Aventure dont Vous êtes le Héros - is a tool that automatically adds internal hyperlinks in your gamebook by finding 'turn to' expressions. It works only with LibreOffice Writer documents.")
    parser.add_argument("filename", help="the name of your *ODT* file to be processed")
    parser.add_argument("--EN", action="store_true", help="find english 'turn to' expressions instead of french ones")
    parser.add_argument("--shuffle", action="store_true", help="shuffle paragraphs")
    parser.add_argument("--keep", nargs='+', type=int, help="when shuffle is on, keep the ones listed in place (default 1 <LAST>)")
    parser.add_argument("--debug", action="store_true", help="turn on DEBUG logging (for developers)")
    parser.add_argument("--prefix", help="custom prefix before wannabe hyperlinks")
    args = parser.parse_args()

    locale = 'fr'
    remove_links_message = "Veuillez supprimer les hyperliens existants du document :"
    remove_bookmarks_message = "Veuillez supprimer tous les repères de texte du document."

    if args.EN:
        locale = 'en'
        remove_links_message = "Please remove existing hyperlinks from document:"
        remove_bookmarks_message = "Please remove all bookmarks from document."

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
    o = '{' + nsmap['office'] + '}'

    # quit if hyperlinks/bookmarks are already present
    links = []
    for h in tree.iter(t+'a'):
        links.append(h)
    if links:
        print(remove_links_message)
        for h in links:
            print(h.getparent().text + h.text)
        quit()
    bkmarks = []
    for h in tree.iter(t+'bookmark'):
        bkmarks.append(h)
    if bkmarks:
        print(remove_bookmarks_message)
        quit()        

    bugged_sections = []

    # create bookmarks into 'heading' nodes, then 'paragraph' nodes
    paragraph = 1
    search = t + 'h'
    paragraph = bookmarks(search, paragraph)
    search = t + 'p'
    paragraph = bookmarks(search, paragraph)
    print(paragraph - 1)

    # create turn to's
    for p in tree.iter(t+'p'): # noeud "paragraph"
        logging.debug('P ================================================')
        logging.debug(show(p))
        sentence = ''.join(p.itertext())
        numbers = find_numbers(sentence, locale=locale, prefix=args.prefix)
        logging.debug(numbers)
        # update 'p' node if turn_to found
        if numbers:
            # reverse processing
            for number in reversed(numbers):
                logging.debug(number + " ---------------------------------------------------")
                done = False
                # process child nodes first
                for c in p.xpath('*'):
                    logging.debug("c = " + show(c))
                    if c.tail and not done:
                        logging.debug("cTAIL = "+c.tail)
                        if number in c.tail:
                            logging.debug("cTAIL !!! = "+c.tail)
                            i = c.getparent().index(c)
                            before, after = isolate_link(number,c.tail)
                            if before != "SKIP":
                                link = hyperlink(number,after)
                                c.getparent().insert(i+1,link)
                                c.tail = before
                                logging.debug("DONE " + number)
                                done = True
                    if c.text and not done:
                        logging.debug("cTEXT = "+c.text)
                        if number in c.text:
                            logging.debug("cTEXT !!! = "+c.text)
                            before, after = isolate_link(number,c.text)
                            if not (before and after) and c.get(x+'href'):
                                logging.debug("SKIP " + number)
                            elif before != "SKIP":
                                link = hyperlink(number,after)
                                c.insert(0,link)
                                c.text = before
                                logging.debug("DONE " + number)
                                done = True
                # process current 'p' node
                if p.text and not done:
                    logging.debug("pTEXT = "+p.text)
                    if number in p.text:
                        logging.debug("pTEXT !!! = "+p.text)
                        before, after = isolate_link(number,p.text)
                        if before != "SKIP":
                            link = hyperlink(number,after)
                            p.insert(0,link)
                            p.text = before
                            logging.debug("DONE " + number)
                            done = True
                if not done:
                    logging.error(f'Could not generate hyperlink pointing to section {number} in sentence "{sentence}". Please add it by hand.')
                    if args.shuffle:
                        logging.warning(f'Section {number} will be excluded from the shuffle to avoid further incidents.')
                        bugged_sections.append(int(number))
            
            logging.debug("p = " + show(p))

    # -------- shuffle --------
    
    if args.shuffle:
        # shuffle : create randomized paragraphs array
        length = sum(1 for _ in tree.iter(t+'bookmark'))
        new_paragraphs = list(range(1,length+1))
        random.shuffle(new_paragraphs)
        # put back kept paragraphs to their own place
        kept = (args.keep or []) + [1, length] + bugged_sections
        for k in kept:
            # logging.debug("k="+str(k))
            a = new_paragraphs[k-1] # value at index k
            # logging.debug("a="+str(a))
            b = new_paragraphs.index(k) # index where k is the value
            # logging.debug("b="+str(b))
            new_paragraphs[k-1] = k
            new_paragraphs[b] = a
        new_paragraphs.insert(0,0)

        # display new paragraphs order
        print(new_paragraphs)

        paragraph=0
        blocks = []
        block = []
        # split document into blocks
        for e in tree.iter():
            if e.tag == t +'p' or e.tag == t +'h':
                logging.debug("~ ~ ~")
                logging.debug(show(e))
                foundbkm = False
                for ee in e.iter(): 
                    if ee.tag == t + 'bookmark':
                        foundbkm = True
                        blocks.append(block)
                        block = []
                        paragraph += 1
                        logging.debug("------------------------------------------")
                        logging.debug(show(ee))
                if not foundbkm:
                    block.append(e) # store text
        # last paragraph
        blocks.append(block)

        logging.debug("\n\nBLOCKS =====================================\n")

        for b in blocks:
            logging.debug("------------- "+str(blocks.index(b)))
            for bb in b:
                logging.debug("~ ~ ~ "+str(b.index(bb)))
                logging.debug(show(bb))

        logging.debug("\n\nNEW BLOCKS =====================================\n")

        # rearrange blocks according to new paragraphs
        new_blocks = [ blocks[0] ] # not used, but better have it at first index
        for i in range(1,len(blocks)):
            new_blocks.append(blocks[new_paragraphs[i]])

        for b in new_blocks:
            logging.debug("------------- "+str(new_blocks.index(b)))
            for bb in b:
                logging.debug("~ ~ ~ "+str(b.index(bb)))
                logging.debug(show(bb))

        # clean all paragraphs, keep only titles
        paragraph = 1
        while paragraph <= length:
            skip = False
            foundbkm = False
            foundnextbkm = False
            for e in tree.iter():
                if e.tag == t +'p' or e.tag == t +'h':
                    for ee in e.iter():
                        if ee.tag == t + 'bookmark':
                            if ee.get(t+'name') == str(paragraph):
                                logging.debug(show(ee)+' --->')
                                foundbkm = True
                                foundnextbkm = False
                                skip = True
                                if paragraph == length:
                                    paragraph += 1
                                break
                            elif ee.get(t+'name') == str(paragraph+1):
                                # logging.debug(show(ee)+' <---')
                                foundbkm = False
                                foundnextbkm = True
                                paragraph += 1
                                break
                    if skip: # skip to next node
                        skip = False
                        continue
                    if foundbkm and not foundnextbkm: # remove text until next bkm or the very end
                        logging.debug('DEL '+show(e))
                        e.getparent().remove(e)
                    if foundnextbkm:
                        break
        logging.debug('END --->')

        # add new block content after each title
        paragraph = 1
        while paragraph < length:
            foundnextbkm = False
            for e in tree.iter():
                if paragraph >= length:
                    break
                if e.tag == t +'p' or e.tag == t +'h':
                    for ee in e.iter():
                        if ee.tag == t + 'bookmark':
                            if ee.get(t+'name') == str(paragraph+1) or paragraph == length:
                                logging.debug(show(ee)+' <---')
                                foundnextbkm = True
                                break
                    if foundnextbkm: # add new block
                        for new_e in new_blocks[paragraph]:
                            logging.debug('ADD '+show(new_e))
                            e.addprevious(new_e)
                        paragraph += 1
        # final paragraph ?
        # for e in tree.iter(o+'text'):
        #     for new_e in new_blocks[paragraph]:
        #         logging.debug('ADD '+show(new_e))
        #         e.append(new_e)
        logging.debug('END <---')

        # replace hyperlinks
        for l in tree.iter(t+'a'):
            number = int(l.text)
            new_number = new_paragraphs.index(number)
            logging.debug(str(number)+' <> '+str(new_number))
            l.set(x+'href', "#" + str(new_number))
            l.text = str(new_number)
    # end shuffle ------------------------------------------

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
        
