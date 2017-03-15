def f(x):
    ys = []

    # import IPython; IPython.embed()
    # import pudb; pudb.set_trace()

    for i in range(x):
        ys.append(i ** 2)
    return ys

ys = f(5)
print(ys)
print(sum(ys))
