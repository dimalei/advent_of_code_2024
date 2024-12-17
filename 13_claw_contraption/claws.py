import re


class Vector2:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other: object):
        if not isinstance(other, Vector2):
            return self
        return Vector2(self.x + other.x, self.y + other.y)

    def __lt__(self, other: object):
        if not isinstance(other, Vector2):
            return False
        return self.x < other.x and self.y < other.y

    def __gt__(self, other: object):
        if not isinstance(other, Vector2):
            return False
        return self.x > other.x or self.y > other.y

    def __eq__(self, other: object):
        if not isinstance(other, Vector2):
            return False
        return self.x == other.x and self.y == other.y

    def __mul__(self, other: object):
        if isinstance(other, int):
            return Vector2(self.x * other, self.y * other)
        if isinstance(other, 'Vector2'):
            return Vector2(self.x * other.x, self.y * other.y)
        return self

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"Vector2({self.x},{self.y})"


class Ray2:
    def __init__(self, start: Vector2, direction: Vector2):
        self.s = start
        self.d = direction
        pass

    def get_intersection(self, other: 'Ray2') -> Vector2:
        # Compute determinant
        det = other.d.x * self.d.y - other.d.y * self.d.x

        # Check if rays are parallel (det is zero)
        if abs(det) < 1e-10:
            return None  # No intersection (rays are parallel)

        # Solve for parameters u and v (distances along the ray directions)
        dx = other.s.x - self.s.x
        dy = other.s.y - self.s.y

        u = (dy * other.d.x - dx * other.d.y) / det
        v = (dy * self.d.x - dx * self.d.y) / det

        # Check if intersection is "in front" of the start of both rays
        if u >= 0 and v >= 0:
            # Intersection point: self.s + u * self.d
            intersection_x = self.s.x + u * self.d.x
            intersection_y = self.s.y + u * self.d.y
            return Vector2(intersection_x, intersection_y)

        return None  # No valid intersection (lies behind one or both rays)


class Claw_Machine:
    def __init__(self, button_a: Vector2, button_b: Vector2, prize: Vector2):
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize
        self.min_cost = 0
        print(self)
        self.compute_min_cost()

    def compute_min_cost(self):
        print("next machine")
        costAB = 0
        costBA = 0

        intersectionAB = Ray2(Vector2(0, 0), self.button_a).get_intersection(
            Ray2(self.prize, self.button_b * -1))

        
        intersectionBA = Ray2(Vector2(0, 0), self.button_b).get_intersection(
            Ray2(self.prize, self.button_a * -1))

        if intersectionAB != None and intersectionAB.x % self.button_a.x == 0:
            amount_a = intersectionAB.x // self.button_a.x
            amount_b = (self.prize.x - intersectionAB.x) // self.button_b.x

            costAB = self.get_cost(amount_a, amount_b)

        if intersectionBA != None and intersectionBA.x % self.button_b.x == 0:
            amount_b = intersectionBA.x // self.button_b.x
            amount_a = (self.prize.x - intersectionBA.x) // self.button_a.x
            print(f"a: {amount_a}, b: {amount_b}")

            costBA = self.get_cost(amount_a, amount_b)
        
        print(f"costAB {costAB}")
        print(f"costBA {costBA}")

        if costAB > 0 and costAB <= costBA:
            self.min_cost = costAB

        if costBA > 0 and costBA <= costAB:
            self.min_cost = costBA
        

    def get_cost(self, amount_a: int, amount_b: int):
        return amount_a * 3 + amount_b

    def __str__(self):
        return f"prize: {self.prize} A:{self.button_a} B:{self.button_b}"


def get_input(file_name="test_input.txt"):
    with open(file_name, "r") as file:
        out = []
        A = None
        B = None
        P = None
        for row in file:
            if "A" in row:
                a, b = re.findall('\d+', row.strip())
                A = Vector2(a, b)
            if "B" in row:
                a, b = re.findall('\d+', row.strip())
                B = Vector2(a, b)
            if "P" in row:
                a, b = re.findall('\d+', row.strip())
                P = Vector2(a, b)
                out.append(Claw_Machine(A, B, P))
        return out


if __name__ == "__main__":
    # input = get_input()
    input = get_input("input.txt")

    for i, m in enumerate(input):
        print(f"machine {i+1:03}: {m.min_cost}")
    print(f"total sum {sum([m.min_cost for m in input])}")

    # ray1 = Ray2(Vector2(0, 0), Vector2(3, 2))
    # ray2 = Ray2(Vector2(9, 10), Vector2(-1, -2))

    # print(ray1.get_intersection(ray2))
