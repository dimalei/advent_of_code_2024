import re
from itertools import product

class Vector2:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
    
    def __str__(self):
        return f"({self.x},{self.y})"
    
    def __repr__(self):
        return f"Vector2({self.x},{self.y})"

class Claw_Machine:
    def __init__(self, button_a: Vector2, button_b: Vector2, prize: Vector2):
        self.pos = Vector2(0,0)
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize
        self.combinations = []

    def create_combinations(self):
        all_combos = product((self.button_a, self.button_b), repeat=4)
        for l in list(all_combos):
            print(l)

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
                a, b = re.findall("\d+", row.strip())
                A = Vector2(a,b)
            if "B" in row:
                a, b = re.findall("\d+", row.strip())
                B = Vector2(a,b)
            if "P" in row:
                a, b = re.findall("\d+", row.strip())
                P = Vector2(a,b)
                out.append(Claw_Machine(A,B,P))
        return out


if __name__ == "__main__":
    input = get_input()

    input[0].create_combinations()


    for m in input:
        print(m)
