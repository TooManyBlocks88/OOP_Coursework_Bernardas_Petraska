from datetime import timedelta, date

from user import User
from membership_plan import MembershipPlan

class Member(User):
    def __init__(self, user_id, name, email, phone):
        super().__init__(user_id, name, email, phone)
        self._membership_plan = None # plan is assigned with a method, not manually. dates are tied to it.
        self._start_date = None
        self._expiry_date = None
        self._booked_sessions = []
    
    @property
    def membership_plan(self):
        return self._membership_plan
    
    @membership_plan.setter
    def membership_plan(self, value):
        if value is not None and not isinstance(value, MembershipPlan):
            raise TypeError("membership_plan must be a MembershipPlan object or None")
        self._membership_plan = value
    
    @property
    def booked_sessions(self):
        return self._booked_sessions.copy()

    @property
    def start_date(self):
        return self._start_date

    @property
    def expiry_date(self):
        return self._expiry_date

    @property
    def booked_sessions(self):
        return self._booked_sessions.copy()
    
    def assign_membership_plan(self, plan):
        if not isinstance(plan, MembershipPlan):
            raise TypeError("Plan must be a MembershipPlan object")
        self._membership_plan = plan
        self._start_date = date.today()
        self._expiry_date = plan.calculate_expiry_date(self._start_date)
    
    def has_active_membership(self):
        return (
            self.membership_plan is not None
            and self.expiry_date is not None
            and self.expiry_date >= date.today()
        )
    
    def book_session(self, session):
        from session import Session
        if not isinstance(session, Session):
            raise TypeError("Session must be a Session object.")
        if not self.has_active_membership():
            raise ValueError("Inactive membership.")
        if session in self._booked_sessions:
            raise ValueError("This session is already booked.")
                
        session.add_participant(self) # controls its own validation
        self._booked_sessions.append(session)
    
    def cancel_session(self, session):
        from session import Session
        if not isinstance(session, Session):
            raise TypeError("Session must be a Session object.")
        if session not in self._booked_sessions:
            raise ValueError("Session not booked.")

        session.remove_participant(self)
        self._booked_sessions.remove(session)
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "membership_plan": (
                self.membership_plan.name
                if self.membership_plan is not None
                else None
            ),
            "membership_start_date": (
                self.membership_start_date.isoformat()
                if self.membership_start_date is not None
                else None
            ),
            "membership_expiry_date": (
                self.membership_expiry_date.isoformat()
                if self.membership_expiry_date is not None
                else None
            )
        }
