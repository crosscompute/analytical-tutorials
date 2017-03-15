from random import randint
random_integers = [randint(-1, 1) for x in xrange(3)]
is_negative = lambda x: x > 0
if any(is_negative(x) for x in random_integers):
    print('No')
