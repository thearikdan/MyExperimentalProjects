from read_write import read


N = 36
file_name = "tickers/cannabis.txt"
read.download_list_of_tickers(file_name, N)

file_name = "tickers/cannot_be_positive.txt"
read.download_list_of_tickers(file_name, N)

file_name = "tickers/cannot_be_negative.txt"
read.download_list_of_tickers(file_name, N)

file_name = "tickers/battery.txt"
read.download_list_of_tickers(file_name, N)


