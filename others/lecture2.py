# Dictionary

id_card = {
    'Username': 'Benaniosam',
    'Age': 24,
    'Phone': 9002913342 
    }
id_card['Status']= 'Married'
print(id_card)
print(id_card.get('Status'))
print(len(id_card))

for x,y in id_card.items():
    print(x,'-',y)