import random
from .base_bot import BaseBot

class HunterBot(BaseBot):
    def init_board(self, cols, rows, win_length, obstacles, time_given):
        self.c, self.r, self.w, self.b, self.ops = cols, rows, win_length, {p:-2 for p in obstacles}, set()

    def notify_move(self, pid, m):
        self.b[m] = pid
        if pid != self.unique_id: self.ops.add(pid)

    def make_a_move(self, t):
        cands = {(x+dx, y+dy) for x,y in self.b if self.b[(x,y)]>=0 for dx in (-1,0,1) for dy in (-1,0,1)
                 if (x+dx, y+dy) not in self.b and 0<=x+dx<self.c and 0<=y+dy<self.r}
        if not cands: return (self.c//2, self.r//2)

        best, max_s = list(cands)[0], -1
        for m in cands:
            my_s = self.eval(m, self.unique_id)
            opp_s = max([self.eval(m, o) for o in self.ops], default=0)
            if my_s >= 1e5: return m
            if opp_s >= 1e5: s = 50000
            elif opp_s >= 5000: s = 20000
            else: s = my_s * 2 + opp_s + random.random()
            if s > max_s: best, max_s = m, s
        return best

    def eval(self, m, p):
        s = 0
        for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
            l, e = 1, 0
            for d in (1, -1):
                k = 1
                while self.b.get((m[0]+k*dx*d, m[1]+k*dy*d)) == p: k+=1; l+=1
                if 0<=m[0]+k*dx*d<self.c and 0<=m[1]+k*dy*d<self.r and (m[0]+k*dx*d, m[1]+k*dy*d) not in self.b: e+=1
            if l >= self.w: return 1e5
            if l == self.w-1 and e>0: s += 5000
            elif l == self.w-2 and e==2: s += 1000
            elif l+e >= self.w: s += l**3 + e
        return s
