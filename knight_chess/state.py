import numpy as np
from .action import Action
from copy import deepcopy

WHITE = 1
BLACK = 2

# Knights positions:

# + 4 + 3 +
# 5 + + + 2
# + + C + +
# 6 + + + 1
# + 7 + 0 +

MOVEMENTS = {
    0: (2, 1),
    1: (1, 2),
    2: (-1, 2),
    3: (-2, 1),
    4: (-2, -1),
    5: (-1, -2),
    6: (1, -2),
    7: (2, -1),
}


class State:

    def __init__(self, knight_dict):
        self.my_knights = knight_dict.get('my_knights_dict')
        self.enemy_knights = knight_dict.get('enemy_knights_dict')
        self.my_id = int(int(list(self.my_knights.keys())[0])/100)
        self.isMax = True
        # 8x8 matrix, using float reads null as nan integer comparison is still
        # possible
        self.board = np.array(knight_dict.get('ids'), dtype=float)

    def transition(self, action: Action):
        # Copia del estado actual
        new_state = deepcopy(self)

        # identificacion de casilla actual y objetivo
        start, end = self.get_movement_positions(action)

        # identifica el elemento que se encuentra en la casilla objetivo
        if not np.isnan(new_state.board[start]):
            element = str(int(new_state.board[start]))
            self.my_knights[element] = list(end)
        else:
            element = np.nan

        new_state.board[start] = np.nan

        end_element = new_state.board[end]

        # Remueve elemento de la lista si es que existe
        if end_element in self.enemy_knights.keys():
            new_state.enemy_knights.pop(element)
        elif end_element in self.my_knights.keys():
            new_state.my_knights.pop(element)

        new_state.board[end] = action.knight_id
        return new_state

    def get_movement_positions(self, action):
        movement = MOVEMENTS.get(action.knight_movement)
        if int(action.knight_id/100) == self.my_id:
            position = self.my_knights.get(str(action.knight_id))
        else:
            position = self.enemy_knights.get(str(action.knight_id))
        row, col = position[1], position[0]
        new_row, new_col = row + movement[0], col + movement[1]

        return (row, col), (new_row, new_col)

    def is_valid_action(self, action):
        # identificacion de casilla actual y objetivo
        player_id = int(action.knight_id/100)
        # Esto no deberia ocurrir, por eso es excepcion
        if player_id == self.my_id:
            if self.my_knights.get(str(action.knight_id)) is None:
                raise ValueError(f'Knight {action.knight_id} not in board')
        else:
            if self.enemy_knights.get(str(action.knight_id)) is None:
                raise ValueError(f'Knight {action.knight_id} not in board')

        # Validacion de accion
        start, end = self.get_movement_positions(action)
        shape = self.board.shape
        if end[0] < 0 or end[1] < 0:
            return False
        if end[0] >= shape[0] or end[1] >= shape[1]:
            return False
        if (not np.isnan(self.board[end])) and int(self.board[end]/100) == player_id:
            return False

        return True

    def is_final(self):
        lose = len(self.my_knights) == 0
        win = len(self.enemy_knights) == 0

        # Retornando resultado de estado final
        return lose or win

    def value(self):
        value = 200
        if self.my_id == 1:
            enemy_id = 2.0
        else:
            enemy_id = 1.0
        # Estados mejores:
        #   Cuando enemy knights sea menor al estado
        value -= (len(self.enemy_knights))
        #   Cuando my caballo no puede comido por otro
        for pos in self.my_knights.values():
            for i in MOVEMENTS.values():
                x = i[0] + pos[0] 
                y = i[1] + pos[1]
                if x<0 or x>=self.board.shape[0] or y<0 or y>=self.board.shape[1]:
                    #print("out of border")
                    continue
                
                if not np.isnan(self.board[(x,y)]):
                    if int(self.board[(x,y)]/100) == enemy_id:
                        value-=1 

        #   avanzar > retroceder
        #   lure
        #   mejor supervivencia de nuetros caballos
        return value


    def get_actions(self, player=None):
        
        if player is None:
            player = self.my_id
        
        if self.my_id == player:
            ids = self.my_knights.keys()
        else:
            ids = self.enemy_knights.keys()
        
        """
        if self.isMax:
            ids = self.my_knights.keys()
        else:
            ids = self.enemy_knights.keys()
        # 0 1 6 7 bajan
        # 4 5 2 3 suben
        if my_id==1: # baja
            movements = [0,1,6,7]
        else:
            movements = [2,3,4,5]
        """

        valid_actions = []
        actions = []
        size = len(MOVEMENTS)

        for _ in ids:
            actions += map(self.create_action, [_]*size, MOVEMENTS.keys())

        for action in actions:
            if self.is_valid_action(action):
                valid_actions.append(action)
        # Seleccionar los caballos que estan mas adelante
        # Buscar hasta que se coma a un caballo enemigo

        return valid_actions

    def create_action(self, knight_id, movement):
        return Action(knight_id, movement)

    def __lt__(self, other):
        return self.value() < other.value()
        pass
