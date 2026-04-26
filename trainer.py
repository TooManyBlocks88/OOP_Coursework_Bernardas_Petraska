from user import User

class Trainer(User):
    def __init__(self, user_id, name, email, phone,
                 specialization):
        super().__init__(user_id, name, email, phone)
        self.specialization = specialization
        self._assigned_sessions = []
    
    @property
    def specialization(self):
        return self._specialization

    @specialization.setter
    def specialization(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Specialization cannot be empty.")
        self._specialization = value
    
    @property
    def assigned_sessions(self):
        return self._assigned_sessions.copy()
    
    def has_session(self, session):
        return session in self._assigned_sessions
    
    def assign_session(self, session):
        if not hasattr(session, "session_id") or not hasattr(session, "trainer"):
            raise TypeError("Invalid session object")
        if self.has_session(session):
            raise ValueError("Session is already assigned to this trainer.")
        self._assigned_sessions.append(session)
    
    def remove_session(self, session):
        if not hasattr(session, "session_id") or not hasattr(session, "trainer"):
            raise TypeError("Invalid session object")
        if not self.has_session(session):
            raise ValueError("Session is not assigned to this trainer.")
        self._assigned_sessions.remove(session)
    
    def get_summary(self):
        base = super().get_summary()
        return f"{base}\nSpecialization: {self.specialization}"
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "specialization": self.specialization
        }