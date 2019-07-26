from numpy import empty, set_printoptions, inf
from random import randint, choice, uniform
import constants as cs
import json
import os
from time import sleep

MAX = 29
MIN = 0

# for self.object:   0 = null   1 = water 2 = plant 3 = meat   4 = rabbit   5 = fox
dirname, filename = os.path.split(os.path.abspath(__file__))
data = {} # Start a new data
data['carrot'] = []
data['meat'] = []
data['rabbit'] = []
data['fox'] = []



class Game:
    def __init__(self,ob):
        self.object = ob
        self.turn = 0
        for i in range (0,0):
            self.Spawn_carrot()

        for i in range (0,1):
            self.Spawn_rabbit()

        for i in range (0,3):
            self.Spawn_fox()

        while True:
            self.Next_turn()
        

    def Next_turn(self):
        sleep(1)
        self.turn += 1
        self.Alive_check()
        if self.turn % 20 == 0 and len(data['carrot']) <= 10:
            self.Spawn_carrot()
        self.Rabbit_next()
        self.Fox_next()
        print(self.object)
        self.Save_file()

    def Alive_check(self):
        delList = []
        for i in range (0,len(data['rabbit'])):
            if data['rabbit'][i]['health'] <= 0:
                delList.append(('rabbit',i))
        for i in range (0,len(data['carrot'])):
            if data['carrot'][i]['health'] <= 0:
                delList.append(('carrot',i))
        for i in range (0,len(data['meat'])):
            if data['meat'][i]['health'] <= 0:
                delList.append(('meat',i))
        for i in range (0,len(data['fox'])):
            if data['fox'][i]['health'] <= 0:
                delList.append(('fox',i))
        for item in delList:
            print("{}th {} deleted".format(item[1],item[0]))
            if item[0] == 'Rabbit':
                Y,X = data[item[0]][item]['Y'], data[item[0]][item]['X']
                self.Data_save_meat(X,Y,100)
            del data[item[0]][item[1]]
            

    def Rabbit_next(self):
        for rabbit in (data["rabbit"]):
            speed, distance, nextMove, objective = self.Rabbit_vision(rabbit)
            #print([rabbit['y'],rabbit['x']],"speed",speed,"distance",distance,"next move",nextMove, "objective", objective)

            self.Rabbit_action(rabbit, speed, distance, nextMove, objective)

    def Rabbit_action(self,rabbit,speed,distance,nextMove,objective):
        def Rabbit_cost():
            if rabbit['thirst'] <= 0:
                rabbit['health'] -= 5
            elif rabbit['thirst'] > 0:
                rabbit['thirst'] -= 1
            if rabbit['hunger'] <= 0:
                rabbit['health'] -= 5
            elif rabbit['hunger'] > 0:
                rabbit['hunger'] -= 1
        def Correct_direction():
            if nextMove[0] == 0 or nextMove[1] == 0:
                if nextMove == [0,1]:
                    rabbit['direction'] = "E"
                elif nextMove == [1,0]:
                    rabbit['direction'] = "S"
                elif nextMove == [0,-1]:
                    rabbit['direction'] = "W"
                elif nextMove == [-1,0]:
                    rabbit['direction'] = "N"
            else:
                if nextMove == [1,1]:
                    rabbit['direction'] = choice("ES")
                elif nextMove == [-1,-1]:
                    rabbit['direction'] = choice("NW")
                elif nextMove == [1,-1]:
                    rabbit['direction'] = choice("SW")
                elif nextMove == [-1,-1]:
                    rabbit['direction'] = choice("NE")
        def Move_adjust(nextMove):
            '''
            input: none
            output: none
            If the nextMove is not movable, consider the adjasent one, loop till the chosen one is movable
            '''
            print(nextMove)
            if (0 > rabbit['y']+nextMove[0] or rabbit['y']+nextMove[0] > 29) and (0 > rabbit['x']+nextMove[1] or rabbit['x']+nextMove[1] > 29):
                nextMove[0] = nextMove[0]*-1
                nextMove[1] = nextMove[1]*-1
                nextMove[choice([0,1])] = 0
                Correct_direction()

            elif (0 > rabbit['y']+nextMove[0] or rabbit['y']+nextMove[0] > 29) or (0 > rabbit['x']+nextMove[1] or rabbit['x']+nextMove[1] > 29):
                if nextMove == [-1,0]:
                    nextMove = choice([[0,1],[0,-1]])
                elif nextMove == [0,-1]:
                    nextMove = choice([[1,0],[-1,0]])
                elif nextMove == [1,0]:
                    nextMove = choice([[0,1],[0,-1]])
                elif nextMove == [0,1]:
                    nextMove = choice([[1,0],[-1,0]])
                Correct_direction()

            if self.object[rabbit['y']+nextMove[0],rabbit['x']+nextMove[1]] == 0:
                return True

            elif self.object[rabbit['y']+nextMove[0],rabbit['x']+nextMove[1]] != 0:
                if nextMove[0] == 0:
                    nextMove[0] = choice([-1,1])
                    if 0 > rabbit['y']+nextMove[0] or rabbit['y']+nextMove[0] > 29 or 0 > rabbit['x']+nextMove[1] or rabbit['x']+nextMove[1] > 29:
                        Correct_direction()
                        return True
                elif nextMove[1] == 0:
                    nextMove[1] = choice([-1,1])
                    if 0 > rabbit['y']+nextMove[0] or rabbit['y']+nextMove[0] > 29 or 0 > rabbit['x']+nextMove[1] or rabbit['x']+nextMove[1] > 29:
                        Correct_direction()
                    return True
                else:
                    nextMove[choice([0,1])] = 0
                    if 0 > rabbit['y']+nextMove[0] or rabbit['y']+nextMove[0] > 29 or 0 > rabbit['x']+nextMove[1] or rabbit['x']+nextMove[1] > 29:
                        Correct_direction()
                    return True
            return False
        def Rabbit_move():
            if rabbit['action'] == "Moving2":
                rabbit['thirst'] += 1
                rabbit['hunger'] += 1
                rabbit['action'] = "Moving1"
            elif rabbit['action'] == "Moving1":
                rabbit['thirst'] += 1
                rabbit['hunger'] += 1
                rabbit['action'] = "Moving"
            elif rabbit['action'] == "Moving":
                rabbit['action'] = "None"
                movable = Move_adjust(nextMove)
                if not movable:
                    return None
                self.object[rabbit['y'],rabbit['x']] = 0
                rabbit['y'] = rabbit['y'] + nextMove[0]
                rabbit['x'] = rabbit['x'] + nextMove[1]            
                self.object[rabbit['y'],rabbit['x']] = 4
        def Rabbit_drink():
            rabbit['thirst'] += 5
            if rabbit['thirst'] >= 100:
                rabbit['action'] = 'None'
        def Rabbit_eat():
            for i in range (0,len(data['carrot'])):
                if data['carrot'][i]['y'] == rabbit['y']+nextMove[0] and data['carrot'][i]['x'] == rabbit['x']+nextMove[1]:
                    data['carrot'][i]['health'] -= 5
            rabbit['hunger'] += 5

            if rabbit['hunger'] >= 100:
                rabbit['action'] = 'None'
        def Rabbit_mate():
            if rabbit['desire'] <= 0:
                rabbit['action'] = 'None'
            rabbit['desire'] -= 100
        def Rabbit_birth():
            rabbit['pregnant'] -= randint(15,30)
            Move_adjust(nextMove)
            self.object[rabbit['y']+nextMove[0],rabbit['x']+nextMove[1]] = 4
            self.Data_save_rabbit(rabbit['y']+nextMove[0],rabbit['x']+nextMove[1],100,choice([0,1]),0,"Moving")
                
            if rabbit['pregnant'] <= 0:
                rabbit['pregnant'] = 0
                rabbit['action'] = 'None'
        def Status_check(rabbit):
            rabbit['age'] += 1 # Age is relative to the number of turns
            if rabbit['gender'] == 1: 
                if rabbit['pregnant'] >= 1 and rabbit['pregnant'] < 100:
                    rabbit['pregnant'] += 5
                elif rabbit['pregnant'] >= 100:
                    rabbit['action'] = "Birth"
            elif rabbit['gender'] == 0:
                rabbit['desire'] += 1

        Status_check(rabbit)
        
        if rabbit['action'] != "Moving1" or rabbit['action'] != "Moving2":
            Rabbit_cost()

        if speed == 2 and objective == 5: # First priority: being chased by fox, undo any action and move
            rabbit['action'] = 'Moving'
            Rabbit_move()
            return None

        elif rabbit['action'] != 'None': # Second priority: there is already an action
            if rabbit['action'] == "Moving" or rabbit['action'] == "Moving1" or rabbit['action'] == "Moving2":
                Rabbit_move()
                return None
            elif rabbit['action'] == 'Drinking':
                Rabbit_drink()
                return None
            elif rabbit['action'] == 'Eating':
                Rabbit_eat()
                return None
            elif rabbit['action'] == 'Mating':
                Rabbit_mate()
                return None
            elif rabbit['action'] == 'Birth':
                Rabbit_birth()
                return None

        elif rabbit['action'] == 'None': # Third priority: no action given, make new action and does it
            if distance == 1 and self.object[rabbit['y']+nextMove[0],rabbit['x']+nextMove[1]] == 1:
                rabbit['action'] = 'Drinking'
                Rabbit_drink()
                return None
            elif distance == 1 and self.object[rabbit['y']+nextMove[0],rabbit['x']+nextMove[1]] == 2:
                rabbit['action'] = 'Eating'
                Rabbit_eat()
                return None
            elif distance == 1 and self.object[rabbit['y']+nextMove[0],rabbit['x']+nextMove[1]] == 4:
                rabbit['action'] = 'Mating'
                for i in range (0,len(data['rabbit'])):
                    if data['rabbit'][i]['y'] == rabbit['y']+nextMove[0] and data['rabbit'][i]['x'] == rabbit['x']+nextMove[1]:
                        if data['rabbit'][i]['pregnant'] == 0:
                            data['rabbit'][i]['pregnant'] += 1
                Rabbit_mate()
                return None
            else:
                if speed == 0:
                    rabbit['action'] = 'Moving2'
                    Rabbit_move()
                    return None
                elif speed == 1:
                    rabbit['action'] = 'Moving1'
                    Rabbit_move()
                    return None
        
    def Rabbit_vision(self,rabbit):
        '''
        input: rabbit object under data
        output:  a list containing a integer of rabbit speed mode and a list of next move's direction
        '''
        def Direct(direction):
            '''
            input: a list of objective's location
            output: input's value that is changed to 1 or -1 or 0
            this will just set the location, so the next move is directly adressed
            '''
            if direction[0] < 0:
                direction[0] = -1
            if direction[0] > 0:
                direction[0] = 1
            if direction[1] < 0:
                direction[1] = -1
            if direction[1] > 0:
                direction[1] = 1
            return direction
        def Go_water():
            shortest = [99,[]]
            for i in inVision[0]:
                if i[0] < shortest[0]:
                    shortest = i
            return([1,shortest[0],shortest[1],1])
        def Go_food():
            shortest = [99,[]]
            for i in inVision[1]:
                if i[0] < shortest[0]:
                    shortest = i
            return([1,shortest[0],shortest[1],2])
        def Go_rabbit():
            shortest = [99,[]]
            for i in inVision[2]:
                if i[0] < shortest[0]:
                    shortest = i
            return([2,shortest[0],shortest[1],4])

        def Roam():
            '''
            input: none
            output: a list of direction
            randomly set a direction according to the direction value
            '''
            if rabbit['direction'] == 'N':
                if uniform(0,1) <= 0.1:
                    rabbit['direction'] = choice("WE")
                return [[-1,-1],[-1,0],[-1,1]][randint(0,2)]
            elif rabbit['direction'] == 'E':
                if uniform(0,1) <= 0.1:
                    rabbit['direction'] = choice("NS")
                return [[-1,1],[0,1],[1,1]][randint(0,2)]
            elif rabbit['direction'] == 'S':
                if uniform(0,1) <= 0.1:
                    rabbit['direction'] = choice("WE")
                return [[1,-1],[1,0],[1,1]][randint(0,2)]
            elif rabbit['direction'] == 'W':
                if uniform(0,1) <= 0.1:
                    rabbit['direction'] = choice("NS")
                return [[-1,-1],[0,-1],[1,-1]][randint(0,2)]
            
        # Check if there are wall in vision range
        Ymin = rabbit['y'] - cs.visionR
        Ymax = cs.visionR - (MAX - rabbit['y'])
        Xmin = rabbit['x'] - cs.visionR
        Xmax = cs.visionR - (MAX - rabbit['x'])
        
        if Ymin > 0:
            Ymin = 0
        if Ymax <= 0:
            Ymax = 0
        if Xmin > 0:
            Xmin = 0
        if Xmax <= 0:
            Xmax = 0

        inVision = [[],[],[]] # first list for water, second for food, third for other rabbits
        for col in range (rabbit['y']-cs.visionR-Ymin, rabbit['y']+cs.visionR-Ymax):
            for row in range (rabbit['x']-cs.visionR-Xmin, rabbit['x']+cs.visionR-Xmax):
                if self.object[col,row] == 1:
                    distance = max(abs(rabbit['x']-row),abs(rabbit['y']-col))
                    direction = Direct([col - rabbit['y'], row - rabbit['x']])
                    inVision[0].append([distance,direction])
                if self.object[col,row] == 2:
                    distance = max(abs(rabbit['x']-row),abs(rabbit['y']-col))
                    direction = Direct([col - rabbit['y'], row - rabbit['x']])
                    inVision[1].append([distance,direction])
                if self.object[col,row] == 4:
                    gender = 0
                    for i in range (0,len(data['rabbit'])):
                        if data['rabbit'][i]['y'] == col and data['rabbit'][i]['x'] == row:
                            gender = data['rabbit'][i]['gender']
                            break
                    distance = max(abs(rabbit['x']-row),abs(rabbit['y']-col))
                    direction = Direct([col - rabbit['y'], row - rabbit['x']])
                    if gender == 1:
                        inVision[2].append([distance,direction,gender])
                if self.object[col,row] == 5:
                    direction = Direct([rabbit['y'] - col, rabbit['x'] - row]) #direction is opposite from the objective         
                    return (2,1,direction,5)
        if len(inVision[0]+inVision[1]+inVision[2]) == 0: # no objective found
            return ([0,-1,Roam(),0])
        
        if len(inVision[0]) != 0 and len(inVision[1]) != 0:
            if (rabbit['thirst'] < rabbit['hunger']) and rabbit['thirst'] < 70:
                return(Go_water())
            elif (rabbit['thirst'] >= rabbit['hunger']) and rabbit['hunger'] < 70:
                return(Go_food())
        if len(inVision[0]) != 0 and rabbit['thirst'] < 70:
            return(Go_water())
        elif len(inVision[1]) != 0 and rabbit['hunger'] < 70:
            return(Go_food())


        elif rabbit['gender'] == 0:
            #print("invision",inVision,len(inVision[2]))
            if len(inVision[2]) != 0:
                if rabbit['desire'] >= 40:
                    return(Go_rabbit())

        return ([0,-1,Roam(),0])

    def Fox_next(self):
        for fox in (data["fox"]):
            speed, distance, nextMove, objective = self.Fox_vision(fox)
            print([fox['y'],fox['x']],"speed",speed,"distance",distance,"next move",nextMove, "objective", objective)
            self.Fox_action(fox, speed, distance, nextMove, objective)

    def Fox_action(self, fox, speed, distance, nextMove, objective):
        def Fox_cost():
            if fox['thirst'] <= 0:
                fox['health'] -= 5
            elif fox['thirst'] > 0:
                fox['thirst'] -= 1
            if fox['hunger'] <= 0:
                fox['health'] -= 5
            elif fox['hunger'] > 0:
                fox['hunger'] -= 1
        def Correct_direction():
            if nextMove[0] == 0 or nextMove[1] == 0:
                if nextMove == [0,1]:
                    fox['direction'] = "E"
                elif nextMove == [1,0]:
                    fox['direction'] = "S"
                elif nextMove == [0,-1]:
                    fox['direction'] = "W"
                elif nextMove == [-1,0]:
                    fox['direction'] = "N"
            else:
                if nextMove == [1,1]:
                    fox['direction'] = choice("ES")
                elif nextMove == [-1,-1]:
                    fox['direction'] = choice("NW")
                elif nextMove == [1,-1]:
                    fox['direction'] = choice("SW")
                elif nextMove == [-1,-1]:
                    fox['direction'] = choice("NE")

        def Move_adjust(nextMove):
            '''
            input: none
            output: none
            If the nextMove is not movable, consider the adjasent one, loop till the chosen one is movable
            '''
            print
            if (0 > fox['y']+nextMove[0] or fox['y']+nextMove[0] > 29) and (0 > fox['x']+nextMove[1] or fox['x']+nextMove[1] > 29):
                nextMove[0] = nextMove[0]*-1
                nextMove[1] = nextMove[1]*-1
                nextMove[choice([0,1])] = 0
                Correct_direction()

            elif 0 > fox['y']+nextMove[0] or fox['y']+nextMove[0] > 29 or 0 > fox['x']+nextMove[1] or fox['x']+nextMove[1] > 29:
                if nextMove == [-1,0]:
                    nextMove = choice([[0,1],[0,-1]])
                elif nextMove == [0,-1]:
                    nextMove = choice([[1,0],[-1,0]])
                elif nextMove == [1,0]:
                    nextMove = choice([[0,1],[0,-1]])
                elif nextMove == [0,1]:
                    nextMove = choice([[1,0],[-1,0]])
                Correct_direction()

            if self.object[fox['y']+nextMove[0],fox['x']+nextMove[1]] == 0:
                return True

            elif self.object[fox['y']+nextMove[0],fox['x']+nextMove[1]] != 0:
                if nextMove[0] == 0:
                    nextMove[0] = choice([-1,1])
                    if 0 > fox['y']+nextMove[0] or fox['y']+nextMove[0] > 29 or 0 > fox['x']+nextMove[1] or fox['x']+nextMove[1] > 29:
                        Correct_direction()
                        return True
                elif nextMove[1] == 0:
                    nextMove[1] = choice([-1,1])
                    if 0 > fox['y']+nextMove[0] or fox['y']+nextMove[0] > 29 or 0 > fox['x']+nextMove[1] or fox['x']+nextMove[1] > 29:
                        Correct_direction()
                    return True
                else:
                    nextMove[choice([0,1])] = 0
                    if 0 > fox['y']+nextMove[0] or fox['y']+nextMove[0] > 29 or 0 > fox['x']+nextMove[1] or fox['x']+nextMove[1] > 29:
                        Correct_direction()
                    return True
            return False

            
        def Fox_move():
            if fox['action'] == "Moving2":
                fox['thirst'] += 1
                fox['hunger'] += 1
                fox['action'] = "Moving1"
            elif fox['action'] == "Moving1":
                fox['thirst'] += 1
                fox['hunger'] += 1
                fox['action'] = "Moving"
            elif fox['action'] == "Moving":
                fox['action'] = "None"
                movable = Move_adjust(nextMove)
                if not movable:
                    return None
                self.object[fox['y'],fox['x']] = 0
                fox['y'] = fox['y'] + nextMove[0]
                fox['x'] = fox['x'] + nextMove[1]            
                self.object[fox['y'],fox['x']] = 5
        def Fox_drink():
            fox['thirst'] += 5
            if fox['thirst'] >= 100:
                fox['action'] = 'None'
        def Fox_meat():
            for i in range (0,len(data['meat'])):
                if data['meat'][i]['y'] == fox['y']+nextMove[0] and data['meat'][i]['x'] == fox['x']+nextMove[1]:
                    data['meat'][i]['health'] -= 5
            fox['hunger'] += 5

            if fox['hunger'] >= 100:
                fox['action'] = 'None'
        def Fox_hunt():
            for i in range (0,len(data['rabbit'])):
                if data['rabbit'][i]['y'] == fox['y']+nextMove[0] and data['rabbit'][i]['x'] == fox['x']+nextMove[1]:
                    data['rabbit'][i]['health'] -= 100
        '''        
        def Rabbit_mate():
            if rabbit['desire'] <= 0:
                rabbit['action'] = 'None'
            rabbit['desire'] -= 100
        def Rabbit_birth():
            rabbit['pregnant'] -= randint(15,30)
            Move_adjust()
            self.object[rabbit['y']+nextMove[0],rabbit['x']+nextMove[1]] = 4
            self.Data_save_rabbit(rabbit['y']+nextMove[0],rabbit['x']+nextMove[1],100,choice([0,1]),0,"Moving")
                
            if rabbit['pregnant'] <= 0:
                rabbit['pregnant'] = 0
                rabbit['action'] = 'None'
        '''

        def Status_check(fox):
            fox['age'] += 1 # Age is relative to the number of turns
            if fox['gender'] == 1: 
                if fox['pregnant'] >= 1 and fox['pregnant'] < 100:
                    fox['pregnant'] += 5
                elif fox['pregnant'] >= 100:
                    fox['action'] = "Birth"
            elif fox['gender'] == 0:
                fox['desire'] += 1

        Status_check(fox)
        
        if fox['action'] != "Moving1" or fox['action'] != "Moving2":
            Fox_cost()


        if fox['action'] != 'None': # First priority: there is already an action
            if fox['action'] == "Moving" or fox['action'] == "Moving1" or fox['action'] == "Moving2":
                Fox_move()
                return None
            elif fox['action'] == 'Drinking':
                Fox_drink()
                return None
            elif fox['action'] == 'Eating':
                Fox_meat()
                return None
            '''
            elif fox['action'] == 'Mating':
                Rabbit_mate()
                return None
            elif fox['action'] == 'Birth':
                Rabbit_birth()
                return None
            '''

        elif fox['action'] == 'None': # Second priority: no action given, make new action and does it
            if distance == 1 and self.object[fox['y']+nextMove[0],fox['x']+nextMove[1]] == 1:
                fox['action'] = 'Drinking'
                Fox_drink()
                return None
            elif distance == 1 and self.object[fox['y']+nextMove[0],fox['x']+nextMove[1]] == 3:
                fox['action'] = 'Eating'
                Fox_meat()
                return None
            elif distance == 1 and self.object[fox['y']+nextMove[0],fox['x']+nextMove[1]] == 4:
                Fox_hunt()
            elif objective == 4 and speed == 2:
                fox['action'] = 'Moving'
                Fox_move()
            else:
                if speed == 0:
                    fox['action'] = 'Moving2'
                    Fox_move()
                    return None
                elif speed == 1:
                    fox['action'] = 'Moving1'
                    Fox_move()
                    return None
            '''
            elif distance == 1 and self.object[rabbit['y']+nextMove[0],rabbit['x']+nextMove[1]] == 4:
                rabbit['action'] = 'Mating'
                for i in range (0,len(data['rabbit'])):
                    if data['rabbit'][i]['y'] == rabbit['y']+nextMove[0] and data['rabbit'][i]['x'] == rabbit['x']+nextMove[1]:
                        if data['rabbit'][i]['pregnant'] == 0:
                            data['rabbit'][i]['pregnant'] += 1
                Rabbit_mate()
                return None
            '''
            

    def Fox_vision(self,fox):
        '''
        input: fox object under data
        output:  a list containing necessary information for next move
        '''
        def Direct(direction):
            '''
            input: a list of objective's location
            output: input's value that is changed to 1 or -1 or 0
            this will just set the location, so the next move is directly adressed
            '''
            if direction[0] < 0:
                direction[0] = -1
            if direction[0] > 0:
                direction[0] = 1
            if direction[1] < 0:
                direction[1] = -1
            if direction[1] > 0:
                direction[1] = 1
            return direction
        def Go_water():
            shortest = [99,[]]
            for i in inVision[0]:
                if i[0] < shortest[0]:
                    shortest = i
            return([1,shortest[0],shortest[1],1])
        def Go_meat():
            shortest = [99,[]]
            for i in inVision[1]:
                if i[0] < shortest[0]:
                    shortest = i
            return([1,shortest[0],shortest[1],3])
        
        def Go_hunt():
            shortest = [99,[]]
            for i in inVision[2]:
                if i[0] < shortest[0]:
                    shortest = i
            return([2,shortest[0],shortest[1],4])
        def Go_fox():
            shortest = [99,[]]
            for i in inVision[2]:
                if i[0] < shortest[0]:
                    shortest = i
            return([2,shortest[0],shortest[1],5])
        def Roam():
            '''
            input: none
            output: a list of direction
            randomly set a direction according to the direction value
            '''
            if fox['direction'] == 'N':
                if uniform(0,1) <= 0.1:
                    fox['direction'] = choice("WE")
                return [[-1,-1],[-1,0],[-1,1]][randint(0,2)]
            elif fox['direction'] == 'E':
                if uniform(0,1) <= 0.1:
                    fox['direction'] = choice("NS")
                return [[-1,1],[0,1],[1,1]][randint(0,2)]
            elif fox['direction'] == 'S':
                if uniform(0,1) <= 0.1:
                    fox['direction'] = choice("WE")
                return [[1,-1],[1,0],[1,1]][randint(0,2)]
            elif fox['direction'] == 'W':
                if uniform(0,1) <= 0.1:
                    fox['direction'] = choice("NS")
                return [[-1,-1],[0,-1],[1,-1]][randint(0,2)]
            
        # Check if there are wall in vision range
        Ymin = fox['y'] - cs.visionF
        Ymax = cs.visionF - (MAX - fox['y'])
        Xmin = fox['x'] - cs.visionF
        Xmax = cs.visionF - (MAX - fox['x'])
        
        if Ymin > 0:
            Ymin = 0
        if Ymax <= 0:
            Ymax = 0
        if Xmin > 0:
            Xmin = 0
        if Xmax <= 0:
            Xmax = 0

        inVision = [[],[],[],[]] # first list for water, second for meat, third for rabbit, forth for other foxes
        for col in range (fox['y']-cs.visionF-Ymin, fox['y']+cs.visionF-Ymax):
            for row in range (fox['x']-cs.visionF-Xmin, fox['x']+cs.visionF-Xmax):
                if self.object[col,row] == 1:
                    distance = max(abs(fox['x']-row),abs(fox['y']-col))
                    direction = Direct([col - fox['y'], row - fox['x']])
                    inVision[0].append([distance,direction])
                if self.object[col,row] == 3:
                    distance = max(abs(fox['x']-row),abs(fox['y']-col))
                    direction = Direct([col - fox['y'], row - fox['x']])
                    inVision[1].append([distance,direction])
                if self.object[col,row] == 4:
                    distance = max(abs(fox['x']-row),abs(fox['y']-col))
                    direction = Direct([col - fox['y'], row - fox['x']])
                    inVision[2].append([distance,direction])
                if self.object[col,row] == 5:
                    gender = 0
                    for i in range (0,len(data['fox'])):
                        if data['fox'][i]['y'] == col and data['fox'][i]['x'] == row:
                            gender = data['fox'][i]['gender']
                            break
                    distance = max(abs(fox['x']-row),abs(fox['y']-col))
                    direction = Direct([col - fox['y'], row - fox['x']])
                    if gender == 1:
                        inVision[3].append([distance,direction,gender])


        if len(inVision[0]+inVision[1]+inVision[2]+inVision[3]) == 0: # no objective found
            return ([0,-1,Roam(),0])
        
        if len(inVision[0]) != 0 and (len(inVision[1]) != 0 or len(inVision[2]) != 0):
            if (fox['thirst'] < fox['hunger']) and fox['thirst'] < 70:
                return(Go_water())
            elif (fox['thirst'] >= fox['hunger']) and fox['hunger'] < 70:
                if len(inVision[1]) != 0:
                    return(Go_meat())
                else:
                    return(Go_hunt())

        if len(inVision[0]) != 0 and fox['thirst'] < 70:
            return(Go_water())
        elif len(inVision[1]) != 0 and fox['hunger'] < 70:
            return(Go_meat())
        elif len(inVision[2]) != 0 and fox['hunger'] < 70:
            return(Go_hunt())
        '''
        elif fox['gender'] == 0:
            #print("invision",inVision,len(inVision[3]))
            if len(inVision[3]) != 0:
                if fox['desire'] >= 40:
                    return(Go_fox())
        '''

        return ([0,-1,Roam(),0])

    def Save_file(self):
        with open('{}\\data.json'.format(dirname), 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def Data_save_carrot(self,x,y,health):
        global data
        data['carrot'].append({
            'x': x,
            'y': y,
            'health': health
        })

    def Data_save_rabbit(self,x,y,health,gender,age,action): # gender 0 represents male, 1 for female, age is relative value parallel to the turn, 20 below status will be young, 200 above will be elder
        '''
        input: rabit's data
        output: none
        writes the necessray data into the json file
        '''
        global data # hunger and thirst the maximum value is 100, any of two reaches zero, health starts to decrease
            
        if gender == 0 and age == 0:
            data['rabbit'].append({
            'x': x,
            'y': y,
            'health': health,
            'gender': gender,
            'age': age,
            'hunger': 49,
            'thirst': 50,
            'direction': choice('NEWS'),
            'action': action,
            'desire': randint(-50,-30)
        })

        elif gender == 0:
            data['rabbit'].append({
            'x': x,
            'y': y,
            'health': health,
            'gender': gender,
            'age': age,
            'hunger': 49,
            'thirst': 50,
            'direction': choice('NEWS'),
            'action': action,
            'desire': randint(0,30)
        })
        elif gender == 1: 
            data['rabbit'].append({
            'x': x,
            'y': y,
            'health': health,
            'gender': gender,
            'age': age,
            'hunger': 49,
            'thirst': 50,
            'direction': choice('NEWS'),
            'action': action,
            'pregnant': 0
        })


    def Data_save_meat(self,x,y,health):
        global data
        data['meat'].append({
            'x': x,
            'y': y,
            'health': health
        })

    def Data_save_fox(self,x,y,health,gender,age,action):
        global data
        if gender == 0:
            data['fox'].append({
            'x': x,
            'y': y,
            'health': health,
            'gender': gender,
            'age': age,
            'hunger': 49,
            'thirst': 50,
            'direction': choice('NEWS'),
            'action': action,
            'desire': randint(-40,-10)
        })
        elif gender == 1: 
            data['fox'].append({
            'x': x,
            'y': y,
            'health': health,
            'gender': gender,
            'age': age,
            'hunger': 49,
            'thirst': 50,
            'direction': choice('NEWS'),
            'action': action,
            'pregnant': 0
        })

    def Spawn_carrot(self):
        ranX = randint(0,29) # Generate a random number that is not taken and spawn a plant, the plant value is 2
        ranY = randint(0,29)   
        while self.object[ranY,ranX] != 0: # while the location is not null
            ranX = randint(0,29)
            ranY = randint(0,29)
        
        self.object[ranY,ranX] = 2
        self.Data_save_carrot(ranX,ranY,100)

    def Spawn_rabbit(self):
        ranX = randint(0,29) # Generate a random number that is not taken and spawn a plant, the plant value is 2
        ranY = randint(0,29)  
        while self.object[ranY,ranX] != 0: # while the location is not null
            ranX = randint(0,29)
            ranY = randint(0,29)
            

        self.object[ranY,ranX] = 4
        self.Data_save_rabbit(ranX,ranY,100,randint(0,1),10,"None")

    def Spawn_fox(self):
        ranX = randint(0,29)
        ranY = randint(0,29)
        while self.object[ranY,ranX] != 0:
            ranX = randint(0,29)
            ranY = randint(0,29)
        
        self.object[ranY,ranX] = 5
        self.Data_save_fox(ranX,ranY,100,randint(0,1),10,"None")


ob = empty([30,30], dtype=int)
for col in range (0,30):
    for row in range (0,30):
        ob[col,row] = 0

for col in range(0,30):
    for row in range(0,30):
        if cs.mapValues[col,row] == 0 or cs.mapValues[col,row] == 1 or cs.mapValues[col,row] == 2 or cs.mapValues[col,row] == 3:
            ob[col,row] = 1

set_printoptions(threshold=inf,linewidth=250)
main = Game(ob)