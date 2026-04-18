from datetime import timedelta, date

from user import User
from membership_plan import MembershipPlan

class Member(User):
    def __init__(self, user_id, name, email, phone):
        super().__init__(user_id, name, email, phone)
        self._membership_plan = None # plan is assigned with a method, not manually. dates are tied to it.
        self._start_date = None
        self._expiry_date = None
        self.booked_sessions = []
    
    @property
    def membership_plan(self):
        return self._membership_plan
    
    @membership_plan.setter
    def membership_plan(self, value):
        if value is not None and not isinstance(value, MembershipPlan):
            raise TypeError("membership_plan must be a MembershipPlan object or None")
        self._membership_plan = value
    
    def assign_membership_plan(self, plan):
        if not isinstance(plan, MembershipPlan):
            raise TypeError("Plan must be a MembershipPlan object")
        self._membership_plan = plan
        self._start_date = date.today()
        self._expiry_date = plan.calculate_expiry_date(self._start_date)