def make_node(value):
    return {"value":value,"left":None,"right":None}

def build():
    root = make_node(50)
    root["left"]=make_node(30)
    root["right"]=make_node(70)

    root["left"]["left"]=make_node(20)
    root["left"]["right"]=make_node(40)

    root["right"]["left"]= make_node(60)
    root["right"]["right"]=make_node(80)

    current = root
    while current["left"]is not None:
        current=current["left"]
    print("leftmost Element:",current["value"])

    while current["right"]is not None:
        current=current["right"]
    print("rightmost Element:",current["value"])

    return root

   



t = build()
print(t)


