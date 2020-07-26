price = float(input('Enter a price: '))

rrsp = 260512
inv = 102489
tfsa = 56717

rrsp_count = int(rrsp / price)
inv_count = int(inv / price)
tfsa_count = int(tfsa / price)

print ('{} {}'.format('RRSP count: ', rrsp_count))
print ('{} {}'.format('Investment count: ', inv_count))
print ('{} {}'.format('TFSA count: ', tfsa_count))
