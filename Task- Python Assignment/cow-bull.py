import random
s=str(random.randint(1000,9999))
count=0
while True:
    n=input("Enter a number: ")
    cows=bulls=0
    for i in range(4):
        if n[i]==s[i]:
            cows+=1
        elif n[i] in s:
            bulls+=1
    count+=1
    print(cows, "cows, " ,bulls,"bulls")
    if cows == 4:
        print("You guessed the number!")
        print("Number =", n)
        print("Total guesses =", count)
        break   
    