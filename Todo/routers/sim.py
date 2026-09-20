# class outer():
#     def __init__(self):
#         self.name = "bena"
#         self.__age = 24
        
#     def get_age(self):
#         return self.__age
# brand = outer()
# bingo = brand.get_age()
# print(bingo)

# from array import array

# my_array = array('i',[10,20,34])
# x=10
# my_array.append(50)
# my_array.extend([20,34,50,20])
# my_array.remove(20)
# print(my_array)
# print(my_array[0:5:2])
# print(hash("name"))

# person = {
#     "name": "Ben",
#     "age": 24
# }

# if "name" in person:
#     print("Key exists")

# print(person.get("name"))

# def create_cube(n):
    
#     for x in range(n):
#         yield x**3
    

# for i in create_cube(10):
#     print(i)

# a = {"name":"ben",
#      "age": 24,
#      "cgp":4.5}

# print(a.get("name"))


# numbers = [1,2,3,4,5]

# results = filter(lambda x: x%2==0, numbers)

# print(list(results))


# def name():
#     print("hello")
# def same(function):
#     function()

# same(name)

# def countdown(n):
#     if n==0:
#         return

#     print(n)
#     countdown(n-1)

# countdown(5)

# with open("sim.txt", "r")as file:
#     content = file.read()
#     print(content)
# numbers = [1,2,3,4]
# start = list(filter(lambda x:x%2==0, numbers))
# print(start)

# for i in range(1,11):
#     print(f"5 x {i} = {i * 5}")

        
# RECURRSION 
# def normal_func(n):
#       if n == 0:  #its base condition
#             return
#       print(n)
#       normal_func(n-1)

# normal_func(5)

for i in range(3):
      print(i)
else:
      print("done")