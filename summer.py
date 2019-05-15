from pathlib import Path
import csv


def summer(index: int) -> int:
    tot = 0
    with Path("data.csv").open("r") as op:
        reader = csv.reader(op, delimiter=",")
        data = [line[index] for line in reader if line[index].isdigit()]
        for value in data:
            tot += int(value)
        return tot
