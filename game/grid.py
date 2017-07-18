class Grid:
    def __init__(self, width, height, initial_value=False, bit_representation=None):
        if initial_value not in [False, True]:
            raise Exception("Grids can only contain boolean values.")

        self.CELLS_PER_INT = 30

        self.width = width
        self.height = height
        self.data = [[initial_value for _ in range(height)] for _ in range(width)]

        if bit_representation:
            self.unpack_bits(bit_representation)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])

    def __eq__(self, other):
        if other is None:
            return False

        return self.data == other.data

    def __hash__(self):
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deep_copy(self):
        return self.copy()

    def shallow_copy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item=True):
        return sum([x.count(item) for x in self.data])

    def as_list(self, key=True):
        grid_list = []

        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key:
                    grid_list.append((x, y))

        return grid_list

    def pack_bits(self):
        bits = [self.width, self.height]
        current_int = 0

        for i in range(self.height * self.width):
            bit = self.CELLS_PER_INT - (i % self.CELLS_PER_INT) - 1
            x, y = self._cell_index_to_position(i)

            if self[x][y]:
                current_int += 2 ** bit
            if (i + 1) % self.CELLS_PER_INT == 0:
                bits.append(current_int)
                current_int = 0

        bits.append(current_int)
        return tuple(bits)

    def _cell_index_to_position(self, index):
        x = index / self.height
        y = index % self.height
        return x, y

    def unpack_bits(self, bits):
        cell = 0
        for packed in bits:
            for bit in self.unpack_int(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height:
                    break
                x, y = self._cell_index_to_position(cell)
                self[x][y] = bit
                cell += 1

    def unpack_int(self, packed, size):
        values = []
        if packed < 0:
            raise ValueError("must be a positive integer")

        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)

            if packed >= n:
                values.append(True)
                packed -= n
            else:
                values.append(False)

        return values


def reconstitute_grid(bit_rep):
    if type(bit_rep) is not type((1, 2)):
        return bit_rep

    width, height = bit_rep[:2]

    return Grid(width, height, bit_representation=bit_rep[2:])
