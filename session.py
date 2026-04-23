from trainer import Trainer
from datetime import datetime

class Session:
    def __init__(self, session_id, session_type, date_time, duration, trainer, capacity):
        self._id = session_id
        self._type = session_type
        self.date_time = date_time
        self.duration = duration
        self.trainer = trainer
        self.capacity = capacity
        self._participants = []
    
    @property
    def date_time(self):
        return self._date_time
    
    @date_time.setter
    def date_time(self, value):
        if not isinstance(value, datetime):
            raise TypeError("date_time must be a datetime object.")
        self._date_time = value
    
    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, value):
        if not isinstance(value, int) or value <= 0:
            raise TypeError("Duration must be a positive integer")
        self._duration = value
    
    @property
    def trainer(self):
        return self._trainer
    
    @trainer.setter
    def trainer(self, value):
        if not isinstance(value, Trainer):
            raise TypeError("Trainer must be a trainer object")
        self._trainer = value
    
    @property
    def capacity(self):
        return self._capacity
    
    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int) or value <= 0:
            raise TypeError("Capacity must be a positive integer")
        self._capacity = value
    

    
