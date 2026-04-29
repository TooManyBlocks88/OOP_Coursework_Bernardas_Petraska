from datetime import datetime

from gym import Gym
from membership_plan import MembershipPlan
from session import Session
from user_factory import UserFactory


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    input("Press Enter to run this section...")


def demo_factory_pattern():
    print_section("1. FACTORY PATTERN")

    user_data = [
        {
            "user_type": "member",
            "user_id": 1,
            "name": "John Smith",
            "email": "john@example.com",
            "phone": "123456789"
        },
        {
            "user_type": "trainer",
            "user_id": 2,
            "name": "Anna Brown",
            "email": "anna@example.com",
            "phone": "987654321",
            "specialization": "Yoga"
        }
    ]

    created_users = []

    for data in user_data:
        user = UserFactory.create_user(**data)
        created_users.append(user)

        print(f"Created {type(user).__name__}: {user.name}")

    print("\nThe same creation code handled both Member and Trainer objects.")
    print("The main program did not directly call Member(...) or Trainer(...).")

    return created_users


def demo_inheritance_polymorphism(users):
    print_section("2. INHERITANCE AND POLYMORPHISM")

    print("Calling the same method, get_summary(), on different user types:\n")

    for user in users:
        print(f"{type(user).__name__} output:")
        print(user.get_summary())
        print("-" * 40)

    print("Same method name, different behavior depending on object type.")


def demo_membership(member):
    print_section("3. MEMBERSHIP PLAN")

    plan = MembershipPlan("Basic", 29.99, 30, "Standard")
    member.assign_membership_plan(plan)

    print(f"Assigned plan: {member.membership_plan.name}")
    print(f"Membership active: {member.has_active_membership()}")
    print(f"Start date: {member.start_date}")
    print(f"Expiry date: {member.expiry_date}")

    return plan


def demo_session_booking(gym, member, trainer):
    print_section("4. SESSION BOOKING")

    session = Session(
        1,
        "Morning Yoga",
        datetime(2026, 5, 10, 10, 0),
        60,
        trainer,
        2
    )

    gym.add_session(session)
    member.book_session(session)

    print(f"Session created: {session.session_type}")
    print(f"Trainer: {session.trainer.name}")
    print(f"Member booked: {member.name}")
    print(f"Participants in session: {len(session.participants)}")
    print(f"Available spots: {session.available_spots()}")

    return session


def demo_encapsulation(member, session):
    print_section("5. ENCAPSULATION")

    print("Trying to modify booked_sessions directly...\n")

    before = len(member.booked_sessions)

    member.booked_sessions.remove(session)

    after = len(member.booked_sessions)

    print(f"Before modification attempt: {before}")
    print(f"After modification attempt:  {after}")

    print("\nResult:")
    print("The number of booked sessions did not change.")
    print("External code cannot modify the internal list directly.")


def demo_validation(gym, member, trainer, session):
    print_section("6. VALIDATION")

    examples = [
        ("Duplicate member", lambda: gym.add_member(member)),
        ("Duplicate booking", lambda: member.book_session(session)),
        ("Invalid trainer email", lambda: UserFactory.create_user(
            "trainer",
            3,
            "Bad Trainer",
            "invalid-email",
            "111222333",
            specialization="Strength"
        )),
        ("Invalid session capacity", lambda: Session(
            2,
            "Boxing",
            datetime(2026, 5, 11, 12, 0),
            60,
            trainer,
            0
        )),
        ("Invalid factory type", lambda: UserFactory.create_user(
            "manager",
            4,
            "Fake Manager",
            "manager@example.com",
            "444555666"
        ))
    ]

    for description, action in examples:
        try:
            action()
        except (ValueError, TypeError) as error:
            print(f"{description} prevented: {error}")


def demo_file_handling(gym):
    print_section("7. FILE HANDLING")

    filename = "gym_data.json"

    gym.save_to_file(filename)
    print(f"Saved gym data to {filename}")

    loaded_gym = Gym.load_from_file(filename)
    print(f"Loaded gym: {loaded_gym.name}")

    loaded_member = loaded_gym.find_member(1)
    loaded_session = loaded_gym.find_session(1)

    print(f"Loaded member: {loaded_member.name}")
    print(f"Loaded session: {loaded_session.session_type}")
    print(f"Loaded participants: {len(loaded_session.participants)}")


def main():
    print("\nGYM ADMINISTRATION SYSTEM DEMO")

    gym = Gym("City Gym")

    users = demo_factory_pattern()
    member = users[0]
    trainer = users[1]

    gym.add_member(member)
    gym.add_trainer(trainer)

    demo_inheritance_polymorphism(users)

    plan = demo_membership(member)
    gym.add_membership_plan(plan)

    session = demo_session_booking(gym, member, trainer)

    demo_encapsulation(member, session)

    demo_validation(gym, member, trainer, session)

    demo_file_handling(gym)

    print("\nDemo complete.")


if __name__ == "__main__":
    main()