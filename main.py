from algorithm import alpha_beta, minmax
from knight_chess import State
from knight_chess.action import Action
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
    state = json.loads(state_json)

    # Generando el estado
    state = State(state)
    
    #state.print_state()
    #for action in state.get_actions():
    #    new_state = state.transition(action)
    #    new_state.print_state()

    ## Copiando el estado
    state_c1 = copy(state)
    #state_c2 = copy(state)
    
    # Aplicando algoritmos de busqueda
    action_result1 = alpha_beta(state_c1, float('-inf'), float('inf'), maxDepth=3)[0]
    # action_result2 = minmax(state_c2, maxDepth=1)[0]
    
    # Imprimiendo resultado de accion
    action_result1.send()
    # action_result2.send()


