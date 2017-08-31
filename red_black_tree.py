#!/usr/bin/python3.5


from random import shuffle
from math import log
c = 0

class TreeNode(object):
    _value  = None
    _left   = None
    _right  = None

    def _create_leafs(self, left, right):
        self._left = left
        self._right = right

    def left(self):
        return self._left

    def right(self):
        return self._right

    def value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self._create_leafs(TreeNode(), TreeNode())

    def is_empty(self):
        return self._value is None

class RBTreeNode(TreeNode):
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

class Tree(object):
    _head = None

    def __init__(self):
        self._head = TreeNode()

    def insert(self, value):
        global c

        node = tree._head
        while True:
            c += 1

            if node.is_empty():
                node.set_value(value)
                return node

            if value >= node.value():
                node = node.right()
            else:
                node = node.left()

    def in_order(self):
        stack = []
        node = tree._head

        while True:
            if node.value() != None:
                stack.append([node.right(), node.value()])
                node = node.left()
            else:
                if len(stack) == 0 and node.is_empty():
                    break

                [node, v] = stack.pop()

                yield v

    def depth(self, node = None, depth = 0):
        if node == None:
            return self.depth(self._head)

        if node.is_empty():
            return depth

        depth += 1

        left_depth = self.depth(node.left(), depth)
        right_depth = self.depth(node.right(), depth)

        if left_depth > right_depth:
            return left_depth
        else:
            return right_depth

    def dump(self, node = None, d = 0):
        if node == None:
            return self.dump(self._head)

        if (node.value() != None):
            self.dump(node.left(), d + 1)
            print('%s%s' % ('  '*d, node.value()))
            self.dump(node.right(), d + 1)

class RBTree(Tree):
    def __init__(self):
        self._head = RBTreeNode()

    def insert(self, value):
        node = super(RBTree, self).insert(value)
        self.__balance(node)
        return node

    def __balance(self, node):
        global c

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
            c += 1
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

n = 1000

data = list(range(0, n))
shuffle(data)

tree = RBTree()
for v in data:
    tree.insert(v)
tree.dump()

result = list(tree.in_order())
t = result[0]
for x in result[1:]:
    if( x != t + 1 ):
        print('Assertion failed on %s!' % x)
    t = x;

print('Depth: %s' % tree.depth())
print('len: %s, n*log(n): %s, insert_time: %s, insert_k: %s' % (n, n*log(n), c, c/n/log(n)))
