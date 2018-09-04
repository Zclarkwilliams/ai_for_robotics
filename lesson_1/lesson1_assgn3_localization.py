#! Python3

## Parameters and variables
colors = [['R', 'G', 'G', 'R', 'R'],
          ['R', 'R', 'G', 'R', 'R'],
          ['R', 'R', 'G', 'G', 'R'],
          ['R', 'R', 'R', 'R', 'R']]
measurements= ['G', 'G', 'G', 'G', 'G']
motions = [[0,0], [0,1], [1,0], [1,0], [0,1]]
sensor_right = 0.7
p_move = 0.8

''' 
motions
-----------------
 - [0,0]  -> stay
 - [0,1]  -> right
 - [0,-1] -> left
 - [1,0]  -> down
 - [-1,0] -> up
'''

def reshape(p,r,c):
    q = []
    i = 0
    j = 0
    k = 0
    for j in range(len(r)):
        q.append([])
        for k in range(len(c)):
            q[j].append(p[i])
            i += 1
    return q

def sumAll(q):
    s=0
    for i in range(len(q)):
        s += sum(q[i])
    return s

def normalized(q):
    i=0
    s = sumAll(q)
    for i in range(len(q)):
        for j in range(len(q[i])):
            q[i][j] = q[i][j]/s
    return q

def move(p,U,p_move):
    q = []
    for i in range(len(p)):
        q.append([])
        for j in range(len(p[i])):
            s_success = p_move * p[(i - U[0]) % len(p)][(j - U[1]) % len(p[0])]
            s_fail    = (1-p_move) * p[i][j]
            s         = s_fail + s_success
            q[i].append(s)
    return q

def sense(p, Z, sensor_confidence, world):
    q = []
    j = 0
    i = 0
    for j in range(len(world)):
        q.append([])
        for i in range(len(world[j])):
            hit = (Z == world[j][i])
            q[j].append(p[j][i] * (float(hit) * sensor_confidence + (1-float(hit)) * (1-sensor_confidence)))
            '''
            if hit == True:
                print("HIT  @ %c %i %i"%(world[j][i],j,i))
            else:
                print("MISS @ %c %i %i"%(world[j][i],j,i))
            '''
    return normalized(q)

def localize(colors,measurements,motions,sensor_right,p_move):
    #init p to a uniform distribution over a grid of the same dimentions as colors
    pinit = 1.0/float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]

    #------------------ My code below -----------------------#
    for i in range(len(measurements)):
        p = move(p, motions[i], p_move)
        p = sense(p, measurements[i], sensor_right, colors)
    #--------------------------------------------------------#

    return p

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print('[' + ',\n'.join(rows) + ']')

p = localize(colors, measurements, motions, sensor_right, p_move);
#print(p)
show(p)