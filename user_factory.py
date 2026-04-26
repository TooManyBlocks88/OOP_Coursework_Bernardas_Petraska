from member import Member
from trainer import Trainer


class UserFactory:
    @staticmethod
    def create_user(user_type, user_id, name, email, phone, specialization=None):
        if user_type == "member":
            return Member(user_id, name, email, phone)

        if user_type == "trainer":
            if specialization is None:
                raise ValueError("Trainer requires a specialization.")
            return Trainer(user_id, name, email, phone, specialization)

        raise ValueError("Invalid user type.")