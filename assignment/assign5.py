'''
Given: my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

- Create a while loop that prints all elements of the my_list variable 3 times.

- When printing the elements, use a for loop to print the elements

- However, if the element of the for loop is equal to Monday, continue without printing
'''

my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
length = 0
while length < 5:
    length += 1
    print(my_list)
    if length == 3:
        break

for i in my_list:
    print(i)

for i in my_list:
    if i == 'Monday':
        continue
    print(i)