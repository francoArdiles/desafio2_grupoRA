import math
from knight_chess.state import State

def minmax(state: State, maxDepth = 99999):
    if state.is_final() or maxDepth == 0:
        return (None, state.value())

    if state.isMax:
        maxValue = -math.inf
        childs = []
        for action in state.get_actions():
            child = state.transition(action)
            child.isMax = False
            value = minmax(child, maxDepth-1)[1] # retorna el valor del estado
            childs.append((action, value))
            if value > maxValue:
                maxValue = value
            
        for i in childs:
            if i[1] == maxValue:
                return i

    else:
        minValue = math.inf
        childs = []
        for action in state.get_actions():
            child = state.transition(action)
            child.isMax = True
            value = minmax(child, maxDepth-1)[1] # retorna el valor del estado
            childs.append((action, value))
            if value < minValue:
                minValue = value
            
        for i in childs:
            if i[1] == minValue:
                return i

    return (None, 0)
