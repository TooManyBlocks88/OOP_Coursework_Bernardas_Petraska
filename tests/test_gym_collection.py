import unittest
from datetime import datetime

from gym import Gym
from member import Member
from trainer import Trainer
from membership_plan import MembershipPlan
from session import Session

class TestGym(unittest.TestCase):
    def setUp(self):
        self.gym = Gym("City Gym")

        self.member = Member(
            "M001",
            "John Smith",
            "john@example.com",
            "123456789"
        )

        self.trainer = Trainer(
            "T001",
            "Anna Brown",
            "anna@example.com",
            "987654321",
            "Yoga"
        )

        self.plan = MembershipPlan(
            "Basic",
            29.99,
            30,
            "standard"
        )

        self.session = Session(
            "S001",
            "Yoga",
            datetime(2026, 5, 10, 10, 0),
            60,
            self.trainer,
            10
        )

    def test_add_member_adds_member(self):
        self.gym.add_member(self.member)

        self.assertEqual(self.gym.find_member("M001"), self.member)

    def test_find_member_returns_none_when_not_found(self):
        result = self.gym.find_member("M999")

        self.assertIsNone(result)

    def test_add_member_rejects_duplicate_user_id(self):
        duplicate_member = Member(
            "M001",
            "Different Name",
            "different@example.com",
            "111222333"
        )

        self.gym.add_member(self.member)

        with self.assertRaises(ValueError):
            self.gym.add_member(duplicate_member)

    def test_add_member_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            self.gym.add_member("not a member")

    def test_remove_member_removes_existing_member(self):
        self.gym.add_member(self.member)

        self.gym.remove_member("M001")

        self.assertIsNone(self.gym.find_member("M001"))

    def test_remove_member_raises_error_when_member_not_found(self):
        with self.assertRaises(ValueError):
            self.gym.remove_member("M999")

    def test_add_trainer_adds_trainer(self):
        self.gym.add_trainer(self.trainer)

        self.assertEqual(self.gym.find_trainer("T001"), self.trainer)

    def test_find_trainer_returns_none_when_not_found(self):
        result = self.gym.find_trainer("T999")

        self.assertIsNone(result)

    def test_add_trainer_rejects_duplicate_user_id(self):
        duplicate_trainer = Trainer(
            "T001",
            "Different Trainer",
            "trainer2@example.com",
            "111222333",
            "Pilates"
        )

        self.gym.add_trainer(self.trainer)

        with self.assertRaises(ValueError):
            self.gym.add_trainer(duplicate_trainer)

    def test_add_trainer_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            self.gym.add_trainer("not a trainer")

    def test_add_membership_plan_adds_plan(self):
        self.gym.add_membership_plan(self.plan)

        self.assertEqual(
            self.gym.find_membership_plan("Basic"),
            self.plan
        )

    def test_find_membership_plan_returns_none_when_not_found(self):
        result = self.gym.find_membership_plan("Premium")

        self.assertIsNone(result)

    def test_add_membership_plan_rejects_duplicate_name(self):
        duplicate_plan = MembershipPlan(
            "Basic",
            49.99,
            60,
            "premium"
        )

        self.gym.add_membership_plan(self.plan)

        with self.assertRaises(ValueError):
            self.gym.add_membership_plan(duplicate_plan)

    def test_add_membership_plan_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            self.gym.add_membership_plan("not a plan")

    def test_add_session_adds_session(self):
        self.gym.add_session(self.session)

        self.assertEqual(self.gym.find_session("S001"), self.session)

    def test_find_session_returns_none_when_not_found(self):
        result = self.gym.find_session("S999")

        self.assertIsNone(result)

    def test_add_session_rejects_duplicate_session_id(self):
        duplicate_session = Session(
            "S001",
            "Pilates",
            datetime(2026, 5, 11, 12, 0),
            45,
            self.trainer,
            8
        )

        self.gym.add_session(self.session)

        with self.assertRaises(ValueError):
            self.gym.add_session(duplicate_session)

    def test_add_session_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            self.gym.add_session("not a session")