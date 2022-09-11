from cmath import pi
from math import cos, sin


def f1(x):
    x = x[0]

    if x <= 1:
        return -x
    elif 1 < x <= 3:
        return x-2
    elif 3 < x <= 4:
        return 4-x
    elif x > 4:
        return x-4

def f2(x):
    return (x[0]-5)**2

FOO1 = [f1, f2]
bounds1 = [(-5, 10)]

def f3(x):
    x, y = x
    A1 = 0.5*sin(1) - 2*cos(1) + sin(2) - 1.5*cos(2)
    A2 = 1.5*sin(1) - cos(1) + 2*sin(2) - 0.5*cos(2)
    B1 = lambda x, y: 0.5*sin(x) - 2*cos(x) + sin(y) - 1.5*cos(y)
    B2 = lambda x, y: 1.5*sin(x) - cos(x) + 2*sin(y) - 0.5*cos(y)

    return (1 + (A1 - B1(x, y)**2 + (A2 - B2(x, y))))

def f4(x):
    x, y = x
    return (x+3)**2 + (y+1)**2

FOO2 = [f3, f4]
bounds2 = [(-pi, pi), (-pi, pi)]


