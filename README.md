# Desafío 2 GrupoRA: Knight Chess

Implementación de algoritmos de búsqueda adversaria en ejecución de juego knight chess

## Descripción

El presente código ejecuta un controlador para responder al problema de búsqueda adversaria para knight chess. Este juego consiste en eliminar todas las piezas del adversario en un tablero de 8x8 como el de ajedrez utilizando piezas de caballo con su respectivo movimiento en "L".

## Estructura

Se presentan dos partes, algorithm y knight_chess. El primero contiene los algoritmos de búsqueda adversaria, mientras que el segundo está encargado de las acciones y estados del tablero.

### Knight Chess

Contiene la representación del tablero y las acciones disponibles a realizar.

Contiene la información del jugador, el adversario y si está en una búsqueda de máximos. Estos se describen a continuación.

* **My id**: ID del jugador. 1 si es blanco, 2 si es negro.
* **My knights**: Diccionario de los caballos del jugador, indicando el ID y la posición de cada uno.
* **Enemy knights**: Diccionario de los caballos del oponente, indicando el ID y la posición de cada uno.
* **Board**: Matriz que contiene la posición de cada caballo en el tablero, indicando con ```nan``` aquellas ubicaciones vacías. Su objetivo es agilizar la detección de movimientos de ataque.

#### Validación de acciones

Cada caballo puede llegar a tener un máximo de 8 acciones disponibles. Sin embargo, estas pueden estar limitadas por dos factores.

* El movimiento resulta con el caballo fuera del tablera.
* El movimiento resulta en la superposición de un caballo sobre otro de su mismo color.

Fuera de esas dos excepciones todos los otros movimientos son considerados válidos

#### Estado final

El estado se declara como estado final cuando quede un solo color de caballos en el tablero. Esto considera tanto aliados como enemigos.

#### Valor de un Estado

Los estados deben poder ser evaluados, para esto, se toman en consideración los caballos tanto oponentes como propios y la capacidad de supervivencia de los caballos del mismo jugador.

El valor del estado actualmente está definido de la siguiente manera:

```
E = cantidad de enemigos vivos
A = cantidad de aliados vivos
S = sum(casillas de aliados fuera de riesgo)
Si es_final(estado) & ganador(estado) == id(estado):
    valor = 99999
sino:
    valor = 200 - 6*E + 4*A + S

````

### Algorithm

Se presenta la función de búsqueda adversaria alpha beta pruning. El ha sido definido de manera recursiva y recibe un estado, alpha, beta y profundidad como argumento y retorna un estado junto al valor de éste.

En un comienzo, se comprueba que la profundidad alcanzada por la búsqueda no es la máxima, y que el estado actual no sea final. en cualquiera de estos casos, se retorna ```None``` acompañado por el valor del estado. Luego, si la búsqueda continúa, se determina si el estado viene definido como máximo o no.

#### Alpha beta pruning

Si estado es max:

Itera sobre las acciones disponibles generando estados hijos e indicando que su valor de ```max``` como ```False```. entonces hace otro llamado a la función **alpha beta** para obtener el valor del estado.

CUando se obtiene el valor  de un estado, este es agregado a una lista de hijos, el cual indica la acción y el valor de dicha acción.  Entonces, se comprueba si el valor alcanzado por el hijo es mayor al maximo valor alcanzado en la búsqueda. Si este valor es mayor al alpha entregado a la función, entonces éste último es actualizado al al valor obtenido. Finalmente, si ```beta <= alpha```, se termina la búsqueda y retorna la acción conseguida.

Si estado es min

Al igual que en la búsqueda de máximos, se realiza una iteración sobre estados hijos al estado actual y se obtiene el valor de éstos de manera recursiva. Su diferencia recae al momento de evaluar el valor obtenido, en este caso si el valor del estado hijo es menor a beta, entonces se actualiza a dicho nuevo valor. Finalmente, se comprueba si ```beta <= alpha``` se rompen las iteraciones y retorna el valor y acción obtenidos.

