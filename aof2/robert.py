import subprocess
import time
import os

class ROBERT:

    def __init__(self, left, right, up, down, punch, kick, recharge, idle):
        cmd = "xdotool search --pid `pgrep mame`"
        r =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v = r.read()
        self.winid = hex(int(v.decode()))
        os.system('xdotool windowfocus --sync ' + self.winid)
        self.l  = left
        self.r  = right
        self.u  = up
        self.d  = down
        self.p  = punch
        self.k  = kick
        self.rc = recharge
        self.i  = idle

    def punch(self):
        os.system('xdotool key --window ' + self.winid + ' key ' + self.p)

    def kick(self):
        os.system('xdotool key --window ' + self.winid + ' key ' + self.k)

    def downpunch(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' key ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)

    def downkick(self):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' key ' + self.k)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)

    def left(self, ts):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.l)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.l)

    def right(self, ts):
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.r)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.r)

    def shift(self, pos):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        for i in range(4):
            os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
            time.sleep(0.1)
            os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def recharge(self, ts):
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.rc)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.rc)

    def idle(self):
        os.system('xdotool key --window ' + self.winid + ' key ' + self.i)

    def ryugekiken(self, pos):
        z = self.r
        if pos == 0:
            z = self.r
        else:
            z = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def ryuuga(self, pos):
        z = self.r
        if pos == 0:
            z = self.r
        else:
            z = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        time.sleep(0.1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def kyokugenryuurenbuken(self, pos):
        z = self.l
        if pos == 0:
            z = self.l
        elif pos == 1:
            z = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def hienshippuukyaku(self, pos):
        z1 = self.l
        z2 = self.r
        if pos == 0:
            z1 = self.l
            z2 = self.r
        elif pos == 1:
            z1 = self.r
            z2 = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.k)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.k)

    def geneikyaku(self, pos):
        z1 = self.l
        z2 = self.r
        if pos == 0:
            z1 = self.l
            z2 = self.r
        elif pos == 1:
            z1 = self.r
            z2 = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z2)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.k)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.k)

    def haohshoukohken(self, pos):
        z1 = self.l
        z2 = self.r
        if pos == 0:
            z1 = self.l
            z2 = self.r
        elif pos == 1:
            z1 = self.r
            z2 = self.l

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z2)
        time.sleep(0.3)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z1)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.p)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z2)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.p)

    def hienryuujinkyaku(self, pos, ts):
        z = self.l
        if pos == 0:
            z = self.l
        elif pos == 1:
            z = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.u)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.u)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.d)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.k)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + z)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + self.k)

    def defendup(self, pos, ts):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)

    def defenddown(self, pos, ts):
        key = self.l
        if pos == 0:
            key = self.l
        elif pos == 1:
            key = self.r

        os.system('xdotool key --window ' + self.winid + ' keydown ' + key)
        os.system('xdotool key --window ' + self.winid + ' keydown ' + self.d)
        time.sleep(ts)
        os.system('xdotool key --window ' + self.winid + ' keyup ' + key)
        os.system('xdotool key --window ' + self.winid + ' keyup Down')

    def insertcoin(self):
        os.system('xdotool key --window ' + self.winid + ' key 5')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' key 1')

    def select(self):
        os.system('xdotool key --window ' + self.winid + ' keydown A')
        time.sleep(0.2)
        os.system('xdotool key --window ' + self.winid + ' keyup A')
        time.sleep(2)
