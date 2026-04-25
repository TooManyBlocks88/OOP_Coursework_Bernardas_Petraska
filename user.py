class User:
    def __init__(self, user_id, name, email, phone):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._phone = phone
    
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        if not value or not value.strip():
            raise ValueError("ID cannot be empty")
        self._user_id = value
    
    @property
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