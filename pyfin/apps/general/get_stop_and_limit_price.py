rrsp_count = 3134
inv_count = 1232
tfsa_count = 666

price = float(input('Enter a price: '))
stop = float(input('Enter stop percentage: '))
limit = float(input('Enter limit percentage: '))

stop_price = price * (1 - stop / 100.)
limit_price = price * (1 - limit / 100.)

print("\n")
print ('{} {}'.format('Stop price: ', stop_price))
print ('{} {}'.format('Limit price: ', limit_price))
print("\n")
print ('{} {}'.format('Current RRSP count: ', rrsp_count))
print ('{} {}'.format('Current Investment count: ', inv_count))
print ('{} {}'.format('Current TFSA count: ', tfsa_count))
print("\n")
print ('{} {}'.format('Estimated RRSP count: ', rrsp_count * stop_price / limit_price))
print ('{} {}'.format('Estimated Investment count: ', inv_count * stop_price / limit_price))
print ('{} {}'.format('Estimated TFSA count: ', tfsa_count * stop_price / limit_price))


