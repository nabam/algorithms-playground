#!/usr/bin/env python3

import test
from bintree import BinTree, BinTreeNode

class RBTreeNode(BinTreeNode):
    _parent = None
    _color  = None

    def __init__(self, parent = None):
        super(RBTreeNode, self).__init__()
        self._parent = parent
        self.set_black()

    def set_value(self, value):
        self._value = value
        self.set_red()
        self._create_leafs(RBTreeNode(self), RBTreeNode(self))

    def parent(self):
        return self._parent

    def color(self):
        return self._color

    def set_red(self):
        self._color = 1

    def set_black(self):
        self._color = 0

    def is_black(self):
        return self._color == 0

    def is_red(self):
        return self._color == 1

    def grandparent(self):
        if self._parent != None:
            return self._parent._parent
        else:
            return None

    def uncle(self):
        g = self.grandparent()
        if g is None:
            return None
        if self._parent is g._left:
            return g._right
        if self._parent is g._right:
            return g._left

    def rotate_left(self):
        p = self._parent
        r = self._right

        self._parent    = r
        self._right     = r._left
        r._left._parent = self

        if p != None:
            if p._left is self:
                p._left = r
            else:
                p._right = r

        r._parent = p
        r._left   = self

        return r

    def rotate_right(self):
        p = self._parent
        l = self._left

        self._parent     = l
        self._left       = l._right
        l._right._parent = self

        if p != None:
            if p._left is self:
                p._left = l
            else:
                p._right = l

        l._parent = p
        l._right  = self

        return l

class RBTree(BinTree):
    def __init__(self):
        self._head = RBTreeNode()

    def insert(self, value):
        node = super(RBTree, self).insert(value)
        self.__balance(node)
        return node

    def __balance(self, node):
        u = node.uncle()
        g = node.grandparent()

        if node.parent() is None:
            node.set_black()
            return

        if node.parent().is_black():
            return

        if u != None and u.is_red():
            node.parent().set_black()
            u.set_black()
            g.set_red()
            self.__balance(g)
            return

        n = node
        if n is node.parent().right() and node.parent() is g.left():
            node.parent().rotate_left()
            n = node.left()
        elif n is node.parent().left() and node.parent() is g.right():
            node.parent().rotate_right()
            n = node.right()

        n.parent().set_black()
        g.set_red()

        top = None

        if n is n.parent().left():
            top = g.rotate_right()
        else:
            top = g.rotate_left()

        if top.parent() is None:
            self._head = top

        return

if __name__ == "__main__":
    test.tree_test(RBTree(), 1000)
