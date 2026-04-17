class Gym:
    pass


class User:
    def __init__(self, user_id, name, email, phone):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
    
    @property # getter
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not value.strip(): # not empty or whitespace
            raise ValueError("Name cannot be empty")
        self._name = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not value or not value.strip():
            raise ValueError("Email cannot be empty")
        if '@' not in value:
            raise ValueError("Invalid email format")
        self._email = value
    
class Member(User):
    def __init__(self, member_id, name, email, phone,
                 membership_plan=None, join_date=None, expiry_date=None):
        super().__init__(member_id, name, email, phone)
        self.membership_plan = membership_plan
        self.join_date = join_date
        self.expiry_date = expiry_date
        self.booked_sessions = []


class Trainer(User):
    def __init__(self, trainer_id, name, email, phone,
                 specialization):
        super().__init__(trainer_id, name, email, phone)
        self.specialization = specialization
        self.assigned_sessions = []


class Session:
    pass


class MembershipPlan:
    pass