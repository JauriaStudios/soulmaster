from random import randint


def dice(dice_faces, num):
    results = []
    for i in range(num):
        result = randint(1, dice_faces)
        results.append(result)

    return results
