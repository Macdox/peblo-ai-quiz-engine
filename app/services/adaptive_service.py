def adjust_difficulty(current, correct):

    levels = ["easy","medium","hard"]

    index = levels.index(current)
    print(index)
    print(correct)

    if correct and index < 2:
        return levels[index + 1]

    if not correct and index > 0:
        return levels[index - 1]

    return current
