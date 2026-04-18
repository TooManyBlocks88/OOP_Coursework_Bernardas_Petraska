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


if __name__ == "__main__":
    unittest.main()