#! Python3

from math import *

x = 8
u = 10
g = 13
nu2 = 2
sig2 = 8

# Gaussian distribution calculator
def f(u, sig2, x):
    return 1/(sqrt(2*(pi)*sig2)) * exp((-1/2)*((x-u)**2/sig2))

# Calculating new mu from 2 combined gauss dist.
def u_new(u, sig2, g, nu2):
    return 1/(sig2+nu2) * (nu2*u + sig2*g)

# Calculating new sigma, variance, from 2 combined gauss dist.
def sig2_new(sig2, nu2):
    return 1/(1/sig2 + 1/nu2)

#print(f(u, sig2, x))
print(u_new(u, sig2, g, nu2))
print(sig2_new(sig2, nu2))