import os
import tempfile
import unittest
from datetime import datetime

from gym import Gym
from member import Member
from trainer import Trainer
from session import Session
from membership_plan import MembershipPlan


class TestGymFileHandling(unittest.TestCase):

    def test_save_and_load_gym_data(self):
        gym = Gym("Test Gym")

        plan = MembershipPlan("Basic", 30, 30, "Gym")
        trainer = Trainer(1, "John", "john@gym.com", "123", "Strength")
        member = Member(2, "Alice", "alice@mail.com", "456")

        gym.add_membership_plan(plan)
        gym.add_trainer(trainer)
        gym.add_member(member)

        member.assign_membership_plan(plan)

        session = Session(
            1,
            "Yoga",
            datetime(2026, 5, 1, 10, 0),
            60,
            trainer,
            5
        )

        member.book_session(session)
        gym.add_session(session)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            filename = temp_file.name

        try:
            gym.save_to_file(filename)
            loaded_gym = Gym.load_from_file(filename)

            loaded_member = loaded_gym.find_member(2)
            loaded_trainer = loaded_gym.find_trainer(1)
            loaded_plan = loaded_gym.find_membership_plan("Basic")
            loaded_session = loaded_gym.find_session(1)

            self.assertIsNotNone(loaded_member)
            self.assertIsNotNone(loaded_trainer)
            self.assertIsNotNone(loaded_plan)
            self.assertIsNotNone(loaded_session)

            self.assertEqual(loaded_member.name, "Alice")
            self.assertEqual(loaded_member.membership_plan.name, "Basic")
            self.assertEqual(loaded_session.trainer.user_id, 1)
            self.assertTrue(loaded_session.has_participant(loaded_member))
            self.assertIn(loaded_session, loaded_member.booked_sessions)
            self.assertTrue(loaded_trainer.has_session(loaded_session))

        finally:
            os.remove(filename)
