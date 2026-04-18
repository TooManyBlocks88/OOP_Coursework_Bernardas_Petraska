from user import User

class Trainer(User):
    def __init__(self, user_id, name, email, phone,
                 specialization):
        super().__init__(user_id, name, email, phone)
        self.specialization = specialization
        self.assigned_sessions = []