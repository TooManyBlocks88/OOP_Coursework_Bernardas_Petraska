from member import Member
from trainer import Trainer
from membership_plan import MembershipPlan
from session import Session

import json

class Gym:
    def __init__(self, name):
        self.name = name
        self._members = []
        self._trainers = []
        self._sessions = []
        self._membership_plans = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Gym name must be a string.")
        if not value.strip():
            raise ValueError("Gym name cannot be empty.")
        self._name = value.strip()
    
    def find_member(self, user_id):
        for member in self._members:
            if member.user_id == user_id:
                return member
        return None
    
    def add_member(self, member):
        if not isinstance(member, Member):
            raise TypeError("Member must be a Member object.")
        if self.find_member(member.user_id) is not None:
            raise ValueError("Member with this ID already exists.")
        self._members.append(member)
    
    def remove_member(self, user_id):
        member = self.find_member(user_id)

        if member is None:
            raise ValueError("Member not found.")

        self._members.remove(member)

    def find_trainer(self, user_id):
        for trainer in self._trainers:
            if trainer.user_id == user_id:
                return trainer
        return None

    def add_trainer(self, trainer):
        if not isinstance(trainer, Trainer):
            raise TypeError("Trainer must be a Trainer object.")
        if self.find_trainer(trainer.user_id) is not None:
            raise ValueError("Trainer with this ID already exists.")
        self._trainers.append(trainer)

    def find_membership_plan(self, name):
        for plan in self._membership_plans:
            if plan.name == name:
                return plan
        return None
    
    def add_membership_plan(self, plan):
        if not isinstance(plan, MembershipPlan):
            raise TypeError("Plan must be a MembershipPlan object.")
        if self.find_membership_plan(plan.name) is not None:
            raise ValueError("Membership plan with this name already exists.")
        self._membership_plans.append(plan)
    
    def find_session(self, session_id):
        for session in self._sessions:
            if session.session_id == session_id:
                return session
        return None
    
    def add_session(self, session):
        if not isinstance(session, Session):
            raise TypeError("Session must be a Session object.")
        if self.find_session(session.session_id) is not None:
            raise ValueError("Session with this ID already exists.")
        self._sessions.append(session)
    
    def save_to_file(self, filename):
        data = {
            "name": self.name,
            "membership_plans": [
                plan.to_dict() for plan in self.membership_plans
            ],
            "trainers": [
                trainer.to_dict() for trainer in self.trainers
            ],
            "members": [
                member.to_dict() for member in self.members
            ],
            "sessions": [
                session.to_dict() for session in self.sessions
            ]
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)