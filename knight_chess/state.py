import json
import numpy as np
from .action import Action

WHITE = 1
BLACK = 2

# Knights positions:

# + 4 + 3 +
# 5 + + + 2
# + + C + +
# 6 + + + 1
# + 7 + 0 +


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
        # elimina el caballo de su posición actual y lo pone en una nueva
        # sin importar el estado al que llegue
        pass

    def is_valid_action(self, action):
        # Un caballo no puede saltar sobre otro del mismo tipo
        # un caballo debe saltar dentro del tablero
        pass

    def is_final(self):
        #retorna True si es final, False si no
        pass

    @property
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
