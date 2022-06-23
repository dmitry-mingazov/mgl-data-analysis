class Chain():

    def __init__(self, _id, rows):
        self._id = _id
        self.rows = rows

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i < len(self.rows):
            row = self.rows[self._i]
            self._i += 1
            return row
        raise StopIteration

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, name):
        return self.rows[name]

class ChainFactory():
    @staticmethod
    def create_chains(chains_array):
        chains = []
        for index, rows in enumerate(chains_array, 1):
            chains.append(Chain(index, rows))
        return chains

