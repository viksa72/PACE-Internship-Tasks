#1. convert integer to roman numeral and vice versa
class Roman:
    def int_to_roman(self, num):
        val=[1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        sym=["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman=""
        for i in range(len(val)):
            while num>=val[i]:
                roman+=sym[i]
                num-=val[i]
        return roman
    
    def roman_to_int(self, s):
        d={"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}
        num=0
        for i in range(len(s)-1):
            if d[s[i]]<d[s[i+1]]:
                num-=d[s[i]]
            else:
                num+=d[s[i]]
        num+=d[s[-1]]
        return num
r=Roman()
print(r.int_to_roman(25))
print(r.roman_to_int("XXV"))

#2. Validity of parentheses
class Parentheses:
    def check(self,s):
        stack=[]
        pairs={')':'(', '}':'{', ']':'['}
        for ch in s:
            if ch in pairs.values():
                stack.append(ch)
            elif ch in pairs.keys():
                if not stack or stack.pop() != pairs[ch]:
                    return False
        return len(stack)==0
p = Parentheses()
print(p.check("()[]{}"))  
print(p.check("([)]"))    

#3. unique subsets
class Subsets:
    def get_subsets(self, nums):
        result = [[]]
        for num in nums:
            result += [item + [num] for item in result]
        return result
s = Subsets()
print(s.get_subsets([4,5,6]))

#4. Two Sum
class TwoSum:
    def find(self, nums, target):
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return i, j
t = TwoSum()
print(t.find([90,20,10,40,50,60,70],50))

#5. Three number sum=0
class ThreeSum:
    def find(self,nums):
        result=[]
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                for k in range(j+1, len(nums)):
                    if nums[i]+nums[j]+nums[k]==0:
                        result.append((nums[i], nums[j], nums[k]))
        return result
s = ThreeSum()
print(s.find([-25, -10, -7, -3, 2, 4, 8, 10]))

#6. Power
class Power:
    def power(self,x,n):
        return x**n
p = Power()
print(p.power(2,5))

#7. Reverse string by word
class ReverseWord:
    def reverse(self,s):
        words=s.split()
        words.reverse()
        return " ".join(words)
r = ReverseWord()
print(r.reverse("hello .py"))

#8.get string and print string
class StringClass:
    def get_string(self):
        self.s=input("Enter a string: ")
    def print_string(self):
        print("You entered:", self.s)
s = StringClass()
s.get_string()
s.print_string()

#9. Circle area and perimeter
class Circle:
    def initialize(self, radius):
        self.r = radius
    def area(self):
        return 3.14 * (self.r ** 2)
    def perimeter(self):
        return 2 * 3.14 * self.r
c = Circle()
c.initialize(5)
print("Area:", c.area())
print("Perimeter:", c.perimeter())

#10. class name
class Circle:
    pass
c = Circle()
print(type(c))
    