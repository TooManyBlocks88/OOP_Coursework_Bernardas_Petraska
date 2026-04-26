# Gym Management System

## Description

This is a Python based gym management system developed using Object Oriented Programming principles. The application allows managing members, trainers, sessions, and membership plans, as well as booking sessions and saving/loading data from a file.

## Features

* Create members and trainers using a factory pattern
* Assign membership plans to members
* Create and manage training sessions
* Book and cancel session participation
* Prevent invalid actions (duplicate users, overbooking, etc.)
* Save and load system data from a JSON file

## How to Run

Make sure Python is installed, then run in the root folder:

```
python main.py
```

Follow the prompts in the terminal. Press Enter to move through each demo section.

## Example Usage

The demo will:

* Create users (member and trainer)
* Assign a membership plan
* Create a session and book a member into it
* Demonstrate validation and encapsulation
* Save data to a file and load it back

## Project Structure

```
gym.py
member.py
trainer.py
session.py
membership_plan.py
user.py
user_factory.py
main.py
tests/
```

## Notes

* The system uses OOP concepts such as inheritance, encapsulation, and polymorphism
* A factory pattern is used for creating user objects
* Core functionality is demonstrated through the `main.py` demo script

---
