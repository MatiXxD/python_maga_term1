def findMan(trains, searchMan):
    place = {}
    carNum = 0
    
    for train in trains:
        for car in train["cars"]:
            for man in car["people"]:
                if man == searchMan:
                    car["people"].remove(man)
                    place["dist"] = carNum
                    place["name"] = train["name"]
                    return place
            carNum += 1

    if not place: return -1

def move(trains, event, place):
    destination = place["dist"] + event["distance"]
    for train in trains:
        for car in train["cars"]:
            if destination == 0 and train["name"] == place["name"]:
                car["people"].append(event.get("passenger"))
                return 1
            destination -= 1

    return -1

def switch(trains, event):

    count = event.get("cars")
    source = event.get("train_from")
    target = event.get("train_to")
    
    if count > 0:
        tail = []
        for train in trains:
            if train["name"] == source:
                for car in train["cars"][::-1]:
                    if count > 0:
                        train["cars"].remove(car)
                        count -= 1
                        tail.append(car)

        for train in trains:
            if train["name"] == target:
                train["cars"].extend(reversed(tail))

    else:
        return -1


def process(trains, events, result):

    for event in events:
        if event["type"] == "walk":
            place = findMan(trains, event["passenger"])
            if place == -1: 
                print("Wrong man in input.")
                return -1
            
            check = move(trains, event, place)
            if check == -1:
                print("Can't move man.")
                return -1


        elif event["type"] == "switch":
            check = switch(trains, event)
            if check == -1:
                print("Can't switch cars")
                return -1


        else:
            print("Wrong event!")
            return -1
    

    for train in trains:
        for car in train["cars"]:
            if car["name"] == result:
                return len(car["people"])



# [1, 2, 3, 4, 5] - [6, 7, 8] - [9, 10, 11, 12] ------>
# [6, 7, 8] -> [8, 7, 6]