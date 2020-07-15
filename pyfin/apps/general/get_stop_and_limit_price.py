price = float(input('Enter a price: '))
print('3% drop will lead to 5% with 86% of probability')
stop = float(input('Enter stop percentage (recommended 3 for TQQQ): '))
limit = float(input('Enter limit percentage (recommended 5 for TQQQ): '))

stop_price = price * (1 - stop / 100.)
limit_price = price * (1 - limit / 100.)

print ('{} {}'.format('Stop price: ', stop_price))
print ('{} {}'.format('Limit price: ', limit_price))

