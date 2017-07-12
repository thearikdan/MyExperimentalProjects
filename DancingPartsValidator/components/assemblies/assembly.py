import json
import cPickle as pkl

class Assembly:
    def __init__(self):
        self.id = 0
        self.boxes = []
        self.cylinders = []
        self.ellipsoids = []

    @property
    def id(self):
        return self.id

    @property
    def boxes(self):
        return self.boxes

    @property
    def cylinders(self):
        return self.cylinders

    @property
    def ellipsoids(self):
        return self.ellipsoids

    def getClass(self):
        return "assembly"

    def getBoxesCount(self):
        return len(self.boxes)

    def getCylindersCount(self):
        return len(self.cylinders)

    def getEllipsoidsCount(self):
        return len(self.ellipsoids)

    def getPrimitivesCount(self):
        return self.getBoxesCount() + self.getCylindersCount() + self.getellipsoidsCount()


    def save(self, filename):
        with open(filename, 'w') as f:
            pkl.dump(self, f)


    def open(self, filename):
        with open(filename, 'r') as f:
            obj = pkl.load(f)
        return obj


'''
    def save1(self, filename):
        with open(filename, 'w') as f:
            dic = {
	        "boxes":self.getBoxesCount(),
	        "cylinders":self.getCylindersCount(),
	        "ellipsoids":self.getEllipsoidsCount()
	    }
            json.dump(dic, f)

            for box in self.boxes:
                box.save(f)
            for cylinder in self.cylinders:
                cylinder.save(f)
            for ellipsoid in self.ellipsoids:
                ellipsoid.save(f)
'''

'''
            for box in self.boxes:
                box.save(f)
            for cylinder in self.cylinders:
                cylinder.save(f)
            for ellipsoid in self.ellipsoids:
                ellipsoid.save(f)
'''


