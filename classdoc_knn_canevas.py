#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys
import re
from optparse import OptionParser


class Example:
    """
    Un exemple : 
    vector = représentation vectorielle (Ovector) d'un objet
    gold_class = la classe gold pour cet objet
    """
    def __init__(self, example_number, gold_class):
        self.gold_class = gold_class
        self.example_number = example_number
        self.vector = Ovector()

    def add_feat(self, featname, val):
        self.vector.add_feat(featname, val)


class Ovector:
    """
    Un vecteur représentant un objet

    membres
    - f= simple dictionnaire nom_de_trait => valeur
         Les traits non stockés correspondent à une valeur nulle
    - norm_square : la norme au carré
    """
    def __init__(self):
        self.f = {}
        self.norm_square = 0

    def add_feat(self, featname, val=0.0):
        self.f[featname] = val

    def set_norm_square(self):
        """ calcul et stockage de la norme au carré (utile pour le calcul optimisé de la distance) """
        self.norm_square = sum([x ** 2 for x in self.f.values()])

    def prettyprint(self):
        for feat in sorted(self.f, lambda x, y: cmp(self.f[y], self.f[x]) or cmp(x, y)):
            print feat + "\t" + str(self.f[feat])

    def distance_to_vector(self, other_vector):
        """ distance euclidienne entre self et other_vector, en ayant precalculé les normes au carre de chacun """
        # TODO
        # NB: passer par la formulation  sigma [ (ai - bi)^2 ] = sigma (ai^2) + sigma (bi^2) -2 sigma (ai*bi) 
        #                                                    = norm_square(A) + norm_square(B) - 2 A.B
        res = self.norm_square + other_vector.norm_square
        rest = 0.
        for key in self.f:
            if key in other_vector.f:
                rest += self.f[key] * other_vector.f[key]
        return res - 2 * rest


class KNN:
    """
    K-NN pour la classification de documents (multiclasse)

    membres = 

    k = l'hyperparametre K : le nombre de voisins a considerer

    examples = liste d'instances de Example

    classes = liste des classes (telles que recensées dans les exemples)

    """
    def __init__(self, _examples, _k=1, _weight_neighbors=False, _trace=False):
        """ 
        simple positionnement des membres et recensement des classes connues
        """
        # les exemples : liste d'instances de Example
        self.examples = _examples
        # le nb de voisins
        self.k = _k
        # booleen : on pondere les voisins (par inverse de la distance) ou pas
        self.weight_neighbors = _weight_neighbors

        self.trace = _trace
        
        # recensement des classes connues
        self.classes = set([x.gold_class for x in self.examples])

    def classify(self, ovector):
        """
        A partir d'un vecteur de traits représentant un objet
        retourne la classe assignée, d'après l'algo K-NN et les exemples stockés ds self.examples
        """
        # TODO
        examples_with_distances = []
        for ex in self.examples:
            examples_with_distances.append((ex, ovector.distance_to_vector(ex.vector)))

        sorted_examples = sorted(examples_with_distances, cmp=lambda x, y: cmp(x[1], y[1]))
        classes = {}
        i = 0
        max_index = min(self.k, len(sorted_examples))
        while i < max_index:
            if sorted_examples[i][0].gold_class in classes:
                classes[sorted_examples[i][0].gold_class] += 1. / sorted_examples[i][1] if weight_neighbors else 1
            else:
                classes[sorted_examples[i][0].gold_class] = 1. / sorted_examples[i][1] if weight_neighbors else 1
            i += 1
        return max(classes, key=classes.get)

    def evaluate_on_test_set(self, _test_examples):
        """ Application du classifieur sur une liste d'exemples de test, et evaluation (accuracy)
            Retourne la precision (en pourcentage), le nb d'exemples bien classés, le nb total d'exemples"""
        _acc = 0.
        _nbcorrect = 0.
        _nbtotal = 0.

        # TODO
        for ex in _test_examples:
            _nbtotal += 1
            if ex.gold_class == self.classify(ex.vector):
                _nbcorrect += 1
        _acc = _nbcorrect / _nbtotal
        return _acc, _nbcorrect, _nbtotal
        

def read_examples(infile):
    """ Lit un fichier d'exemples 
    et retourne une list d'instances de Example
    """
    stream = open(infile)
    _examples = []
    example = None
    while 1:
        line = stream.readline()
        if not line:
            break
        line = line[0:-1]
        if line.startswith("EXAMPLE_NB"):
            if example is not None:
                example.vector.set_norm_square()
                _examples.append(example)
            cols = line.split('\t')
            gold_class = cols[3]
            example_number = cols[1]
            example = Example(example_number, gold_class)
        elif line and example is not None:
            (featname, val) = line.split('\t')
            example.add_feat(featname, float(val))
    
    if example is not None:
        example.vector.set_norm_square()
        _examples.append(example)
    return _examples

usage = """ CLASSIFIEUR de DOCUMENTS, de type K-NN

  %prog [options] EXAMPLES_FILE TEST_FILE

  EXAMPLES_FILE et TEST_FILE sont au format *.examples

"""

parser = OptionParser(usage=usage)
parser.add_option("--trace", action="store_true", dest="trace", default=False,
                  help="A utiliser pour declencher un mode verbeux. Default=False")
parser.add_option("--weight-neighbors", action="store_true", dest="weight_neighbors", default=False,
                  help="A utiliser pour declencher la ponderation des voisins lors "
                       "du vote (ponderation par la distance inverse). Default=False")
parser.add_option("--k", dest="k", default=1,
                  help='Hyperparametre K : le nombre de voisins a considerer pour la classification. Default=1')
(opts, args) = parser.parse_args()

k = int(opts.k)
trace = bool(opts.trace)
weight_neighbors = bool(opts.weight_neighbors)

if len(args) < 1:
    exit(usage)

examples_file = args[0]
test_file = None
if len(args) > 1:
    test_file = args[1]

#------------------------------------------------------------
# Chargement des exemples du classifieur KNN
examples = read_examples(examples_file)

#------------------------------------------------------------
# Cas où un fichier de test est fourni
if test_file:
    test_examples = read_examples(test_file)

    # le classifieur
    myclassifier = KNN(_examples=examples,
                       _k=k,
                       _weight_neighbors=weight_neighbors,
                       _trace=trace)

    (acc, nbcorrect, nbtotal) = myclassifier.evaluate_on_test_set(test_examples)

    print "ACCURACY =", acc, '(',  nbcorrect, '/', nbtotal, ')'
