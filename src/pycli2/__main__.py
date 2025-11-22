import random

from .app import run


def message(message: str, recipient: str | None = None) -> None:
    """Prints a message to the recipient."""
    recipient = recipient or "everyone"
    print(f"Message for {recipient}: {message}!")


def shoutout(names: list[str] | None = None) -> None:
    """Prints a shoutout to all names."""
    if not names:
        s = "all my homies"
    elif len(names) == 1:
        (s,) = names
    else:
        s = ", ".join(names[:-1]) + f", and {names[-1]}"

    print(f"Shoutout to {s}!")


def roll(sides: int = 6) -> None:
    """Rolls a dice and prints the result."""
    if sides <= 0:
        raise ValueError("The sides of the dice must be greater than zero.")

    r = random.randint(1, sides)
    print(f"You roll a {r}!")


if __name__ == "__main__":
    a = run(
        message,
        shoutout,
        roll,
        description="Welcome to the PyCLI2 demo example! Select a function to try out!",
    )
