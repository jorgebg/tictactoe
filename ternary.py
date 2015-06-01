from array import array


class Number(bytearray):

    Base = 3
    Length = 0

    def __init__(self, x=0):
        super(Number, self).__init__(self.Length)

        if isinstance(x, int):
            while x > 0:
                x, r = divmod(x, self.Base)
                self.append(r)
        else:
            l = len(x)
            if isinstance(x, str):
                x = map(int, x)
            self[:l] = x

        if len(self) and max(self) > 2:
            raise ValueError

    @property
    def int(self):
        return int(self.str, self.Base)

    @property
    def str(self):
        return ('{}'*len(self)).format(*self)

    def __str__(self):
        return self.str

    def __eq__(self, other):
        return self.int == other.int

    def __lt__(self, other):
        return self.int < other.int
