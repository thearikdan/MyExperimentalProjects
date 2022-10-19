#[expression for element in iterable if condition]

a = [1,2,3]
b = [x**2 for x in a]
print (b)

c = [x**2 for x in a if x%2 == 0]
print(c)

