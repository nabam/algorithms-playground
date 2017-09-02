#!/usr/bin/env python3

import test

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

class Tree(object):
    _head = None

    def __init__(self):
        self._head = TreeNode()

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

if __name__ == "__main__":
    test.tree_test(Tree(), 1000)
