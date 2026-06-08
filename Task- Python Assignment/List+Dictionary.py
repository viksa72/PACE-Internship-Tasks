#1. sort dictionary by value
d = {'a': 3, 'b': 1, 'c': 2}
asc = dict(sorted(d.items()))
print(asc)
desc = dict(sorted(d.items(), reverse=True))
print(desc)

#2. Add key to dictionary
d={0:10, 1:20}
d[2]=30
print(d)

#3. Concatenate dictionaries
d1={1:10, 2:20}
d2={3:30, 4:40}
d3={5:50, 6:60}
result={}
result.update(d1)
result.update(d2)
result.update(d3)
print(result)

#4. Check if key exists in dictionary
d={0:10, 1:20}
key=1
if key in d:
    print("Key exists")
else:
    print("Key does not exist")
    
#5. iterate over dictionary using for loops
d={0:10, 1:20, 2:30}
for key in d:
    print(key, d[key])

#6. generate and print diction in the form (x,x*x)
n=int(input("Enter number: "))
d={}
for i in range(1,n+1):
    d[i]=i*i
print(d)

#7.merge 2 dictionaries
d1={1:10, 2:20}
d2={3:30, 4:40}
d1.update(d2)
print(d1)

#8. sum of all items in a dictionary
d={1:10, 2:20, 3:30}
total=0
for key in d:
    total+=d[key]
print("Sum of all items:", total)

#9. multiply all items in a dictionary
d={1:10, 2:20, 3:30}
product=1
for key in d:
    product*=d[key]
print("Product of all items:", product)

#10. remove a key from dictionary
d={1:10, 2:20, 3:30}
key=2
if key in d:
    d.pop(key)
print(d)

#11. sort dictionary by key
d={3:30, 1:10, 2:20}
asc=dict(sorted(d.items()))
print(asc)

#12. max/min value in dictionary
d={1:10, 2:20, 3:30}
max_val=max(d.values())
min_val=min(d.values())
print("Max value:", max_val)
print("Min value:", min_val)

#13. remove duplicates from dictionary
d = {'a': 10, 'b': 20, 'c': 10, 'd': 30}
result = {}
for key, value in d.items():
    if value not in result.values():
        result[key] = value
print(result)

#14. Check if dictionary is empty
d={}
if not d:
    print("Dictionary is empty")
else:
    print("Dictionary is not empty")
    
#15. add values of same key in two dictionaries
d1={1:10, 2:20}
d2={1:5, 2:15}
result={}
for key in d1:
    result[key]=d1[key]+d2[key]
print(result)

#16. highest 3 values in dictionary
d={1:10, 2:20, 3:30, 4:40, 5:50}
d = {'a': 10, 'b': 50, 'c': 70, 'd': 20, 'e': 90}
values = sorted(d.values(), reverse=True)
print("Highest 3 values:", values[:3])

#17. match key values in two dictionaries
d1 = {'key1': 1, 'key2': 3, 'key3': 2}
d2 = {'key1': 1, 'key2': 2}
for key in d1:
    if key in d2 and d1[key] == d2[key]:
        print(key, ":", d1[key], "is present in both dictionaries")
        
#18. Check is dictionaries in list are empty or not
lst = [{}, {}, {}]
flag = True
for d in lst:
    if len(d) != 0:
        flag = False
        break
print(flag)

#19. remove duplicates from list of lists
list=[[10,20],[40],[30,56,25],[10,20],[33],[40]]
nlist=[]
for i in list:
    if i not in nlist:
        nlist.append(i)
print(nlist)

#20. extend list without append
l1=[10,20,30]
l2=[40,50,60]
l2+=l1
print(l2)        