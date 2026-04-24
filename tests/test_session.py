import unittest
from datetime import datetime

from session import Session
from member import Member
from trainer import Trainer


class TestSessionParticipants(unittest.TestCase):

    def setUp(self):
        self.trainer = Trainer(
            user_id=1,
            name="John Trainer",
            email="john@gym.com",
            phone="123456",
            specialization="Strength"
        )

        self.member1 = Member(
            user_id=2,
            name="Alice Member",
            email="alice@email.com",
            phone="111111"
        )

        self.member2 = Member(
            user_id=3,
            name="Bob Member",
            email="bob@email.com",
            phone="222222"
        )

        self.session = Session(
            session_id=1,
            session_type="Yoga",
            date_time=datetime(2026, 5, 1, 10, 0),
            duration=60,
            trainer=self.trainer,
            capacity=2
        )

    def test_add_participant_adds_member(self):
        self.session.add_participant(self.member1)

        self.assertTrue(self.session.has_participant(self.member1))

    def test_add_participant_rejects_non_member(self):
        with self.assertRaises(TypeError):
            self.session.add_participant("not a member")

    def test_add_participant_rejects_duplicate_member(self):
        self.session.add_participant(self.member1)

        with self.assertRaises(ValueError):
            self.session.add_participant(self.member1)

    def test_is_full_returns_true_when_capacity_reached(self):
        self.session.add_participant(self.member1)
        self.session.add_participant(self.member2)

        self.assertTrue(self.session.is_full())

    def test_add_participant_rejects_when_session_full(self):
        self.session.add_participant(self.member1)
        self.session.add_participant(self.member2)

        third_member = Member(
            user_id=4,
            name="Charlie Member",
            email="charlie@email.com",
            phone="333333"
        )

        with self.assertRaises(ValueError):
            self.session.add_participant(third_member)

    def test_remove_participant_removes_existing_member(self):
        self.session.add_participant(self.member1)
        self.session.remove_participant(self.member1)

        self.assertFalse(self.session.has_participant(self.member1))

    def test_remove_participant_rejects_missing_member(self):
        with self.assertRaises(ValueError):
            self.session.remove_participant(self.member1)