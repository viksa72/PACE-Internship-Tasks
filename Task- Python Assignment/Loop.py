# 1. Numbers divisible by 7 & multiple of 5
for i in range(1500,2700):
    if (i%7==0) and (i%5==0):
        print(i)
        
# 2. print number from 0 to 6 except 3 and 6
for i in range(7):
    if i == 3 or i == 6:
        continue
    print(i)
    
#3. FizzBuzz
for i in range(1,51):
    if i%3==0:
        print("Fizz")
    elif i%5==0:
        print("Buzz")
    elif i%3==0 and i%5==0:
        print("FizzBuzz")
    else:        
        print(i)
        
#4. triangle is equilateral, isosceles or scalene
x=int(input("Enter first side: "))
y=int(input("Enter second side: "))
z=int(input("Enter third side: "))
if x==y==z:
    print("Equilateral triangle")
elif x==y or y==z or z==x:
    print("Isosceles triangle")
else:    
    print("Scalene triangle")

#5. sum and average of n numbers
sum=0
count=0
while True:
    n=int(input("Enter number (0 to stop): "))
    if n==0: 
        break
    sum+=n
    count+=1
if count>0:
    print("Sum:", sum)
    print("Average:", sum/count)
    
#6. Nested Loop for pattern
for i in range(1,10):
    for j in range(i):
        print(i, end="")
    print()
    
#7. count number of elements in a list greater than 30
numbers = [10, 25, 30, 45, 50, 15]
count = 0
for num in numbers:
    if num > 30:
        count += 1
print("Number of elements greater than 30:", count)

#8. length and breaadth of rectangle to check if its a square
l=int(input("ENter length of rectangle: "))
b=int(input("Enter breadth of rectangle: "))
if l==b:
    print("It's a square")
    
#9. total cost
discount=10/100
quantity=int(input("Enter quantity: "))
if quantity>1000:
    price=100*quantity*(1-discount)
else:
    price=100*quantity
print("Total cost:", price)

# 10. Employee bonus
salary=int(input("Enter salary: "))
years=int(input("Enter years of service: "))
if years>5:
    bonus=salary*5/100
else:    bonus=0
print("Bonus:", bonus)

#11. Grading System
marks=int(input("Enter marks: "))
if marks<25:
    grade='F'
elif marks<45 and marks>=25:
    grade='E'
elif marks<50 and marks>=45:
    grade='D'
elif marks<60 and marks>=50:
    grade='C'
elif marks<80 and marks>=60:
    grade='B'
else:
    grade='A'
print("Grade:", grade)

#12. Atterndance
c=int(input("Enter number of classes held: "))
an=int(input("Enter number of classes attended: "))
attendance=(an/c)*100
print("Attendance percentage:", attendance)
if attendance>=75:
    print("Allowed to sit in exam")
else:    
    print("Not allowed to sit in exam")
    
#13. average value
for i in range(10):
    num=int(input("Enter number: "))
    sum+=num
    count+=1
print("Average:", sum/count)

#14. multiplication table of 24,50 and 29
for i in range(1,11):
    print("24 x", i, "=", 24*i)
for i in range(1,11):
    print("50 x", i, "=", 50*i)
for i in range(1,11):
    print("29 x", i, "=", 29*i)
    
#15. use input numbers until user presses q
sum=0
count=0
product=1
while True:
    s=input("Enter number (or 'q' to quit): ")
    if s=='q':
        break
    sum+=int(s)
    product*=int(s)
    count+=1
if count>0:
    print("Product:", product)
    print("Average:", sum/count)
    
#16. Search and delete number from list
list=[]
n=int(input("Enter number of elements: "))
for i in range(n):
    num=int(input("Enter number: "))
    list.append(num)
key=int(input("Enter number to delete: "))
if key in list:
    list.remove(key)
    print("Deleted")
else:
    print("Not Found")
print(list)

#17. Lists of even,odd, prime numbers
even=[]
odd=[]
prime=[]
for i in range(1,101):
    if i%2==0:
        even.append(i)
    else:
        odd.append(i)
    if i>1:
        for j in range(2,i):
            if i%j==0:
                break
        else:
            prime.append(i)
print("Even numbers:", even)
print("Odd numbers:", odd)
print("Prime numbers:", prime)

#18. Numbers divisible by 4,6,8,10.3.5.7,9
div4 = []
div6 = []
div8 = []
div10 = []
div3 = []
div5 = []
div7 = []
div9 = []
for i in range(1,101):
    if i % 4 == 0:
        div4.append(i)
    if i % 6 == 0:
        div6.append(i)
    if i % 8 == 0:
        div8.append(i)
    if i % 10 == 0:
        div10.append(i)
    if i % 3 == 0:
        div3.append(i)
    if i % 5 == 0:
        div5.append(i)
    if i % 7 == 0:
        div7.append(i)
    if i % 9 == 0:
        div9.append(i)
print(div4)
print(div6)
print(div8)
print(div10)
print(div3)
print(div5)
print(div7)
print(div9)

#19. Lists for int,string,floats
lst = [10, 2.5, "hello", 15, "python", 4.8]
ints = []
floats = []
strings = []
for i in lst:
    if type(i) == int:
        ints.append(i)
    elif type(i) == float:
        floats.append(i)
    elif type(i) == str:
        strings.append(i)
print("Integers =", ints)
print("Floats =", floats)
print("Strings =", strings)

#20. square of elements:
list=[1, 2, 3, 4, 5]
squares=[]
for i in list:
    squares.append(i**2)
print("Original list:", list)
print("Squares:", squares)