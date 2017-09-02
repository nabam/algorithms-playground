#!/usr/bin/env python3

from random import shuffle

def gen(n):
    data = list(range(0, n))
    shuffle(data)
    return data

def create(data, tree):
    for v in data:
        tree.insert(v)

    return tree

def dump_tree(tree):
    tree.dump()

def verify_sorted(lst):
    t = lst[0]
    for x in lst[1:]:
        if( x != t + 1 ):
            print('Assertion failed on %s!' % x)
        t = x;

def tree_test(tree, n):
    data = gen(n)
    tree = create(data, tree)
    dump_tree(tree)
    verify_sorted(list(tree.in_order()))
    print('Height: %s' % tree.height())
