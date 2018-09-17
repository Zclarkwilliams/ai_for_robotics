#! Python3 

# Make a robot called myrobot that starts at
# coordinates 30, 50 heading north (pi/2).
# Have your robot turn clockwise by pi/2, move
# 15 m, and sense. Then have it turn clockwise
# by pi/2 again, move 10 m, and sense again.
#
# Your program should print out the result of
# your two sense measurements.
#
# Don't modify the code below. Please enter
# your code at the bottom.

from math import *
import random



landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise    = 0.0
        self.sense_noise   = 0.0
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError('X coordinate out of bound')
        if new_y < 0 or new_y >= world_size:
            raise ValueError('Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('Robot cant move backwards')         
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        
        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):
        
        # calculates how likely a measurement should be
        
        prob = 1.0
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
    
    
    
    def __repr__(self):
        return ('[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation)))



def evaluate(r, p):
    sum_fin = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum_fin += err
    return sum_fin / float(len(p))



####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####

##  STEP 1:
# starts at 30.0, 50.0, heading north (=pi/2)
# turns clockwise by pi/2, moves 15m
# senses
# turns clockwise by pi/2, moves 10m
# senses

##  STEP 2:
# Add noise to the robot
# Forward Noise = 5.0
# Turn Noise    = 0.1
# Sense Noise   = 5.0

##  STEP 3
# Create a list of particles of size N=1000
# N = 1000
# P = []

##  STEP 4
# Make the particles generated in STEP 3 move
# turn by 0.1
# forward by 5

##  STEP 5
# Generate the importance weights for particles
# Use measure_prob function
# set noise to 0.05, 0.05, 5
# Forward Noise = 0.05
# Turn Noise    = 0.05
# Sense Noise   = 5.0

##  STEP 6
# Make it so that the particles with the smallest
# importance weight are sampled less frequently

'''
## My Code Here ##
myrobot = robot()
myrobot.set_noise(f_noise, t_noise, s_noise)
myrobot.set(30.0, 50.0, pi/2)
print(myrobot)
myrobot = myrobot.move(-pi/2, 15)
print(myrobot)
print(myrobot.sense())
myrobot = myrobot.move(-pi/2, 10)
print(myrobot)
print(myrobot.sense())
'''

f_noise = 5.0
t_noise = 0.1
s_noise = 5.0

N = 1000
p = []

# Generate paticles and configure
for i in range(0, N):
    x = robot()
    x.set_noise(f_noise, t_noise, s_noise)
    p.append(x)

# Move the particles
p2 = []
for i in range(len(p)):
    p2.append(p[i].move(0.1, 5.0))
p = p2

# Calculate the particle measurement importnace weights
w = []
for i in range(len(p)):
    w.append(p[i].measurement_prob(p[i].sense()))

'''
for i in range(len(p)):
    print(p[i])
    print(w[i])
'''

# Normalize the particle importance weights
w_norm = []
for i in range(len(w)):
    w_norm.append(w[i]/sum(w))

# Resampling according to all particles and weights
'''
p3 = []
for i in range(len(p)):
    curr_sum = 0.
    val_lim = random.random()
    for j in range(len(p)):
        curr_sum += w_norm[j]
        if val_lim < curr_sum:
            p3.append(p[j])
            break
'''

# Resampling wheel 
w_max = max(w)
idx = int(random.random() * N)
p3 = []
b = 0.
for i in range(len(p)):
    b += random.random() * 2.0 * w_max
    while w[i] < b:
        b -= w[i]
        idx = (idx + 1) % N
    p3.append(p[idx])


print(p3)