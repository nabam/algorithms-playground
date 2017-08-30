#!/usr/bin/python3.5

from random import shuffle
from math import log
from random import randint
import sys

c = 0

stack = []
threshold = 4

def dump(a):
    if len(a) > 0:
        sys.stdout.write('%s' % a[0])
        for i in range(1, len(a)):
            sys.stdout.write(', %s' % a[i])

    sys.stdout.write('\n')

def swap(array, a, b):
    if (a != b):
        t = array[a]
        array[a] = array[b]
        array[b] = t

def partition(array, s, e):
    global c

    t = False
    m = s + ((e - s) >> 1)
    if array[m] > array[e]:
        swap(array, m, e)
    if array[m] < array[s]:
        swap(array, s, m)
        t = True
    if t and array[m] > array[e]:
        swap(array, m, e)
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
            swap(array, i, j)
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
            p = partition(array, s, e);

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
        swap(array, 0, t)

    for i in range(0, len(array)):
        j = i
        c += 1

        if j > 0 and array[j - 1] > array[j]:
            c -= 1

        while j > 0 and array[j - 1] > array[j]:
            c += 1
            swap(array, j, j - 1)
            j = j - 1


n = 10000
a = list(range(0, n))
shuffle(a)
sort(a)

t = a[0]
for x in a[1:]:
    if( x != t + 1 ):
        print('Assertion failed on %s!' % x)
    t = x;

print('len: %s, n*log(n): %s, c: %s, k: %s' % (n, n*log(n), c, c/n/log(n)))


