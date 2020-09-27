import datetime

class Timer:

    init_time: datetime.datetime
    limit_time: datetime.datetime

    # Tiempo limite para realizar una accion
    TIME_OUT = datetime.timedelta(seconds=4)

    def __init__(self):
        self.reset()

    def reset(self):
        self.init_time = datetime.datetime.now()
        self.limit_time = self.init_time + self.TIME_OUT

    def current_time(self) -> datetime.timedelta:
        """
        Obtiene el tiempo transcurrido desde que se inicializó el timer

        Returns:
            datetime.timedelta: Tiemop transcurrido desde que se inicilizó el
                                timer.
        """
        if self.time_out():
            return datetime.timedelta(seconds=0)
        return self.limit_time - datetime.datetime.now()

    def time_out(self) -> bool:
        return datetime.datetime.now() > self.limit_time
