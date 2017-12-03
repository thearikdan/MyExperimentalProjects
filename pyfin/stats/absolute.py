from input import read

def get_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    cp = read.get_closing_price_from_numeric_data(data)

    diff = cp - op

    return diff


def get_max_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    hp = read.get_high_price_from_numeric_data(data)

    diff = hp - op

    return diff


def get_min_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    lp = read.get_low_price_from_numeric_data(data)

    diff = lp - op

    return diff

