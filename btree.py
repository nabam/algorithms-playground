#!/usr/bin/env python3

import test

class BTreeNode(object):
    _values   = None
    _children = None
    _parent = None
    _m = None

    def __init__(self, m, parent = None, values = None, children = None):
        self._m = m

        self._values = []
        self._children = []

        if values != None:
            if len(values) > m - 1:
                raise Exception("B-Tree node can contain only m-1 values (m is %s)" % (m))
            self._values = values

        if children != None:
            self._children = children

        self._parent = parent

    def values(self):
        return self._values

    def get_child(self, value):
        for i in range(0, len(self._values)):
            if value <= self._values[i]:
                if i < len(self._children):
                    return self._children[i]

        if len(self._values) < len(self._children):
            return self._children[len(self._values)]

    def parent(self):
        return self._parent

    def children(self):
        return self._children

    def insert(self, value, l = None, r = None):
        split = False

        if len(self._values) == 0:
            self._values.append(value)
            self._children.append(l)
            self._children.append(r)
        else:
            found = False
            for i in range(0, len(self._values)):
                if value <= self._values[i]:
                    self._values.insert(i, value)
                    self._children.insert(i, l)
                    self._children[i + 1] = r
                    found = True
                    break

            if not found:
                self._values.append(value)
                self._children[len(self._values) - 1] = l
                self._children.append(r)

        # hackish approach
        if len(self._children) > self._m:
            # perform split, return root if touched
            return self._split()

    # should be in a tree class
    def _split(self):
        med = len(self._values) >> 1

        parent = self.parent()
        if parent == None:
            parent = BTreeNode(self._m, None)

        l = BTreeNode(self._m, parent, self._values[:med], self._children[:med + 1])
        for c in self._children[:med + 1]:
            if c != None:
                c._parent = l

        r = BTreeNode(self._m, parent, self._values[med + 1:], self._children[med + 1:])
        for c in self._children[med + 1:]:
            if c != None:
                c._parent = r

        insert = parent.insert(self._values[med], l, r)

        if insert != None:
            # root passed
            return insert
        elif parent.parent() == None:
            # "root found"
            return parent

class BTree(object):
    _head = None
    _m = None

    def __init__(self, m):
        self._head = BTreeNode(m)
        self._m = m

    def insert(self, value):
        node = self._head

        child = node.get_child(value)
        while child != None:
            node = child
            child = child.get_child(value)

        insert = node.insert(value)
        if insert != None:
            self._head = insert
        return

    def dump(self, node = None, d = 0):
        if node == None:
            return self.dump(self._head)

        print('%s%s' % ('  '*d, node.values()))
        for c in node.children():
            if c != None:
                self.dump(c, d + 1)

    def in_order(self, node=None):
        if node == None:
            yield from self.in_order(self._head)
            return

        i = 0
        children = node.children()

        for v in node.values():
            if children[i] != None:
                yield from self.in_order(children[i])

            i += 1
            yield v

        if children[i] != None:
            yield from self.in_order(children[i])

    def height(self, node=None, height=0):
        if node == None:
            return self.height(self._head, 0)

        mheight = height

        for c in node.children():
            if c != None:
                d = self.height(c, height + 1)

                if d > mheight:
                    mheight = d

        return mheight

if __name__ == "__main__":
    test.tree_test(BTree(30), 10000)
