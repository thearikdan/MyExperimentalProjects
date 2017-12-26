from input import read

timestamp, volume , open, close, high, low = read.get_intraday_data_from_web("WEED.TO", "1m")
print open

