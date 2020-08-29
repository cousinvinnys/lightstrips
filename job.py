from time import time

class Job:
    def __init__(self, generator, nice=0, ttl=60):
        self.generator = generator
        self.nice = nice
        self.ttl = ttl
        self.never_die = self.ttl < 0
        self._is_alive = False
        self._started = False
        self._timeStart = 0

    def start(self):
        self._is_alive = True
        self._started = True
        self._time_start = time.time()

    def get_next_line(self):
        if time.time() - self._is_alive > self.ttl and not self.never_die:
            self._is_alive = False
        
        return next(self.generator) if self._is_alive else None

    def is_running(self):
        return self._is_alive
    
    def is_dead(self):
        return not self._is_alive and self._started
