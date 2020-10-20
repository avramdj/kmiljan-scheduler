import numpy as np
import json


class Scheduler:

    def __init__(self, courses):
        self.bitmap = np.zeros(shape=(5, 13))
        self.placed = set([])
        self.courses = courses

    def find(self):
        if self._find(0):
            #print(self.bitmap)
            return [json.loads(x) for x in self.placed]

    def _find(self, i):
        if i == len(self.courses):
            return True
        for term in self.courses[i][2]:
            if not self.conflict(term):
                self.place(term, i)
                if self._find(i+1):
                    return True
                self.remove(term)
        return False

    def conflict(self, term: dict):
        for i in range(term['start']-8, term['end']-8):
            if self.bitmap[term['day']][i] != 0:
                return True
        return False

    def place(self, term, bit):
        for i in range(term['start']-8, term['end']-8):
            self.bitmap[term['day']][i] = bit
        self.placed.add(json.dumps(term))

    def remove(self, term):
        for i in range(term['start']-8, term['end']-8):
            self.bitmap[term['day']][i] = 0
        self.placed.remove(json.dumps(term))
        
    def done(self):
        return len(self.placed) == len(self.courses)
