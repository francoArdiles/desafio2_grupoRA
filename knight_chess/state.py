from typing import List, Tuple, Dict
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
    0: (1, 2),
    1: (2, 1),
    2: (2, -1),
    3: (1, 2),
    4: (-1, 2),
    5: (-2, 1),
    6: (-2, -1),
    7: (-1, -2),
}

class State:

    my_knights: Dict[str, Tuple[int, int]]
    enemy_knight: Dict[str, Tuple[int, int]]
    isMax: bool

    board: List[List]

    def __init__(self, knight_dict):
        self.my_knights = knight_dict.get('my_knights_dict')
        self.enemy_knights = knight_dict.get('enemy_knights_dict')
        self.my_id = int(int(list(self.my_knights.keys())[0])/100)
        self.isMax = True
        # 8x8 matrix, using float reads null as nan integer comparison is still
        # possible
        self.board = knight_dict.get('ids')

    def print_state(self):
        # Este print es feo, pero funciona... no lo cuestionen
        print("State: ")
        print('\n'.join([''.join(['{:5}'.format("    ." if item is None \
            else item) for item in row]) for row in self.board]))

    def transition(self, action: Action):
        # Copia del estado actual
        new_state = deepcopy(self)

        # identificacion de casilla actual y objetivo
        start, end = self.get_movement_positions(action)
        x, y = start
        nx, ny = end

        # identifica el elemento que se encuentra en la casilla objetivo
        id_a_mover = self.board[y][x]
        id_objetivo = self.board[ny][nx]

        new_state.board[y][x] = None

        # Remueve elemento de la lista si es que existe
        if str(id_objetivo) in self.enemy_knights.keys():
            new_state.enemy_knights.pop(str(id_objetivo))
        elif str(id_objetivo) in self.my_knights.keys():
            new_state.my_knights.pop(str(id_objetivo))

        if id_a_mover in self.enemy_knights.keys():
            new_state.enemy_knights[id_a_mover] = [nx, ny]
        elif id_a_mover in self.my_knights.keys():
            new_state.my_knights[id_a_mover] = [nx, ny]

        new_state.board[ny][nx] = id_a_mover
        return new_state

    def get_movement_positions(self, action):
        if action.knight_id in self.enemy_knights.keys():
            pos = self.enemy_knights[action.knight_id]
        elif action.knight_id in self.my_knights.keys():
            pos = self.my_knights[action.knight_id]

        movement_number = action.knight_movement
        nx, ny = pos
        if movement_number == 0:
            nx += 1
            ny += 2
        elif movement_number == 1:
            nx += 2
            ny += 1
        elif movement_number == 2:
            nx += 2
            ny += -1
        elif movement_number == 3:
            nx += 1
            ny += -2
        elif movement_number == 4:
            nx += -1
            ny += -2
        elif movement_number == 5:
            nx += -2
            ny += -1
        elif movement_number == 6:
            nx += -2
            ny += 1
        elif movement_number == 7:
            nx += -1
            ny += 2
        else:
            print("Error: Movimiento no encontrado")
        return (pos[0], pos[1]), (nx, ny)

    def is_valid_action(self, action):
        # identificacion de casilla actual y objetivo
        player_id = int(int(action.knight_id)/100)
        # Esto no deberia ocurrir, por eso es excepcion
        if player_id == self.my_id:
            if self.my_knights.get(str(action.knight_id)) is None:
                raise ValueError(f'Knight {action.knight_id} not in board')
        else:
            if self.enemy_knights.get(str(action.knight_id)) is None:
                raise ValueError(f'Knight {action.knight_id} not in board')

        # Validacion de accion
        start, end = self.get_movement_positions(action)
        x, y = start
        nx, ny = end
        shape = (8, 8)
        
        # Validando que esta dentro del tablero
        if end[0] < 0 or end[1] < 0:
            return False
        if end[0] >= shape[0] or end[1] >= shape[1]:
            return False

        # Validando que no se quiere comer a un amigo
        if (not self.board[ny][nx] is None) and int(self.board[ny][nx]/100) == player_id:
            return False

        return True

    def is_final(self):
        lose = len(self.my_knights) == 0
        win = len(self.enemy_knights) == 0

        # Retornando resultado de estado final
        return lose or win

    def value(self):
        if len(self.enemy_knights) == 0:
            return 99999
        value = 200
        if self.my_id == 1:
            enemy_id = 2
        else:
            enemy_id = 1
        # Estados mejores:
        #   Cuando enemy knights sea menor al estado
        value -= (len(self.enemy_knights)) * 4
        value += (len(self.my_knights)) * 5
        #   Cuando my caballo no puede comido por otro

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
