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


class Claw_Machine:
    def __init__(self, button_a: Vector2, button_b: Vector2, prize: Vector2):
        self.pos = Vector2(0, 0)
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize
        self.combinations = []
        self.min_cost = 0
        self.compute_min_cost()

    def compute_min_cost(self):
        MAX_LENGTH = 100
        amount_a = 0
        amount_b = 0

        for i in range(MAX_LENGTH):
            position = Vector2(0, 0)
            amount_a = 0
            position = self.button_b * amount_b
            if position > self.prize:
                break

            while position < self.prize:
                amount_a += 1
                position += self.button_a

            if position == self.prize:
                # viable solution
                cost = self.get_cost(amount_a, amount_b)
                if cost < self.min_cost or self.min_cost <= 0:
                    self.min_cost = cost

            amount_b += 1

    def get_cost(self, amount_a: int, amount_b: int):
        return amount_a * 3 + amount_b

    def __str__(self):
        return f"pos: {self.pos} prize: {self.prize} A:{self.button_a} B:{self.button_b}"


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
    input = get_input()
    input = get_input("input.txt")

    for i, m in enumerate(input):
        print(f"machine {i+1:03}: {m.min_cost}")
    print(f"total sum {sum([m.min_cost for m in input])}")
