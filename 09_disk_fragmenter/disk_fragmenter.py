def get_input(file_name="test_input.txt"):
    with open(file_name, "r") as f:
        return f.read()


def get_disk(map: str):
    out = []
    for index, digit in enumerate(map):
        if index % 2 == 0:
            file = index//2
        else:
            file = "."
        for c in range(int(digit)):
            out.append(file)
    return out


def fragment(disk: list):
    empy_space = disk.count(".")
    counter = 1
    for i in range(empy_space):
        last_digit = disk.pop(-1)
        if last_digit == ".":
            continue
        index = disk.index(".")
        disk[index] = last_digit

        print(f"{counter:05d} of {empy_space:05d}, index: {index}")
        counter += 1
    return disk


def checksum(disk: list):
    out = 0
    for i, f in enumerate(disk):
        if f == '.':
            continue
        out += i * f
    return out


def last_file_id(disk):
    index = -1
    while disk[index] == '.':
        index -= 1
    return disk[index]


def file_from_id(id: int, disk: list):
    file = []
    index = disk.index(id)
    while index < len(disk) and disk[index] == id:
        file.append(disk[index])
        index += 1
    return file


def find_free_space(file: list, disk: list):
    file_size = len(file)
    file_index = disk.index(file[0])
    index = 0
    while index < len(disk) and index < file_index:
        free_space = 1
        if disk[index] == '.':
            while index + free_space < len(disk) and disk[index + free_space] == '.':
                free_space += 1
            if free_space >= file_size:
                return index
            index += free_space
        else:
            index += 1
    return -1


def delete_file(file_id: int, disk: list):
    for i in range(len(disk)):
        if disk[i] == file_id:
            disk[i] = '.'


def insert_file(file: list, index: int, disk: list):
    for j, file_fragment in enumerate(file):
        disk[index + j] = file_fragment


def defragment(disk: list):
    file_id = last_file_id(disk)

    while file_id > 1:

        print(f"files to go {file_id}")

        file = file_from_id(file_id, disk)
        free_index = find_free_space(file, disk)

        if free_index != -1:
            delete_file(file_id, disk)
            insert_file(file, free_index,  disk)
        file_id -= 1

    return disk


if __name__ == "__main__":
    # input = get_input()
    input = get_input("input.txt")

    # part 1
    # disk = get_disk(input)
    # disk = fragment(disk)
    # print(checksum(disk))

    # part 2
    disk = get_disk(input)
    disk = defragment(disk)
    print(checksum(disk))
