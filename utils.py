students = [
    {'name': 'Alice', 'marks': 85},
    {'name': 'Bob', 'marks': 72},
    {'name': 'Charlie', 'marks': 90}
]

# Filter students with marks >= 80
top_students = list(filter(lambda s: s['marks'] >= 80,students))
print(top_students)

# Extract names of top students
names = list(map(lambda s: s['name'], top_students))
print("Top Students:", names)
