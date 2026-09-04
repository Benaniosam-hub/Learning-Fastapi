'''
- Create a function that takes in 3 parameters(firstname, lastname, age) and

returns a dictionary based on those values
'''

def data(firstname,lastname,age):
    d = {'firstname':firstname,'lastname':lastname,'age':age}
    return d

mydata = data(firstname='Benanio',lastname='sam',age=24)

print(mydata)
