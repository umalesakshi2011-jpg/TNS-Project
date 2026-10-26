raw_stock = [("Apple",0.75,50),
             ("Banana",0.40,100),
             ("Milk",2.50,15),
             ("Bread",1.80,20),
             ("Apple",0.75,30)]

shopping_card = ["Apple","Apple","Milk","Dragonfruite","Bread"]

#Convert into dictionary
def build_inventory (raw_stock):
    inventory = {}
    for name ,price,quantity in raw_stock:
        if name in inventory:
            inventory[name]["stock"]+= quantity
        else:
            inventory[name]={"price" : price, "stock":quantity}
    return inventory
inventory = build_inventory(raw_stock)

def checkOut(inventory,card):
    recipt =[]
    for item in card :
        if item  not in inventory:
            print(f"{item }is not carried in store")
        
        elif inventory[item]["price"]<=0:

                 print(f"{item}is sold out")
        else:
            inventory[item]["stock"] -=1
            price = inventory[item]["price"]
            recipt.append((item,price))
            
    return recipt

print("----- RECIPT ----")
inventory= build_inventory(raw_stock)
recipt = checkOut(inventory,shopping_card)


total = 0
for item , price in recipt:
    print( item , price)
    total+=price
print("Total :",total)
 