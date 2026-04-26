from trainer import Trainer
from member import Member
from datetime import datetime

class Session:
    def __init__(self, session_id, session_type, date_time, duration, trainer, capacity):
        self.session_id = session_id
        self._type = session_type
        self.date_time = date_time
        self.duration = duration
        self.trainer = trainer
        self.capacity = capacity
        self._participants = []

        trainer.assign_session(self)
    
    @property
    def session_id(self):
        return self._session_id
    
    @session_id.setter
    def session_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise TypeError("session_id must be a positive integer")
        self._session_id = value
    
    @property
    def session_type(self):
        return self._type

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
        if not isinstance(value, int):
            raise TypeError("Duration must be an integer")
        if value <= 0:
            raise ValueError("Duration must be positive")
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
    
    @property
    def participants(self):
        return self._participants.copy()
    
    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int):
            raise TypeError("Capacity must be an integer")
        if value <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = value
    
    def available_spots(self):
        return self.capacity - len(self._participants)
    
    def is_full(self):
        return len(self._participants) >= self._capacity
    
    def has_participant(self, member):
        return member in self._participants
    
    def add_participant(self, member):
        if not isinstance(member, Member):
            raise TypeError("Participant must be a Member object.")
        if self.is_full():
            raise ValueError("Session is already full.")
        if self.has_participant(member):
            raise ValueError("Member is already enrolled in this session.")
        self._participants.append(member)
    
    def remove_participant(self, member):
        if not isinstance(member, Member):
            raise TypeError("Participant must be a Member object.")
        if not self.has_participant(member):
            raise ValueError("Member is not enrolled in this session.")
        self._participants.remove(member)
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "session_type": self.session_type,
            "date_time": self.date_time.isoformat(),
            "duration": self.duration,
            "trainer_id": self.trainer.user_id,
            "participant_ids": [
                member.user_id for member in self.participants
            ],
            "capacity": self.capacity
        }