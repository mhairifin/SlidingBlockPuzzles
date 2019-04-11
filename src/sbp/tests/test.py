import copy
class Test():
    def __init__(self, d):
        self.dict = copy.deepcopy(d)
        
    def change(self):
        self.dict["test"]="changed"

nd = {"test": "notchanged"}

t = Test(nd)
t.change()
print(t.dict)
print(nd)