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

    def __init__(self, knight_dict):
        self.my_knights = knight_dict.get('my_knights_dict')
        self.enemy_knights = knight_dict.get('enemy_knights_dict')
        self.isMax = None
        for ids in self.my_knights.keys():
            self.my_id = int(int(ids)/100)
        # 8x8 matrix, using float reads null as nan integer comparison is still
        # possible
        self.board = np.array(knight_dict.get('ids'), dtype=float)

    def transition(self, action: Action):
        # Copia del estado actual
        new_state = deepcopy(self)

        # identificacion de casilla actual y objetivo
        start, end = self.get_movement_positions(action)

        # identifica el elemento que se encuentra en la casilla objetivo
        element = str(new_state.board[end])
        # Limpia la posicion desocupada por el caballo
        new_state.board[start] = np.nan

        # Remueve elemento de la lista si es que existe
        if element in self.enemy_knights.keys():
            new_state.enemy_knights.pop(element)
        elif element in self.my_knights.keys():
            new_state.my_knights.pop(element)

        new_state.board[end] = action.knight_id
        return new_state

    def get_movement_positions(self, action):
        movement = MOVEMENTS.get(action.knight_movement)
        if int(action.knight_id/100) == self.my_id:
            position = self.my_knights.get(str(action.knight_id))
        else:
            position = self.enemy_knights.get(str(action.knight_id))
        row, col = position[0], position[1]
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
        if (self.board[end]/100) == player_id:
            return False
        return True

    def is_final(self):
        lose = len(self.my_knights) == 0
        win = len(self.enemy_knights) == 0

        # Retornando resultado de estado final
        return lose or win

    def value(self):
        # Estados mejores:
        #   Cuando enemy knights sea menor al estado
        #   Cuando my caballo no puede comido por otro
        #   avanzar > retroceder
        #   lure
        #   mejor supervivencia de nuetros caballos
        return 1

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
        # for a in actions:
        #     print(a)

        for action in actions:
            if self.is_valid_action(action):
                valid_actions.append(action)
        # Seleccionar los caballos que estan mas adelante
        # Buscar hasta que se coma a un caballo enemigo
        # print('valid actions\n')
        # for action in valid_actions:
        #     print(action)
        return valid_actions

    def create_action(self, knight_id, movement):
        return Action(knight_id, movement)

    def __lt__(self, other):
        return self.value() < other.value()
        pass
