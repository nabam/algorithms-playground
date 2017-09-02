#!/usr/bin/env python3

import test

class BinTreeNode(object):
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
        self._create_leafs(BinTreeNode(), BinTreeNode())

    def is_empty(self):
        return self._value is None

class BinTree(object):
    _head = None

    def __init__(self):
        self._head = BinTreeNode()

    def insert(self, value):
        node = self._head
        while True:
            if node.is_empty():
                node.set_value(value)
                return node

            if value >= node.value():
                node = node.right()
            else:
                node = node.left()

    def in_order(self):
        stack = []
        node = self._head

        while True:
            if node.value() != None:
                stack.append([node.right(), node.value()])
                node = node.left()
            else:
                if len(stack) == 0 and node.is_empty():
                    break

                [node, v] = stack.pop()

                yield v

    def dump(self, node = None, d = 0):
        if node == None:
            return self.dump(self._head)

        if (node.value() != None):
            self.dump(node.left(), d + 1)
            print('%s%s' % ('  '*d, node.value()))
            self.dump(node.right(), d + 1)

    def height(self, node = None, height = 0):
        if node == None:
            return self.height(self._head)

        if node.is_empty():
            return height - 1

        left_height = self.height(node.left(), height + 1)
        right_height = self.height(node.right(), height + 1)

        if left_height > right_height:
            return left_height
        else:
            return right_height

if __name__ == "__main__":
    test.tree_test(BinTree(), 1000)
