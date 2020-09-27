import math
from knight_chess.state import State
from algorithm.timer import Timer

timer = Timer()

def alpha_beta(state: State, alpha, beta, maxDepth=99999):
    global timer
    if state.is_final() or maxDepth == 0 or timer.time_out():
        # print("[FINAL] state.value():", state.value())
        # print("[FINAL] state:", state.my_knights)
        # print("[FINAL] state:", state.enemy_knights)
        return (None, state.value())

    if state.isMax:
        maxValue = -math.inf
        childs = []
        for action in state.get_actions(1):
            child = state.transition(action)
            child.isMax = False
            value = alpha_beta(child, alpha, beta, maxDepth - 1)[1] # retorna el valor del estado
            childs.append((action, value))
            if value > maxValue:
                # print("Mejor valor: ", value)
                i = (action, value)
                maxValue = value
            if value > alpha:
                alpha = value
            if beta <= alpha:
                break

        return i

    else:
        minValue = math.inf
        childs = []
        for action in state.get_actions(2):
            child = state.transition(action)
            child.isMax = True
            value = alpha_beta(child, alpha, beta, maxDepth - 1)[1] # retorna el valor del estado
            childs.append((action, value))
            if value < minValue:
                # print("Menor valor: ", value)
                i = (action, value)
                minValue = value
            if value < beta:
                beta = value
            if beta <= alpha:
                break

        return i

    return (None, 0)

