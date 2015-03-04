import math


def OUT_CIRC(t, b, c, d):
    t = t/d - 1
    return c * math.sqrt(1 - t*t) + b


def OUT_QUART(t, b, c, d):
    t = t/d - 1
    return -c * (t**4 - 1) + b


def INOUT_CIRC(t, b, c, d):
    t1 = t / (d / 2)

    if (t / (d/2)) < 1:
        return -c/2 * (math.sqrt(1 - (t/(d/2))**2) - 1) + b

    return c/2 * (math.sqrt(1 - (t1-2)**2) + 1) + b


def IN_CUBIC(t, b, c, d):
    t /= d
    return c * t**3 + b


def OUT_QUAD(t, b, c, d):
    t /= d
    return -c * t * (t-2) + b


def OUT_BOUNCE(t, b, c, d):
    t /= d

    if t < (1/2.75):
        return c * (7.5625 * t**2) + b
    else:
        if t < (2/2.75):
            t -= (1.5/2.75)
            return c * (7.5625 * t**2 + .75) + b
        else:
            if t < (2.5/2.75):
                t -= (2.25/2.75)
                return c * (7.5625 * t**2 + .9375) + b
            else:
                t -= (2.625/2.75)
                return c * (7.5625 * t**2 + .984375) + b


def INOUT_EXP(t, b, c, d):
    t1 = t / (d/2)
    if t == 0:
        return b
    if t == d:
        return b+c
    if t1 < 1:
        return c/2 * math.pow(2, 10 * (t1 - 1)) + b - c * 0.0005
    return c/2 * 1.0005 * (-math.pow(2, -10 * (t1-1)) + 2) + b
