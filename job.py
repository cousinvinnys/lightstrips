from time import time

class Job:
    _num_jobs = 0
    def __init__(self, generator, nice=0, ttl=60, name=None):
        self.generator = generator
        self.nice = nice
        self.ttl = ttl
        self.never_die = self.ttl < 0
        self._is_alive = False
        self._started = False
        self._time_start = 0

        self.name = f"job{_num_jobs}" if name is None else name

        Job._num_jobs += 1

    def __str__(self):
        return f'{self.name} started at {self._timeStart}'

    def start(self):
        self._is_alive = True
        self._started = True
        self._time_start = time()

    def get_next_line(self):
        if time() - self._time_start > self.ttl and not self.never_die:
            self._is_alive = False
        
        return next(self.generator) if self._is_alive else None

    def is_running(self):
        return self._is_alive
    
    def is_dead(self):
        return not self._is_alive and self._started

    def time_remaining(self):
        return self.ttl - time() + self._time_start 
