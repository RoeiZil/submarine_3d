from enum import Enum
import numpy as np
import random



class UnitTypes(Enum):
    SUBMARINE = 1
    DESTROYER = 2
    JET = 3
    GENERAL=4

class Signal(Enum):
    MISS = 1
    HIT = 2
    KILL = 3
    END = 4

    
jet_shape_1 = np.array([[0, 0, 1, 0],
                        [1, 1, 1, 1],
                        [0, 0, 1, 0]])

jet_shape_2 = np.array([[0, 1, 0],
                        [0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]])

jet_shape_3 = np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0],
                        [0, 1, 0]])

jet_shape_4 = np.array([[0, 1, 0, 0],
                        [1, 1, 1, 1],
                        [0, 1, 0, 0]])


 
UNIT_SHAPES = {
    UnitTypes.GENERAL: np.ones((1, 1)),
    UnitTypes.SUBMARINE: [np.ones((1, 3)), np.ones((3, 1))],
    UnitTypes.DESTROYER: [np.ones((1, 4)) , np.ones((4,1))],
    UnitTypes.JET: [jet_shape_1, jet_shape_2, jet_shape_3, jet_shape_4]
}
    
#for orientation in UNIT_SHAPES[UnitTypes.SUBMARINE]:
 #   print(orientation)
  #  print()   
    
    
