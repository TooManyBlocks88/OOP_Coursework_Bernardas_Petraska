# 1. Introduction

## Goal of the Coursework

The goal of this coursework is to develop a software application using object-oriented programming (OOP) principles. The project demonstrates the use of core OOP concepts: inheritance, encapsulation, polymorphism, and abstraction. Additional features it shows are file handling, design patterns, and unit testing.

---

## Application Overview

This project is a gym management system. It models the core elements of a real gym, including members, trainers, sessions, and membership plans. The system has the core functionalities a commercial gym's system would use, such as managing users, assigning plans, creating sessions, and booking members into sessions. However, more complex and expansive systems such as payment were beyond the coursework's scope.

The application is designed using multiple interacting classes, where each class represents a specific part of the system and is responsible for its own data and behavior.

---

## How to Run the Program

To run the program, Python must be installed on the system. The application can be started by running the main script after opening cmd in the root folder:

```
python main.py
```

The program will execute a demo that showcases the main functionality of the system.

---

## How to Use the Program

The program runs as a console based demo. Each section of the demo focuses on a different part of the system, such as object creation, session booking, validation, and file handling.

The user progresses through the demo by pressing Enter after each section. The output in the terminal shows how the system behaves and how different components interact.

The demo is best utilized by analyzing the script and using the output to confirm how OOP concepts and previously mentioned features are handled.

---

# 2. Body / Analysis

## Overview

The application is designed as a gym management system consisting of multiple interacting classes. Each class represents a real-world entity and is responsible for managing its own data and behavior. The system follows object-oriented programming principles to ensure modularity, maintainability, and logical structure.

For example, the gym is a central entity which governs everything within it, while member and trainer are both users, sharing some attributes and differing in others. A member may have a membership plan, while a session functions with a trainer leading it and a number of members participating.

---

## Functional Requirements Implementation

### Managing Members and Trainers

The system allows creating and managing both members and trainers. These are represented as separate classes that inherit from a common base class.

```
class User:
    def __init__(self, user_id, name, email, phone):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._phone = phone
```
One of the child classes:
```
class Member(User):
    def __init__(self, user_id, name, email, phone):
        super().__init__(user_id, name, email, phone)
        self._membership_plan = None # plan is assigned with a method, not manually. dates are tied to it.
        self._start_date = None
        self._expiry_date = None
        self._booked_sessions = []
```

An inheritance structure here is suited for two objects that have something in common, ensuring that shared attributes such as name and email are defined once, while allowing each subclass to implement its own specific behavior. In this case, only a member may have a membership plan and the data tied to it, while only a trainer is required to lead a session, and is assigned one rather than booking it.

---

### Session Management

The system supports creating and managing training sessions. Each session is associated with a trainer and maintains a list of participating members.

```
class Session:
    def __init__(self, session_id, session_type, date_time, duration, trainer, capacity):
        self.session_id = session_id
        self._type = session_type
        self.date_time = date_time
        self.duration = duration
        self.trainer = trainer
        self.capacity = capacity
        self._participants = []

        trainer.assign_session(self)
```

A session cannot exist without a trainer, and as the session is initialized with one, a method from the trainer class is called in order to automatically add the session to the trainer's list, ensuring symmetry.

Sessions enforce rules such as capacity limits and prevent duplicate participants. For example, this method checks three seperate exceptions before executing its purpose:

```
def add_participant(self, member):
        if not isinstance(member, Member):
            raise TypeError("Participant must be a Member object.")
        if self.is_full():
            raise ValueError("Session is already full.")
        if self.has_participant(member):
            raise ValueError("Member is already enrolled in this session.")
        self._participants.append(member)
```

Each of these:

* wrong types,
* overfilled sessions,
* duplicate members,

would have the potential to cause problems in a real system if not ruled out.

---

### Membership Plans

Members can be assigned membership plans, which determine access and validity period. The system calculates membership expiry dates based on the selected plan.

```
def assign_membership_plan(self, plan):
        if not isinstance(plan, MembershipPlan):
            raise TypeError("Plan must be a MembershipPlan object")
        self._membership_plan = plan
        self._start_date = date.today()
        self._expiry_date = plan.calculate_expiry_date(self._start_date)
```

