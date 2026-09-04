value = 10
tax_percent = 0.35
tax = value * tax_percent
price = value + tax
print(price)
first_name = "Benanio"
second_name = "sam"

print(first_name + second_name)

sets = {1,2,3,2,1,3,4,6,7,8,6,5,4,3,2,7,7}
print(sets.pop())
print(sets)
print(f"length of sets: {len(sets)}")

for unique in sets:
    print(unique)

sets.discard(7)

sets.add(19)

sets.update([7,11])

sets.pop()

print(sets)