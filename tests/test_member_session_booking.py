import unittest
from datetime import date, datetime, timedelta

from member import Member
from trainer import Trainer
from session import Session
from membership_plan import MembershipPlan


class TestMemberSessionBooking(unittest.TestCase):

    def setUp(self):
        self.trainer = Trainer(
            user_id=1,
            name="John Trainer",
            email="john@gym.com",
            phone="123456",
            specialization="Strength"
        )

        self.plan = MembershipPlan(
            name="Basic",
            price=30,
            duration_days=30,
            access_level="Gym"
        )

        self.member = Member(
            user_id=2,
            name="Alice Member",
            email="alice@email.com",
            phone="111111"
        )

        self.session = Session(
            session_id=1,
            session_type="Yoga",
            date_time=datetime(2026, 5, 1, 10, 0),
            duration=60,
            trainer=self.trainer,
            capacity=5
        )
    
    def test_member_without_plan_has_inactive_membership(self):
        self.assertFalse(self.member.has_active_membership())
    
    def test_member_with_valid_plan_has_active_membership(self):
        self.member.assign_membership_plan(self.plan)

        self.assertTrue(self.member.has_active_membership())
    
    def test_member_with_expired_membership_is_inactive(self):
        self.member.assign_membership_plan(self.plan)
        self.member._expiry_date = date.today() - timedelta(days=1)

        self.assertFalse(self.member.has_active_membership())

    def test_book_session_rejects_non_session_object(self):
        self.member.assign_membership_plan(self.plan)

        with self.assertRaises(TypeError):
            self.member.book_session("not a session")

    def test_book_session_rejects_inactive_membership(self):
        with self.assertRaises(ValueError):
            self.member.book_session(self.session)

    def test_book_session_adds_session_to_member(self):
        self.member.assign_membership_plan(self.plan)
        self.member.book_session(self.session)

        self.assertIn(self.session, self.member.booked_sessions)

    def test_book_session_adds_member_to_session(self):
        self.member.assign_membership_plan(self.plan)
        self.member.book_session(self.session)

        self.assertTrue(self.session.has_participant(self.member))

    def test_book_session_rejects_duplicate_booking(self):
        self.member.assign_membership_plan(self.plan)
        self.member.book_session(self.session)

        with self.assertRaises(ValueError):
            self.member.book_session(self.session)

    def test_cancel_session_removes_session_from_member(self):
        self.member.assign_membership_plan(self.plan)
        self.member.book_session(self.session)

        self.member.cancel_session(self.session)

        self.assertNotIn(self.session, self.member.booked_sessions)

    def test_cancel_session_removes_member_from_session(self):
        self.member.assign_membership_plan(self.plan)
        self.member.book_session(self.session)

        self.member.cancel_session(self.session)

        self.assertFalse(self.session.has_participant(self.member))

    def test_cancel_session_rejects_non_session_object(self):
        with self.assertRaises(TypeError):
            self.member.cancel_session("not a session")

    def test_cancel_session_rejects_unbooked_session(self):
        with self.assertRaises(ValueError):
            self.member.cancel_session(self.session)

    def test_booked_sessions_returns_copy(self):
        self.member.assign_membership_plan(self.plan)
        self.member.book_session(self.session)

        copied_sessions = self.member.booked_sessions
        copied_sessions.clear()

        self.assertIn(self.session, self.member.booked_sessions)