I chose a realistic option: a member may not immediately buy a plan at the same time as registration, therefore it's possible to exist without one. It would have also been illogical to initialize a member with start date and expiry date as arguments, since those would be loosely connected and have more failure modes. Instead, they are naturally given values through the process of assigning a membership plan, where the plan object has its own logic being called here, and methods validate each step accordingly.

Since it is possible for a member to exist without a plan, it is also necessary to check for a plan before allowing a member to book a session, as shown in the next section.

### Booking System

Members can book and cancel sessions, and the process is initiated by a member rather than the session. The system ensures that:

* only valid members can book sessions
* sessions are not over capacity
* duplicate bookings are prevented

```
def book_session(self, session):
        from session import Session
        if not isinstance(session, Session):
            raise TypeError("Session must be a Session object.")
        if not self.has_active_membership():
            raise ValueError("Inactive membership.")
        if session in self._booked_sessions:
            raise ValueError("This session is already booked.")
                
        session.add_participant(self) # controls its own validation
        self._booked_sessions.append(session)
```

The process can't be unilateral, and two different classes share responsibility for validation, the other half shown in the method session.add_participant(), which is called here. It is displayed in a previous section.

This logic maintains consistency between members and sessions, as they both have seperate lists for each other. When a session is booked, two processes happen.
Addition to the member's list of booked sessions:
```
self._booked_sessions.append(session)
```
And, symmetrically, to the session's list of participants:
```
self._participants.append(member)
```

---

### File Handling

The application supports saving and loading data using a JSON file. I chose this format because it's structured, as is the data this projects works with. Python objects still cannot be stored directly, so they are converted into dictionaries while saving. A trainer object being turned into a dictionary:

``` 
def to_dict(self):
    return {
        "user_id": self.user_id,
        "name": self.name,
        "email": self.email,
        "phone": self.phone,
        "specialization": self.specialization
    }
```

File handling is centralized through the Gym class, which already contains lists of other objects.

Loading is more complicated than saving, as direct relationships between objects must be recreated. This is done by loading objects first, in specific order so that dependencies aren't violated, such as session requiring a trainer to be initialized. A different example of relationships being reconstructed:

```
members_by_id = {
    member.user_id: member
    for member in gym._members
}

for member_id in session_data["participant_ids"]:
    member = members_by_id[member_id]
    session.add_participant(member)
    member._booked_sessions.append(session)

gym.add_session(session)
```

Here, a lookup dictionary is used to go from knowing ID's to having objects. A two directional relationship between member and session is recreated, while the gym aggregates objects.

---

### Validation and Error Handling

The system includes validation to prevent invalid operations, such as:

* duplicate users
* invalid input values
* overbooking sessions

Errors are handled by raising errors to ensure that incorrect operations do not corrupt the system state. Python has different ways to raise errors, here is an example demonstrating the prevention of invalid inputs:

```
@capacity.setter
    def capacity(self, value):
        if not isinstance(value, int):
            raise TypeError("Capacity must be an integer")
        if value <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = value
```

Type error is more basic: a program cannot do math if the input is "Three" rather than 3. But value errors are essential as well, because if the duration of the program is 0, it is already invalid on the day you bought it, making it pointless. Seperating errors by types helps inform the user what specifically went wrong, so the mistake can be corrected before running the program again.

---

## Object-Oriented Programming Principles

### Encapsulation

Encapsulation is implemented by restricting direct access to internal attributes. Instead, properties and methods are used to control how data is accessed and modified. For example, instead of a program blindly accepting any attribute values when initialized, arguments are passed through a setter:

```
@name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Gym name must be a string.")
        if not value.strip():
            raise ValueError("Gym name cannot be empty.")
        self._name = value
```

Instead of self._name, the initialization sets self.name. This is considered good practice as it seperates a clean front from a protected internal attribute, hiding the logic.

When retrieving the value of an internal list, a property is used to allow a user to view it by calling self.booked_sessions, but not directly modify it.

```
@property
    def booked_sessions(self):
        return self._booked_sessions.copy()
```

This prevents manually appending or removing list elements. My program demo shows how attempts to remove an element from a protected list without using a method fail. An alternative is created by allowing the user to do it with controlled methods, which go through steps of validation before modifying a list. 

