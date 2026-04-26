import unittest
from datetime import datetime

from trainer import Trainer
from session import Session


class TestTrainerSession(unittest.TestCase):

    def setUp(self):
        self.trainer = Trainer(
            user_id=1,
            name="John Trainer",
            email="john@gym.com",
            phone="123456",
            specialization="Strength"
        )

        self.session = Session(
            session_id=1,
            session_type="Yoga",
            date_time=datetime(2026, 5, 1, 10, 0),
            duration=60,
            trainer=self.trainer,
            capacity=2
        )

    def test_trainer_initializes_with_empty_sessions(self):
        trainer = Trainer(
            user_id=2,
            name="Jane Trainer",
            email="jane@gym.com",
            phone="654321",
            specialization="Cardio"
        )
        self.assertEqual(len(trainer.assigned_sessions), 0)

    def test_specialization_validation(self):
        with self.assertRaises(ValueError):
            Trainer(3, "Bad", "bad@mail.com", "000", "")

    def test_session_auto_assigned_on_creation(self):
        self.assertTrue(self.trainer.has_session(self.session))

    def test_assign_session_rejects_duplicate(self):
        with self.assertRaises(ValueError):
            self.trainer.assign_session(self.session)

    def test_assign_session_rejects_invalid_object(self):
        with self.assertRaises(TypeError):
            self.trainer.assign_session("not a session")

    def test_remove_session_removes_existing(self):
        self.trainer.remove_session(self.session)
        self.assertFalse(self.trainer.has_session(self.session))

    def test_remove_session_rejects_unassigned(self):
        self.trainer.remove_session(self.session)

        with self.assertRaises(ValueError):
            self.trainer.remove_session(self.session)

    def test_remove_session_rejects_invalid_object(self):
        with self.assertRaises(TypeError):
            self.trainer.remove_session("not a session")

    def test_assigned_sessions_returns_copy(self):
        sessions_copy = self.trainer.assigned_sessions
        sessions_copy.clear()

        # original list must remain unchanged
        self.assertEqual(len(self.trainer.assigned_sessions), 1)

    def test_session_trainer_relationship(self):
        self.assertEqual(self.session.trainer, self.trainer)
        self.assertIn(self.session, self.trainer.assigned_sessions)