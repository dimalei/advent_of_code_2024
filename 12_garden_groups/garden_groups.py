import copy


def get_input(file_name="test_input.txt"):
    with open(file_name, "r") as file:
        out = []
        for row in file:
            out.append(list(row.strip()))
        return out


class Plot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Plot):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Plot({self.x},{self.y})"


class Perimeter(Plot):
    def __init__(self, x, y, label: str):
        super().__init__(x, y)
        self.label = label

    def __repr__(self):
        return f"Perimeter({self.x},{self.y},{self.label})"

    def increment_label(self):
        self.label = str(int(self.label) + 1)


class Region:
    def __init__(self, label, initial_plot: Plot, map: list):
        self.label = label
        self.plots = []
        self.perimeters = []
        self.corners = []
        self.plots.append(initial_plot)
        self.build_region(map)
        self.build_perimeters()
        self.build_corners()

    def add_plot(self, plot: Plot):
        self.plots.append(plot)

    def build_region(self, map: list):
        initial_plot = [self.plots[0]]
        self.grow_region(initial_plot, map)

    def grow_region(self, plots: Plot, map: list):
        for p in plots:
            map[p.y][p.x] = "."
            next_plots = self.get_adjacents(p, map)
            self.plots.extend(next_plots)
            self.grow_region(next_plots, map)

    def get_adjacents(self, plot: Plot, map: list):
        adjacent = []
        # north
        if plot.y - 1 >= 0 and map[plot.y - 1][plot.x] == self.label:
            adjacent.append(Plot(plot.x, plot.y - 1))
        # east
        if plot.x - 1 >= 0 and map[plot.y][plot.x - 1] == self.label:
            adjacent.append(Plot(plot.x - 1, plot.y))
        # south
        if plot.y + 1 < len(map) and map[plot.y + 1][plot.x] == self.label:
            adjacent.append(Plot(plot.x, plot.y + 1))
        # west
        if plot.x + 1 < len(map[plot.y]) and map[plot.y][plot.x + 1] == self.label:
            adjacent.append(Plot(plot.x + 1, plot.y))

        for p in adjacent:
            if p in self.plots:
                self.plots.remove(p)

        return adjacent

    def get_perimeters(self, plot: Plot):
        adjacent = []
        # north
        adjacent.append(Perimeter(plot.x, plot.y - 1, "-"))
        # east
        adjacent.append(Perimeter(plot.x - 1, plot.y, "|"))
        # south
        adjacent.append(Perimeter(plot.x, plot.y + 1, "-"))
        # west
        adjacent.append(Perimeter(plot.x + 1, plot.y, "|"))

        to_remove = []
        for p in adjacent:
            if p in self.plots:
                to_remove.append(p)

        for p in to_remove:
            adjacent.remove(p)

        return adjacent

    def build_perimeters(self):
        for p in self.plots:
            self.perimeters.extend(self.get_perimeters(p))

    def build_corners(self):
        corners = []
        min_x, min_y, max_x, max_y = self.get_bounaries()
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                if Plot(x, y) in self.plots:
                    continue
                c_val = self.corner_value(x, y)
                if c_val > 0:
                    corners.append(Perimeter(x, y, str(c_val)))
        self.corners = corners

    def corner_value(self, x: int, y: int):
        sample = []
        value = 0
        for p_y in range(y - 1, y + 2):
            row = []
            for p_x in range(x - 1, x + 2):
                row.append(Plot(p_x, p_y) in self.plots)
            sample.append(row)

        # concave corners
        # nw
        if sample[0][1] and sample[1][0]:
            value += 1
        # sw
        if sample[2][1] and sample[1][0]:
            value += 1
        # se
        if sample[2][1] and sample[1][2]:
            value += 1
        # ne
        if sample[0][1] and sample[1][2]:
            value += 1

        # convex corners
        # nw
        if sample[0][0] and not sample[0][1] and not sample[1][0]:
            value += 1
        # sw
        if sample[2][0] and not sample[1][0] and not sample[2][1]:
            value += 1
        # se
        if sample[2][2] and not sample[1][2] and not sample[2][1]:
            value += 1
        # ne
        if sample[0][2] and not sample[0][1] and not sample[1][2]:
            value += 1

        return value

    def get_corners(self):
        return sum([int(c.label) for c in self.corners])

    def get_price(self):
        return len(self.plots) * len(self.perimeters)

    def get_discount_price(self):
        return len(self.plots) * self.get_corners()

    def get_bounaries(self):
        max_x = 0
        max_y = 0
        min_x = self.plots[0].x
        min_y = self.plots[0].y

        for p in self.plots + self.perimeters:
            if p.x > max_x:
                max_x = p.x
            if p.y > max_y:
                max_y = p.y

            if p.x < min_x:
                min_x = p.x
            if p.y < min_y:
                min_y = p.y

        return (min_x, min_y, max_x, max_y)

    def __str__(self):
        min_x, min_y, max_x, max_y = self.get_bounaries()
        out = ""
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                if Plot(x, y) in self.plots:
                    out += "\033[92m" + self.label
                elif Plot(x, y) in self.corners:
                    index = self.corners.index(Plot(x, y))
                    out += "\033[96m" + self.corners[index].label
                elif Plot(x, y) in self.perimeters:
                    index = self.perimeters.index(Plot(x, y))
                    out += "\033[96m" + self.perimeters[index].label
                else:
                    out += "\033[0m" + "."
                out += "  "
            out += "\n\n"

        return out


def create_region(x, y, map: list):
    label = map[y][x]
    r = Region(label, Plot(x, y), map)
    return r


def get_regions(map: list):
    map = copy.deepcopy(map)
    regions = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == ".":
                continue
            regions.append(create_region(x, y, map))
    return regions


if __name__ == "__main__":
    input = get_input("input.txt")
    # input = get_input("test_input2.txt")
    # input = get_input()

    regions = get_regions(input)

    index = 0

    print(f"regions: {len(regions)}")
    print(f"region {index}: \n\033[0m{regions[index]}plots: {
          len(regions[index].plots)} perimeters: {len(regions[index].perimeters)} cost: {regions[index].get_price()} discount-price: {regions[index].get_discount_price()} corners: {regions[index].get_corners()}")


    print(f"full price: {sum([r.get_price() for r in regions])}")
    print(f"discount price: {sum([r.get_discount_price() for r in regions])}")
