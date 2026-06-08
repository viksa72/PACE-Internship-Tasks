#1. add 15 and x*y
add = lambda x: x + 15
mul = lambda x,y: x * y
print(add(10))
print(mul(6,8))

#2. sor list of tuples
l= [('English', 88), ('Science', 90), ('Maths', 97), ('Social sciences', 82)]
l.sort(key=lambda x:x[1])
print(l)

#3. sort list of dictionaries
ld= [{'make': 'Nokia', 'model': 216, 'color': 'Black'}, {'make': 'Mi Max', 'model': '2', 'color': 'Gold'}, {'make': 'Samsung', 'model': 7, 'color': 'Blue'}] 
r=sorted(ld, key=lambda x:x['color'])
print(r)

#4. check if string starts with given character
check = lambda s,ch : s.startswith(ch)
print(check("Python","P"))

#5. check string is number
isnum=lambda s:s.isdigit()
print(isnum("123"))

#6. Divisible by 19 or 13
lst = [19,65,57,39,152,639,121,44,90,190]
check = lambda x: x % 19 == 0 or x % 13 == 0
result = []
for i in lst:
    if check(i):
        result.append(i)
print(result)

#7. sort according to sum of rows
matrix=[[1,2,3],[2,4,5],[1,1,1]]
r=sorted(matrix,key=lambda x:sum(x))
print(r)

#8. string has capital letter/lower case letter/number/min length
s = input("Enter a string: ")
upper = False
lower = False
digit = False
for ch in s:
    if ch.isupper():
        upper = True
    elif ch.islower():
        lower = True
    elif ch.isdigit():
        digit = True
valid = lambda: len(s) >= 10 and upper and lower and digit
if valid():
    print("Valid String")
else:
    print("Invalid String")
    
#9. contains specific substring
lst = ['red', 'black', 'white', 'green', 'orange']
sub = input("Enter substring: ")
check = lambda x: sub in x
result = []
for item in lst:
    if check(item):
        result.append(item)
print(result)

#10. sort list by numbers and strings
lst = [19,'red',12,'green','blue',10,'white','green',1]
result = sorted(lst, key=lambda x: (type(x) == str, x))
print(result)
