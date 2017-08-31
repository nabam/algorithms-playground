#!/usr/bin/python3.5


from random import shuffle
from math import log
from enum import Enum
c = 0

class Color:
    RED = 0
    BLACK = 1

def empty_node(parent = None):
    return {'value': None, 'parent': parent, 'color': Color.BLACK}

def grandparent(node):
    if node['parent'] != None:
        return node['parent']['parent']
    else:
        return None

def uncle(node):
    g = grandparent(node)
    if g is None:
        return None
    if node['parent'] is g['left']:
        return g['right']
    if node['parent'] is g['right']:
        return g['left']

def rotate_left(node):
    p = node['parent']
    r = node['right']

    node['parent'] = r
    node['right'] = r['left']
    r['left']['parent'] = node

    if p != None:
        if p['left'] is node:
            p['left'] = r
        else:
            p['right'] = r

    r['parent'] = p
    r['left'] = node

    return

def rotate_right(node):
    p = node['parent']
    l = node['left']

    node['parent'] = l
    node['left'] = l['right']
    l['right']['parent'] = node

    if p != None:
        if p['left'] is node:
            p['left'] = l
        else:
            p['right'] = l

    l['parent'] = p
    l['right'] = node

    return

def balance(n):
    global c

    u = uncle(n)
    g = grandparent(n)

    if n['parent'] is None:
        n['color'] = Color.BLACK
        return None

    if n['parent']['color'] == Color.BLACK:
        return None

    if u != None and u['color'] == Color.RED:
        n['parent']['color'] = Color.BLACK
        u['color'] = Color.BLACK
        g['color'] = Color.RED
        c += 1
        return balance(g)

    if n is n['parent']['right'] and n['parent'] is g['left']:
        rotate_left(n['parent'])
        n = n['left']
    elif n is n['parent']['left'] and n['parent'] is g['right']:
        rotate_right(n['parent'])
        n = n['right']

    n['parent']['color'] = Color.BLACK
    g['color'] = Color.RED

    if n is n['parent']['left']:
        rotate_right(g)
    else:
        rotate_left(g)

    if grandparent(g) is None:
        return g['parent']
    else:
        return None

def insert(tree, value):
    global c

    node = tree
    while True:
        c += 1

        if node['value'] is None:
            node['value']  = value
            node['color'] = Color.RED
            node['left']     = empty_node(node)
            node['right']     = empty_node(node)

            # dump(tree, 0)
            # print('---\/\/\/---')
            res = balance(node)
            if res != None:
                # dump(res, 0)
                # print('---')
                return res
            else:
                # dump(tree, 0)
                # print('---')
                return tree

        if value >= node['value']:
            node = node['right']
        else:
            node = node['left']


def in_order(tree):
    stack = []
    depth = 0
    node = tree

    while True:
        if node['value'] != None:
            stack.append([node['right'], node['value']])
            node = node['left']
        else:
            [node, v] = stack.pop()

            d = 0
            p = node['parent']
            while p != None:
                d += 1
                p = p['parent']

            if d > depth:
                depth = d
            yield v

        if len(stack) == 0 and node['value'] == None:
            break

    print('Depth: %s' % depth)

def dump(tree, d):
    if (tree['value'] != None):
        dump(tree['left'], d+1)
        print('%s%s' % ('  '*d, tree['value']))
        dump(tree['right'], d+1)

n = 10000

tree = empty_node()
data = list(range(0, n))
shuffle(data)

for v in data:
    tree = insert(tree, v)

dump(tree, 0)
result = list(in_order(tree))

t = result[0]

for x in result[1:]:
    if( x != t + 1 ):
        print('Assertion failed on %s!' % x)
    t = x;

print('len: %s, n*log(n): %s, insert_time: %s, insert_k: %s' % (n, n*log(n), c, c/n/log(n)))