class Submarine:
    def __init__(self, player1_name: str, player2_name: str, col_num=6, row_num=5, levels=3) -> None:
        #self.board_size=x, y , z
        self.row_num=row_num
        self.col_num=col_num
        self.levels=levels
        if levels!=3:
            print("dimensions are incorrect")
        self.board = np.full((self.levels, self.row_num, self.col_num), 0, dtype=object) #to be able to change zeros to strs
        self.player1_units=[] #creates a unit list for each player
        self.player2_units=[]
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1 = self.board.copy().astype(object)  # Board for player 1
        self.player2 = self.board.copy().astype(object)  # Board for player 2
        self.headlines = ['Deep', 'Sea', 'Air']

    
    #function to insert a specific unit to the board
    def insert_unit(self, player: str, unit_type: UnitTypes, row: int, col: int, orientation: int = 0):
         
        #which player and list to add the unit to
        if player == self.player1_name:
            board = self.player1
            unit_list=self.player1_units
        elif player == self.player2_name:
            board = self.player2
            unit_list=self.player2_units
        else:
            print(f"Invalid player name: {player}")
            return
                          
        shape = UNIT_SHAPES[unit_type][orientation]        
        # Check if the general can fit at the specified position and puts it in the correct board        
        if unit_type == UnitTypes.GENERAL:            
            raise ValueError("Cannot insert another General to the board.")
        elif unit_type == UnitTypes.JET or unit_type == UnitTypes.DESTROYER or unit_type == UnitTypes.SUBMARINE: #for any other type of unit
            shape_height, shape_width = shape.shape #depends on the orientation we chose

            for i in range(shape_height): #this loop checks if the new unit will overlap with an existing one for each point
                for j in range(shape_width):
                    if shape[i,j]==1 and board[unit_type.value - 1, row + i, col + j] != 0: #the loop is neccesary especially for the jets
                        raise ValueError("Cannot insert unit. Overlapping with another unit.")
            else:                
                if row + shape_height <= self.row_num and col + shape_width <= self.col_num: #checks for exceeding boundaries
                    unit_name = f"{unit_type.name}{len(unit_list)+1}"
                    unit_list.append(unit_name) #adds name of unit with its number in the player's list    
                    for i in range(shape_height): #loop for puting unit's name at each point (row and column)
                        for j in range(shape_width): #this loop comes to make sure that when puting a new jets, the shapes zeros do not delete previews inserted jets
                            if shape[i, j] == 1 and board[unit_type.value - 1, row + i, col + j] != 1: #only values of 1 indicating a unit will replace a zero
                                board[unit_type.value - 1, row + i, col + j] = unit_list[-1] #giving each spot the name of the unit from the list
                
                    return board,unit_list, unit_name #returning board, updated unit list and name of new unit
                else:
                    raise ValueError("Cannot insert unit at the specified position. The shape exceeds the board boundaries.")
        else: 
            raise ValueError("Wrong unit name.") #if the name given as unit_type is not part of the UnitType enum



    #this is the automatic insertion of all units in both boards, depanding on the unit amount set for each level    
    def random_insertion(self, player: str,unit_amount=(2,2,2)):
        self.unit_amount=unit_amount
                #which player and list to add the unit to
        if player == self.player1_name: 
            board = self.player1
            unit_list=self.player1_units
            print(f"{player} is player 1")
        elif player == self.player2_name:
            board = self.player2
            unit_list=self.player2_units
            print(f"{player} is player 2")
        else:
            print(f"wrong player's name")
            return
               
        #adding general to board:
        
        unit_list.append(f"{UnitTypes(4).name}1")
        board[random.choice(range(self.levels)), random.choice(range(self.row_num)), random.choice(range(self.col_num))] = 'GENERAL1'

        #adding the units one by one:       
        for level, amount in enumerate(self.unit_amount): #for amount of units in each level
            for unit in range(amount): #go over each unit in the amount of each level
                #print(UnitTypes(level+1).name)
                unit_name=UnitTypes(level+1).name
                unit_list.append(f"{unit_name}{len(unit_list)+1}") #adds name of unit with its number in the player's list
                

                attempt_count = 0
                while True:  # Continue looping until a valid shape is found
                    attempt_count += 1
                    if attempt_count>400: #random number to show that the loop of finding space for units doesnt find space anymore on board
                        raise ValueError("No space available for unit shapes.")
                        
                    shape = random.choice(UNIT_SHAPES[UnitTypes(level+1)])
                    shape_height, shape_width = shape.shape
                    
                    row= random.choice(range(self.row_num))
                    col = random.choice(range(self.col_num))
                    valid_shape = True  # Variable to track if the shape is valid0
                    if row + shape_height > self.row_num or col + shape_width > self.col_num:
                        valid_shape = False
                        continue
                    else:                        
                        for i in range(shape_height): #this loop checks if the new unit will overlap with an existing one for each point
                            for j in range(shape_width):
                                if shape[i,j]==1 and board[level, row+i, col+j] != 0: #the loop is neccesary especially for the jets
                                    valid_shape = False  # Set the shape as invalid if overlapping is found
                                    break
                            if not valid_shape:
                                break
                            
                    if valid_shape:
                        # if row + shape_height <= self.col_num and col + shape_width <= self.row_num:
                        for i in range(shape_height):
                            for j in range(shape_width): #this loop comes to make sure that when puting a new jets, the shapes zeros do not delete previews inserted jets
                                if shape[i, j] == 1 and board[level, row + i, col + j] != 1: #only values of 1 indicating a unit will replace a zero
                                    board[level, row + i, col + j] = unit_list[-1] #giving each spot the name of the nuit        
                        break
                    
   
        return board, unit_list    #returning the board and list after they are filled                     

                    
    def print_board(self, player: str):
        if player == self.player1_name:
            print("\n", player,"'s board:\n\n Deep:\n", self.player1[0],"\n\nSea:\n", self.player1[1], "\n\nAir:\n", self.player1[2])
        elif player == self.player2_name:
            print("\n", player,"'s board:\n\n Deep:\n", self.player2[0],"\n\nSea:\n", self.player2[1], "\n\nAir:\n", self.player2[2])
        else:
            print(f"Invalid player name: {player}")
            return
        
    def print_list(self, player: str):
            if player == self.player1_name:
                print("\n", player,"'s unit list:\n", self.player1_units)
            elif player == self.player2_name:
                print("\n", player,"'s unit list:\n", self.player2_units)
            else:
                print(f"Invalid player name: {player}")
                return           

     
