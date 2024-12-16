
import numpy as np
from sub import *

player_ex='player1'
player_2ex='player2'

def test_boards():
    game = Submarine(player_ex, player_2ex, row_num=5)
    assert type(game.player1) == np.ndarray and type(game.player2) == np.ndarray #testing type of boards
    assert game.row_num>3 and game.col_num>3 and game.levels==3 #testing sizes of dimensions
    assert np.shape(game.player1) == (game.levels, game.row_num, game.col_num) #testing dimensions of the board
    assert np.shape(game.player2) == (game.levels, game.row_num, game.col_num)

def test_insert_units():
    game = Submarine(player_ex, player_2ex, row_num=5)
    type_of_unit = random.choice(list(UnitTypes))
    ori_options= np.arange(len(UNIT_SHAPES[type_of_unit]))
    orientation = random.choice(ori_options)
    row=0
    col=0
    if type_of_unit == UnitTypes.GENERAL: #if the chosen unitType is general, an error will be raised
        return
    else:
        board, unit_list, unit_name =game.insert_unit(player_ex, type_of_unit, row,col,orientation)        
        assert unit_list[-1] == f"{type_of_unit.name}1" and unit_name == f"{type_of_unit.name}{len(unit_list)}" #asserting that the last unit in list is the unit we created
        assert np.count_nonzero(board == unit_name) == np.count_nonzero(UNIT_SHAPES[type_of_unit][orientation]) #asserting the time of incidants of the unit in the board
    
def is_list_correct():
    game = Submarine(player_ex, player_2ex, row_num=5)
    players_board, unit_list=game.random_insertion(player_2ex)
    assert set(unit_list) ==  set(np.unique(players_board[players_board != 0])) #making sure all the units on the board also appear in the list
    flattened_board = players_board.flatten() #making all the board one list of all the coordinates
    assert all(isinstance(value, (int, str)) for value in flattened_board) #checks if the entire board is build of integers and strings only
    
def unit_count():
        game = Submarine(player_ex, player_2ex, row_num=6, col_num=7)
        pl1_board, pl1_unit_list=game.random_insertion(player_ex)
        pl2_board, _=game.random_insertion(player_2ex)
        players = [pl1_board, pl2_board]

        for player_board in players:
            count_list=[]
            for unit in pl1_unit_list:
                count = np.count_nonzero(player_board == unit)
                count_list.append(count)
            assert count_list == [1,3,3,4,4,6,6] #counting correct amount of unit incidents for each player
            


#def is_board_correct():
 #   game = Submarine(player_ex, player_2ex, row_num=5)
  #  players_board, unit_list=game.random_insertion(player_ex)     
   # game.insert_unit(player_ex, UnitTypes.DESTROYER, 2, 2, 1)

    # Assert units are inserted at the correct positions




test_boards()
test_insert_units()
is_list_correct()
unit_count()

