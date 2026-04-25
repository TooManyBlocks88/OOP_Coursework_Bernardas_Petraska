import unittest
from datetime import date

from member import Member
from membership_plan import MembershipPlan


class TestMember(unittest.TestCase):
    def test_member_starts_without_membership(self):
        member = Member(1, "John", "john@example.com", "12345678")

        self.assertIsNone(member.membership_plan)
        self.assertIsNone(member._start_date)
        self.assertIsNone(member._expiry_date)
        self.assertEqual(member.booked_sessions, [])
    
    def test_assign_membership_plan_sets_plan_and_dates(self):
        member = Member(1, "John", "john@example.com", "12345678")
        plan = MembershipPlan("Monthly", 17, 30, "Basic")

        member.assign_membership_plan(plan)

        self.assertEqual(member.membership_plan, plan)
        self.assertEqual(member._start_date, date.today())
        self.assertEqual(
            member._expiry_date,
            plan.calculate_expiry_date(date.today())
        )

    def test_assign_membership_plan_with_invalid_type_raises_error(self):
        member = Member(1, "John", "john@example.com", "12345678")

        with self.assertRaises(TypeError):
            member.assign_membership_plan("not a plan")
    
    