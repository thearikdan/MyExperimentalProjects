from input import read



def get_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    cp = read.get_closing_price_from_numeric_data(data)

    diff = cp - op

    per = diff / op
    return per


def get_max_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    hp = read.get_high_price_from_numeric_data(data)

    diff = hp - op

    per = diff / op
    return per


def get_min_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    lp = read.get_low_price_from_numeric_data(data)

    diff = lp - op

    per = diff / op
    return per

