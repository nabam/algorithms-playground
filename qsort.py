#!/usr/bin/env python3

from random import shuffle
from math import log
from random import randint
import sys
import test

c = 0

stack = []
threshold = 4

def _swap(array, a, b):
    if (a != b):
        t = array[a]
        array[a] = array[b]
        array[b] = t

def _partition(array, s, e):
    global c

    t = False
    m = s + ((e - s) >> 1)
    if array[m] > array[e]:
        _swap(array, m, e)
    if array[m] < array[s]:
        _swap(array, s, m)
        t = True
    if t and array[m] > array[e]:
        _swap(array, m, e)
    p = array[m]

    i = s + 1
    j = e - 1

    if (i <= j):
        c -= 1

    while i <= j:
        c += 1

        if array[i] < p:
            c -= 1

        while array[i] < p:
            i += 1
            c += 1

        if array[j] > p:
            c -= 1

        while array[j] > p:
            j -= 1
            c += 1

        if (i < j):
            _swap(array, i, j)
            i += 1
            j -= 1
        elif (i == j):
            break

    return j

def sort(array):
    global c

    if len(array) == 0:
        return

    if len(array) > threshold:
        stack.append([None,None])
        s = 0
        e = len(array) - 1

        while (len(stack) > 0):
            c += 1
            p = _partition(array, s, e);

            if (e - (p + 1)) < threshold:
                if (p - s) < threshold:
                    s,e = stack.pop()
                else:
                    e = p
            elif (p - s) < threshold:
                s = p + 1
            elif (e - (p + 1)) > (p - s):
                stack.append([p + 1, e])
                e = p
            else:
                stack.append([s, p])
                s = p + 1

    t = 0
    for i in range(1, min(len(array), threshold)):
        c += 1
        if array[i] < array[t]:
            t = i

    if t != 0:
        _swap(array, 0, t)

    for i in range(0, len(array)):
        j = i
        c += 1

        if j > 0 and array[j - 1] > array[j]:
            c -= 1

        while j > 0 and array[j - 1] > array[j]:
            c += 1
            _swap(array, j, j - 1)
            j = j - 1


if __name__ == "__main__":
    n = 1000
    a = test.gen(n)
    sort(a)
    test.verify_sorted(a)

    print('len: %s, n*log(n): %s, c: %s, k: %s' % (n, n*log(n), c, c/n/log(n)))
