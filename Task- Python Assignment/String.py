#  1. Length of a string
s = input("1. Enter a string: ")
print("Length:", len(s))

#  2. Character frequency
s = input("2. Enter a string: ")
checked = ""
for ch in s:
    if ch not in checked:
        print(ch, "=", s.count(ch))
        checked += ch

#  3. First 2 + last 2 chars
s = input("3. Enter a string: ")
if len(s) < 2:
    print("")
else:
    print(s[:2] + s[-2:])

#  4. Replace first char (except first occurrence) with '$'
s = input("4. Enter a string: ")
result = s[0] + s[1:].replace(s[0], "$")
print("Result:", result)

#  5. Swap first 2 chars of two strings
a = input("5. Enter first string: ")
b = input("Enter second string: ")
result = b[:2] + a[2:] + " " + a[:2] + b[2:]
print("Result:", result)

#  6. Add 'ing' or 'ly' 
s = input("6. Enter a string: ")
if len(s) < 3:
    print(s)
elif s[-3:] == "ing":
    print(s + "ly")
else:
    print(s + "ing")

#  7. Replace 'not'...'poor' with 'good' 
s = input("7. Enter a string: ")
n = s.find("not")
p = s.find("poor")
if n != -1 and p != -1 and n < p:
    s = s[:n] + "good" + s[p+4:]
print(s)

#  8. Length of longest word 
def longest_word(words):
    return max(len(w) for w in words)

s = input("8. Enter words separated by spaces: ")
print("   Longest word length:", longest_word(s.split()))

#  9. Remove nth index character 
s = input("9. Enter a string: ")
n = int(input("Enter index: "))
print(s[:n] + s[n+1:])

#  10. Unique sorted words from comma-separated input 
s = input("10. Enter comma separated words: ")
words = ""
word = ""
for ch in s + ",":
    if ch != ",":
        word += ch
    else:
        word = word.strip()
        if word not in words:
            words += word + " "
        word = ""
print(words)

#  11. Reverse if length is multiple of 4 
def reverse_if_multiple_of_4(s):
    if len(s) % 4 == 0:
        rev = ""
        for i in range(len(s) - 1, -1, -1):
            rev += s[i]
        return rev
    else:
        return s
s = input("11. Enter a string: ")
print(reverse_if_multiple_of_4(s))

#  12. Uppercase if first 4 chars have >= 2 uppercase 
def convert_upper(s):
    count = 0
    for ch in s[:4]:
        if 'A' <= ch <= 'Z':
            count += 1
    if count >= 2:
        return s.upper()
    else:
        return s
s = input("12. Enter a string: ")
print(convert_upper(s))

#  13. Check if string starts with specified characters 
s= input("13. Enter a string: ")
prefix= input("Enter prefix to check: ")
print("Starts with prefix:", s.startswith(prefix))

#  14. Float to 2 decimal places 
num = 3.1415926
print("%.2f" % num)

#  15. Count repeated characters 
s = input("15. Enter a string: ")
checked = ""
for ch in s:
    if ch not in checked:
        if s.count(ch) > 1:
            print(ch, s.count(ch))
        checked += ch

#  16. Print index of each character 
s = input("16. Enter a string: ")
for i in range(len(s)):
    print(s[i], "=", i)

#  17. Convert string to list of characters 
s = input("17. Enter a string: ")
for ch in s:
    print(ch)

#  18. Swap comma and dot 
s = input("18. Enter string: ")
s = s.replace(".", "#")
s = s.replace(",", ".")
s = s.replace("#", ",")
print(s)

#  19. Smallest and largest word 
s = input("19. Enter a sentence: ")
words = s.split()
smallest = min(words, key=len)
largest = max(words, key=len)
print("Smallest word =", smallest)
print("Largest word =", largest)

#  20. Remove consecutive duplicates 
s = input("20. Enter a string: ")
result = s[0]
for i in range(1, len(s)):
    if s[i] != s[i-1]:
        result += s[i]
print(result)