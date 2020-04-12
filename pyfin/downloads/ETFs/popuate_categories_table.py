from etf_utils import etf_utils as eu

ROOT_DIR = "etf_data"


categories = eu.get_all_categories(ROOT_DIR)

print(categories)

