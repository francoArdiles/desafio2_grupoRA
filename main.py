from algorithm import alpha_beta, minmax
from knight_chess import State
from copy import deepcopy as copy
import sys
import json

if __name__ == '__main__':
    # Obteniendo entrada del controlador
    if "-test" in sys.argv:
        state_json = open("test.json", "r").read()
    else:
        state_json = sys.argv[1]
        state_json = state_json.replace(r'\"', '"')

    # Obteniendo entrada del controlador
    state_json = sys.argv[1]
    state_json = state_json.replace(r'\"', '"')
    state = json.loads(state_json)

    # Generando el estado
    state = State(state)
    
    # Copiando el estado
    state_c1 = copy(state)
    state_c2 = copy(state)

    # Aplicando algoritmos de busqueda
    action_result1 = alpha_beta(state_c1, float('inf'), float('-inf'))
    action_result2 = minmax(state_c2)
    
    # Imprimiendo resultado de accion
    print(action_result2.send())
