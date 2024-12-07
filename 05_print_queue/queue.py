def get_input_data(filename="input.txt"):
    with open(filename, "r") as f:
        '''parses the data like this: (rules: dictionary<int, list<int>>, updates: list<int>)'''

        rules = {}
        updates = []

        for line in f:
            if '|' in line:
                rule_id, rule = [int(i) for i in line.strip().split('|')]
                if rule_id not in rules:
                    rules[int(rule_id)] = []
                rules[int(rule_id)].append(int(rule))

            elif ',' in line:
                updates.append([int(i) for i in line.strip().split(',')])

    return rules, updates


def check_update(update: list, rules: list) -> bool:
    # check each page in the update
    for page_index, page in enumerate(update):

        # check if a rule for that page exists
        if page in rules:

            # iterate through each successive page in that rule
            for successive_page in rules[page]:

                # if the successive page exists in the update, it has to be after the page
                if successive_page in update:
                    if page_index > update.index(successive_page):
                        return False

    return True


def part_1(updates: list, rules: dict):
    sum = 0
    for update in updates:
        if check_update(update, rules):
            sum += update[len(update)//2]
    return sum


def place_suitable(page: int, new_order: list, rules: dict):

    # print(f"checking page: {page}")
    # print(f"order so far: {new_order}")

    for j in range(len(new_order)+1):

        uncertain_order = new_order[:j] + [page] + new_order[j:]
        # print(f"uncertain order: {uncertain_order}")

        if (check_update(uncertain_order, rules)):
            # print("order OK!")
            return uncertain_order

        # print("order NOT ok! continue ...")

    # order can not be fixed
    return new_order


def fix_order(update: list, rules: dict) -> list:
    old_order = update
    new_order = []

    for page in old_order:
        new_order = place_suitable(page, new_order, rules)

    return new_order


def part_2(updates: list, rules: dict) -> int:
    sum = 0
    for update in updates:
        if not check_update(update, rules):
            update = fix_order(update, rules)
            sum += update[len(update)//2]
    return sum


if __name__ == "__main__":

    # rules, updates = get_input_data("test_input.txt")
    rules, updates = get_input_data()

    # part 1
    print(f"Part 1: {part_1(updates, rules)}")

    # part 2
    print(f"Part 2: {part_2(updates, rules)}")
