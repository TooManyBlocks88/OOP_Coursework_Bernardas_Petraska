import unittest

from user_factory import UserFactory
from member import Member
from trainer import Trainer


class TestUserFactory(unittest.TestCase):

    def test_create_member(self):
        user = UserFactory.create_user(
            "member",
            1,
            "Alice",
            "alice@mail.com",
            "123456"
        )

        self.assertIsInstance(user, Member)
        self.assertEqual(user.name, "Alice")

    def test_create_trainer(self):
        user = UserFactory.create_user(
            "trainer",
            2,
            "John",
            "john@mail.com",
            "654321",
            specialization="Strength"
        )

        self.assertIsInstance(user, Trainer)
        self.assertEqual(user.specialization, "Strength")

    def test_trainer_requires_specialization(self):
        with self.assertRaises(ValueError):
            UserFactory.create_user(
                "trainer",
                3,
                "NoSpec",
                "nospec@mail.com",
                "000000"
            )

    def test_invalid_user_type(self):
        with self.assertRaises(ValueError):
            UserFactory.create_user(
                "admin",
                4,
                "Admin",
                "admin@mail.com",
                "111111"
            )