#this is the game:    
    def start_playing(self):
        game_over = False 
        turn_num=1   
        
        while not game_over:
         
            if turn_num % 2 != 0: #gives player 1 the turn for all odd number of turns
                player = self.player1_name #chooses whos board is being attacked, depends on the player who is playing
                targeted_player=self.player2
                targeted_list=self.player2_units
            elif turn_num % 2 == 0: #gives player 1 the turn for all even number of turns
                player = self.player2_name
                targeted_player=self.player1
                targeted_list=self.player1_units
            else:
                    print("wrong player name. Please enter a correct name to start playing the game.")
                    return 
            
            turn_num +=1 #the next turn will go to the other player
                                                
            print("\n", player,", what is the coordinate you're targeting (x, y, z)?")
            coordinates = input(">? ").split(",")
            if coordinates == ['quit']: #all type of valid inputs that are not coordinates
                print("game is over.")
                game_over = True
                return
            elif coordinates == ['show']: 
                self.print_board(player)
                turn_num -= 1 #this comes to make sure that the turn will not go to the other player
                continue
            elif coordinates == ['show_list']:
                self.print_list(player)
                turn_num -= 1 #this comes to make sure that the turn will not go to the other player
                continue
            elif len(coordinates) != 3:
                print("Invalid number of coordinates. Please enter three comma-separated values.")
                turn_num -= 1 #this comes to make sure that the turn will not go to the other player                
                continue


                                
            try:
               #len(coordinates) != 3 #see if there are exactly three integers in input
                x = int(coordinates[0].strip("(")) #if put in paranthesis, removes paranthesis
                y = int(coordinates[1].strip())
                z = int(coordinates[2].strip(")")) #if put in paranthesis, removes paranthesis
            except:
                print("Invalid coordinate values. Please enter numeric values for x, y, and z.")
                turn_num -= 1 #this comes to make sure that the turn will not go to the other player
                continue 
            

            if y>self.col_num-1 or x>self.row_num-1 or z>self.levels-1: #pay attention to difference between self.col_num and input x
                print("Invalid coordinate values. Please enter correct values for x, y, and z.")
                turn_num -= 1 #this comes to make sure that the turn will not go to the other player
                
            else: #Only in case that the coordinates are valid for the game            
                
                if targeted_player[z,x,y]==0: #if there is no unit in the attacked spot
                    print(Signal.MISS)
                    continue
                    
                elif targeted_player[z,x,y] != 0: #in case there is a unit in the attacked spot
                    if "GENERAL" in (targeted_player[z,x,y]): #if hitting the general, the game is over
                        print(Signal.END)
                        print(f"The game is over! The enemy's general is dead. The winner is {player}")
                        game_over = True #When the game is over
                        return
                
                    else:                
                        if z==0 or z==2: #in case of targeting jets or submarines
                            print(Signal.KILL)
                            name=targeted_player[z,x,y]
                            unit_where= targeted_player == targeted_player[z,x,y]
                            targeted_player[unit_where]=0
                            targeted_list.remove(name)
                                
                        if z==1: #in case of hitting a destroyer
                            name = targeted_player[z,x,y] #finds name of destroyer
                            targeted_player[z,x,y] = 0 #changing only the specific spot to zero
                            if np.any(targeted_player == name): #if there are still more spots of the specific destroyer on board
                                print(Signal.HIT)
                            else:
                                print(Signal.KILL) #if all the spots of the destroyer were hit, then the destroyer is gone
                                targeted_list.remove(name)

                            
                if len(targeted_list) == 1:
                    print(Signal.END) #if the list of units has only one unit left (meaning its the general), then the game is over
                    print(f"The game is over! The winner is {player}")
                    game_over = True
                else:
                    #print(targeted_list)
                    continue
            
            
            if not game_over: #game continues as long as game_over is not changed to true
                continue                     
    
            


        

game= Submarine(col_num=6,row_num=5, player1_name='Zvi', player2_name='Gal')  
Zvi_board, Zvi_list = game.random_insertion('Zvi')
Gal_board,Gal_list = game.random_insertion('Gal', unit_amount=(2,2,2))

#game.start_playing()


#game.insert_unit(game.player1_name, UnitTypes.SUBMARINE, 1,0)
#game.insert_unit(game.player1_name, UnitTypes.JET, 2, 1)

#game.insert_unit("player2", UnitTypes.SUBMARINE, 1, 1 ,orientation=1)
#game.insert_unit("player2", UnitTypes.DESTROYER, 0, 0)







