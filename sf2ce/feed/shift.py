import os
import time
import mss
import cv2
import numpy
import pickle
import imagehash
from PIL import Image

from ryu import *

BLOOD      = [2744512, 4089536, 745816 * 4]
RESUME     = [1358640, 2617406, 2264400, 2623509]

class RINGBUFFER:

    def __init__(self, size):
        self.data = [None for i in xrange(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data

class TRANSFORM:

    def __init__(self):
        self.b = None

    def blue(self, frame):
        self.b = frame.copy()
        self.b[:,:,1] = 0
        self.b[:,:,2] = 0
        self.b[self.b < 250] = 0
        return self.b

class HASH:

    def __init__(self):
        self.root       = str(time.time()) + '/'
        self.Z          = {}
        self.action     = ['left', 'jumpleft|kick', 'kick|left|kick', 'defendup(0)', 'defenddown(0)', 'fire(0)', 'superpunch(0)', 'superkick(0)', 'punch', 'kick', 'downkick', 'kick|jumpup|kick', 'right', 'jumpright|kick', 'kick|right|kick', 'defendup(1)', 'defenddown(1)', 'fire(1)', 'superpunch(1)', 'superkick(1)']
        self.p          = numpy.random.rand(len(self.action))
        self.p         /= numpy.sum(self.p)
        self.shift      = 0
        self.prevhit    = [0, 0]
        self.currenthit = [0, 0]

    def next(self):
        return numpy.random.choice(len(self.p), 1, p=self.p)[0]

    def compute(self, frame):
        phash = imagehash.phash(frame)
        return phash

    def append(self, h, r, hit):
        self.Z[h] = [r, hit]

    def flush(self):
        for k, v in self.Z.items():
            if numpy.sum(v[1]) == 0:
                del self.Z[k]

    def dump(self):
        pickle.dump(self.Z, open(self.root + 'hash-' + str(time.time()) + '.pkl', 'wb'))
    
def skewone(V, LR, p):

    def _rndsumone(n):
        R = []
        while (numpy.sum(R)) != 1.0:
            R = numpy.random.multinomial(100.0, numpy.ones(n)/n, size=1)[0]/100.0
        return R

    prob = numpy.zeros(len(LR))
    if p == 0:
        for i in range(len(LR)/2):
            prob[i] += LR[i] * V[i]
    elif p == 1:
        for i in range(len(LR)/2, len(LR)):
            prob[i] += LR[i] * V[i]
    prob /= numpy.sum(prob)

    if numpy.sum(prob) != 1.0:
        return _rndsumone(len(LR))

    return prob

def lerp(V0, V1, t):
    l = []
    if len(V0) == len(V1):
        for x, y in zip(V0, V1):
            l.append((1 - t) * x + t * y)
    return l

def preact(blue, ryu, hash, sumb1, sumb2):

    h = hash.compute(blue)
    r = hash.next()
    if h in hash.Z:
        r = hash.Z[h][0]

    hash.currenthit[0], hash.currenthit[1] = (0.4089536-sumb1/10000000.0), (0.4089536-sumb2/10000000.0)

    hit = [0, 0]
    hit[0], hit[1] = hash.currenthit[0] - hash.prevhit[0], hash.currenthit[1] - hash.prevhit[1]
    hit[0], hit[1] =  -1 if hit[0] else 0, 1 if hit[1] else 0

    if hit[0] == -1:
        hash.shift = (hash.shift + 1) % 2
        hash.p = skewone(hash.p, lerp(hash.p, hash.p, numpy.random.rand()), hash.shift)
        '''
        hash.p[(r+1)%len(hash.p)] += hash.p[r]
        hash.p[r] = 0.0
        '''

    hash.append(h, r, hit)

    ryu.act(r)

    for i in range(2):
        hash.prevhit[i] = hash.currenthit[i]

    print("(%d) - [%s] %s (%s) [%d]" %(len(hash.Z), h, hash.Z[h], hash.action[r], hash.shift))

with mss.mss() as sct:

    border = 24
    blood = {"top": 100+border, "left": 100, "width": 800, "height":600}
    scene = {"top": 240+border, "left": 100, "width": 800, "height":400}

    startGame = False

    ryu         = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')
    rb          = RINGBUFFER(4)
    transform   = TRANSFORM()
    hash        = HASH()

    while [ 1 ]:

        p1 = numpy.array(sct.grab(blood))
        p2 = p1.copy()

        b1 = p1[60:78, 68:364]
        b2 = p2[60:78, 68+366:364+366]
        ko = p1[60:80, 378:424]

        sumb1, sumb2, kosum = numpy.sum(b1), numpy.sum(b2), numpy.sum(ko)

        rbsum = 0
        try:
            rbsum = numpy.sum(rb.get())
        except:
            pass

        if sumb1 >= BLOOD[0] and sumb1 <= BLOOD[1]:

            if startGame:
                x = cv2.resize(numpy.array(sct.grab(scene)),(200,100))
                blue = transform.blue(x)
                preact(Image.fromarray(blue), ryu, hash, sumb1, sumb2)
                
            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(1)

            elif sumb1 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P1 [KO]'
                hash.flush()
                startGame = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P2 [KO]'
                hash.flush()
                startGame = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1] or sumb1 == RESUME[2] or sumb1 == RESUME[3]:
            ryu.select()