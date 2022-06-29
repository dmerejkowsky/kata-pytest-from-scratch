from enum import Enum

class Outcome(Enum):
    success = "success"
    failure = "failure"

def run(func):
    try:
        func()
        return Outcome.success
    except:
        return Outcome.failure
