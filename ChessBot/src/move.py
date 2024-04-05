class Move:
    def __init__(self, initial, final) -> None:
        #initial and final are square objects
        self.initial = initial
        self.final = final

    def __eq__(self, other):
        return self.initial==other.initial and self.final==other.final