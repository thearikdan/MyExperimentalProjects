import os.path

def get_company_name_from_file_name(filename):
    name_ext = os.path.basename(filename)  
    name = os.path.splitext(name_ext)[0]
    return name


def get_filename_from_ticker_day_interval(ticker, day, interval):
    filename = "%s_%s-%s-%s_%s.pickle" % (ticker, day.year, day.month, day.day, interval)
    return filename


def get_directory_from_ticker_day_interval(ticker, day, interval):
    dir_name = "%s/%s-%s-%s/%s" % (ticker, day.year, day.month, day.day, interval)
    return dir_name


def get_symbol_without_suffix(name, suffix_list):
    count = len(name)
    pos = name.rfind(".")
    suffix = name[pos:]
    if suffix in suffix_list:
        symbol = name[:(count - pos + 1)]
        return symbol
    else:
        return name


def get_suffix_without_symbol(name, suffix_list):
    count = len(name)
    pos = name.rfind(".")
    suffix = name[pos:]
    if suffix in suffix_list:
        return suffix
    else:
        return ""
