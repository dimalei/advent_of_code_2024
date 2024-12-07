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


def check_rule(update: list, rules: list) -> bool:
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
        if check_rule(update, rules):
            sum += update[len(update)//2]
    return sum

if __name__ == "__main__":

    rules, updates = get_input_data("test_input.txt")
    # rules, updates = get_input_data()

    # part 1
    print(part_1(updates, rules))

    # part 2

