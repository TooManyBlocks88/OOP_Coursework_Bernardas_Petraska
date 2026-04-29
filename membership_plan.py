from datetime import timedelta, date

class MembershipPlan:
    def __init__(self, name, price, duration_days, access_level):
        self.name = name
        self.price = price
        self.duration_days = duration_days
        self._access_level = access_level
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
    
    @property
    def duration_days(self):
        return self._duration_days
    
    @duration_days.setter
    def duration_days(self, value):
        if not isinstance(value, int):
            raise TypeError("Duration must be an integer")
        if value <= 0:
            raise ValueError("Duration must be positive")
        self._duration_days = value
    
    @property
    def access_level(self):
        return self._access_level

    def calculate_expiry_date(self, start_date):
        if not isinstance(start_date, date):
            raise TypeError("start_date must be a date object")
        return start_date + timedelta(days=self.duration_days)
    
    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "duration_days": self.duration_days,
            "access_level": self.access_level
        }