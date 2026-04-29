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
        self._name = value
    
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
        
        for session in member.booked_sessions:
            session.remove_participant(member)

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
                plan.to_dict() for plan in self._membership_plans
            ],
            "trainers": [
                trainer.to_dict() for trainer in self._trainers
            ],
            "members": [
                member.to_dict() for member in self._members
            ],
            "sessions": [
                session.to_dict() for session in self._sessions
            ]
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    
    @classmethod
    def load_from_file(cls, filename):
        from datetime import datetime, date

        with open(filename, "r") as file:
            data = json.load(file)

        gym = cls(data["name"])

        # 1. Load membership plans
        for plan_data in data["membership_plans"]:
            plan = MembershipPlan(
                plan_data["name"],
                plan_data["price"],
                plan_data["duration_days"],
                plan_data["access_level"]
            )
            gym.add_membership_plan(plan)

        plans_by_name = {
            plan.name: plan
            for plan in gym._membership_plans
        }

        # 2. Load trainers
        for trainer_data in data["trainers"]:
            trainer = Trainer(
                trainer_data["user_id"],
                trainer_data["name"],
                trainer_data["email"],
                trainer_data["phone"],
                trainer_data["specialization"]
            )
            gym.add_trainer(trainer)

        trainers_by_id = {
            trainer.user_id: trainer
            for trainer in gym._trainers
        }

        # 3. Load members
        for member_data in data["members"]:
            member = Member(
                member_data["user_id"],
                member_data["name"],
                member_data["email"],
                member_data["phone"]
            )

            plan_name = member_data["membership_plan"]
            if plan_name is not None:
                member.membership_plan = plans_by_name[plan_name]

            if member_data["start_date"] is not None:
                member._start_date = date.fromisoformat(member_data["start_date"])

            if member_data["expiry_date"] is not None:
                member._expiry_date = date.fromisoformat(member_data["expiry_date"])

            gym.add_member(member)

        members_by_id = {
            member.user_id: member
            for member in gym._members
        }

        # 4. Load sessions and reconnect trainers/members
        for session_data in data["sessions"]:
            trainer = trainers_by_id[session_data["trainer_id"]]

            session = Session(
                session_data["session_id"],
                session_data["session_type"],
                datetime.fromisoformat(session_data["date_time"]),
                session_data["duration"],
                trainer,
                session_data["capacity"]
            )

            for member_id in session_data["participant_ids"]:
                member = members_by_id[member_id]
                session.add_participant(member)
                member._booked_sessions.append(session)

            gym.add_session(session)

        return gym

