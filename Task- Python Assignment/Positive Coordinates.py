def shift_coordinates(points):
    min_x = min(x for x, y in points)
    min_y = min(y for x, y in points)

    shift_x = -min_x if min_x < 0 else 0
    shift_y = -min_y if min_y < 0 else 0

    return [(x + shift_x, y + shift_y) for x, y in points]


# Single input
points = eval(input("Enter points: "))

result = shift_coordinates(points)

print("Shifted Points:", result)