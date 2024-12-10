import sys

# interesting: implementing a "verrbose mode" to print extra output when desired
verbose_mode = "--verbose" in sys.argv


def part1():
    with open("day09.txt", "r", encoding="UTF-8") as f:
        data = f.read().strip()
        if len(data) % 2 != 0:
            data = data + "0"

    disk_map = []
    address = 0
    file_id = 0

    i = 0
    # build block-based data structure for part 1 because we are moving file blocks
    while i < len(data):
        file = int(data[i : i + 1])
        free = int(data[i + 1])

        for _ in range(file):
            disk_map.append({"address": address, "type": "file", "file_id": file_id})
            address += 1

        for _ in range(free):
            disk_map.append({"address": address, "type": "free", "file_id": -1})
            address += 1

        file_id += 1
        i += 2

    # Sort disk_map by address
    disk_map.sort(key=lambda x: x["address"])

    files = [block for block in disk_map if block["type"] == "file"]
    files.sort(key=lambda x: -x["address"])
    free = [block for block in disk_map if block["type"] == "free"]
    free.sort(key=lambda x: x["address"])

    for file_block in files:
        if verbose_mode:
            print(f"File ID {file_block['file_id']}: Block Address: {file_block['address']}")

        for free_block in free:
            if free_block["address"] < file_block["address"]:
                # Swap addresses
                file_block["address"], free_block["address"] = free_block["address"], file_block["address"]
                break

    # update disk_map
    disk_map = files + free
    disk_map.sort(key=lambda x: x["address"])

    checksum = sum(block["address"] * block["file_id"] for block in disk_map if block["type"] == "file")

    print("Part 1:", checksum)


def part2():
    with open("day09.txt", "r", encoding="UTF-8") as f:
        f = f.read()

    file, free = [], []
    isEven, currentAddress = 0, False

    # build unit-based data structure for part 2 because we are moving all file blocks (entire file)
    for N in f:
        # interesting: using ord() to convert a character to its ASCII value
        N = ord(N) - ord("0")
        if not isEven:  # file entry
            file.append({"address": currentAddress, "length": N})
        else:  # free block entry
            free.append({"address": currentAddress, "length": N})
        isEven, currentAddress = not isEven, currentAddress + N

    if verbose_mode:
        print("Files:", file)
        print("Free:", free)

    # interesting: using range() with a negative step to iterate backwards
    for fileid in range(len(file) - 1, -1, -1):
        for freeid in range(len(free)):
            if free[freeid]["address"] > file[fileid]["address"]:
                break
            if free[freeid]["length"] >= file[fileid]["length"]:
                file[fileid]["address"] = free[freeid]["address"]
                if free[freeid]["length"] == file[fileid]["length"]:
                    free.pop(freeid)  # matches perfectly, delete free block
                else:
                    free[freeid]["address"] += file[fileid]["length"]
                    free[freeid]["length"] -= file[fileid]["length"]
                break

    checksum = 0
    for fileid in range(len(file)):
        checksum += fileid * sum(range(file[fileid]["address"], file[fileid]["address"] + file[fileid]["length"]))
    print("Part 2:", checksum)


if __name__ == "__main__":
    part1()
    part2()
