#https://www.youtube.com/watch?v=BCZWQTY9xPE&ab_channel=BharatiDWConsultancy

def is_prime(number):
	half = int (number / 2)
	for i in range (2, half):
		if (number % i) == 0:
			return False
	return True
	
for i in range (100, 200):
	if is_prime(i):
		print(i)	
