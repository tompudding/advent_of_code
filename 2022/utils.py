import functools


@functools.total_ordering
class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.iter_pos = 0

    def __add__(self, other_point):
        return Point3D(self.x + other_point.x, self.y + other_point.y, self.z + other_point.z)

    def __sub__(self, other_point):
        return Point3D(self.x - other_point.x, self.y - other_point.y, self.z + other_point.z)

    def __mul__(self, other_point):
        if isinstance(other_point, Point3D):
            return Point3D(self.x * other_point.x, self.y * other_point.y, self.z * other_point.z)
        else:
            return Point3D(self.x * other_point, self.y * other_point, self.z * other_point)

    def __floordiv__(self, factor):
        if isinstance(factor, Point3D):
            return Point3D(self.x // factor.x, self.y // factor.y, self.z // factor.z)
        else:
            return Point3D(self.x // factor, self.y // factor, self.z // factor)

    def __truediv__(self, factor):
        if isinstance(factor, Point3D):
            return Point3D(self.x / factor.x, self.y / factor.y, self.z / factor.z)
        else:
            return Point3D(self.x / factor, self.y / factor, self.z / factor)

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]

    def __setitem__(self, index, value):
        setattr(self, ("x", "y", "z")[index], value)

    def __iter__(self):
        return self

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "(%.2f,%.2f,%.2f)" % (self.x, self.y, self.z)

    def __lt__(self, other):
        try:
            if other.x < self.x:
                return True
            if other.x > self.x:
                return False
            if other.y < self.y:
                return True
            if other.y > self.y:
                return False
            if other.z < self.z:
                return True
            return False
        except AttributeError:
            raise TypeError(f"'<' not supported between instances of {type(self)} and {type(other)}")

    def __eq__(self, other):
        if not isinstance(other, Point3D):
            return False
        try:
            return self.x == other.x and self.y == other.y and self.z == other.z
        except AttributeError:
            return False

    def __hash__(self):
        return (int(self.x) << 24) | (int(self.y) << 16) | int(self.z)

    def to_float(self):
        return Point3D(float(self.x), float(self.y), float(self.z))

    def to_int(self):
        return Point3D(int(self.x), int(self.y), int(self.z))

    def __next__(self):
        try:
            out = (self.x, self.y, self.z)[self.iter_pos]
            self.iter_pos += 1
        except IndexError:
            self.iter_pos = 0
            raise StopIteration
        return out

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


@total_ordering
class Point2D(object):
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
        self.iter_pos = 0

    def __add__(self, other_point):
        return Point2D(self.x + other_point.x, self.y + other_point.y)

    def __sub__(self, other_point: Point2D):
        return Point2D(self.x - other_point.x, self.y - other_point.y)

    def __mul__(self, other_point):
        if isinstance(other_point, Point2D):
            return Point2D(self.x * other_point.x, self.y * other_point.y)
        else:
            return Point2D(self.x * other_point, self.y * other_point)

    def __floordiv__(self, factor):
        if isinstance(factor, Point2D):
            return Point2D(self.x // factor.x, self.y // factor.y)
        else:
            return Point2D(self.x // factor, self.y // factor)

    def __truediv__(self, factor):
        if isinstance(factor, Point2D):
            return Point2D(self.x / factor.x, self.y / factor.y)
        else:
            return Point2D(self.x / factor, self.y / factor)

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __setitem__(self, index: int, value: float):
        setattr(self, ("x", "y")[index], value)

    def __iter__(self)
        return self

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "(%.2f,%.2f)" % (self.x, self.y)

    def __lt__(self, other):
        try:
            if other.x < self.x:
                return True
            return other.y < self.y
        except AttributeError:
            raise TypeError(f"'<' not supported between instances of {type(self)} and {type(other)}")

    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return False
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:
            return False

    def __hash__(self):
        return int(self.x) << 16 | int(self.y)

    def to_float(self):
        return Point2D(float(self.x), float(self.y))

    def to_int(self):
        return Point2D(int(self.x), int(self.y))

    def __next__(self):
        try:
            out = (self.x, self.y)[self.iter_pos]
            self.iter_pos += 1
        except IndexError:
            self.iter_pos = 0
            raise StopIteration
        return out

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_heuristic(self, other):
        diff = other - self
        return (abs(diff.x) + abs(diff.y)) * 20

    def diaglength(self):
        return max(abs(self.x), abs(self.y))
