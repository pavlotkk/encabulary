import csv


def lines(path, encoding='utf-8', delimiter=','):
    keys = None
    with open(path, encoding=encoding) as file:
        for row in csv.reader(file, delimiter=delimiter):
            if keys is None:
                keys = {i: r for i, r in enumerate(row)}
                continue
            yield {keys[i]: r for i, r in enumerate(row)}
