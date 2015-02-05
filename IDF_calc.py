#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from __future__ import print_function

from sys import stderr
from argparse import ArgumentParser
from HTMLParser import HTMLParser
from tokenise import tokenise
from math import log


def info(str):
    print("[INFO] ", str, file=stderr)

class CorpusParser(object, HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.documents_count = 0.
        self.words = {}
        self.current_body = set()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

    def handle_endtag(self, tag):
        closed_tag = self.tags.pop()
        if closed_tag != "body":
            return
        for w in self.current_body:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
        self.documents_count += 1
        if self.documents_count % 100 == 0:
            info("Analyzed %d documents." % self.documents_count)

    def handle_data(self, data):
        if not self.tags or self.tags[-1] != "body":
            return
        self.current_body = self.current_body.union(set(tokenise(data.rstrip('\n'))))

    def get_final_data(self):
        for k in self.words:
            self.words[k] = log(self.documents_count / self.words[k])
        return self.words

ap = ArgumentParser(usage="Generate a file containing word IDFs from SGML files")
ap.add_argument("file", help="The SGML file to be analysed")
argv = ap.parse_args()
fd = open(argv.file)

cp = CorpusParser()

for line in fd:
    cp.feed(line)
cp.close()

res = cp.get_final_data()
for k in res:
    print("%s\t%f" % (k, res[k]))