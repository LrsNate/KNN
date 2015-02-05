#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import re


def tokenise(string):
    """ Tron�onnage de la chaine en une liste de tokens
    (tr�s basique)
    La ponctuation est supprim�e
    Les expressions num�riques sont remplac�es par le token NUMEXPR
    Les tokens sont minusculis�s
    """
    numre = re.compile("^[0-9][0-9\.\-\,_\/]*$")
    # on splitte sur certains caract�res
    # mais ni le point ni la virgule (cf. on veut rep�rer les tokens num�riques)
    pretoks = re.split('[ :;\(\)\[\]\!\?\"\/\^\t]+', string)
    tokens = []
    for tok in pretoks:
        if tok <> '':
            m = numre.search(tok)
            # si le token matche la regexp des nombres
            if m:
                tokens.append('NUMEXP')
            else:
                # sinon, on peut supprimer les . , - d�butant et finissant les tokens
                tok = tok.rstrip('\.\,-').lstrip('\.\,-')
                # on minusculise
                tok = tok.lower()
                # pour l'anglais, on supprime les marques de g�nitif
                if tok.endswith('\'s'):
                    tok = tok[:-2]

                if len(tok) > 0:
                    tokens.append(tok)
    return tokens
