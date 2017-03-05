from random import randint


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def dice(dice_faces, num):
    results = []
    for i in range(num):
        result = randint(1, dice_faces)
        results.append(result)

    return results
