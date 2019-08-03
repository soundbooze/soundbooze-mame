import os
import mss
import cv2
import time
import numpy

from ring import *
from ryu import *

BLOOD      = [2744512, 4089536, 745816 * 4]
RESUME     = [1358640, 2617406, 2264400, 2623509]

class ACT:

    def __init__(self):
        self.action  = ['left', 'jumpleft|kick', 'kick|left|kick', 'defendup(0)', 'defenddown(0)', 'fire(0)', 'superpunch(0)', 'superkick(0)', 'punch', 'kick', 'downkick', 'kick|jumpup|kick', 'right', 'jumpright|kick', 'kick|right|kick', 'defendup(1)', 'defenddown(1)', 'fire(1)', 'superpunch(1)', 'superkick(1)']
        self.max_sigma = 1.0
        self.min_sigma = 0.1
        self.t         = 0.8
        self.decay_period = 1000000
        self.action_space = len(self.action)

    def next(self, Z):
        self.max_sigma = numpy.argmax(Z)
        self.min_sigma = numpy.argmin(Z)
        sigma = (self.max_sigma - (self.max_sigma - self.min_sigma) * min(1.0, self.t * 1.0 / self.decay_period))
        if self.decay_period < 0: 
            self.decay_period = 1000000
        self.decay_period -= 0.1
        p  = numpy.clip(numpy.random.normal(size=len(self.action)) * sigma, 0, len(self.action))
        p /= numpy.sum(p)
        return numpy.random.choice(len(p), 1, p=p)[0]

with mss.mss() as sct:

    scene = {"top": 124, "left": 100, "width": 800, "height":600}

    startGame = False

    ryu = RYU('Left', 'Right', 'Up', 'Down', 'c', 'd')
    act = ACT()
    rb  = RINGBUFFER(4)

    ZP = []

    while [ 1 ]:

        p1 = numpy.array(sct.grab(scene))
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

                img = cv2.resize(numpy.array(sct.grab(scene)),(400,300))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                H = numpy.hsplit(img, 2)
                L = numpy.vsplit(H[0], 2)
                R = numpy.vsplit(H[1], 2)
                l, r = L[1], R[1]
                l, r = l[0:100, 40:140], r[0:100, 40:140]
                
                Lsum = numpy.sum(l)/10000000.0
                Rsum = numpy.sum(r)/10000000.0
                Z = [Lsum, Rsum]

                r = act.next(Z)
                ryu.act(r)

                subd = numpy.absolute(Lsum - Rsum)
                ZP.append(subd)

                if    subd      < numpy.percentile(ZP, 20):
                    print '[0]',
                elif  subd    >=  numpy.percentile(ZP, 20) and subd < numpy.percentile(ZP, 30):
                    print '[1]',
                elif  subd    >=  numpy.percentile(ZP, 40) and subd < numpy.percentile(ZP, 50):
                    print '[2]',
                elif  subd    >=  numpy.percentile(ZP, 50) and subd < numpy.percentile(ZP, 60):
                    print '[3]',
                elif  subd    >=  numpy.percentile(ZP, 60) and subd < numpy.percentile(ZP, 70):
                    print '[4]',
                elif  subd    >=  numpy.percentile(ZP, 70) and subd < numpy.percentile(ZP, 80):
                    print '[5]',
                elif  subd    >=  numpy.percentile(ZP, 80) and subd < numpy.percentile(ZP, 90):
                    print '[6]',
                elif  subd    >=  numpy.percentile(ZP, 90):
                    print '[7]',

                print("[%d] - [%.5f %.5f] - [%.5f] %d | %s" %(numpy.argmax(Z), Lsum, Rsum, numpy.absolute(Lsum - Rsum), r, act.action[r]))

            if sumb1 == BLOOD[1] and sumb2 == BLOOD[1] and not startGame:
                print '[Start]'
                startGame = True
                time.sleep(1)

            elif sumb1 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P1 [KO]'
                startGame = False
                time.sleep(1)

            elif sumb2 == BLOOD[0] and rbsum == BLOOD[2]:
                print 'P2 [KO]'
                startGame = False
                time.sleep(1)

        elif sumb1 == RESUME[0]:
            ryu.insertcoin()
        
        elif sumb1 == RESUME[1] or sumb1 == RESUME[2] or sumb1 == RESUME[3]:
            ryu.select()
