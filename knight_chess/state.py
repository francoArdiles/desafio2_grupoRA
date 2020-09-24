import json
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
    3: (1, -2),
    4: (-1, -2),
    5: (-2, -1),
    6: (-2, 1),
    7: (-1, 2),
}


class State:

    def __init__(self):
        self.my_id = None
        self.my_knights = None
        self.enemy_knights = None
        self.isMax = None
        # 8x8 matrix
        self.board = None
        print('created empty state!')

    def transition(self, action: Action):
        # Copia del estado actual
        new_state = deepcopy(self)

        # identificacion de casilla actual y objetivo
        start, end = self.get_movement_positions(action)

        # identifica el elemento que se encuentra en la casilla objetivo
        element = new_state.board[end]
        # Limpia la posicion desocupada por el caballo
        new_state.board[start] = np.nan

        # Remueve elemento de la lista si es que existe
        if element in self.enemy_knights:
            new_state.enemy_knights.remove(element)
        elif element in self.my_knights:
            new_state.my_knights.remove(element)

        new_state.board[end] = action.knight_id
        pass

    def get_movement_positions(self, action):
        movement = MOVEMENTS.get(action.knight_movement)
        position = np.where(self.board == action.knight_id)
        row, col = position[0][0], position[1][0]
        new_row, new_col = row + movement[0], col + movement[1]

        return (row, col), (new_row, new_col)

    def is_valid_action(self, action):
        # identificacion de casilla actual y objetivo
        player_id = int(action.knight_id/100)
        # Esto no deberia ocurrir, por eso es excepcion
        if player_id == 1:
            if action.knight_id not in self.my_knights:
                raise ValueError(f'Knight {action.knight_id} not in board')
        else:
            if action.knight_id not in self.enemy_knights:
                raise ValueError(f'Knight {action.knight_id} not in board')

        # Validacion de accion
        start, end = self.get_movement_positions(action)
        shape = self.board.shape
        if end[0] < 0 or end[1] < 0:
            return False
        if end[0] > shape[0] or end[1] > shape[1]:
            return False
        if (self.board[end]/100) == player_id:
            return False
        return True

    def is_final(self):
        #retorna True si es final, False si no
        pass

    def value(self):
        # Estados mejores:
        #   Cuando enemy knights sea menor al estado
        #   Cuando my caballo no puede comido por otro
        #   avanzar > retroceder
        #   lure
        #   mejor supervivencia de nuetros caballos
        return 1

    def get_actions(self):
        # Seleccionar los caballos que estan mas adelante
        # Buscar hasta que se coma a un caballo enemigo
        pass

    def __lt__(self, other):
        return self.value() < other.value()
        pass
