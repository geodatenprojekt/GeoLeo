
class AbsParser:

    def __init__(self, min, max):

        self.min = min
        self.max = max
        self.mid = []

        self.init_values()

    def init_values(self):
        for i in range(0, 3):
            self.mid.append((self.max[i] - self.min[i]) / 2)

    def parse_coords(self, x, y, z):
        list = []

        x -= self.min[0]
        y -= self.min[1]
        z -= self.min[2]

        x = int(x * 1000)
        y = int(y * 1000)
        z = int(z * 1000)

        list.append(x)
        list.append(y)
        list.append(z)

        return list


    def parse_list(self, list):
        '''
        x -= self.min[index]
                    x -= mid
                    x = int(x * 1000)
        '''
        parsed = []
        try:
            for x in range(0, list.__len__()):
                inner = []
                for y in range(0, 3):
                    curr = list[x][y]
                    curr -= self.min[y]
                    #curr -= self.mid[y]
                    curr = int(curr * 1000)
                    inner.append(curr)
                for y in range(3, 6):
                    if(list[x].__len__() > y):
                        curr = list[x][y]
                        curr += 1000
                        curr = int(curr)
                        inner.append(curr)
                if inner:
                    #print(inner)
                    parsed.append(inner)
        except TypeError:
            print("list is not iterable")

        return parsed