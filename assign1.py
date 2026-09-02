'''
Write a Python program that can do the following:

- You have $50

- You buy an item that is $15, that has a 3% tax

- Using the print()  Print how much money you have left, after purchasing the item.
'''
money = 50
item = 15
sell = item * 0.03
tax = item + sell
purchase = money - tax

print(purchase)
