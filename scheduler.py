import numpy as np
from pprint import pprint
import json
from random import shuffle


class Scheduler:

    def __init__(self, courses):
        self.bitmap = np.zeros(shape=(5, 13))
        self.placed = set([])
        self.courses = courses
        self.schedules = []

    def find(self):
        self._find(0)
        shuffle(self.schedules)
        return self.schedules

    def _find(self, i):
        if i == len(self.courses):
            placed_list = [json.loads(x) for x in self.placed]
            placed_list.sort(key=lambda x: (x['day'], x['end']), reverse=True)
            self.schedules.append(placed_list)
            return True
        for term in self.courses[i][2]:
            if not self.conflict(term):
                self.place(term)
                self._find(i+1)
                self.remove(term)
        return len(self.schedules) > 0

    def conflict(self, term):
        for i in range(term['start']-8, term['end']-8):
            if self.bitmap[term['day']][i] == 1:
                return True
        return False

    def place(self, term):
        for i in range(term['start']-8, term['end']-8):
            self.bitmap[term['day']][i] = 1
        self.placed.add(json.dumps(term))

    def remove(self, term):
        for i in range(term['start']-8, term['end']-8):
            self.bitmap[term['day']][i] = 0
        self.placed.remove(json.dumps(term))
        
    def done(self):
        return len(self.placed) == len(self.courses)
