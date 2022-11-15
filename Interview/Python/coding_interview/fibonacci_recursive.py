def fib(n):
    if n == 0:
        number = 0
    elif n == 1:
        number = 1
    else:
        number = fib(n-1) + fib(n-2)
    return number

for i in range (10):
    print (fib(i))
