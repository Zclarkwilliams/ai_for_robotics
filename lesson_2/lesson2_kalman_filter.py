#! Python3

from math import *
from numpy.testing.nose_tools.utils import measure

# Gaussian distribution calculator
def f(mean1, var1, x):
    return 1/(sqrt(2*(pi)*var1)) * exp((-1/2)*((x-mean1)**2/var1))

# Calculating new mu from 2 combined gauss dist.
def mean_new(mean1, var1, mean2, var2):
    return (var1*mean2 + var2*mean1)/(var1+var2)

# Calculating new sig, variance, from 2 combined gauss dist.
def var_new(var1, var2):
    return (var2*var1/(var1+var2))
    #return 1/(1/var1 + 1/var2)

# Motion updating mean and var
def predict(mean1, var1, mean2, var2):
    return [(mean1+mean2), (var1+var2)]

# Get updated mean and varience by utilizing the funtions above
def update(mean1, var1, mean2, var2):
    mean = mean_new(mean1, var1, mean2, var2)
    var  = var_new(var1, var2)
    return [mean, var]


measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0.
sig = 10000.
#sig = 0.0001

for i in range(len(measurements)):
    [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
    print("update: " + str([mu,sig]))
    [mu, sig] = predict(mu, sig, motion[i], motion_sig)
    print("predict: " + str([mu,sig]))

print([mu,sig])
'''
x = 8
var1  = 4.
mean1 = 10.
var2  = 4.
mean2 = 12.
'''