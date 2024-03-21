class Vertex:
    def __init__(self, number, partition, neighbors):
        self._vertex_number = number
        self._partitioning = partition
        self._gain = None
        self._connected_vertexes = neighbors
        self._predecessor = None
        self._successor = None
        self._flipped = False

    @property
    def vertex_number(self):
        return self._vertex_number

    @vertex_number.setter
    def vertex_number(self, value):
        self._vertex_number = value

    @property
    def partitioning(self):
        return self._partitioning

    @partitioning.setter
    def partitioning(self, value):
        self._partitioning = value

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value):
        self._gain = value

    @property
    def connected_vertexes(self):
        return self._connected_vertexes

    @connected_vertexes.setter
    def connected_vertexes(self, value):
        self._connected_vertexes = value

    @property
    def predecessor(self):
        return self._predecessor

    @predecessor.setter
    def predecessor(self, value):
        self._predecessor = value

    @property
    def successor(self):
        return self._successor

    @successor.setter
    def successor(self, value):
        self._successor = value

    @property
    def flipped(self):
        return self._flipped

    @flipped.setter
    def flipped(self, value):
        self._flipped = value

    def __str__(self):
        return f"flipped: {self.flipped} "\
               f"Vertex Number: {self.vertex_number} " \
               f"Partitioning: {self.partitioning} " \
               f"Gain: {self.gain} " \
               f"Connected Vertexes: {self.connected_vertexes} " \
               f"Predecessor: {self.predecessor} " \
               f"Successor: {self.successor} \n"

    def __repr__(self):
        return self.__str__()
