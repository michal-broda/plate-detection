import easyocr



def new_plate(name_file):
    #plate = "C:/Users/rycch/Desktop/a.jpg"
    plate = "model/" + name_file
    reader = easyocr.Reader(['en'])
    aaa = reader.readtext(plate)
    print(aaa)
    print(type(aaa))
    print(len(aaa))
    print(len(aaa[0]))

    for put in aaa:
        one, two, tree = put
        #print(one, two, tree)
        #print("ssssss")
        print(two)


new_plate("a.jpg")