```
def add_member(self, member):
    if not isinstance(member, Member):
        raise TypeError("Member must be a Member object.")
    if self.find_member(member.user_id) is not None:
        raise ValueError("Member with this ID already exists.")
    self._members.append(member)
```

---

### Inheritance

Inheritance is used to define a base User class, which is extended by Member and Trainer classes.

```
class Member(User):
    def __init__(self, user_id, name, email, phone):
        super().__init__(user_id, name, email, phone)
        self._membership_plan = None # plan is assigned with a method, not manually. dates are tied to it.
        self._start_date = None
        self._expiry_date = None
        self._booked_sessions = []

class Trainer(User):
    def __init__(self, user_id, name, email, phone,
                 specialization):
        super().__init__(user_id, name, email, phone)
        self.specialization = specialization
        self._assigned_sessions = []
```

Both factually are users, and all users have IDs, names and contact info. This prevents two classes repeating the same code, and allows more room for shared functionality.

---

### Polymorphism

Polymorphism is demonstrated through methods that behave differently depending on the object type.

```
# in User
def get_summary(self):
        return f"{self.name} ({self.email})"

# in Member
def get_summary(self):
    base = super().get_summary()
    if self.membership_plan:
        return f"{base}\nMember plan: {self.membership_plan.name}"
    return f"{base}\nMember plan: None"

# in Trainer
def get_summary(self):
    base = super().get_summary()
    return f"{base}\nSpecialization: {self.specialization}"
```

This allows the system to treat different objects uniformly while maintaining specific behavior. My demo shows how running this method on a list of users, without distinction, produces different results.

---

### Abstraction

Abstraction is achieved by separating the interface of classes from their internal implementation. Users of the system interact with methods without needing to know how the internal logic is handled. When member.book_session() is called, the user knows the result of the action, but not multiple steps of validation, interaction between two classes, and a second method, session.add_participant(), being called. 

```
gym.add_session(session)
member.book_session(session)
```

These two lines are enough to describe what happens, but under the surface, more than 20 lines of code run.

---

## Design Pattern

The application uses the Factory Pattern to create user objects. Instead of directly instantiating classes, a factory method determines which type of object to create based on input.

```
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
```

This simplifies object creation and makes the system easier to extend.

---

## Composition and Aggregation

The system demonstrates relationships between objects through aggregation and dependency. For example:

* A Gym contains members, trainers, and sessions
* A session depends on a trainer

```
class Gym:
    def __init__(self, name):
        self.name = name
        self._members = []
        self._trainers = []
        self._sessions = []
        self._membership_plans = []

class Session:
    def __init__(self, ..., trainer):
        self.trainer = trainer
        ...

        trainer.assign_session(self)
```

Aggregation is used to model relationships between objects, and the gym mainly exists as the center of those relationships. Interaction between members, trainers and sessions also involve lists of objects, demonstrating aggregation. This allows objects to have a hierarchy while maintaining independent existance. Flexibility is notably higher when objects' lifecycles are not restricted inside a single instance.

If I had used composition, the gym class would be responsible for creating and managing objects strictly internally. Instead of a rigid relationship, aggregation achieves the same functional goals by linking objects, while making tasks such as initializing them or recreating them from data simpler. 

---

# 3. Results and Summary

## Results

* The application successfully implements a gym management system using object-oriented programming principles.
* Core functionality such as managing users, sessions, and membership plans works as intended.
* File handling allows the system state to be saved and reconstructed correctly.
* Validation mechanisms prevent invalid operations and help maintain system consistency.
* The project scope was intentionally limited and maintained, despite initial ambiguity and challenges.
---

## Conclusions

The coursework resulted in a functional and structured application that models a simplified real world system using object oriented design. The use of OOP principles improved code organization and made the system easier to maintain and extend.

The final program demonstrates correct implementation of core features such as user management, session booking, and data persistence. It also shows how design decisions, such as using aggregation and a factory pattern, influence the flexibility and structure of the system.

Unit testing has been crucial in ensuring that code works as intended, contains fewer logical errors or inconsistencies, and changes can be made with less fear of hidden consequences.

---

## Possible Extensions

The application could be extended in several ways:

* Implement a graphical user interface (GUI) for easier interaction
* Add methods and unique functionality based on attributes like trainer specialization or membership access level.
* Introduce additional features such as payment tracking or attendance history
* Improve validation and error handling for more complex scenarios

---
