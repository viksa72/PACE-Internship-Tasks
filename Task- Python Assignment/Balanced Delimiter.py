def is_balanced(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in "([{":
            stack.append(char)
        else:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()

    return len(stack) == 0

s = input("Enter Delimiter: ").strip()
print(is_balanced(s))