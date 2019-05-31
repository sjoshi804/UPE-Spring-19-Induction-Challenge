import requests 
 
# defining the api-endpoint  
API_ENDPOINT = "http://ec2-34-211-81-131.us-west-2.compute.amazonaws.com/"

headers = {'Content-type': 'application/x-www-form-urlencoded'}

# post request to retrieve session token
session_request = {"uid" : "105032378"}
session_req_response = requests.post(API_ENDPOINT + "session", session_request, headers)
SESSION_TOKEN = session_req_response.json()["token"]

# post and get request prototype for game
API_REQUEST = API_ENDPOINT + "game?token=" + SESSION_TOKEN

UP = {"action": "up"}
DOWN = {"action": "down"}
LEFT = {"action": "left"}
RIGHT = {"action": "right"}
# solve game
while (True):
    # get game
    game_request_response = requests.get(API_REQUEST, headers)
    if (game_request_response.json()["status"] == "FINISHED"):
        print("Completed.")
        break
    print(game_request_response.json())
    # solve level

    level_completed = False
    traversed = []
    for x in range(0, game_request_response.json()["size"][0]):
        col = []
        for y in range(0, game_request_response.json()["size"][1]):
            col.append(False)
        traversed.append(col)
    startx = game_request_response.json()["cur_loc"][0]
    starty = game_request_response.json()["cur_loc"][1]
    point_stack = [(startx, starty, 0)]
    dir_stack = []
    traversed[startx][starty] = True

    while(True):
        top = point_stack.pop()
        current_x = top[0]
        current_y = top[1]
        current_dir = top[2]

        #print(str(current_x) + " " + str(current_y) + " " + str(current_dir) + "\n")
        if (current_dir > 3):
            undo = requests.post(API_REQUEST, dir_stack.pop(), headers)
            continue
        else:
            point_stack.append((current_x, current_y, current_dir + 1))
        
        if (current_dir == 3 and current_y + 1 < game_request_response.json()["size"][1]):
            if (traversed[current_x][current_y + 1]):
                continue
            else:
                traversed[current_x][current_y + 1] = True
            move = requests.post(API_REQUEST, DOWN, headers)
            if (move.json()["result"] == 1):
                break
            elif (move.json()["result"] == -1):
                continue
            elif (move.json()["result"] == 0):
                point_stack.append((current_x, current_y + 1, 0))
                dir_stack.append(UP)
            else:
                print("ERROR RIGHT" + str(move.json()["result"]))
                exit
            
        elif (current_dir == 1 and current_x + 1 < game_request_response.json()["size"][0]):
            if (traversed[current_x + 1][current_y]):
                continue
            else:
                traversed[current_x + 1][current_y] = True
            move = requests.post(API_REQUEST, RIGHT, headers)
            if (move.json()["result"] == 1):
                break
            elif (move.json()["result"] == -1):
                continue
            elif (move.json()["result"] == 0):
                point_stack.append((current_x + 1, current_y, 0))
                dir_stack.append(LEFT)
            else:
                print("ERROR DOWN" + str(move.json()["result"]))
                exit

        elif (current_dir == 0 and current_x - 1 >= 0):
            if (traversed[current_x - 1][current_y]):
                continue
            else:
                traversed[current_x - 1][current_y] = True
            move = requests.post(API_REQUEST, LEFT, headers)
            if (move.json()["result"] == 1):
                break
            elif (move.json()["result"] == -1):
                continue
            elif (move.json()["result"] == 0):
                point_stack.append((current_x - 1, current_y, 0))
                dir_stack.append(RIGHT)
            else:
                print("ERROR UP" + str(move.json()["result"]))
                exit
        
        elif (current_dir == 2 and current_y - 1 >= 0):
            if (traversed[current_x][current_y - 1]):
                continue
            else:
                traversed[current_x][current_y - 1] = True
            move = requests.post(API_REQUEST, UP, headers)
            if (move.json()["result"] == 1):
                break
            elif (move.json()["result"] == -1):
                continue
            elif (move.json()["result"] == 0):
                point_stack.append((current_x, current_y - 1, 0))
                dir_stack.append(DOWN)
            else:
                print("ERROR LEFT" + str(move.json()["result"]))
                exit
    print("Level completed")

        

            

                




        
        

