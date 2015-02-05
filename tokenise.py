#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import re


def tokenise(string):
    """ Tronçonnage de la chaine en une liste de tokens
    (très basique)
    La ponctuation est supprimée
    Les expressions numériques sont remplacées par le token NUMEXPR
    Les tokens sont minusculisés
    """
    numre = re.compile("^[0-9][0-9\.\-\,_\/]*$")
    # on splitte sur certains caractères
    # mais ni le point ni la virgule (cf. on veut repérer les tokens numériques)
    pretoks = re.split('[ :;\(\)\[\]\!\?\"\/\^\t]+', string)
    tokens = []
    for tok in pretoks:
        if tok <> '':
            m = numre.search(tok)
            # si le token matche la regexp des nombres
            if m:
                tokens.append('NUMEXP')
            else:
                # sinon, on peut supprimer les . , - débutant et finissant les tokens
                tok = tok.rstrip('\.\,-').lstrip('\.\,-')
                # on minusculise
                tok = tok.lower()
                # pour l'anglais, on supprime les marques de génitif
                if tok.endswith('\'s'):
                    tok = tok[:-2]

                if len(tok) > 0:
                    tokens.append(tok)
    return tokens
